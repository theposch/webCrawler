
import requests
from bs4 import BeautifulSoup

# Base URL for article list pages
base_url = 'https://99percentinvisible.org/episodes/page/{}'

# List to store article URLs
article_urls = []

# Iterate through all the pages
for page_number in range(1, 47):
    page_url = base_url.format(page_number)
    response = requests.get(page_url)
    
    # Check if the request was successful
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        # Extract individual article URLs
        articles = soup.find_all('a', class_='episode-title')
        for article in articles:
            article_urls.append(article['href'])
    else:
        print(f'Failed to retrieve page {page_number}')

# Save the article URLs to a file
with open('article_urls.txt', 'w') as url_file:
    for url in article_urls:
        url_file.write(f'{url}\n')
