---
title: "framework"
permalink: tag_framework.html
sidebar: blog_sidebar
search: include
topnav: topnav
output: web
---

<p class="tag-post-count">
  {%- assign tag_posts = site.tags['framework'] -%}
  {{ tag_posts | size }} {% if tag_posts.size != 1 %}posts{% else %}post{% endif %} tagged <strong>#framework</strong>
</p>

{% if site.tags['framework'] %}
<ul class="tag-post-list">
{% for post in site.tags['framework'] %}
<li>
  <a href="{{ post.url | remove: '/' }}">
    <span class="tag-post-date">{{ post.date | date: "%b %-d, %Y" }}</span>
    <span class="tag-post-title">{{ post.title }}</span>
  </a>
</li>
{% endfor %}
</ul>
{% else %}
<p class="text-muted">No posts tagged <em>#framework</em> yet.</p>
{% endif %}
