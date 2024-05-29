
from flask import Flask, render_template, request, redirect, url_for
import requests

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    query = request.form.get('query')
    platform = request.form.get('platform')
    if platform == 'all':
        results = get_all_results(query)
    else:
        results = get_platform_results(query, platform)
    return render_template('index.html', results=results)

def get_all_results(query):
    reddit_results = search_reddit(query)
    youtube_results = search_youtube(query)
    tiktok_results = search_tiktok(query)
    instagram_results = search_instagram(query)
    return {
        'reddit': reddit_results,
        'youtube': youtube_results,
        'tiktok': tiktok_results,
        'instagram': instagram_results
    }

def get_platform_results(query, platform):
    if platform == 'reddit':
        return search_reddit(query)
    elif platform == 'youtube':
        return search_youtube(query)
    elif platform == 'tiktok':
        return search_tiktok(query)
    elif platform == 'instagram':
        return search_instagram(query)

def search_reddit(query):
    url = 'https://www.reddit.com/search.json'
    params = {'q': query}
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36'}
    response = requests.get(url, params=params, headers=headers)
    data = response.json()
    return data['data']['children']

def search_youtube(query):
    url = 'https://www.googleapis.com/youtube/v3/search'
    params = {'part': 'snippet', 'q': query}
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36'}
    response = requests.get(url, params=params, headers=headers)
    data = response.json()
    return data['items']

def search_tiktok(query):
    url = 'https://www.tiktok.com/api/search'
    params = {'q': query}
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36'}
    response = requests.get(url, params=params, headers=headers)
    data = response.json()
    return data['itemList']

def search_instagram(query):
    url = 'https://www.instagram.com/web/search/topsearch/'
    params = {'query': query}
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36'}
    response = requests.get(url, params=params, headers=headers)
    data = response.json()
    return data['users']

if __name__ == '__main__':
    app.run(debug=True)
