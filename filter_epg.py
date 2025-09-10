import xml.etree.ElementTree as ET

input_file = 'epg.xml'
output_file = 'filtered_epg.xml'

print("Loading XML file...")
tree = ET.parse(input_file)
root = tree.getroot()
print("XML loaded. Filtering channels...")

# Paste your channel IDs exactly like this example:
channels_to_keep = [
    'ABC(WMTWDT).us',
    'Laff(LAFF).us',
    'Comet(COMET).us',
    # add the rest of your channels here
]

count_removed = 0
for i, channel in enumerate(root.findall('channel'), 1):
    if channel.get('id') not in channels_to_keep:
        root.remove(channel)
        count_removed += 1
    if i % 100 == 0:  # print every 100 channels
        print(f"Processed {i} channels...")

print(f"Filtering complete. {count_removed} channels removed.")
print("Saving new XML...")
tree.write(output_file, encoding='utf-8')
print("Done! filtered_epg.xml created.")
