# Unified Security Workflow for Fetching URLs

## Overview
This script is designed to fetch URLs related to a specified domain from various sources, including AlienVault OTX, URLScan.io, the Wayback Machine, and Shodan. It provides a unified interface to aggregate, process, and optionally save the results to a file.

## Features
- Fetch URLs from multiple sources:
  - AlienVault OTX
  - URLScan.io
  - Wayback Machine
  - Shodan
- Support for parallel fetching using threads.
- Option to ensure unique and sorted URLs in the output.
- Save the results to a specified file.

## Requirements
- Python 3.7+
- `requests` library

## Installation
1. Clone or download this repository.
2. Install the required dependencies:
   ```bash
   pip install requests
   ```

## Usage
Run the script with the following command:
```bash
python script_name.py <domain> [options]
```

### Positional Arguments
- `domain`: The domain to fetch URLs for.

### Optional Arguments
- `--api-key-urlscan`: API key for URLScan.io (optional).
- `--api-key-shodan`: API key for Shodan (optional).
- `--unique`: Ensure unique and sorted URLs in the output.
- `--threads`: Number of threads to use (default: 5).
- `--output`: File path to save the results.

### Example
1. Fetch URLs for `example.com` and ensure the output is unique and sorted:
   ```bash
   python script_name.py example.com --unique
   ```
2. Fetch URLs for `example.com` and save the results to `output.txt`:
   ```bash
   python script_name.py example.com --output output.txt
   ```
3. Fetch URLs for `example.com` using API keys for URLScan.io and Shodan:
   ```bash
   python script_name.py example.com --api-key-urlscan YOUR_URLSCAN_API_KEY --api-key-shodan YOUR_SHODAN_API_KEY
   ```

## Functions

### `fetch_alienvault_urls(domain)`
Fetch URLs from AlienVault OTX.

### `fetch_urlscan_urls(domain, api_key)`
Fetch URLs from URLScan.io (requires API key).

### `fetch_wayback_urls(domain)`
Fetch URLs from the Wayback Machine.

### `fetch_shodan_urls(domain, api_key)`
Fetch URLs from Shodan (requires API key).

### `merge_results(*args, unique=True)`
Merge results from all sources, ensuring uniqueness if required.

### `save_results_to_file(results, file_path)`
Save results to a specified file.

## Notes
- Make sure to replace `YOUR_URLSCAN_API_KEY` and `YOUR_SHODAN_API_KEY` with your actual API keys.
- Results will be printed to the console if no output file is specified.
- The script uses threading for better performance when fetching from multiple sources.

## License
This project is licensed under the MIT License. See the LICENSE file for details.

## Contribution
Feel free to submit issues and pull requests to improve the script.
