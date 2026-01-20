import argparse
import sys
import os
import json
import logging
from typing import Dict, Any, List
from dataclasses import asdict, is_dataclass

# Add project root to sys.path to allow 'src' imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.config import Config
from src.scrapers.mock_scraper import MockScraper
from src.scrapers.indeed_nl import IndeedNLScraper

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Site Registry
SCRAPERS = {
    "mock": MockScraper,
    "indeed_nl": IndeedNLScraper,
}

def load_filters(args) -> Dict[str, Any]:
    if args.filters_file:
        try:
            with open(args.filters_file, 'r') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Failed to load filters from file: {e}")
            sys.exit(1)
    
    if args.filters:
        try:
            return json.loads(args.filters)
        except json.JSONDecodeError:
            # Try to handle single quoted json string if passed from shell
            try:
                return json.loads(args.filters.replace("'", '"'))
            except:
                logger.error("Failed to parse filters JSON string")
                sys.exit(1)
                
    return {}

def make_serializable(obj):
    if is_dataclass(obj):
        return asdict(obj)
    if isinstance(obj, list):
        return [make_serializable(item) for item in obj]
    return obj

def run_cli(args):
    site_key = args.site
    action = args.action
    
    if not site_key or not action:
        print("Error: --site and --action are required for CLI mode")
        sys.exit(1)

    if site_key not in SCRAPERS:
        print(f"Error: Unknown site '{site_key}'. Available: {list(SCRAPERS.keys())}")
        sys.exit(1)
        
    scraper_cls = SCRAPERS[site_key]
    # Pass debug_dir to scraper if it supports it (via PlaywrightScraper)
    scraper = scraper_cls(debug_dir=args.debug_dir) if args.debug_dir else scraper_cls()
    
    result = None
    
    try:
        if action == "get_filters":
            result = scraper.get_filters()
        elif action == "get_jobs":
            filters = load_filters(args)
            logger.info(f"Running get_jobs for {site_key} with filters: {filters}")
            result = scraper.get_jobs(filters)
        elif action == "get_details":
            filters = load_filters(args)
            url = filters.get("url")
            if not url:
                 logger.error("Error: 'url' is required in filters for get_details")
                 sys.exit(1)
            logger.info(f"Running get_job_details for {site_key} on {url}")
            result = scraper.get_job_details(url)
        elif action == "debug_search":
            if not args.search_keys:
                logger.error("Error: --search-keys file is required for debug_search")
                sys.exit(1)
            
            with open(args.search_keys, 'r') as f:
                search_params_list = json.load(f)
            
            if not isinstance(search_params_list, list):
                search_params_list = [search_params_list]
                
            all_jobs_details = []
            
            for params in search_params_list:
                logger.info(f"Searching for: {params}")
                jobs = scraper.get_jobs(params)
                
                for job in jobs[:args.limit or 5]: # Default limit to 5 per search to avoid huge runs
                    logger.info(f"Fetching details for job: {job.id}")
                    # Update scraper debug_dir for this specific job's folder
                    if args.debug_dir:
                        job_dir = os.path.join(args.debug_dir, f"job_{job.id}")
                        os.makedirs(job_dir, exist_ok=True)
                        scraper.debug_dir = job_dir
                        
                        # Save summary
                        with open(os.path.join(job_dir, "summary.json"), 'w', encoding='utf-8') as f:
                            json.dump(make_serializable(job), f, indent=2, ensure_ascii=False)
                    
                    details = scraper.get_job_details(job.id)
                    all_jobs_details.append(details)
                    
                    if args.debug_dir:
                        # Save details
                        with open(os.path.join(job_dir, "details.json"), 'w', encoding='utf-8') as f:
                            json.dump(make_serializable(details), f, indent=2, ensure_ascii=False)
            
            result = all_jobs_details
        else:
            print(f"Error: Unknown action '{action}'")
            sys.exit(1)
            
        # Convert dataclasses to dicts for serialization
        result = make_serializable(result)
            
        # Output handling
        if args.output_file:
            # Ensure directory exists
            os.makedirs(os.path.dirname(os.path.abspath(args.output_file)), exist_ok=True)
            with open(args.output_file, 'w', encoding='utf-8') as f:
                json.dump(result, f, indent=2, ensure_ascii=False)
            logger.info(f"Output saved to {args.output_file}")
        elif action != "debug_search" or not args.debug_dir:
            print(json.dumps(result, indent=2, ensure_ascii=False))
            
    except Exception as e:
        logger.error(f"Action failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

def run_worker():
    logger.info("Worker mode not fully implemented yet. Use --mode cli for debugging.")
    # Placeholder for worker loop
    pass

def main():
    parser = argparse.ArgumentParser(description="Scanner Service CLI")
    parser.add_argument("--mode", choices=["cli", "worker"], default="cli", help="Run mode")
    parser.add_argument("--site", help="Site key (e.g. indeed_nl)")
    parser.add_argument("--action", choices=["get_filters", "get_jobs", "get_details", "debug_search"], help="Action to perform")
    parser.add_argument("--filters", help="JSON string of filters")
    parser.add_argument("--filters-file", help="Path to JSON file containing filters")
    parser.add_argument("--search-keys", help="Path to JSON file containing list of search filters")
    parser.add_argument("--output-file", help="Path to save output JSON")
    parser.add_argument("--debug-dir", help="Path to directory for saving debug HTML and per-job files")
    parser.add_argument("--limit", type=int, help="Limit number of jobs per search in debug_search")
    
    args = parser.parse_args()
    
    if args.mode == "cli":
        run_cli(args)
    else:
        run_worker()

if __name__ == "__main__":
    main()
