# Posting Guide

Everything you need to add new content to the blog.

---

## Folder Structure

```
gourab026.github.io/
├── _posts/           ← all blog posts go here
├── pages/            ← static pages (blog, portfolio, projects, etc.)
├── images/           ← images and static assets
├── css/
│   └── site-theme.css  ← all custom styles
├── _data/
│   ├── sidebars/     ← sidebar nav definitions (YAML)
│   ├── tags/         ← allowed-tags list
│   └── topnav.yml    ← top navbar links
├── _layouts/         ← page templates
├── _includes/        ← reusable HTML partials
└── _config.yml       ← site-wide config
```

---

## Writing a New Post

### 1. File location and naming

All posts go in `_posts/`. The filename must follow this exact format:

```
YYYY-MM-DD-your-post-title.md
```

Examples:
```
_posts/2025-06-15-active-directory-attacks.md
_posts/2025-07-01-wazuh-custom-rules.md
```

The date in the filename controls when the post appears and how it sorts. Future-dated posts will not appear until that date passes.

### 2. Post frontmatter template

Copy this block to the top of every new post:

```yaml
---
title: "Your Post Title"
date: YYYY-MM-DD HH:MM:SS +0000
tags: [cybersecurity]
summary: "One sentence describing the post — appears as a subtitle under the title."
---
```

**Required fields:**
- `title` — displayed at the top of the post and in the blog list
- `date` — must match the filename date; include time as `00:00:00 +0000` if you don't have a specific time

**Optional fields:**
- `tags` — one or more tags from the allowed list (see Tags section below)
- `summary` — short description shown at the top of the post

### 3. Post body

Write standard Markdown below the frontmatter block. Everything works as expected:

```markdown
## Section Heading

Normal paragraph text.

- Bullet list item
- Another item

**Bold text**, *italic text*, `inline code`

```python
# Code block
print("hello world")
```

[Link text](https://example.com)
```

Images (see below for where to put image files):

```markdown
![Alt text](images/your-image.png)
```

---

## Allowed Tags

Tags must match this exact list (case-sensitive). Using a tag not on this list will not break the build, but the tag will not link to a tag page.

Current allowed tags (defined in `_data/tags/allowed-tags.yml`):

- `cybersecurity`
- `home-lab`
- `python`
- `osint`
- `phishing-analysis`
- `malware`
- `ctf`
- `automation`
- `networking`
- `web`
- `tools`
- `risk-management`
- `governance`
- `incident-response`
- `identity`
- `hardening`

Add multiple tags as a YAML list:

```yaml
tags: [cybersecurity, malware, home-lab]
```

To add a new tag, you need to:
1. Add it to `_data/tags/allowed-tags.yml`
2. Create a tag page in `pages/tags/tag_yournewtag.md` (copy an existing one and update the tag name and title)

---

## Images and Static Files

### Images

Put all images in the `images/` folder at the project root.

Reference them in posts like this:

```markdown
![Description](images/filename.png)
```

Or with HTML for sizing control:

```html
<img src="images/filename.png" alt="Description" style="max-width: 100%;">
```

Supported formats: PNG, JPG, GIF, SVG, WebP.

### Other static files

PDFs, downloads, or other attachments go in the same `images/` folder (or create a dedicated `files/` or `downloads/` folder — Jekyll will copy any non-underscore folder to `_site/`).

Reference a PDF:

```markdown
[Download PDF](images/report.pdf)
```

---

## Static Pages

Static pages (not posts) live in `pages/`. They use a different frontmatter format:

```yaml
---
title: Page Title
sidebar: home_sidebar
permalink: page-name.html
toc: false
---
```

**Key fields:**
- `permalink` — the URL of the page (e.g. `projects.html` → `yourdomain/projects.html`)
- `sidebar` — which sidebar nav to show (defined in `_data/sidebars/`)
- `toc: false` — disable the auto table-of-contents (useful for landing pages)

**Note:** Markdown headings (`##`) do not render inside HTML `<div>` blocks in pages. Use raw `<h2>` tags instead if you wrap content in divs.

---

## Building and Serving Locally

Run the dev server:

```bash
bundle exec jekyll serve --livereload
```

Then open `http://localhost:4000` in a browser. Changes to posts and pages reload automatically.

Build without serving (for checking output):

```bash
bundle exec jekyll build
```

Output goes to `_site/`. Do not commit this folder — it is in `.gitignore`.

If the port is busy (e.g. another instance is running):

```bash
bundle exec jekyll serve --port 4001
```

---

## Publishing (Git Push)

Commit and push to `main`:

```bash
git add _posts/2025-06-15-your-new-post.md images/any-new-image.png
git commit -m "add post: Your Post Title"
git push origin main
```

GitHub Pages rebuilds automatically after each push. Allow 1–2 minutes for changes to appear live.

---

## Quick Reference

| What | Where |
|------|-------|
| New post | `_posts/YYYY-MM-DD-title.md` |
| Images | `images/` |
| Static pages | `pages/` |
| Tag pages | `pages/tags/tag_name.md` |
| Allowed tags list | `_data/tags/allowed-tags.yml` |
| Sidebar nav | `_data/sidebars/home_sidebar.yml` |
| Top navbar | `_data/topnav.yml` |
| Site config | `_config.yml` |
| All styles | `css/site-theme.css` |
