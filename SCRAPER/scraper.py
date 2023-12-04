
import requests
from bs4 import BeautifulSoup

# Base URL for the article list pages
define_base_url = 'https://99percentinvisible.org/episodes/page/'

# Function to make HTTP requests and parse HTML content
def get_html_content(url):
    response = requests.get(url)
    if response.status_code == 200:
        return BeautifulSoup(response.content, 'html.parser')
    else:
        return None


# Function to extract article URLs from a list page
def extract_article_urls(soup):
    article_urls = []
    for article in soup.select('article.post'):  # Assuming 'article.post' is the correct selector
        link = article.find('a', href=True)
        if link:
            article_urls.append(link['href'])
    return article_urls

# Function to navigate through the article list pages and extract URLs
def scrape_article_list_pages(base_url, total_pages):
    all_article_urls = []
    for page_number in range(1, total_pages + 1):
        page_url = f'{base_url}{page_number}'
        soup = get_html_content(page_url)
        if soup:
            article_urls = extract_article_urls(soup)
            all_article_urls.extend(article_urls)
        else:
            print(f'Failed to retrieve content from {page_url}')
    return all_article_urls

# Example usage
# all_article_urls = scrape_article_list_pages(define_base_url, 46)  # Uncomment to run
