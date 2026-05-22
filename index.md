---
title: Home
sidebar: home_sidebar
permalink: index.html
toc: false
---

<div class="hero">
<h1>Gourab Dasgupta</h1>
<p class="subtitle">Cybersecurity &nbsp;·&nbsp; Security Research &nbsp;·&nbsp; Development</p>
<p>Security professional documenting the journey — home labs, threat intel, CTF write-ups, and tooling. Learning in public.</p>

<div class="cta-buttons">
<a href="portfolio.html" class="btn">View Portfolio</a>
<a href="blog.html" class="btn btn-outline">Read the Blog</a>
<a href="projects.html" class="btn btn-outline">Projects</a>
</div>
</div>

<div class="home-section">

<h2>Featured Work</h2>

<div class="featured-list">

<a href="tag_cybersecurity.html" class="featured-item">
<div class="featured-item-icon"><i class="fa fa-shield" aria-hidden="true"></i></div>
<div class="featured-item-body">
<div class="featured-item-title">Cybersecurity</div>
<div class="featured-item-desc">Vulnerability assessment, threat analysis, incident response, and security architecture write-ups.</div>
</div>
<span class="featured-item-arrow">Browse posts →</span>
</a>

<a href="home-lab-1-start-here.html" class="featured-item">
<div class="featured-item-icon"><i class="fa fa-server" aria-hidden="true"></i></div>
<div class="featured-item-body">
<div class="featured-item-title">Home Lab</div>
<div class="featured-item-desc">Building a personal SOC from scratch — SIEM, IDS, threat detection, Splunk, Wazuh, and OpenCTI.</div>
</div>
<span class="featured-item-arrow">Start the series →</span>
</a>

<a href="tag_python.html" class="featured-item">
<div class="featured-item-icon"><i class="fa fa-code" aria-hidden="true"></i></div>
<div class="featured-item-body">
<div class="featured-item-title">Development</div>
<div class="featured-item-desc">Python security tools, automation scripts, and small projects that scratch real itches.</div>
</div>
<span class="featured-item-arrow">Browse posts →</span>
</a>

<a href="projects.html" class="featured-item">
<div class="featured-item-icon"><i class="fa fa-rocket" aria-hidden="true"></i></div>
<div class="featured-item-body">
<div class="featured-item-title">Projects</div>
<div class="featured-item-desc">Completed builds and documented experiments — from desktop AI companions to static web tooling.</div>
</div>
<span class="featured-item-arrow">View projects →</span>
</a>

</div>

</div>

<div class="home-section">

<h2>Latest Posts</h2>

<div class="blog-preview">
{% assign recent_posts = site.posts | sort: 'date' | reverse | slice: 0, 5 %}
{% for post in recent_posts %}
<div class="blog-preview-item">
  <span class="blog-preview-date">{{ post.date | date: "%b %-d" }}</span>
  <a class="blog-preview-title" href="{{ post.url | remove: '/' }}">{{ post.title }}</a>
</div>
{% endfor %}
</div>

<div class="mt-posts-cta">
<a href="blog.html" class="btn btn-outline">All posts →</a>
</div>

</div>
