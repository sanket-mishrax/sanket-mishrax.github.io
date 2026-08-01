---
layout: page
permalink: /publications/
title: Publications
description: Peer-reviewed publications with summaries.
nav: true
nav_order: 2
---

<div class="publications">

<p class="publications-note">Publications are grouped by type — <strong>journal articles</strong>, <strong>conference papers</strong>, and <strong>book chapters</strong> — each in reverse chronological order. Every entry is labelled with its type and has three columns: <strong>topic badge</strong>, <strong>paper details</strong>, and <strong>venue metrics</strong> (indexing, quartile, and impact factor for journals; CORE ranking for conferences). Click any <strong>title</strong> to open the paper on the publisher site. Click <strong>Abs</strong> to expand the abstract summary on this page.</p>

<h2 class="pub-section-heading">Journal Articles</h2>
{% bibliography --group_by year --group_order descending --query @article %}

<h2 class="pub-section-heading">Conference Papers</h2>
{% bibliography --group_by year --group_order descending --query @inproceedings %}

<h2 class="pub-section-heading">Book Chapters</h2>
{% bibliography --group_by year --group_order descending --query @incollection %}

</div>
