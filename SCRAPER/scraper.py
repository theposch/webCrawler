import requests
from bs4 import BeautifulSoup
import os

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

# Function to extract details from an article page
def extract_article_details(url):
    soup = get_html_content(url)
    if not soup:
        return None
    
    title_tag = soup.find('h1', class_='entry-title')
    title = title_tag.get_text(strip=True) if title_tag else 'No Title'
    
    author_tag = soup.find('div', class_='meta-author')
    author = author_tag.get_text(strip=True) if author_tag else 'No Author'
    
    date_tag = soup.find('time', class_='updated')
    date = date_tag.get_text(strip=True) if date_tag else 'No Date'
    
    content_tag = soup.find('div', class_='entry-content')
    content = content_tag.get_text(strip=True) if content_tag else 'No Content'
    
    return {
        'title': title,
        'author': author,
        'date': date,
        'content': content
    }

# Function to construct transcript page URL and extract transcript content
def extract_transcript_details(article_url):
    article_slug = article_url.split('/')[-2]
    transcript_url = f'https://99percentinvisible.org/episode/{article_slug}/transcript'
    
    soup = get_html_content(transcript_url)
    if not soup:
        return None
    
    transcript_tag = soup.find('div', class_='page-content transcript-content')
    transcript_content = transcript_tag.get_text(strip=True) if transcript_tag else 'No Transcript Content'
    
    return {
        'transcript_url': transcript_url,
        'transcript_content': transcript_content
    }

# Function to generate Markdown file for article or transcript
def generate_markdown_file(details, file_type, folder_path):
    yaml_front_matter = f"---\ntitle: {details['title']}\ndate: {details['date']}\nauthor: {details['author']}\ntags: [99pi, {file_type}]\n---\n"
    content = details['content'] if file_type == 'article' else details['transcript_content']
    markdown_content = yaml_front_matter + '\n' + content
    
    file_name = details['title'].replace(' ', '_').replace('/', '_') + f'_{file_type}.md'
    file_path = os.path.join(folder_path, file_name)
    with open(file_path, 'w') as file:
        file.write(markdown_content)
    return file_path



# Update the generate_markdown_file function to include internal links
def generate_markdown_file(details, file_type, folder_path, related_file_path=None):
    yaml_front_matter = f"---
title: {details['title']}
date: {details['date']}
author: {details['author']}
tags: [99pi, {file_type}]
---
"
    content = details['content'] if file_type == 'article' else details['transcript_content']
    internal_link = f'
[Link to {"transcript" if file_type == 'article' else "article"}]({related_file_path})' if related_file_path else ''
    markdown_content = yaml_front_matter + '
' + content + internal_link
    file_name = details['title'].replace(' ', '_').replace('/', '_') + f'_{file_type}.md'
    file_path = os.path.join(folder_path, file_name)
    with open(file_path, 'w') as file:
        file.write(markdown_content)
    return file_path
