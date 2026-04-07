import logging
import requests
from typing import Collection

logger = logging.getLogger(__name__)

def check_urls(urls: Collection[str], timeout: int = 5) -> dict[str, str]:
    """
    Check the status of a list of URLs.

    Args:
        urls (list[str]): A list of URLs to check.
        timeout (int): The timeout for the HTTP request in seconds.

    Returns:
        dict[str, str]: A dictionary mapping each URL to its status ("OK" or "FAIL").
    """

    logger.info(f"Checking {len(urls)} URLs with a timeout of {timeout} seconds.")
    
    results = {}
    for url in urls:
        status = "UNKNOWN"

        try:
            logger.debug(f"Checking URL: {url}")
            response = requests.get(url, timeout=timeout)
            if response.ok:
                status = f"{response.status_code} OK"
            else:
                status = f"FAIL (Status Code: {response.status_code}) {response.reason}"
        except requests.exceptions.Timeout as e:
            logger.error(f"Error checking URL {url}: {e}")
            status = f"TIMEOUT"
            logger.warning(f"URL {url} timed out after {timeout} seconds.")
        except requests.exceptions.ConnectionError as e:
            logger.error(f"Error checking URL {url}: {e}")
            status = f"CONNECTION ERROR"
            logger.warning(f"URL {url} could not be reached.")
        except requests.exceptions.RequestException as e:
            status = f"REQUEST ERROR: {type(e).__name__}"
            logger.error(f"Error checking URL {url}: {e}", exc_info=True)
        
        results[url] = status
        logger.debug(f"Checked: {url:<40} -> {status}")

    logger.info("Finished checking URLs.")
    return results
