from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/scrape', methods=['GET'])
def scrape():
    url = request.args.get('url')
    scraping_option = request.args.get('option')
    html = get_html(url)

    if scraping_option == 'fullHtml':
        result = prettify_html(html)
    elif scraping_option == 'divTags':
        result = prettify_html(extract_div_tags(html))
    elif scraping_option == 'allLinks':
        result = prettify_html(extract_links(html))
    elif scraping_option == 'tableHeads':
        result = prettify_html(extract_table_heads(html))
    elif scraping_option == 'tableBody':
        result = prettify_html(extract_table_body(html))
    elif scraping_option == 'allTables':
        result = prettify_html(extract_all_tables(html))
    elif scraping_option == 'extractInfo':
        result = "Info extraction not implemented yet."
    else:
        result = "Invalid scraping option."

    return result

def get_html(url):
    response = requests.get(url)
    return response.text

def extract_div_tags(html):
    soup = BeautifulSoup(html, 'html.parser')
    div_tags = soup.find_all('div')
    return "\n".join(str(tag) for tag in div_tags)

def extract_links(html):
    soup = BeautifulSoup(html, 'html.parser')
    links = [{'url': a['href'], 'text': a.text.strip()} for a in soup.find_all('a', href=True)]
    return "\n".join(f"<a href='{link['url']}' target='_blank'>{link['text']}</a>" for link in links)

def extract_table_heads(html):
    soup = BeautifulSoup(html, 'html.parser')
    table_heads = soup.find_all('th')
    return [th.text.strip() for th in table_heads]

def extract_table_body(html):
    soup = BeautifulSoup(html, 'html.parser')
    table_body = soup.find_all('td')
    return [td.text.strip() for td in table_body]

def extract_all_tables(html):
    soup = BeautifulSoup(html, 'html.parser')
    all_tables = soup.find_all('table')
    return "\n".join(str(table) for table in all_tables)

def prettify_html(html):
    soup = BeautifulSoup(html, 'html.parser')
    return soup.prettify()

if __name__ == "__main__":
    app.run(debug=True)
