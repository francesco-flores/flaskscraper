from flask import Flask, request, render_template
import requests
from bs4 import BeautifulSoup

def get_articles(url):
    # accetta i cookies
    session = requests.Session()
    headers = {
        "User-Agent": ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                       "AppleWebKit/537.36 (KHTML, like Gecko) "
                       "Chrome/98.0.4758.102 Safari/537.36")
    }
    session.headers.update(headers)
    cookies = {"cookieConsent": "accepted"}

    page = session.get(url, cookies=cookies)
    soup = BeautifulSoup(page.content, "html.parser")
    
    titles = soup.find_all(['h2', 'h3', 'h4'])
    
    results = []
    for title in titles:
        title_text = title.get_text(strip=True)
        
        link = title.find('a')
        title_url = link['href'] if link else None
        
        results.append({'title': title_text, 'url': title_url})
    
    return results

app = Flask(__name__)

def remove_articles(articles, id):
    articles = articles.delete(id)

@app.route("/")
def index():
    url = request.args.get('url')
    if url:
        articles = get_articles(url)
    else:
        articles = []
   
    return render_template("index.html", articles=articles, url=url)
