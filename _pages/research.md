---
layout: page
permalink: /research/
title: Research
description: Research areas and impact across IoT security, streaming ML, smart cities, and edge AI.
nav: true
nav_order: 3
---

## Research Areas

{% for area in site.data.research_areas.areas %}
### {{ area.name }}

{{ area.description }}

{% if area.keywords %}
**Keywords:** {{ area.keywords | join: " · " }}
{% endif %}

{% if area.representative_papers %}
**Representative publications:** {% for paper in area.representative_papers %}{{ paper }}{% unless forloop.last %}; {% endunless %}{% endfor %}
{% endif %}

{% endfor %}

## Research Impact

| Metric | Value |
|--------|-------|
| Publications | {{ site.data.research_areas.research_stats.total_publications }}+ |
| Citations | {{ site.data.research_areas.research_stats.total_citations }}+ |
| h-index | {{ site.data.research_areas.research_stats.h_index }} |
| i10-index | {{ site.data.research_areas.research_stats.i10_index }} |
| Active since | {{ site.data.research_areas.research_stats.active_since }} |

**Scholar profiles:** {% for profile in site.data.research_areas.research_stats.profiles %} [{{ profile.label }}]({{ profile.url }}){% unless forloop.last %} · {% endunless %}{% endfor %}

*Citation metrics from [{{ site.data.research_areas.research_stats.metrics_source }}](https://scholar.google.com/citations?user={{ site.scholar_userid }}&hl=en) (updated {{ site.data.research_areas.research_stats.metrics_updated }}).*
