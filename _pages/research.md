---
layout: page
permalink: /research/
title: Research
description: Research areas and impact in online ML, drift detection, deep learning, and IoT security.
nav: true
nav_order: 3
---

## Primary Research Areas

Broad themes distilled from my publication portfolio — spanning IoT security, adaptive and online machine learning, streaming analytics, edge AI, and related application domains.

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

{% include research-impact.liquid %}
