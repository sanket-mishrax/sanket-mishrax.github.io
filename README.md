# Dr. Sanket Mishra — Academic Portfolio

Academic portfolio website for **Dr. Sanket Mishra**, Associate Professor at MIT Bengaluru (MAHE). Built with [Jekyll](https://jekyllrb.com/) and the [al-folio](https://github.com/alshedivat/al-folio) theme.

**Live site:** https://sanket-mishrax.github.io/

## About

Research focus: online machine learning, concept drift detection, deep learning, and IoT security. The site publishes publications, teaching, experience, and academic service in a static, GitHub Pages–hosted format.

| | |
|---|---|
| **Affiliation** | School of Computer Engineering, MIT Bengaluru, MAHE |
| **Email** | sanket.mishra@manipal.edu |
| **Google Scholar** | [LkngaM4AAAAJ](https://scholar.google.com/citations?user=LkngaM4AAAAJ) |
| **ORCID** | [0000-0002-3193-8160](https://orcid.org/0000-0002-3193-8160) |

## Site pages

| Page | URL | Description |
|------|-----|-------------|
| **About** | `/` | Bio, profile photo, selected publications, social links |
| **Publications** | `/publications/` | BibTeX bibliography grouped into journal articles, conference papers, and book chapters |
| **Research** | `/research/` | Research areas, impact metrics, and additional interests |
| **Teaching** | `/teaching/` | B.Tech courses taught (MIT Bengaluru & VIT-AP) and gated course materials |
| **Experience** | `/experience/` | Academic positions and education |
| **Administration** | `/administration/` | Current/past roles, leadership service, peer review, and TPC |

## Repository structure

```
sanket-mishrax.github.io/
├── _config.yml                 # Site settings, social IDs, bibliography & teaching config
├── _pages/                     # Site pages (Markdown + front matter)
│   ├── about.md                #   Homepage (layout: about)
│   ├── publications.md         #   Full bibliography listing
│   ├── research.md             #   Research areas & scholar metrics
│   ├── teaching.md             #   Courses + teaching-materials include
│   ├── experience.md           #   Positions & education
│   └── administration.md       #   Renders roles from _data/admin.yml
│
├── _data/                      # Structured content (YAML)
│   ├── admin.yml               #   Administration roles & academic service
│   ├── subjects.yml            #   Courses taught (MIT & VIT-AP, B.Tech)
│   ├── teaching_materials.yml  #   Gated course files (title, course, url)
│   ├── experience.yml          #   Detailed experience data (reference)
│   ├── institutes.yml          #   Institute profiles (reference)
│   ├── research_areas.yml      #   Research area metadata
│   ├── venues.yml              #   Publication badge colours (abbr → url)
│   └── publications.yml        #   Legacy publication metadata
│
├── _bibliography/
│   └── papers.bib              # All publications (source of truth)
│
├── _layouts/                   # Page templates (Liquid)
│   ├── about.liquid            #   Homepage layout
│   ├── bib.liquid              #   Publication entry (3-column: badge | details | metrics)
│   └── page.liquid             #   Standard content pages
│
├── _includes/                  # Reusable components
│   ├── teaching-materials.liquid   # Email-gated materials UI
│   ├── selected_papers.liquid      # Homepage publication highlights
│   ├── head.liquid                 # HTML head (CSS cache busting)
│   └── header.liquid / footer.liquid
│
├── _plugins/                   # Jekyll plugins
│   ├── cache-bust.rb           #   Asset cache busting for SCSS/CSS
│   └── hide-custom-bibtex.rb   #   Strips custom bib fields from BibTeX output
│
├── assets/
│   ├── img/
│   │   ├── bio-photo.png       #   Profile photo (homepage)
│   ├── css/main.scss           #   Site styles (compiled to main.css)
│   ├── js/
│   │   ├── common.js           #   Abs/Bib toggle handlers
│   │   └── teaching-materials.js   # Manipal email gate for course files
│   └── materials/              #   (optional) Local course file uploads
│
├── .github/workflows/
│   └── deploy.yml              # Build on push to master → deploy to gh-pages
│
├── Gemfile                     # Ruby dependencies
└── README.md                   # This file
```

## Content guide

### Publications (`_bibliography/papers.bib`)

Add or edit BibTeX entries. Custom fields used by the site:

| Field | Purpose |
|-------|---------|
| `abstract` | Shown when visitors click **Abs** |
| `abbr` | Publisher or conference key — logo from `_data/venues.yml` (e.g. `IEEE`, `ICONIP`, `AVSS`) |
| `selected` | `true` to feature on the About page |
| `doi` | Makes the title a link to the publisher |
| `indexing` | Journal indexing (e.g. Scopus, SCIE) — metrics column |
| `quartile` | Journal quartile (Q1–Q4) |
| `impact_factor` | Journal impact factor |
| `impact_factor_year` | IF source year (e.g. JCR 2024) |
| `core_ranking` | Conference CORE rank (A, B, C, etc.) |
| `core_edition` | CORE edition (e.g. CORE 2020) |

Journal entries show indexing / quartile / IF in the right column; conference entries show CORE ranking.

### Teaching

| File | What to edit |
|------|--------------|
| `_data/subjects.yml` | Course name, level, institution, status (`current` / `past`), description |
| `_data/teaching_materials.yml` | Course material links (`course`, `title`, `url`, optional `type`) |
| `_config.yml` → `teaching_materials.allowed_email_domains` | Email domains allowed to view materials (default: `manipal.edu`) |

Course materials are hidden until a visitor verifies a `@manipal.edu` email address (see `_includes/teaching-materials.liquid`).

### Administration (`_data/admin.yml`)

Sections: `current_roles`, `past_roles`, `leadership_roles`, `academic_service`. The Administration page renders this file automatically.

### Homepage & profile

| File | Purpose |
|------|---------|
| `_pages/about.md` | Bio text, subtitle, profile image path |
| `assets/img/bio-photo.png` | Profile photograph |
| `_config.yml` | Name, email, `scholar_userid`, `orcid_id`, social links |

### Site-wide settings (`_config.yml`)

Key settings: `url`, `email`, scholar/ORCID/Scopus IDs, `enable_publication_thumbnails`, `filtered_bibtex_keywords` (fields hidden from exported BibTeX), and `teaching_materials` access rules.

## Local development

**Requirements:** Ruby 3.x, Bundler

```bash
bundle install
bundle exec jekyll serve
```

Open http://localhost:4000

For a production-like build:

```bash
JEKYLL_ENV=production bundle exec jekyll build
```

Output is written to `_site/`.

## Deployment

Pushes to the `master` branch trigger [`.github/workflows/deploy.yml`](.github/workflows/deploy.yml), which builds the site with Jekyll and publishes to the `gh-pages` branch. GitHub Pages serves the site at https://sanket-mishrax.github.io/.

The repository should be named `sanket-mishrax.github.io` with **Settings → Pages → Branch** set to `gh-pages`.

## Licence

Site content © Sanket Mishra. Theme based on [al-folio](https://github.com/alshedivat/al-folio) (MIT licence).
