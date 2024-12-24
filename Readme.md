# README for Final First Script

## Overview
The script is a URL processing tool that extracts various components from URLs. It fetches URLs from multiple sources such as:

- Wayback Machine
- AlienVault OTX
- Common Crawl
- URLScan.io (optional, requires an API key)

### Features:
- Fetch URLs from multiple sources.
- Support for subdomain inclusion/exclusion.
- Multithreaded processing for faster execution.
- JSON and TXT output formats.
- Option to ensure unique and sorted results.

## Usage

### Prerequisites
- Python 3.6 or higher
- Install required libraries:
  ```bash
  pip install requests
  ```

### Command-Line Arguments

| Argument        | Description                                                                 | Default    |
|-----------------|-----------------------------------------------------------------------------|------------|
| `domain`        | The domain to fetch URLs for.                                               | Required   |
| `--no-subs`     | Exclude subdomains from the search.                                         | False      |
| `--threads`     | Number of threads for parallel processing.                                  | 5          |
| `--api-key`     | API key for URLScan.io.                                                     | None       |
| `--unique`      | Ensure unique and sorted results.                                           | False      |
| `--output`      | Output file to save results. If omitted, results are printed to the console.| None       |
| `--format`      | Output format (txt or json).                                                | txt        |

### Examples

1. Fetch URLs for `example.com` and save unique results:
   ```bash
   python script.py example.com --unique --output results.txt
   ```

2. Fetch URLs with 10 threads and save results as JSON:
   ```bash
   python script.py example.com --threads 10 --format json --output results.json
   ```

3. Fetch URLs without subdomains:
   ```bash
   python script.py example.com --no-subs
   ```

---