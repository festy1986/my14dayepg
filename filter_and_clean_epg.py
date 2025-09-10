import xml.etree.ElementTree as ET
from datetime import datetime

# -------------------------
# CONFIGURATION
# -------------------------
input_file = 'epg.xml'  # your original XML
output_file = 'final_epg.xml'

channels_to_keep = [
    'Comet(COMET).us', 'ABC(WMTW).us', 'FOX(WFXT).us', 'NBC(WBTSCD).us'
    # ... add all your channels here
]
channels_to_keep = [x.replace('&', '&amp;') for x in channels_to_keep]

# -------------------------
# HELPER FUNCTIONS
# -------------------------
def clean_text(text):
    """Remove unwanted words like 'Live', 'NEW', extra parentheses or dashes"""
    if not text:
        return ""
    text = text.replace("– Live", "")
    text = text.replace("(Live)", "")
    text = text.replace("NEW", "")
    return text.strip()

def format_description(programme):
    """
    Format description as:
    Show Name - S<season>E<episode>. Description text. (MM/DD/YYYY)
    """
    title_elem = programme.find('title')
    title_text = clean_text(title_elem.text) if title_elem is not None else "Unknown"

    season = programme.find('season-num')
    episode = programme.find('episode-num')
    season_num = season.text if season is not None else "0"
    episode_num = episode.text if episode is not None else "0"

    desc_elem = programme.find('desc')
    desc_text = clean_text(desc_elem.text) if desc_elem is not None else ""

    start_attr = programme.get('start')
    if start_attr:
        air_date = datetime.strptime(start_attr[:8], '%Y%m%d').strftime('%m/%d/%Y')
    else:
        air_date = "Unknown"

    return f"{title_text} - S{season_num}E{episode_num}. {desc_text} ({air_date})"

# -------------------------
# LOAD XML
# -------------------------
print("Loading XML...")
tree = ET.parse(input_file)
root = tree.getroot()
print("XML loaded. Filtering channels...")

# -------------------------
# FILTER CHANNELS
# -------------------------
for channel in list(root.findall('channel')):
    if channel.get('id') not in channels_to_keep:
        root.remove(channel)

# -------------------------
# CLEAN PROGRAMME TITLES AND DESCRIPTIONS
# -------------------------
for programme in list(root.findall('programme')):
    if programme.get('channel') not in channels_to_keep:
        root.remove(programme)
        continue

    # Clean title
    title_elem = programme.find('title')
    if title_elem is not None and title_elem.text:
        title_elem.text = clean_text(title_elem.text)

    # Create or modify description
    desc_elem = programme.find('desc')
    if desc_elem is None:
        desc_elem = ET.SubElement(programme, 'desc')
    desc_elem.text = format_description(programme)

    # Remove all other elements except title and desc
    for child in list(programme):
        if child.tag not in ('title', 'desc'):
            programme.remove(child)

# -------------------------
# SAVE FINAL XML
# -------------------------
print("Saving final XML...")
tree.write(output_file, encoding='utf-8', xml_declaration=True, method='xml')
print(f"Done! Final XML saved as {output_file}")
