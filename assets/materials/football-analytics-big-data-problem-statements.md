# Football Analytics — Big Data Project Problem Statements

**Theme:** End-to-end football analytics on open research datasets using the Apache big-data ecosystem  
**Requirement:** Every submission must implement an **Apache-centric data pipeline** (ingest → store → process → serve/visualize), not a single-notebook analysis.

---

## Problem Statement 1  
### Large-Scale Tactical Intelligence & Expected Threat (xT) Platform on StatsBomb Open Data

#### Motivation
Modern football analysis depends on high-volume event streams (passes, shots, pressures, carry events) rather than box-score aggregates. Clubs and researchers need scalable pipelines that can (i) land nested match JSON at scale, (ii) compute possession value / expected threat surfaces, and (iii) refresh tactical dashboards as new competitions are released—without rebuilding the warehouse manually.

#### Public research dataset
- **StatsBomb Open Data** (CC-licensed research release): [https://github.com/statsbomb/open-data](https://github.com/statsbomb/open-data)
- Contents: competitions, matches, lineups, event logs, and selected StatsBomb 360 freeze-frames
- Format: nested JSON per match (events often 2k–3k+ rows each), suitable for distributed land-and-transform workloads

#### Core research / engineering problem
Design and implement a **batch + near-real-time football event lakehouse** that:

1. Ingests StatsBomb open competitions into a distributed store.
2. Normalizes nested events into analytics-ready tables (passes, shots, pressures, carries, substitutions).
3. Computes **Expected Threat (xT)** / possession-value grids and team pressing intensity over seasons.
4. Detects tactical regime shifts (e.g., formation/style change mid-season) from rolling event features.
5. Serves coach-facing summaries (shot maps, pass networks, xT contribution leaders) from curated marts.

#### Mandatory Apache ecosystem & pipeline
| Stage | Suggested Apache tools | Responsibility |
|---|---|---|
| Orchestration | **Apache Airflow** | DAG: pull → validate → transform → feature compute → publish |
| Landing / storage | **HDFS** or object store + **Apache Parquet** / **Apache Iceberg** (or Hive tables) | Versioned bronze/silver/gold layers |
| Batch compute | **Apache Spark** (PySpark/Scala) | Flatten JSON, pitch-grid xT, pass networks, season aggregates |
| Streaming simulation | **Apache Kafka** (+ Spark Structured Streaming *or* **Apache Flink**) | Replay match events chronologically as a live match feed |
| Serving / SQL | **Apache Hive** / **Trino**-compatible Iceberg SQL, optional **Apache Superset** | Query marts & dashboards |
| Optional enrichment | **Apache HBase** or keyed state in Flink | Live match scoreboard / rolling player form |

**Minimum pipeline shape (must be demonstrated):**

```text
StatsBomb JSON ──► Airflow DAG ──► Bronze (raw JSON/Parquet)
                         │
                         ▼
              Spark ETL ──► Silver (typed events)
                         │
                         ├─► Gold: xT grids, pressing metrics, pass graphs
                         │
Kafka match replay ──► Flink/Spark Streaming ──► live tactical features
                         │
                         ▼
              Hive/Iceberg marts ──► Superset / API / notebook report
```

#### Suggested analytics questions (pick ≥3)
- Which teams generate the highest **xT progression per 90** in open competitions, and how stable is that ranking across matchweeks?
- How do **pressing intensity** and opponent pass completion correlate in the final third?
- Can **pass-network centrality** (degree/betweenness on directed graphs) predict shot creation better than raw pass volume?
- Using 360 freeze-frames (where available), does opponent packing density before a shot change conversion odds?

#### Deliverables
1. Reproducible Airflow-orchestrated pipeline with clear bronze/silver/gold contracts.
2. Spark jobs for event flattening + xT / pressing feature generation.
3. Kafka-based chronological replay of at least one competition matchweek with streaming aggregations.
4. Analytical report (and optional Superset dashboard) answering the chosen research questions.
5. Architecture diagram, data dictionary, and runbook (how to bootstrap from the public GitHub dump).

#### Evaluation focus
Scalability of the pipeline, correctness of event transformations, clarity of the lakehouse layers, and insight quality—not only model accuracy.

---

## Problem Statement 2  
### Cross-League Player Valuation & Concept-Drift Aware Ranking on Wyscout Public Event Logs

#### Motivation
Player comparison across leagues is noisy: minutes, role, opponent strength, and tactical context differ. A research-grade system should build a **feature store of event-derived player signals**, rank players with uncertainty, and explicitly handle **non-stationary form** (concept drift) as seasons progress—mirroring real scouting workflows at big-data scale.

#### Public research dataset
- **Wyscout public soccer-logs** (CC BY 4.0), described in:  
  Pappalardo et al., *A public data set of spatio-temporal match events in soccer competitions*, **Nature Scientific Data** (2019).  
  DOI: [https://doi.org/10.1038/s41597-019-0247-7](https://doi.org/10.1038/s41597-019-0247-7)
- Scale (approx.): **~1,941 matches**, **~3.25M events**, **~4,300 players** across top-5 European leagues (2017/18), FIFA World Cup 2018, and UEFA Euro 2016
- Access: Figshare release / community loaders (e.g. kloppy `wyscout.load_open_data`)

#### Core research / engineering problem
Build a **distributed player-intelligence pipeline** that:

1. Lands and joins competitions, matches, teams, players, and event streams into a unified warehouse.
2. Engineers role-aware features (progressive passes, duel success, shot quality proxies, defensive actions per 90, sequence involvement).
3. Produces **cross-league comparable rankings** (position-normalized) with confidence intervals / Bayesian shrinkage where appropriate.
4. Monitors **feature and ranking drift** over matchweeks (online/streaming detectors) so sudden form collapses or tactical role changes are surfaced.
5. Exposes a scouting API or dashboard: “find similar players”, “rising form”, “declining reliability”.

#### Mandatory Apache ecosystem & pipeline
| Stage | Suggested Apache tools | Responsibility |
|---|---|---|
| Orchestration | **Apache Airflow** (or **Apache NiFi** for ingest + Airflow for ML stages) | Scheduled multi-league refresh |
| Ingest / bus | **Apache Kafka** | Topic per league or `events.raw` / `events.curated` |
| Batch feature engineering | **Apache Spark** + **Spark MLlib** | Per-90 features, similarity (ALS/kNN), baseline ranking models |
| Stream / drift | **Apache Flink** (preferred) or Spark Structured Streaming | Rolling form windows; drift alarms on feature distributions / rank volatility |
| Lakehouse | **Apache Iceberg** (or Hive + Parquet) on HDFS/object storage | Player-match fact table, weekly ranking snapshots |
| Serving | **Apache Hive** SQL marts + optional **Apache Druid** / Superset | Fast scouting queries and charts |
| Governance (bonus) | **Apache Atlas** / schema registry conventions | Dataset lineage for research reproducibility |

**Minimum pipeline shape (must be demonstrated):**

```text
Wyscout open JSON ──► NiFi/Airflow ──► Kafka (raw events)
                              │
                              ▼
                 Spark batch ──► Iceberg player-match features
                              │
                              ├─► MLlib ranking / similarity models
                              │
Flink job ◄── Kafka curated ──► rolling form + drift detectors
                              │
                              ▼
                 Ranking snapshots ──► Hive/Superset scouting views
```

#### Suggested analytics questions (pick ≥3)
- After position and minutes normalization, which midfielders show the highest **progressive-action value** in 2017/18 top-5 leagues?
- Do World Cup / Euro tournament performances **transfer** to club-season rankings, or are they systematically inflated?
- Where do **ADWIN / Page-Hinkley / PSI-style drift alarms** fire on a player’s feature vector, and do they precede measurable rating drops?
- Can graph embeddings of possession sequences cluster “playmaker” vs “carrier” archetypes better than hand-crafted stats?

#### Deliverables
1. End-to-end Apache pipeline with Kafka-backed event flow and Iceberg/Hive curated tables.
2. Spark feature store + ranking/similarity module (MLlib or Spark + external model, trained in-pipeline).
3. Flink (or equivalent) job that emits rolling form metrics and at least one drift signal.
4. Scouting-oriented report/dashboard with cross-league comparisons and drift case studies.
5. Reproducibility pack: seed scripts for public data download, DAG configs, and schema docs.

#### Evaluation focus
Pipeline completeness, correctness of joins/feature definitions, meaningful drift analysis, and interpretability of rankings for a scouting audience.

---

## Cross-cutting submission checklist (both problems)

- [ ] Uses **≥4 Apache ecosystem components**, including orchestration + distributed compute + a messaging *or* streaming engine
- [ ] Implements a documented **multi-stage pipeline** (raw → curated → features → serving)
- [ ] Works from **public research data only** (StatsBomb open-data and/or Wyscout Nature Scientific Data release)
- [ ] Includes architecture diagram, data dictionary, and runnable instructions
- [ ] Separates research insights from engineering: both the *analytics questions* and the *pipeline* must be demonstrated
- [ ] Avoids proprietary club APIs or scraped paywalled sources as primary data

## Recommended starter references
1. StatsBomb Open Data repository & event specification  
2. Pappalardo et al., *Sci Data* (2019) — Wyscout public event dataset  
3. Expected Threat / possession value literature (e.g. Karun Singh xT; related public notebooks)  
4. Apache project docs: Spark, Kafka, Flink, Airflow, Iceberg, Hive, Superset
