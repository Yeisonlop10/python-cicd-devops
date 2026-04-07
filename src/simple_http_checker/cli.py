import logging
import click

from .checker import check_urls

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)-8s - %(name)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
)

logger = logging.getLogger(__name__)

@click.command()
@click.argument('urls', nargs=-1, required=True)
@click.option('--timeout', default=5, help='Timeout for HTTP requests in seconds')
@click.option('--verbose', "-v", is_flag=True, help='Enable verbose logging')
def main(urls, timeout, verbose):
    """Check one or more URLs and print their statuses."""
    if verbose:
        logger.setLevel(logging.DEBUG)
        logging.getLogger().setLevel(logging.DEBUG)
    
    if not urls:
        logger.warning("No URLs provided to check.")
        click.echo("Please provide at least one URL to check.")
        return

    logger.info(f"Starting URL checker with {len(urls)} URLs and timeout of {timeout} seconds. Verbose: {verbose}")
    results = check_urls(urls, timeout=timeout)

    click.echo("\nURL Check Results:")
    for url, status in results.items():
        if "OK" in status:
            click.echo(click.style(f"{url:<40}: {status}", fg='green'))
        elif "FAIL" in status or "ERROR" in status:
            click.echo(click.style(f"{url:<40}: {status}", fg='red'))
        else:
            click.echo(click.style(f"{url}: {status}", fg='yellow'))



