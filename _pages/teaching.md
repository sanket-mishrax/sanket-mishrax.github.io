---
layout: page
permalink: /teaching/
title: Teaching
description: Subjects taught and course materials for Manipal University affiliates.
nav: true
nav_order: 4
---

## Subjects Taught

### MIT Bengaluru, MAHE

{% assign current_subjects = site.data.subjects | where: "status", "current" | where: "institution", "MIT Bengaluru, MAHE" %}
{% for subject in current_subjects %}
**{{ subject.name }}** ({{ subject.level }})  
{{ subject.description }}

{% endfor %}

### VIT-AP University

{% assign past_subjects = site.data.subjects | where: "status", "past" | where: "institution", "VIT-AP University" %}
{% for subject in past_subjects %}
**{{ subject.name }}** ({{ subject.level }})  
{{ subject.description }}

{% endfor %}

---

## Course Materials

{% include teaching-materials.liquid %}
