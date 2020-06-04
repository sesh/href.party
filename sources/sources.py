from urllib.parse import urljoin
from thttp import request
from bs4 import BeautifulSoup

class Source:

    def __init__(self, name, url, selector, skip_articles=0):
        self.name = name
        self.url = url
        self.selector = selector
        self.skip_articles = skip_articles
        self.articles = []

    def fetch_articles(self):
        response = request(self.url)
        soup = BeautifulSoup(response.content, 'html.parser')

        els = soup.select(self.selector)

        articles = []
        for el in els:
            headline = el.get_text()

            if 'href' in el.attrs:
                link = el
            else:
                link = el.find('a')

            if not link:
                link = el.find_parent('a')

            if link and 'href' in link.attrs:
                url = link.attrs['href']
                if url.startswith('/'):
                    url = urljoin(self.url, url)

                if headline not in [a[0] for a in articles] and url not in [a[1] for a in articles]:
                    articles.append((headline, url))

        self.articles = articles[self.skip_articles:]
        return articles[self.skip_articles:]

    def as_html(self, limit=8):
        if not self.articles:
            self.fetch_articles()

        s = "<div>"
        s += f"<h2>{self.name}</h2>"
        s += "<ul class='list--bare'>"

        for a in self.articles[:limit]:
            s += f"<li><a href='{a[1]}'>{a[0]}</a></li>"

        s += "</ul>"
        s += "</div>"
        return s


atlantic = Source('The Atlantic (World)', 'https://www.theatlantic.com/world/', 'main h1,main h2,main h3')
bloomberg = Source('Bloomberg Technology', 'https://www.bloomberg.com/technology', '.single-story-module__headline-link,h3')
guardian_au = Source('The Guardian (Australia)', 'https://www.theguardian.com/au', '.js-headline-text')
itnews = Source('IT News', 'https://www.itnews.com.au/', 'h2')
npr = Source('NPR', 'https://www.npr.org/', 'main, h3')
nyt = Source('New York Times', 'https://www.nytimes.com', 'article h2', 3)
theage = Source('The Age', 'https://www.theage.com.au/', 'h3')
theverge = Source('The Verge', 'https://www.theverge.com', 'h2')
wapo = Source('The Washington Post', 'https://www.washingtonpost.com/', '.headline')
hn500 = Source('Hacker News 500', 'https://hn500.brntn.me', '.col-4-5 a:first-child')
hn = Source('Hacker News', 'https://news.ycombinator.com/', '.storylink')
lobsters = Source('Lobsters', 'https://lobste.rs/', '.link')