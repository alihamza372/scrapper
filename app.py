from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup
import re

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/scrape', methods=['GET'])
def scrape():
    url = request.args.get('url')
    scraping_option = request.args.get('option')
    html = get_html(url)

    if scraping_option == 'allLinks':
        result = extract_all_links(html)
    elif scraping_option == 'phoneNumbers':
        result = extract_phone_numbers(html)
    elif scraping_option == 'emailAddresses':
        result = extract_email_addresses(html)
    elif scraping_option == 'socialMediaLinks':
        result = extract_social_media_links(html)
    else:
        result = "Invalid scraping option."

    return result

def get_html(url):
    response = requests.get(url)
    return response.text

def extract_all_links(html):
    soup = BeautifulSoup(html, 'html.parser')
    links = [{'url': a['href'], 'text': a.text.strip()} for a in soup.find_all('a', href=True)]
    return "\n".join(f"<a href='{link['url']}' target='_blank'>{link['text']}</a>" for link in links)

def extract_phone_numbers(html):
    phone_numbers = re.findall(r'\b\d{10}\b', html)
    return "\n".join(phone_numbers)

def extract_email_addresses(html):
    email_addresses = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', html)
    return "\n".join(email_addresses)

def extract_social_media_links(html):
    soup = BeautifulSoup(html, 'html.parser')
    social_media_links = []

    # Add more social media patterns as needed
    social_media_patterns = [
        re.compile(r'https://www\.facebook\.com/'),
        re.compile(r'https://www\.twitter\.com/'),
        re.compile(r'https://www\.linkedin\.com/'),
        re.compile(r'https://www\.youtube\.com/'),
        re.compile(r'https://www\.instagram\.com/'),
        # Add more patterns for other social media platforms
    ]

    for a in soup.find_all('a', href=True):
        for pattern in social_media_patterns:
            if pattern.match(a['href']):
                social_media_links.append({'url': a['href'], 'text': a.text.strip()})
                break

    return "\n".join(f"<a href='{link['url']}' target='_blank'>{link['text']}</a>" for link in social_media_links)

if __name__ == "__main__":
    app.run(debug=True)
