import gzip
import shutil

with gzip.open('epg.xml.gz', 'rb') as f_in:
    with open('epg.xml', 'wb') as f_out:
        shutil.copyfileobj(f_in, f_out)

print("epg.xml has been created successfully.")
