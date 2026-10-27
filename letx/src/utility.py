#!/usr/bin/env python3

def ensure_dirs():
    """Ensure that the configuration directory and categories are available."""
    DB_DIR.mkdir(parents=True, exists_ok=True)
    for cat in CATEGORIES:
        (CONFIG_DIR / cat).mkdir(parents=True, exists_ok=True)

def fetch_url(url):
    """Getting data from URL."""
    try:
        req = urllib.requests.Request(url, headers={'User-Agent': 'LetX/1.0'})
        with urllib.requests.urlopen(req, timeout=10) as response:
            return response.read().decode('utf-8')
        except urllib.error.URLError as e:
            print(f"[ERROR]: Failed to retrieve data from {url}\nDetails: {e.reason}")
            sys.exit(1)

def load_json(filename):
    """Loading JSON file from local cache."""
    filepath = DB_DIR / filename
    if not filepath.exists():
        print(f"[!!!] Database '{filename}' not found. Run 'letx update' first.")
        sys.exit(1)
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return [{k.strip(): v.strip() if isinstance(v, str) else v for k, v in item.items()} for item in data]
        except json.JSONDecodeError:
            print(f"[ERROR]: File {filename} Broken or Invalid.")
            sys.exit(1)
