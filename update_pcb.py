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

if not esc_key:
    # Fallback if legend is different
    esc_key = all_keys[1]
if not title_key:
    title_key = all_keys[0]

# Build ordered list: Esc (SW1), then others (except Title), then Title (SW86)
others = [k for k in all_keys if k != esc_key and k != title_key]
ordered_keys = [esc_key] + others + [title_key]

# Offset to make Esc (0,0)
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
    dy = cy - 5.0  # Match manual test D1 at -138.25
    
    sw_sexp = f'  (footprint "marbastlib-mx:SW_MX_HS_1u" (layer "F.Cu")\n    (at {cx:.4f} {cy:.4f})\n    (property "Reference" "SW{sw_num}" (at 0 -8.5) (layer "F.SilkS")\n      (effects (font (size 1 1) (thickness 0.15)))\n    )\n    (property "Value" "MX_HS" (at 0 8.5) (layer "F.Fab")\n      (effects (font (size 1 1) (thickness 0.15)))\n    )\n  )'
    
    d_sexp = f'  (footprint "Keebio-Parts:Diode-SOD123" (layer "B.Cu")\n    (at {cx:.4f} {dy:.4f} 180)\n    (property "Reference" "D{sw_num}" (at 0 2) (layer "B.SilkS")\n      (effects (font (size 0.8 0.8) (thickness 0.12)))\n    )\n  )'
    
    footprints.append(sw_sexp)
    footprints.append(d_sexp)

with open(pcb_path, 'r') as f:
    pcb_content = f.read()

# Robust removal of SW1 and D1 footprints
def remove_footprint(content, ref):
    pattern = r'\(footprint [^)]+\(property "Reference" "' + ref + r'"'
    match = re.search(pattern, content)
    if not match: return content
    
    start = match.start()
    # Find the balanced closing parenthesis
    count = 0
    end = -1
    for i in range(start, len(content)):
        if content[i] == "(":
            count += 1
        elif content[i] == ")":
            count -= 1
            if count == 0:
                end = i + 1
                break
    if end != -1:
        return content[:start] + content[end:]
    return content

pcb_content = remove_footprint(pcb_content, 'SW1')
pcb_content = remove_footprint(pcb_content, 'D1')

pcb_content = pcb_content.strip()
if pcb_content.endswith(')'):
    pcb_content = pcb_content[:-1].strip()

new_content = pcb_content + "\n" + "\n".join(footprints) + "\n)\n"

with open(pcb_path, 'w') as f:
    f.write(new_content)

print(f"Successfully processed {len(ordered_keys)} keys.")
