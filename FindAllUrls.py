import requests
import argparse
from concurrent.futures import ThreadPoolExecutor
from bs4 import BeautifulSoup

WAYBACK_API_URL = "http://web.archive.org/cdx/search/cdx"
ALIENVAULT_URL = "https://otx.alienvault.com/api/v1/indicators/domain/{domain}/url_list"
URLSCAN_URL = "https://urlscan.io/api/v1/search/"

def get_latest_commoncrawl_index():
    """
    Fetch the latest Common Crawl index dynamically.
    """
    try:
        response = requests.get("http://index.commoncrawl.org/")
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        # Parse available indices from the HTML
        links = soup.find_all("a", href=True)
        indices = [link['href'].strip("/") for link in links if "CC-MAIN" in link['href']]
        latest_index = sorted(indices, reverse=True)[0]
        return latest_index
    except Exception as e:
        print(f"Error fetching latest Common Crawl index: {e}")
        return None

def fetch_wayback_urls(domain, include_subdomains=True):
    params = {
        "url": f"*.{domain}" if include_subdomains else domain,
        "output": "json",
        "fl": "original",
        "filter": "statuscode:200",
    }
    response = requests.get(WAYBACK_API_URL, params=params)
    response.raise_for_status()
    data = response.json()
    return [row[0] for row in data[1:]]  # Skip header row

def fetch_alienvault_urls(domain):
    url = ALIENVAULT_URL.format(domain=domain)
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    return [entry['url'] for entry in data.get('url_list', [])]

def fetch_commoncrawl_urls(domain):
    """
    Fetch URLs from Common Crawl for the given domain.
    """
    try:
        latest_index = get_latest_commoncrawl_index()
        if not latest_index:
            print("Unable to determine the latest Common Crawl index.")
            return []

        COMMONCRAWL_URL = f"http://index.commoncrawl.org/{latest_index}-index"
        params = {
            "url": f"*.{domain}",
            "output": "json",
            "filter": "statuscode:200",
        }
        response = requests.get(COMMONCRAWL_URL, params=params)
        response.raise_for_status()
        data = response.json()
        return [entry['url'] for entry in data]
    except requests.exceptions.RequestException as e:
        print(f"Error fetching from Common Crawl: {e}")
        return []

def fetch_urlscan_urls(domain, api_key):
    headers = {"API-Key": api_key}
    params = {"q": domain}
    response = requests.get(URLSCAN_URL, headers=headers, params=params)
    response.raise_for_status()
    data = response.json()
    return [result['page']['url'] for result in data.get('results', [])]

def merge_results(*args, unique=True):
    merged = set() if unique else []
    for urls in args:
        if unique:
            merged.update(urls)
        else:
            merged.extend(urls)
    return sorted(merged) if unique else merged

def main():
    parser = argparse.ArgumentParser(description="Combine functionality of waybackurls and gau.")
    parser.add_argument("domain", help="The domain to fetch URLs for.")
    parser.add_argument("--no-subs", action="store_true", help="Exclude subdomains from the search.")
    parser.add_argument("--threads", type=int, default=5, help="Number of threads to use.")
    parser.add_argument("--api-key", help="API key for URLScan.io.")
    parser.add_argument("--unique", action="store_true", help="Ensure unique and sorted URLs in output.")
    args = parser.parse_args()

    include_subdomains = not args.no_subs
    with ThreadPoolExecutor(max_workers=args.threads) as executor:
        futures = [
            executor.submit(fetch_wayback_urls, args.domain, include_subdomains),
            executor.submit(fetch_alienvault_urls, args.domain),
            executor.submit(fetch_commoncrawl_urls, args.domain),
        ]
        if args.api_key:
            futures.append(executor.submit(fetch_urlscan_urls, args.domain, args.api_key))

        results = [future.result() for future in futures]

    merged_results = merge_results(*results, unique=args.unique)
    for url in merged_results:
        print(url)

if __name__ == "__main__":
    main()
