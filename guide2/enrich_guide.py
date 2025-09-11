import xml.etree.ElementTree as ET
from tqdm import tqdm
import shutil

# Files
FILTERED_EPG = "clean_epg.xml"   # your filtered guide with only desired channels
FULL_EPG = "epg.xml"             # the original full EPG
OUTPUT_EPG = "enriched_epg.xml"  # output file

# Backup filtered guide just in case
shutil.copyfile(FILTERED_EPG, FILTERED_EPG + ".bak")

# Load filtered guide (to get channels to keep)
filtered_tree = ET.parse(FILTERED_EPG)
filtered_root = filtered_tree.getroot()

# Get list of channel IDs in filtered guide
channels_to_keep = [ch.get("id") for ch in filtered_root.findall("channel")]

# Load full EPG
full_tree = ET.parse(FULL_EPG)
full_root = full_tree.getroot()

# Build dictionary mapping channel id to program list
programs_by_channel = {}
for prog in tqdm(full_root.findall("programme"), desc="Processing programs"):
    ch_id = prog.get("channel")
    if ch_id not in programs_by_channel:
        programs_by_channel[ch_id] = []
    programs_by_channel[ch_id].append(prog)

# Remove existing programs from filtered guide (to replace with full data)
for prog in filtered_root.findall("programme"):
    filtered_root.remove(prog)

# Count total programs to add for progress bar
total_programs = sum(len(programs_by_channel.get(ch_id, [])) for ch_id in channels_to_keep)

# Add programs from full EPG that match filtered channels with progress bar
with tqdm(total=total_programs, desc="Adding programs") as pbar:
    for ch_id in channels_to_keep:
        for prog in programs_by_channel.get(ch_id, []):
            filtered_root.append(prog)
            pbar.update(1)

# Save enriched guide
filtered_tree.write(OUTPUT_EPG, encoding="utf-8", xml_declaration=True)

print(f"✅ Enriched guide saved as '{OUTPUT_EPG}' with programs for {len(channels_to_keep)} channels.")
