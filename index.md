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

<div class="featured-grid">

<a href="tag_cybersecurity.html" class="featured-card">
<h3><i class="fa fa-shield card-icon" aria-hidden="true"></i> Cybersecurity</h3>
<p>Vulnerability assessment, threat analysis, incident response, and security architecture write-ups.</p>
<span class="featured-link">Browse posts →</span>
</a>

<a href="home-lab-1-start-here.html" class="featured-card">
<h3><i class="fa fa-server card-icon" aria-hidden="true"></i> Home Lab</h3>
<p>Building a personal SOC from scratch — SIEM, IDS, threat detection, Splunk, Wazuh, and OpenCTI.</p>
<span class="featured-link">Start the series →</span>
</a>

<a href="tag_python.html" class="featured-card">
<h3><i class="fa fa-code card-icon" aria-hidden="true"></i> Development</h3>
<p>Python security tools, automation scripts, and small projects that scratch real itches.</p>
<span class="featured-link">Browse posts →</span>
</a>

<a href="projects.html" class="featured-card">
<h3><i class="fa fa-rocket card-icon" aria-hidden="true"></i> Projects</h3>
<p>Completed builds and documented experiments — from desktop AI companions to static web tooling.</p>
<span class="featured-link">View projects →</span>
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
