#!/usr/bin/env python3
# fix_jinja_blocks.py
# Respalda templates/, unifica "block body" -> "block content" y fusiona bloques duplicados por archivo.

import os, re, shutil, datetime, zipfile

TEMPLATES_DIR = "templates"

def backup_templates():
    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    archive_name = f"templates_backup_{ts}.zip"
    print(f"[+] Creando backup: {archive_name}")
    shutil.make_archive(f"templates_backup_{ts}", 'zip', TEMPLATES_DIR)
    print("[+] Backup creado.")

# Encuentra todos los bloques en un archivo, devolviendo lista de dicts con posiciones
BLOCK_TOKEN_RE = re.compile(r'{%\s*(block\s+([A-Za-z_][A-Za-z0-9_]*)|endblock(?:\s+[A-Za-z_][A-Za-z0-9_]*)?)\s*%}', re.IGNORECASE)

def find_blocks_positions(content):
    matches = list(BLOCK_TOKEN_RE.finditer(content))
    stack = []
    blocks = []  # each: {name, start, open_end, inner_start, inner_end, end}
    for m in matches:
        token = m.group(1)
        name = m.group(2)
        if token.lower().startswith("block"):
            stack.append({'name': name, 'start': m.start(), 'open_end': m.end()})
        else:
            # endblock
            if not stack:
                # unmatched endblock - ignore
                continue
            last = stack.pop()
            last['end'] = m.end()
            last['inner_start'] = last['open_end']
            last['inner_end'] = m.start()
            blocks.append(last)
    # blocks list contains blocks in the order they closed (not necessarily start order)
    # sort by start for predictability
    blocks.sort(key=lambda b: b['start'])
    return blocks

def unify_body_to_content(content):
    # Reemplaza { % block body % } -> { % block content % } (case-insensitive)
    content2 = re.sub(r'{%\s*block\s+body\s*%}', '{% block content %}', content, flags=re.IGNORECASE)
    # Reemplaza { % endblock body % } -> { % endblock % }
    content2 = re.sub(r'{%\s*endblock\s+body\s*%}', '{% endblock %}', content2, flags=re.IGNORECASE)
    return content2

def fix_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        orig = f.read()
    content = unify_body_to_content(orig)

    blocks = find_blocks_positions(content)
    # group by name
    by_name = {}
    for b in blocks:
        by_name.setdefault(b['name'], []).append(b)

    modified = False
    report = []
    # For each block name that appears more than once, merge inner contents into first occurrence
    for name, occ in by_name.items():
        if len(occ) <= 1:
            continue
        # Sort occurrences by start
        occ_sorted = sorted(occ, key=lambda x: x['start'])
        first = occ_sorted[0]
        rest = occ_sorted[1:]
        # collect inner texts from rest in ascending order
        collected = []
        # We'll remove rest occurrences from content (reverse order to not break indices),
        # then insert the collected text just before the first block's end (its inner_end).
        for r in reversed(rest):
            inner = content[r['inner_start']:r['inner_end']]
            collected.insert(0, inner)  # keep original order
            # remove the whole r block (from start to end)
            content = content[:r['start']] + content[r['end']:]
        # Now, insert collected text into first block before its endblock.
        # But first need to recompute first.inner_end in the modified content:
        # Recompute blocks again to get updated positions for the first block.
        new_blocks = find_blocks_positions(content)
        # find first block by matching start range approximate (by name and original start)
        # choose the leftmost block with same name
        candidates = [b for b in new_blocks if b['name'] == name]
        if not candidates:
            # unexpected; skip
            continue
        new_first = sorted(candidates, key=lambda x: x['start'])[0]
        insert_pos = new_first['inner_end']
        added_text = ("\n\n" + "\n\n".join(collected) + "\n\n").strip()
        if added_text:
            # Place added_text before insert_pos
            content = content[:insert_pos] + "\n\n" + added_text + content[insert_pos:]
            modified = True
            report.append((name, len(occ_sorted), path))
    if modified:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
    return modified, report

def walk_and_fix():
    all_reports = []
    changed_files = []
    for root, _, files in os.walk(TEMPLATES_DIR):
        for filename in files:
            if not filename.lower().endswith(".html"):
                continue
            path = os.path.join(root, filename)
            try:
                mod, rep = fix_file(path)
                if mod:
                    changed_files.append(path)
                    all_reports.extend(rep)
                    print(f"[MODIFIED] {path}")
            except Exception as e:
                print(f"[ERROR] {path}: {e}")
    print("---- Summary ----")
    if changed_files:
        print(f"Modified files ({len(changed_files)}):")
        for p in changed_files:
            print(" -", p)
    else:
        print("No files modified.")
    if all_reports:
        print("\nMerged duplicate blocks (name, occurrences, file):")
        for r in all_reports:
            print(" -", r)
    print("\n[Done]")

if __name__ == "__main__":
    if not os.path.isdir(TEMPLATES_DIR):
        print(f"ERROR: carpeta '{TEMPLATES_DIR}' no encontrada. Ejecuta el script desde la raíz del proyecto.")
        exit(1)
    backup_templates()
    walk_and_fix()
    print("IMPORTANTE: reinicia tu servidor Flask y borra __pycache__ si es necesario.")
