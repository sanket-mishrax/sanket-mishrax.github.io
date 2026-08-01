---
layout: page
permalink: /administration/
title: Administration
description: Administrative roles and academic service.
nav: true
nav_order: 7
---

## Current Roles

{% for role in site.data.admin.current_roles %}
**{{ role.title }}** — {{ role.organization }} ({{ role.period }})
{% for item in role.responsibilities %}
- {{ item }}
{% endfor %}

{% endfor %}

## Past Roles

{% for role in site.data.admin.past_roles %}
**{{ role.title }}** — {{ role.organization }} ({{ role.period }})
{% for item in role.responsibilities %}
- {{ item }}
{% endfor %}

{% endfor %}

## Leadership & Institutional Service

{% for item in site.data.admin.leadership_roles %}
**{{ item.role }}**{% if item.period %} ({{ item.period }}){% endif %}  
{{ item.description }}

{% endfor %}

## Academic Service

{% for service in site.data.admin.academic_service %}
**{{ service.role }}**{% if service.period %} ({{ service.period }}){% endif %}
{% if service.venues %}
{% for venue in service.venues %}
- {{ venue }}
{% endfor %}
{% elsif service.description %}
{{ service.description }}
{% endif %}

{% endfor %}
