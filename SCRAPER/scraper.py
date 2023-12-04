
import requests
from bs4 import BeautifulSoup

# Base URL for the article list pages
base_url = 'https://99percentinvisible.org/episodes/page/'

# Function to make HTTP requests and parse HTML content
def get_html_content(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors
        return BeautifulSoup(response.content, 'html.parser')
    except requests.RequestException as e:
        print(f'Error fetching {url}: {e}')
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
def scrape_article_list_pages(total_pages):
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
# all_article_urls = scrape_article_list_pages(46)  # Uncomment to run


# Function to extract details from an article page
def extract_article_details(url):
    soup = get_html_content(url)
    if not soup:
        return None
    
    # Extract title
    title_tag = soup.find('h1', class_='entry-title')
    title = title_tag.get_text(strip=True) if title_tag else 'No Title'
    
    # Extract author
    author_tag = soup.find('div', class_='meta-author')
    author = author_tag.get_text(strip=True) if author_tag else 'No Author'
    
    # Extract date
    date_tag = soup.find('time', class_='updated')
    date = date_tag.get_text(strip=True) if date_tag else 'No Date'
    
    # Extract main content
    content_tag = soup.find('div', class_='entry-content')
    content = content_tag.get_text(strip=True) if content_tag else 'No Content'
    
    return {
        'title': title,
        'author': author,
        'date': date,
        'content': content
    }

# Example usage
# article_details = extract_article_details('https://99percentinvisible.org/episode/the-known-unknown/')  # Uncomment to run


# Function to construct transcript page URL and extract transcript content
def extract_transcript_details(article_url):
    # Extract article slug from the URL
    article_slug = article_url.split('/')[-2]
    transcript_url = f'https://99percentinvisible.org/episode/{article_slug}/transcript'
    
    soup = get_html_content(transcript_url)
    if not soup:
        return None
    
    # Extract transcript content
    transcript_tag = soup.find('div', class_='page-content transcript-content')
    transcript_content = transcript_tag.get_text(strip=True) if transcript_tag else 'No Transcript Content'
    
    return {
        'transcript_url': transcript_url,
        'transcript_content': transcript_content
    }

# Example usage
# transcript_details = extract_transcript_details('https://99percentinvisible.org/episode/the-known-unknown/')  # Uncomment to run

import os

# Function to generate Markdown file for article or transcript
def generate_markdown_file(details, file_type, folder_path):
    # Create the YAML front matter
    yaml_front_matter = f"---
title: {details['title']}
date: {details['date']}
author: {details['author']}
tags: [99pi, {file_type}]
---
"
    content = details['content'] if file_type == 'article' else details['transcript_content']
    markdown_content = yaml_front_matter + '
' + content
    
    # Create the file name and save the Markdown file
    file_name = details['title'].replace(' ', '_').replace('/', '_') + f'_{file_type}.md'
    file_path = os.path.join(folder_path, file_name)
    with open(file_path, 'w') as file:
        file.write(markdown_content)
    return file_path

# Example usage
# article_file_path = generate_markdown_file(article_details, 'article', '/path/to/folder')  # Uncomment to run
# transcript_file_path = generate_markdown_file(transcript_details, 'transcript', '/path/to/folder')  # Uncomment to run
