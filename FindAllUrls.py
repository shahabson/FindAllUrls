import requests
import argparse
from concurrent.futures import ThreadPoolExecutor

# API Endpoints
ALIENVAULT_URL = "https://otx.alienvault.com/api/v1/indicators/domain/{domain}/url_list"
URLSCAN_URL = "https://urlscan.io/api/v1/search/"
WAYBACK_API_URL = "http://web.archive.org/cdx/search/cdx"
SHODAN_SEARCH_URL = "https://api.shodan.io/shodan/host/search"

def fetch_alienvault_urls(domain):
    """
    Fetch URLs from AlienVault OTX.
    """
    try:
        url = ALIENVAULT_URL.format(domain=domain)
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return [entry['url'] for entry in data.get('url_list', [])]
    except requests.exceptions.RequestException as e:
        print(f"Error fetching from AlienVault: {e}")
        return []

def fetch_urlscan_urls(domain, api_key):
    """
    Fetch URLs from URLScan.io.
    """
    try:
        headers = {"API-Key": api_key}
        params = {"q": domain}
        response = requests.get(URLSCAN_URL, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        return [result['page']['url'] for result in data.get('results', [])]
    except requests.exceptions.RequestException as e:
        print(f"Error fetching from URLScan.io: {e}")
        return []

def fetch_wayback_urls(domain):
    """
    Fetch URLs from the Wayback Machine.
    """
    try:
        params = {
            "url": f"*.{domain}",
            "output": "json",
            "fl": "original",
            "filter": "statuscode:200",
        }
        response = requests.get(WAYBACK_API_URL, params=params)
        response.raise_for_status()
        data = response.json()
        return [row[0] for row in data[1:]]  # Skip header row
    except requests.exceptions.RequestException as e:
        print(f"Error fetching from Wayback Machine: {e}")
        return []

def fetch_shodan_urls(domain, api_key):
    """
    Fetch URLs from Shodan.
    """
    try:
        params = {"query": domain, "key": api_key}
        response = requests.get(SHODAN_SEARCH_URL, params=params)
        response.raise_for_status()
        data = response.json()
        return [match['ip_str'] for match in data.get('matches', [])]  # Use IPs as URLs
    except requests.exceptions.RequestException as e:
        print(f"Error fetching from Shodan: {e}")
        return []

def merge_results(*args, unique=True):
    """
    Merge results from all sources, ensuring uniqueness if required.
    """
    merged = set() if unique else []
    for urls in args:
        if unique:
            merged.update(urls)
        else:
            merged.extend(urls)
    return sorted(merged) if unique else merged

def save_results_to_file(results, file_path):
    """
    Save results to a specified file.
    """
    try:
        with open(file_path, "w") as file:
            for url in results:
                file.write(f"{url}\n")
        print(f"Results saved to {file_path}")
    except Exception as e:
        print(f"Error saving results to file: {e}")

def main():
    parser = argparse.ArgumentParser(description="Unified security workflow for fetching URLs.")
    parser.add_argument("domain", help="The domain to fetch URLs for.")
    parser.add_argument("--api-key-urlscan", help="API key for URLScan.io.")
    parser.add_argument("--api-key-shodan", help="API key for Shodan.")
    parser.add_argument("--unique", action="store_true", help="Ensure unique and sorted URLs in output.")
    parser.add_argument("--threads", type=int, default=5, help="Number of threads to use.")
    parser.add_argument("--output", help="File path to save the results.")
    args = parser.parse_args()

    domain = args.domain
    unique = args.unique

    # Create a thread pool for parallel fetching
    with ThreadPoolExecutor(max_workers=args.threads) as executor:
        futures = [
            executor.submit(fetch_alienvault_urls, domain),
            executor.submit(fetch_wayback_urls, domain),
        ]
        # Add URLScan.io if API key is provided
        if args.api_key_urlscan:
            futures.append(executor.submit(fetch_urlscan_urls, domain, args.api_key_urlscan))
        # Add Shodan if API key is provided
        if args.api_key_shodan:
            futures.append(executor.submit(fetch_shodan_urls, domain, args.api_key_shodan))

        # Collect results from all threads
        results = [future.result() for future in futures]

    # Merge results
    merged_results = merge_results(*results, unique=unique)

    # Save results to a file if output is specified
    if args.output:
        save_results_to_file(merged_results, args.output)
    else:
        for url in merged_results:
            print(url)

if __name__ == "__main__":
    main()
