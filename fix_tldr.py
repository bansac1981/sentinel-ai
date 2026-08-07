import os
import re
import json

posts_dir = os.path.join(os.path.dirname(__file__), "hugo-site", "content", "posts")

# Pattern 1: tldr_actions: "[\"...\"]"  (outer double-quoted YAML string, inner backslash-escaped)
pattern_quoted = re.compile(r'^(tldr_actions: )"(.*)"(\s*)$', re.MULTILINE)

# Pattern 2: tldr_actions: ["...","..."]  (unquoted JSON array as YAML value)
pattern_unquoted = re.compile(r'^(tldr_actions: )(\[.*\])(\s*)$', re.MULTILINE)

fixed = 0
skipped = 0
errors = []

for fname in sorted(os.listdir(posts_dir)):
    if not fname.endswith('.md'):
        continue
    fpath = os.path.join(posts_dir, fname)
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()

    match = pattern_quoted.search(content)
    if match:
        raw = match.group(2).replace('\\"', '"')
        pat = pattern_quoted
    else:
        match = pattern_unquoted.search(content)
        if match:
            raw = match.group(2)
            pat = pattern_unquoted
        else:
            skipped += 1
            continue

    try:
        actions = json.loads(raw)
    except Exception as e:
        errors.append((fname, str(e), repr(raw[:80])))
        continue

    yaml_lines = '\n'.join('  - "' + a.replace('"', '\\"') + '"' for a in actions)
    replacement = 'tldr_actions:\n' + yaml_lines + match.group(3)
    new_content = pat.sub(replacement, content)

    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    fixed += 1

print(f"Fixed: {fixed}, skipped (already ok): {skipped}")
if errors:
    print(f"Errors ({len(errors)}):")
    for fname, err, snippet in errors[:10]:
        print(f"  {fname}: {err} | {snippet}")
