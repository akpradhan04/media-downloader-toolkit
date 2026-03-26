######################
"""
Summary:
   This script downloads media from multiple .m3u8 playlist URLs and saves each stream as a .ts file.
   It uses a dictionary to map output filenames to their corresponding playlist links, fetches all
   video segments listed in each playlist, and merges them sequentially into a single file per entry.
"""
######################

import requests
from urllib.parse import urljoin

m3u8_dict = {
    "song1.ts": "https://example.com/stream1.m3u8",
    "song2.ts": "https://example.com/stream2.m3u8",
    "song3.ts": "https://example.com/stream3.m3u8"
}

headers = {
    "User-Agent": "Mozilla/5.0"
}

def download_m3u8(m3u8_url, output_file):
    r = requests.get(m3u8_url, headers=headers)
    lines = r.text.splitlines()

    segments = [line for line in lines if line and not line.startswith("#")]

    with open(output_file, "wb") as f:
        for i, seg in enumerate(segments):
            seg_url = urljoin(m3u8_url, seg)
            print(f"{output_file}: {i+1}/{len(segments)}")

            res = requests.get(seg_url, headers=headers)
            f.write(res.content)

    print(f"Saved as {output_file}")


for filename, url in m3u8_dict.items():
    print(f"\nDownloading → {filename}")
    download_m3u8(url, filename)
