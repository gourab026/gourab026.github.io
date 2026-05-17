---
title: "case-study"
permalink: tag_case-study.html
sidebar: blog_sidebar
search: include
topnav: topnav
output: web
---

<p class="tag-post-count">
  {%- assign tag_posts = site.tags['case-study'] -%}
  {{ tag_posts | size }} {% if tag_posts.size != 1 %}posts{% else %}post{% endif %} tagged <strong>#case-study</strong>
</p>

{% if site.tags['case-study'] %}
<ul class="tag-post-list">
{% for post in site.tags['case-study'] %}
<li>
  <a href="{{ post.url | remove: '/' }}">
    <span class="tag-post-date">{{ post.date | date: "%b %-d, %Y" }}</span>
    <span class="tag-post-title">{{ post.title }}</span>
  </a>
</li>
{% endfor %}
</ul>
{% else %}
<p class="text-muted">No posts tagged <em>#case-study</em> yet.</p>
{% endif %}
