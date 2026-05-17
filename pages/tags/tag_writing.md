---
title: "writing"
permalink: tag_writing.html
sidebar: blog_sidebar
search: include
topnav: topnav
output: web
---

<p class="tag-post-count">
  {%- assign tag_posts = site.tags['writing'] -%}
  {{ tag_posts | size }} {% if tag_posts.size != 1 %}posts{% else %}post{% endif %} tagged <strong>#writing</strong>
</p>

{% if site.tags['writing'] %}
<ul class="tag-post-list">
{% for post in site.tags['writing'] %}
<li>
  <a href="{{ post.url | remove: '/' }}">
    <span class="tag-post-date">{{ post.date | date: "%b %-d, %Y" }}</span>
    <span class="tag-post-title">{{ post.title }}</span>
  </a>
</li>
{% endfor %}
</ul>
{% else %}
<p class="text-muted">No posts tagged <em>#writing</em> yet.</p>
{% endif %}
