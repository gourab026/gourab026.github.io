#!/usr/bin/env python3
"""
Generate tag pages for all tags found in posts.
This creates a page for each tag that Jekyll's tag functionality can display.
"""

import os
import re
from pathlib import Path

POSTS_DIR = Path(__file__).resolve().parents[1] / '_posts'
TAGS_DIR = Path(__file__).resolve().parents[1] / 'pages' / 'tags'

def extract_tags_from_posts():
    """Extract all unique tags from posts."""
    tags = set()
    for post_file in POSTS_DIR.glob('*.md'):
        content = post_file.read_text(encoding='utf-8')
        # Extract tags from frontmatter
        match = re.search(r'tags:\s*\[(.*?)\]', content)
        if match:
            tag_str = match.group(1)
            # Parse tags
            tag_list = [t.strip() for t in tag_str.split(',')]
            tags.update(tag_list)
    return sorted(tags)


def create_tag_page(tag_name):
    """Create a tag page for the given tag."""
    # Slugify tag name for filename
    slug = tag_name.lower().replace(' ', '-').replace('_', '-')
    slug = re.sub(r'[^a-z0-9-]+', '', slug)
    slug = re.sub(r'-+', '-', slug).strip('-')
    
    filename = TAGS_DIR / f'tag_{slug}.md'
    
    # If already exists, skip
    if filename.exists():
        print(f"Skipping (exists): {filename.name}")
        return False
    
    # Create frontmatter with Liquid template (not Python f-string)
    frontmatter = """---
title: "{tag}"
sidebar: blog_sidebar
search: include
topnav: topnav
output: web
---

{{% for post in site.tags['{tag}'] %}}
* [{{{{ post.title }}}}]({{{{ post.url | remove: '/' }}}}) - {{{{ post.date | date: "%b %d, %Y" }}}}
{{% endfor %}}
""".format(tag=tag_name)
    
    filename.write_text(frontmatter, encoding='utf-8')
    print(f"Created: {filename.name}")
    return True


def main():
    if not TAGS_DIR.exists():
        TAGS_DIR.mkdir(parents=True)
    
    tags = extract_tags_from_posts()
    print(f"Found {len(tags)} unique tags")
    
    created = 0
    for tag in tags:
        if create_tag_page(tag):
            created += 1
    
    print(f"\nCreated {created} new tag pages")


if __name__ == '__main__':
    main()
