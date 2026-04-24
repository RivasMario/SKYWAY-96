import json
import re
import os

json_path = r'C:\Users\v-mariorivas\OneDrive - Microsoft\Documents\GitHub\Delta Split 75\kle\deltasplit75_onepiece.json'
pcb_path = r'C:\Users\v-mariorivas\OneDrive - Microsoft\Documents\GitHub\Delta Split 75\pcb\DeltaSplit_ProMicro.kicad_pcb'

with open(json_path, 'r') as f:
    data = json.load(f)

all_keys = []
current_x = 0
current_y = 0
current_w = 1
current_h = 1

for row in data:
    row_has_key = False
    for item in row:
        if isinstance(item, str):
            all_keys.append({
                'legend': item,
                'x': current_x,
                'y': current_y,
                'w': current_w,
                'h': current_h
            })
            current_x += current_w
            current_w = 1
            current_h = 1
            row_has_key = True
        elif isinstance(item, dict):
            if 'x' in item: current_x += item['x']
            if 'y' in item: current_y += item['y']
            if 'w' in item: current_w = item['w']
            if 'h' in item: current_h = item['h']
    current_x = 0
    if row_has_key:
        current_y += 1

# Identify Esc and Title
esc_key = None
title_key = None
for k in all_keys:
    if k['legend'] == 'Esc':
        esc_key = k
        break
for k in all_keys:
    if '86 keys' in k['legend']:
        title_key = k
        break

if not esc_key: esc_key = all_keys[1]
if not title_key: title_key = all_keys[0]

others = [k for k in all_keys if k != esc_key and k != title_key]
ordered_keys = [esc_key] + others + [title_key]

offset_x = -esc_key['x']
offset_y = -esc_key['y']

footprints = []
for i, k in enumerate(ordered_keys):
    sw_num = i + 1
    kx = k['x'] + offset_x
    ky = k['y'] + offset_y
    kw = k['w']
    kh = k['h']
    
    cx = -185 + (kx + kw/2.0 - 0.5) * 19.05
    cy = -133.25 + (ky + kh/2.0 - 0.5) * 19.05
    dy = cy - 5.0 
    
    sw_sexp = f'  (footprint "marbastlib-mx:SW_MX_HS_1u" (layer "F.Cu")\n    (at {cx:.4f} {cy:.4f})\n    (property "Reference" "SW{sw_num}" (at 0 -8.5) (layer "F.SilkS")\n      (effects (font (size 1 1) (thickness 0.15)))\n    )\n    (property "Value" "MX_HS" (at 0 8.5) (layer "F.Fab")\n      (effects (font (size 1 1) (thickness 0.15)))\n    )\n  )'
    
    d_sexp = f'  (footprint "Keebio-Parts:Diode-SOD123" (layer "B.Cu")\n    (at {cx:.4f} {dy:.4f} 180)\n    (property "Reference" "D{sw_num}" (at 0 2) (layer "B.SilkS")\n      (effects (font (size 0.8 0.8) (thickness 0.12)))\n    )\n  )'
    
    footprints.append(sw_sexp)
    footprints.append(d_sexp)

with open(pcb_path, 'r') as f:
    content = f.read()

def find_balanced(text, start_index):
    count = 0
    for i in range(start_index, len(text)):
        if text[i] == "(": count += 1
        elif text[i] == ")":
            count -= 1
            if count == 0: return i + 1
    return -1

# Remove ALL SW and D footprints we might have added or that exist
refs_to_remove = [f"SW{i}" for i in range(1, 100)] + [f"D{i}" for i in range(1, 100)]
for ref in refs_to_remove:
    pattern = f'\\(property "Reference" "{ref}"'
    matches = list(re.finditer(pattern, content))
    for match in reversed(matches):
        prop_start = match.start()
        search_idx = prop_start
        footprint_start = -1
        while True:
            idx = content.rfind("(footprint", 0, search_idx)
            if idx == -1: break
            end = find_balanced(content, idx)
            if end != -1 and end > prop_start:
                footprint_start = idx
                footprint_end = end
                break
            search_idx = idx
        if footprint_start != -1:
            content = content[:footprint_start] + content[footprint_end:]

content = content.strip()
if content.endswith(')'):
    content = content[:-1].strip()

new_content = content + "\n" + "\n".join(footprints) + "\n)\n"

with open(pcb_path, 'w') as f:
    f.write(new_content)

print(f"Successfully cleaned and updated {len(ordered_keys)} keys.")
