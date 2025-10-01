# save_as: download_openface_features.py
import os
import urllib.parse
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
import urllib3

BASE_URL = "https://sigmedia.tcd.ie/room_reader_corpus_db/features/OpenFace_Features/"
DEST_FOLDER = "OpenFace_Features"
HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; dataset-downloader/1.0)"}

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def fetch_links(url):
    """Get all file links from a directory index page (skip external)."""
    r = requests.get(url, headers=HEADERS, timeout=30, verify=False)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "html.parser")
    links = []
    for a in soup.find_all("a", href=True):
        href = a["href"]
        if href in ("../", "/"):
            continue
        full_url = urllib.parse.urljoin(url, href)
        # Only keep links inside our dataset base url
        if full_url.startswith(BASE_URL):
            links.append(full_url)
    return links

def download_file(url, dest_path):
    """Download one file with progress bar."""
    if os.path.exists(dest_path):
        return
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with requests.get(url, headers=HEADERS, timeout=60, stream=True, verify=False) as r:
        if r.status_code == 200 and "text/html" not in r.headers.get("Content-Type", ""):
            total = int(r.headers.get("content-length", 0))
            with open(dest_path, "wb") as f, tqdm(
                total=total, unit="B", unit_scale=True,
                desc=os.path.basename(dest_path), leave=False
            ) as pbar:
                for chunk in r.iter_content(chunk_size=1024*1024):
                    if chunk:
                        f.write(chunk)
                        pbar.update(len(chunk))
        else:
            print(f"⚠️ Skipping (not a file): {url}")

def main():
    links = fetch_links(BASE_URL)
    print(f"Found {len(links)} items in {BASE_URL}")
    for link in links:
        filename = link.split("/")[-1]
        dest_path = os.path.join(DEST_FOLDER, filename)
        print(f"⬇️ Downloading {filename}")
        download_file(link, dest_path)

if __name__ == "__main__":
    main()
    print("✅ All downloads completed.")
