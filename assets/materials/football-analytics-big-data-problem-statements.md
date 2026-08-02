# Football Analytics — Broad Problem Statements

**Theme:** Scalable football analytics on open research datasets using an Apache big-data pipeline  
**Shared requirement:** Ingest → store → process (batch + stream) → serve — not a single-notebook analysis

---

## Integrated minimal architecture

One pipeline serves both problems; only the **analytics layer** changes.

```text
┌──────────────────────────────────────────────────────────────────────┐
│                        Apache Airflow (orchestrator)                 │
└───────────────┬──────────────────────────────┬───────────────────────┘
                │                              │
                ▼                              ▼
     ┌────────────────────┐         ┌────────────────────┐
     │  Public datasets   │         │   Apache Kafka     │
     │  StatsBomb /       │────────►│   event bus        │
     │  Wyscout (JSON)    │  land   │   (raw + replay)   │
     └────────────────────┘         └─────────┬──────────┘
                │                              │
                ▼                              ▼
     ┌────────────────────┐         ┌────────────────────┐
     │  Lakehouse         │◄────────│  Stream compute    │
     │  HDFS + Parquet /  │  write │  Flink  (or Spark  │
     │  Iceberg / Hive    │         │  Structured Stream)│
     └─────────┬──────────┘         └────────────────────┘
                │
                ▼
     ┌────────────────────┐
     │  Apache Spark      │
     │  ETL + features +  │
     │  MLlib models      │
     └─────────┬──────────┘
                │
                ▼
     ┌────────────────────┐         ┌────────────────────┐
     │  Curated marts     │────────►│  Serve / visualize │
     │  team · player ·   │         │  Hive SQL /        │
     │  match features    │         │  Superset / report │
     └────────────────────┘         └────────────────────┘
```

**Flow (both problems):** open JSON → Airflow lands raw data into the lakehouse and publishes replay topics on Kafka → Spark builds curated features → Flink/Spark Streaming maintains live windows → Hive/Superset exposes insights.

---

## Problem Statement 1 (broad)

### Scalable tactical analytics on StatsBomb Open Data

**Dataset:** [StatsBomb Open Data](https://github.com/statsbomb/open-data) — public match events, lineups, and selected 360 frames.

**Problem:**  
Football tactics are encoded in millions of fine-grained on-ball events. Build a **distributed analytics system** that turns StatsBomb’s open event logs into **season-scale tactical intelligence**—possession value / Expected Threat surfaces, pressing behaviour, and passing structure—using a shared Apache pipeline (diagram above).

**In scope (high level):**
- Land and normalize multi-competition event JSON into a lakehouse
- Compute team- and player-level tactical indicators at scale
- Replay matches over Kafka for near-real-time tactical aggregates
- Publish coach-facing summaries from curated marts

**Out of scope (keep minimal):** proprietary live APIs, video CV, paywalled tracking feeds.

---

## Problem Statement 2 (broad)

### Cross-league player intelligence on Wyscout public event logs

**Dataset:** Wyscout soccer-logs (CC BY 4.0) — Pappalardo et al., *Nature Scientific Data* (2019), [doi:10.1038/s41597-019-0247-7](https://doi.org/10.1038/s41597-019-0247-7) (~1.9k matches, ~3.25M events, top-5 leagues + WC/Euro).

**Problem:**  
Player comparison across leagues is biased by role, minutes, and context, and form is non-stationary. Build a **distributed player-intelligence system** on the Wyscout public release that produces **comparable cross-league rankings** and surfaces **form change / concept drift**, on the same Apache pipeline (diagram above).

**In scope (high level):**
- Unify competitions, teams, players, and events in the lakehouse
- Engineer role-aware performance features and ranking/similarity models (Spark MLlib)
- Stream rolling form signals and drift alarms over Kafka + Flink
- Serve scouting-oriented views (rising / declining / similar players)

**Out of scope (keep minimal):** transfer-fee prediction markets, private scouting notes, non-public data sources.

---

## Submission note

Both submissions must demonstrate the **integrated architecture** with Apache components (Airflow, Kafka, Spark, Flink or Spark Streaming, Iceberg/Hive/Parquet, optional Superset)—differing mainly in analytics focus: **tactics (PS1)** vs **players & drift (PS2)**.
