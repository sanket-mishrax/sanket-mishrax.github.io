---
layout: about
title: About
permalink: /
subtitle:  Associate Professor | MIT Bengaluru, MAHE · Machine Learning & IoT Security | TCS PhD Research Fellow [2016–2020]

profile:
  align: right
  image: bio-photo.png
  image_circular: false

news: false
selected_papers: true
social: true
---

I am an Associate Professor in the School of Computer Engineering at [Manipal Institute of Technology Bengaluru](https://www.manipal.edu/mu/campuses/mahe-bengaluru.html) (MAHE). My research sits at the intersection of **online machine learning**, **concept drift detection**, **deep learning**, and **Internet of Things security** — building adaptive, scalable frameworks for real-time intrusion detection on evolving IoT data streams.

Previously an Assistant Professor at VIT-AP University, Amaravati, Andhra Pradesh (2020–2025), I earned my Ph.D. from BITS Pilani, Hyderabad. I have published {{ site.data.research_areas.research_stats.total_publications }}+ peer-reviewed papers with {{ site.data.research_areas.research_stats.total_citations }}+ citations (h-index {{ site.data.research_areas.research_stats.h_index }}, i10-index {{ site.data.research_areas.research_stats.i10_index }}) in venues including *Internet of Things*, *Cluster Computing*, *IEEE Access*, and *Scientific Reports*.

**Scholar profiles:** {% for profile in site.data.research_areas.research_stats.profiles %} [{{ profile.label }}]({{ profile.url }}){% unless forloop.last %} · {% endunless %}{% endfor %}

I work on identifying key challenges in IoT ecosystems and solving them with frameworks that are adaptive, lightweight, and scalable. I am open to research collaborations, Ph.D./M.Tech supervision, and invited talks.

**Research areas:** IoT intrusion detection · Online ML & concept drift · Streaming analytics & CEP · Smart cities & ITS · Lightweight edge ML · Deep learning & vision · Mobile crowdsensing · Healthcare & environmental IoT
