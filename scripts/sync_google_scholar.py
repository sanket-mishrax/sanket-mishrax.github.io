#!/usr/bin/env python3
"""Sync citation metrics and publications from Google Scholar into site data files."""

from __future__ import annotations

import argparse
import datetime as dt
import os
import re
import signal
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import bibtexparser
import requests
import yaml
from bibtexparser.bwriter import BibTexWriter
from rapidfuzz import fuzz
from ruamel.yaml import YAML

ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = Path(__file__).with_name("scholar_sync_config.yml")


@dataclass
class ScholarPublication:
    title: str
    year: int | None
    citations: int
    scholar_id: str
    authors: str = ""
    venue: str = ""


@dataclass
class ScholarProfile:
    source: str
    total_citations: int
    h_index: int
    i10_index: int
    total_publications: int
    publications: list[ScholarPublication] = field(default_factory=list)


class TimeoutError(RuntimeError):
    pass


def _timeout_handler(_signum, _frame):
    raise TimeoutError("Google Scholar request timed out")


def load_config() -> dict[str, Any]:
    with CONFIG_PATH.open(encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def normalize_title(title: str) -> str:
    title = title.lower()
    title = re.sub(r"[^\w\s]", " ", title)
    title = re.sub(r"\s+", " ", title).strip()
    return title


def fetch_via_serpapi(author_id: str, api_key: str) -> ScholarProfile | None:
    try:
        from serpapi import GoogleSearch
    except ImportError:
        return None

    results = GoogleSearch(
        {
            "engine": "google_scholar_author",
            "author_id": author_id,
            "num": 100,
            "api_key": api_key,
        }
    ).get_dict()

    if results.get("error"):
        print(f"SerpAPI error: {results['error']}", file=sys.stderr)
        return None

    cited_table = results.get("cited_by", {}).get("table", [])
    citations = h_index = i10_index = 0
    for row in cited_table:
        if "citations" in row:
            citations = int(row["citations"].get("all", 0))
        elif "h_index" in row:
            h_index = int(row["h_index"].get("all", 0))
        elif "i10_index" in row:
            i10_index = int(row["i10_index"].get("all", 0))

    publications: list[ScholarPublication] = []
    for article in results.get("articles", []):
        scholar_id = article.get("citation_id", "")
        if not scholar_id:
            continue
        cited = article.get("cited_by", {}) or {}
        cited_value = cited.get("value", 0) if isinstance(cited, dict) else 0
        year_raw = article.get("year")
        year = int(year_raw) if year_raw and str(year_raw).isdigit() else None
        publications.append(
            ScholarPublication(
                title=article.get("title", "").strip(),
                year=year,
                citations=int(cited_value or 0),
                scholar_id=scholar_id,
                authors=article.get("authors", ""),
                venue=article.get("publication", ""),
            )
        )

    return ScholarProfile(
        source="Google Scholar",
        total_citations=citations,
        h_index=h_index,
        i10_index=i10_index,
        total_publications=len(publications),
        publications=publications,
    )


def fetch_via_scholarly(author_id: str, timeout_seconds: int = 25) -> ScholarProfile | None:
    try:
        from scholarly import scholarly
    except ImportError:
        return None

    signal.signal(signal.SIGALRM, _timeout_handler)
    signal.alarm(timeout_seconds)
    try:
        author = scholarly.search_author_id(author_id)
        author = scholarly.fill(author, sections=["basics", "indices", "counts", "publications"])
    except Exception as exc:
        print(f"scholarly failed: {exc}", file=sys.stderr)
        return None
    finally:
        signal.alarm(0)

    publications: list[ScholarPublication] = []
    for pub in author.get("publications", []):
        scholar_id = pub.get("author_pub_id", "")
        if not scholar_id:
            continue
        bib = pub.get("bib", {})
        title = bib.get("title", "").strip()
        if not title:
            continue
        year_raw = bib.get("pub_year")
        year = int(year_raw) if year_raw and str(year_raw).isdigit() else None
        publications.append(
            ScholarPublication(
                title=title,
                year=year,
                citations=int(pub.get("num_citations", 0) or 0),
                scholar_id=scholar_id.split(":")[-1],
                authors=bib.get("author", ""),
                venue=bib.get("venue", "") or bib.get("journal", "") or bib.get("booktitle", ""),
            )
        )

    return ScholarProfile(
        source="Google Scholar",
        total_citations=int(author.get("citedby", 0) or 0),
        h_index=int(author.get("hindex", 0) or 0),
        i10_index=int(author.get("i10index", 0) or 0),
        total_publications=len(publications),
        publications=publications,
    )


def fetch_via_openalex(orcid_id: str) -> ScholarProfile | None:
    url = f"https://api.openalex.org/authors/https://orcid.org/{orcid_id}"
    response = requests.get(url, timeout=30)
    if response.status_code != 200:
        print(f"OpenAlex error: HTTP {response.status_code}", file=sys.stderr)
        return None

    author = response.json()
    summary = author.get("summary_stats", {})
    works_url = author.get("works_api_url")
    publications: list[ScholarPublication] = []

    if works_url:
        page = requests.get(
            works_url,
            params={"per_page": 100, "sort": "publication_year:desc"},
            timeout=30,
        )
        if page.status_code == 200:
            for work in page.json().get("results", []):
                title = work.get("display_name", "").strip()
                if not title:
                    continue
                year = work.get("publication_year")
                source = (work.get("primary_location") or {}).get("source") or {}
                venue = source.get("display_name", "") if isinstance(source, dict) else ""
                publications.append(
                    ScholarPublication(
                        title=title,
                        year=int(year) if year else None,
                        citations=int(work.get("cited_by_count", 0) or 0),
                        scholar_id=work.get("id", "").rsplit("/", 1)[-1],
                        venue=venue,
                    )
                )

    return ScholarProfile(
        source="OpenAlex (fallback)",
        total_citations=int(author.get("cited_by_count", 0) or 0),
        h_index=int(summary.get("h_index", 0) or 0),
        i10_index=int(summary.get("i10_index", 0) or 0),
        total_publications=int(author.get("works_count", len(publications)) or len(publications)),
        publications=publications,
    )


def fetch_profile(config: dict[str, Any]) -> ScholarProfile:
    author_id = config["scholar_userid"]
    orcid_id = config["orcid_id"]
    api_key = os.environ.get("SERPAPI_API_KEY", "").strip()

    if api_key:
        print("Trying SerpAPI (Google Scholar)...")
        profile = fetch_via_serpapi(author_id, api_key)
        if profile and profile.total_citations > 0:
            return profile
        print("SerpAPI did not return usable data.", file=sys.stderr)

    if os.environ.get("SCHOLARLY_ENABLED", "").lower() in {"1", "true", "yes"}:
        print("Trying scholarly (Google Scholar)...")
        profile = fetch_via_scholarly(author_id)
        if profile and profile.total_citations > 0:
            return profile

    print("Using OpenAlex via ORCID (add SERPAPI_API_KEY for direct Google Scholar sync)...")
    profile = fetch_via_openalex(orcid_id)
    if profile:
        return profile

    raise RuntimeError("Unable to fetch scholar metrics from any provider.")


def load_bib_entries(bib_path: Path) -> list[dict[str, Any]]:
    with bib_path.open(encoding="utf-8") as handle:
        db = bibtexparser.load(handle)
    return db.entries


def save_bib_entries(bib_path: Path, entries: list[dict[str, Any]]) -> None:
    text = bib_path.read_text(encoding="utf-8")
    for entry in entries:
        scholar_id = entry.get("google_scholar_id")
        citations = entry.get("scholar_citations")
        if not scholar_id and not citations:
            continue

        key = entry["ID"]
        entry_pattern = re.compile(
            rf"(@\w+\{{{re.escape(key)},\s*)(.*?)(^\}})",
            re.MULTILINE | re.DOTALL,
        )
        match = entry_pattern.search(text)
        if not match:
            continue

        block = match.group(2)
        if scholar_id:
            if re.search(r"google_scholar_id\s*=", block):
                block = re.sub(
                    r"google_scholar_id\s*=\s*\{[^}]*\}",
                    f"google_scholar_id = {{{scholar_id}}}",
                    block,
                )
            else:
                block = block.rstrip() + f"\n\n  google_scholar_id = {{{scholar_id}}},\n"

        if citations:
            if re.search(r"scholar_citations\s*=", block):
                block = re.sub(
                    r"scholar_citations\s*=\s*\{[^}]*\}",
                    f"scholar_citations = {{{citations}}}",
                    block,
                )
            else:
                block = block.rstrip() + f"\n\n  scholar_citations = {{{citations}}},\n"

        text = text[: match.start(2)] + block + text[match.end(2) :]

    bib_path.write_text(text, encoding="utf-8")


def match_publications(
    scholar_pubs: list[ScholarPublication],
    bib_entries: list[dict[str, Any]],
    threshold: int,
    source: str,
) -> tuple[list[dict[str, Any]], list[ScholarPublication], int]:
    matched_scholar_ids: set[str] = set()
    updated = 0
    use_scholar_ids = source == "Google Scholar"

    for entry in bib_entries:
        bib_title = entry.get("title", "")
        if not bib_title:
            continue
        best_score = 0
        best_pub: ScholarPublication | None = None
        norm_bib = normalize_title(bib_title)

        for pub in scholar_pubs:
            score = fuzz.token_sort_ratio(norm_bib, normalize_title(pub.title))
            if score > best_score:
                best_score = score
                best_pub = pub

        if best_pub and best_score >= threshold:
            matched_scholar_ids.add(best_pub.scholar_id)
            changed = False
            if use_scholar_ids and entry.get("google_scholar_id") != best_pub.scholar_id:
                entry["google_scholar_id"] = best_pub.scholar_id
                changed = True
            if entry.get("scholar_citations") != str(best_pub.citations):
                entry["scholar_citations"] = str(best_pub.citations)
                changed = True
            if changed:
                updated += 1

    pending = [pub for pub in scholar_pubs if pub.scholar_id not in matched_scholar_ids]
    return bib_entries, pending, updated


def write_yaml(path: Path, data: dict[str, Any]) -> None:
    yaml_writer = YAML()
    yaml_writer.default_flow_style = False
    yaml_writer.indent(mapping=2, sequence=4, offset=2)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        yaml_writer.dump(data, handle)


def update_research_areas(path: Path, profile: ScholarProfile, config: dict[str, Any]) -> None:
    text = path.read_text(encoding="utf-8")
    now = dt.datetime.now(dt.timezone.utc).strftime("%b %Y")
    synced_at = dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat()
    active_since = config.get("active_since", 2017)

    replacements = {
        r"(total_publications:\s*)\d+": rf"\g<1>{profile.total_publications}",
        r"(total_citations:\s*)\d+": rf"\g<1>{profile.total_citations}",
        r"(h_index:\s*)\d+": rf"\g<1>{profile.h_index}",
        r"(i10_index:\s*)\d+": rf"\g<1>{profile.i10_index}",
        r'(metrics_updated:\s*)"[^"]*"': rf'\g<1>"{now}"',
        r"(metrics_source:\s*).+": lambda m: f'{m.group(1)}"{profile.source}"',
        r"(active_since:\s*)\d+": rf"\g<1>{active_since}",
    }

    for pattern, replacement in replacements.items():
        if callable(replacement):
            text, count = re.subn(pattern, replacement, text, count=1)
        else:
            text, count = re.subn(pattern, replacement, text, count=1)
        if count == 0 and "last_synced_at" not in pattern:
            print(f"Warning: could not update {pattern} in research_areas.yml", file=sys.stderr)

    if re.search(r"last_synced_at:", text):
        text = re.sub(
            r"(last_synced_at:\s*).+",
            lambda _: f'last_synced_at: "{synced_at}"',
            text,
            count=1,
        )
    else:
        text = re.sub(
            r"(metrics_source:\s*.+)",
            lambda match: f'{match.group(1)}\n  last_synced_at: "{synced_at}"',
            text,
            count=1,
        )

    path.write_text(text, encoding="utf-8")


def write_scholar_publications(path: Path, profile: ScholarProfile) -> None:
    payload = {
        "synced_at": dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat(),
        "source": profile.source,
        "publications": [
            {
                "title": pub.title,
                "year": pub.year,
                "citations": pub.citations,
                "scholar_id": pub.scholar_id,
                "authors": pub.authors,
                "venue": pub.venue,
            }
            for pub in sorted(
                profile.publications,
                key=lambda item: (item.year or 0, item.citations),
                reverse=True,
            )
        ],
    }
    write_yaml(path, payload)


def write_pending_publications(path: Path, pending: list[ScholarPublication], profile: ScholarProfile) -> None:
    payload = {
        "synced_at": dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat(),
        "source": profile.source,
        "note": "Publications found on the sync source but not matched to papers.bib. Add them manually.",
        "publications": [
            {
                "title": pub.title,
                "year": pub.year,
                "citations": pub.citations,
                "scholar_id": pub.scholar_id,
                "authors": pub.authors,
                "venue": pub.venue,
            }
            for pub in pending
        ],
    }
    write_yaml(path, payload)


def main() -> int:
    parser = argparse.ArgumentParser(description="Sync Google Scholar metrics into the site data files.")
    parser.add_argument("--dry-run", action="store_true", help="Fetch and report without writing files.")
    args = parser.parse_args()

    config = load_config()
    paths = {key: ROOT / value for key, value in config["paths"].items()}
    threshold = int(config.get("title_match_threshold", 88))

    profile = fetch_profile(config)
    print(
        f"Fetched {profile.source}: "
        f"{profile.total_publications} works, "
        f"{profile.total_citations} citations, "
        f"h-index {profile.h_index}, "
        f"i10-index {profile.i10_index}"
    )

    bib_entries = load_bib_entries(paths["bibliography"])
    bib_entries, pending, bib_updates = match_publications(
        profile.publications, bib_entries, threshold, profile.source
    )
    print(f"Matched {len(profile.publications) - len(pending)} publications; updated {bib_updates} bib entries.")
    if pending:
        print(f"{len(pending)} publication(s) on Scholar are not yet in papers.bib.")

    if args.dry_run:
        return 0

    update_research_areas(paths["research_areas"], profile, config)
    write_scholar_publications(paths["scholar_publications"], profile)
    write_pending_publications(paths["scholar_pending"], pending, profile)
    if bib_updates:
        save_bib_entries(paths["bibliography"], bib_entries)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
