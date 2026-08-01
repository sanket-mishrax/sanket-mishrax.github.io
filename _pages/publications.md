---
layout: page
permalink: /publications/
title: Publications
description: Peer-reviewed publications with summaries.
nav: true
nav_order: 2
---

<div class="publications">

<h2 class="pub-section-heading">Journal Articles</h2>
{% bibliography --group_by year --group_order descending --query @article %}

<h2 class="pub-section-heading">Conference Papers</h2>
{% bibliography --group_by year --group_order descending --query @inproceedings %}

<h2 class="pub-section-heading">Book Chapters</h2>
{% bibliography --group_by year --group_order descending --query @incollection %}

</div>
