import re

pcb_path = r'C:\Users\v-mariorivas\OneDrive - Microsoft\Documents\GitHub\Delta Split 75\pcb\DeltaSplit_ProMicro.kicad_pcb'

with open(pcb_path, 'r') as f:
    content = f.read()

def find_balanced(text, start_index):
    count = 0
    for i in range(start_index, len(text)):
        if text[i] == "(":
            count += 1
        elif text[i] == ")":
            count -= 1
            if count == 0:
                return i + 1
    return -1

def remove_footprints(text, refs):
    # Sort refs by length descending to avoid partial matches if they were just numbers, 
    # but here we use exact reference property matching.
    
    # We find all (footprint ... (property "Reference" "REF" ...))
    # Since they might be anywhere, we find the property first, then look backwards for the start of the footprint.
    
    for ref in refs:
        # Match (property "Reference" "ref"
        # We use a pattern that matches the property line.
        pattern = f'\\(property "Reference" "{ref}"'
        matches = list(re.finditer(pattern, text))
        
        # Process matches in reverse to not mess up indices
        for match in reversed(matches):
            prop_start = match.start()
            
            # Find the start of the footprint block.
            # We look backwards for "(footprint" that contains this property.
            # This is tricky because there might be other footprints.
            # However, in KiCad, footprints are top-level items inside (kicad_pcb ...).
            # So we look for the nearest "(footprint" before prop_start that is NOT inside another footprint.
            
            # Search backwards for "(footprint"
            footprint_start = -1
            search_idx = prop_start
            while True:
                idx = text.rfind("(footprint", 0, search_idx)
                if idx == -1: break
                # Check if this footprint block contains the property.
                end = find_balanced(text, idx)
                if end != -1 and end > prop_start:
                    footprint_start = idx
                    footprint_end = end
                    break
                search_idx = idx
            
            if footprint_start != -1:
                print(f"Removing {ref} at {footprint_start}")
                text = text[:footprint_start] + text[footprint_end:]
    
    return text

# The SW1 and D1 I added have decimal points, the original might not.
# My script added SW1 to SW86.
# I want to remove ANY SW1 and D1.
new_content = remove_footprints(content, ["SW1", "D1"])

with open(pcb_path, 'w') as f:
    f.write(new_content)
