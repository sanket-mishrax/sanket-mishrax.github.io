---
layout: page
permalink: /experience/
title: Experience
description: Academic positions, research roles, Ph.D. supervision, and education.
nav: true
nav_order: 5
---

## Current Position

**Associate Professor** — Manipal Institute of Technology Bengaluru, MAHE
*Bengaluru, India · Feb 2025 – Present*

Leading research in online machine learning, concept drift adaptation, and IoT intrusion detection. Teaching B.Tech courses and mentoring Ph.D. scholars.

## Past Experience

**Assistant Professor** — VIT-AP University
*Amaravati, Andhra Pradesh, India · Sep 2020 – Feb 2025*

Faculty in the Department of CSE. Published 20+ papers, supervised thesis projects, and developed research frameworks including Tachyon, LIRAD, OASIS, and Aura.

**Ph.D. Research Scholar** — BITS Pilani, Hyderabad Campus
*Hyderabad, India · 2015 – 2020*

Doctoral research on IoT security, complex event processing, and ML for intrusion detection under Dr. Chittaranjan Hota.

## Ph.D. Supervision

{% for student in site.data.students.phd_students %}
**{{ student.name }}** ({{ student.period }})  
{% if student.status == "completed" %}Completed{% else %}Ongoing{% endif %} — {{ student.affiliation }}

{% endfor %}

## Education

- **Ph.D.** in Computer Science — BITS Pilani, Hyderabad (2020)
- **M.E.** in Computer Science — Utkal University (2014)
- **B.Tech** in Computer Science & Engineering
