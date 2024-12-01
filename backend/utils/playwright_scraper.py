import asyncio
import logging
from playwright.async_api import async_playwright, TimeoutError
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import json

from config import Config

# Set up logging using the configuration
logging.basicConfig(
    level=getattr(logging, Config.Logging.LEVEL.upper(), logging.INFO),
    format=Config.Logging.FORMAT,
    handlers=[
        logging.StreamHandler(),
    ]
)
import unicodedata


def normalize_text(text):
    """
    Normalize text by applying a series of preprocessing steps.

    Args:
        text (str): The text to normalize.

    Returns:
        str: Normalized text.
    """
    if not isinstance(text, str):
        return text  # Return as is if not a string
    text = unicodedata.normalize("NFKC", text)  # Unicode normalization
    text = text.replace("\xa0", " ")  # Replace non-breaking spaces
    text = text.lower()  # Convert to lowercase
    text = " ".join(text.split())  # Remove extra whitespace
    return text

def is_valid_url(url, base_url):
    """
    Check if a URL is valid and belongs to the same domain as the base URL.
    """
    parsed_url = urlparse(url)
    parsed_base = urlparse(base_url)
    return parsed_url.netloc == parsed_base.netloc and not parsed_url.fragment


async def scrape_page(page, url):
    """
    Scrape a single page for title, paragraphs, and structured text.
    """
    try:
        logging.info(f"Scraping: {url}")
        await page.goto(url, wait_until="domcontentloaded")
        await page.wait_for_selector("body", timeout=10000)
        page_source = await page.content()

        # Parse the page source with BeautifulSoup
        soup = BeautifulSoup(page_source, "html.parser")
        title = soup.title.string if soup.title else "No title"
        paragraphs = [normalize_text(p.text) for p in soup.find_all("p")]
        content = ' '.join(paragraphs)

        # Extract structured text
        structured_text = await page.evaluate("""
            () => {
                const traverse = (node, depth = 0) => {
                    if (!node || !node.childNodes) return "";
                    let result = "";
                    for (let child of node.childNodes) {
                        if (child.nodeType === Node.TEXT_NODE) {
                            const text = child.textContent.trim();
                            if (text) {
                                result += "  ".repeat(depth) + text + "\\n";
                            }
                        } else if (child.nodeType === Node.ELEMENT_NODE) {
                            result += traverse(child, depth + 1);
                        }
                    }
                    return result;
                };
                return traverse(document.body);
            }
        """)

        return {
            "url": url,
            "title": title,
            "content": content,
            "paragraphs": paragraphs,
            "structured_text": structured_text,
            "page_source": page_source,
        }
    except TimeoutError:
        logging.warning(f"Timeout occurred while loading {url}")
        return {"url": url, "title": "Timeout", "content": "", "paragraphs": "", "page_source": ""}
    except Exception as e:
        logging.error(f"Error scraping {url}: {e}")
        return {"url": url, "title": "Error", "content": "", "paragraphs": "", "page_source": ""}


async def scrape_website_recursive(base_url, max_depth=2):
    """
    Recursively scrape pages starting from the base URL using a shared browser context.
    """
    scraped_data = []
    visited = set()

    async def scrape_recursive(url, depth, context):
        if depth > max_depth or url in visited:
            return
        visited.add(url)

        page = await context.new_page()
        data = await scrape_page(page, url)
        if data:
            scraped_data.append(data)

        try:
            links = await page.evaluate("""
                () => Array.from(document.querySelectorAll('a[href]'))
                          .map(a => a.href)
            """)
            for link in links:
                full_url = urljoin(base_url, link)
                if is_valid_url(full_url, base_url) and full_url not in visited:
                    await scrape_recursive(full_url, depth + 1, context)
        except Exception as e:
            logging.error(f"Error extracting links on {url}: {e}")

        await page.close()

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
            viewport={"width": 1920, "height": 1080},
            ignore_https_errors=True,
        )
        await scrape_recursive(base_url, depth=0, context=context)
        await context.close()
        await browser.close()

    return scraped_data


async def main():
    url = "https://www.ally.com/"
    data = await scrape_website_recursive(url, max_depth=2)
    file_name = "scraped_data.json"
    with open(file_name, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)
    logging.info(f"Scraped data saved to {file_name}")


# if __name__ == "__main__":
#     asyncio.run(main())
