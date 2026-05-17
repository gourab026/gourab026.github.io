#!/usr/bin/env python3
"""
Normalize frontmatter for all posts in _posts.
Will ensure frontmatter contains, in order:
- title
- published
- permalink
- summary
- tags

Rules / assumptions:
- If `published` missing -> set to true
- If `permalink` missing -> derive from filename (remove date prefix and extension, slugify, add .html)
- If `summary` missing -> set to empty string
- If `tags` missing or empty -> set to [uncategorized]
- Preserve existing title, summary, tags when present

This script edits files in place. Make a git commit before running if you want to revert.
"""

import os
import re
import sys
from pathlib import Path

POSTS_DIR = Path(__file__).resolve().parents[1] / '_posts'

slug_re = re.compile(r"[^a-z0-9-]+")

def slugify(s: str) -> str:
    s = s.lower()
    s = s.replace('.md', '')
    s = s.replace('.markdown', '')
    # replace spaces and underscores with hyphens
    s = re.sub(r"[\s_]+", '-', s)
    # remove non-alnum/hyphen
    s = slug_re.sub('-', s)
    s = re.sub(r"-+", '-', s)
    s = s.strip('-')
    return s


def parse_frontmatter(text: str):
    # returns (fm_dict, fm_lines, rest)
    if not text.startswith('---'):
        return None, None, text
    parts = text.split('---', 2)
    if len(parts) < 3:
        return None, None, text
    # parts[0] is empty, parts[1] is frontmatter, parts[2] is rest
    fm_text = parts[1].strip('\n')
    rest = parts[2].lstrip('\n')
    fm_lines = fm_text.splitlines()
    fm = {}
    for line in fm_lines:
        if ':' not in line:
            continue
        key, val = line.split(':', 1)
        key = key.strip()
        val = val.strip()
        fm[key] = val
    return fm, fm_lines, rest


def format_tags(val: str):
    # val may look like "[a, b]" or "" or "\n - a\n - b"
    val = val.strip()
    if val.startswith('[') and val.endswith(']'):
        inner = val[1:-1].strip()
        if not inner:
            return ['uncategorized']
        # split by comma
        tags = [t.strip() for t in inner.split(',') if t.strip()]
        return tags
    # if empty or truthy other forms
    if not val:
        return ['uncategorized']
    # try to parse as YAML list lines
    lines = [l.strip('- ').strip() for l in val.splitlines() if l.strip()]
    if lines:
        return lines
    return [val]


def tags_to_inline(tags):
    elems = [t for t in tags]
    return '[' + ', '.join(elems) + ']'


def process_file(path: Path):
    text = path.read_text(encoding='utf-8')
    fm, fm_lines, rest = parse_frontmatter(text)
    if fm is None:
        print(f"Skipping (no frontmatter): {path}")
        return False
    # Extract values
    title = None
    published = None
    permalink = None
    summary = None
    tags = None

    # preserve raw values if present
    if 'title' in fm:
        title = fm['title'].strip()
    if 'published' in fm:
        published = fm['published'].strip()
    if 'permalink' in fm:
        permalink = fm['permalink'].strip()
    if 'summary' in fm:
        summary = fm['summary'].strip()
    if 'tags' in fm:
        # reconstruct the original tags line content from fm_lines to support multi-line
        # find the tags line index
        tag_line_idx = None
        for i, line in enumerate(fm_lines):
            if line.strip().startswith('tags:'):
                tag_line_idx = i
                break
        if tag_line_idx is not None:
            # collect from tag_line_idx to end or next key
            tag_block = []
            for j in range(tag_line_idx, len(fm_lines)):
                line = fm_lines[j]
                if ':' in line and j != tag_line_idx:
                    # assume new key
                    break
                tag_block.append(line[len('tags:'):].strip() if j==tag_line_idx else line)
            tag_val = '\n'.join(tag_block).strip()
            tags = format_tags(tag_val)

    # Derive defaults
    if not title:
        # try to get from filename after date
        name = path.name
        if re.match(r'^\d{4}-\d{2}-\d{2}-(.*)$', name):
            title = re.sub(r'^\d{4}-\d{2}-\d{2}-(.*)\.md$', r'\1', name)
            title = title.replace('-', ' ').replace('_', ' ').strip()
        else:
            title = path.stem
        title = '"' + title + '"'
    if not published:
        published = 'true'
    if not permalink:
        # derive slug from filename after date
        name = path.name
        slug = name
        m = re.match(r'^\d{4}-\d{2}-\d{2}-(.*)\.(md|markdown)$', name, re.IGNORECASE)
        if m:
            slug = m.group(1)
        else:
            slug = path.stem
        slugified = slugify(slug)
        permalink = slugified + '.html'
    if summary is None:
        summary = ''
    if not tags:
        tags = ['uncategorized']

    # Build new frontmatter lines in requested order
    new_fm_lines = []
    new_fm_lines.append('title: ' + (title if title.startswith('"') else title))
    new_fm_lines.append('published: ' + published)
    new_fm_lines.append('permalink: ' + permalink)
    # ensure summary is quoted if contains double quotes
    if summary:
        # keep existing quoting if present
        if (summary.startswith('"') and summary.endswith('"')) or (summary.startswith("'") and summary.endswith("'")):
            new_fm_lines.append('summary: ' + summary)
        else:
            new_fm_lines.append('summary: "' + summary.replace('"', '\\"') + '"')
    else:
        new_fm_lines.append('summary: ""')
    new_fm_lines.append('tags: ' + tags_to_inline(tags))

    new_text = '---\n' + '\n'.join(new_fm_lines) + '\n---\n\n' + rest
    if new_text != text:
        path.write_text(new_text, encoding='utf-8')
        print(f"Updated: {path}")
        return True
    else:
        print(f"No change: {path}")
        return False


def main():
    if not POSTS_DIR.exists():
        print("_posts directory not found", file=sys.stderr)
        return
    changed = 0
    total = 0
    for p in sorted(POSTS_DIR.glob('*.md')):
        total += 1
        if process_file(p):
            changed += 1
    print(f"Processed {total} files, updated {changed} files.")

if __name__ == '__main__':
    main()
