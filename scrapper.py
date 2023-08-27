import requests
from bs4 import BeautifulSoup


class Scrap_news_owl:
    headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OSX 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko)Chrome/71.0.3578.98 Safari/537.36",
               "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8"}

    @staticmethod
    def kantipur(date1=None):
        from datetime import date
        if date1 is None:
            date1 = date.today().strftime("%Y/%m/%d")
        domain = "https://ekantipur.com"
        date1 = str(date1)
        webpage = requests.get(domain+"/news/"+date1,
                               headers=Scrap_news_owl.headers).text
        soup = BeautifulSoup(webpage, "lxml")

        articles = soup.find_all('article', class_='normal')
        data = []

        for article in articles:
            title = article.select_one('.teaser h2 a').text.strip()
            link = article.select_one('.teaser h2 a')['href']
            author = article.select_one('.teaser .author a').text.strip()
            author_link = article.select_one('.teaser .author a')['href']
            description = article.select_one('.teaser p').text.strip()
            image_link = article.select_one('.image img')['data-src']
            date = date
            data.append({"date": date, "title": title, "link": domain+link, "author": author,
                        "author_link": author_link, "description": description, "image_link": image_link})

        return data

    @staticmethod
    def online_khabar(page=1, search=None):
        domain = "https://www.onlinekhabar.com"
        if search is None:
            page = str(page)
            webpage = requests.get(
                domain+"/content/news/page/"+page, headers=Scrap_news_owl.headers).text
            soup = BeautifulSoup(webpage, "lxml")
            news_posts = soup.select('.span-4 .ok-news-post')
            data = []

            for post in news_posts:
                title = post.select_one('a .ok-post-content-wrap h2').text
                link = post.select_one('a')['href']
                image_link = post.select_one('a img')['src']
                date = post.select_one('.ok-news-post-hour span').text
                author = domain
                data.append({"date": date, "title": title, "link": link,
                            "image_link": image_link, "author": author, "description": ""})

            return data
        else:
            webpage = requests.get(
                domain+"/?search_keyword="+search, headers=Scrap_news_owl.headers).text
            soup = BeautifulSoup(webpage, "lxml")
            news_posts = soup.select('.ok-news-post')
            data = []
            for post in news_posts:
                title = post.select_one('.ok-news-title-txt').text.strip()
                link = post.select_one('a')['href']
                image_link = post.select_one('a img')['src']
                webpage1 = requests.get(link, Scrap_news_owl.headers).text
                author = domain
                url_parts = link.split('/')
                year = url_parts[-3]
                month = url_parts[-2]
                date = year+"/"+month
                data.append({"date": date, "title": title, "link": link,
                            "image_link": image_link, "author": author, "description": " "})

            return data

    @staticmethod
    def hamro_patro(search_title="", date="", st=""):
        domain = f"https://www.hamropatro.com/news?t={date}&st={st}&ss=&q={search_title}"
        print(domain)
        webpage = requests.get(domain, headers=Scrap_news_owl.headers).text
        soup = BeautifulSoup(webpage, "lxml")
        news_info_list = soup.find_all('div', class_='newsInfo')
        data = []
        for news_info in news_info_list:
            title = news_info.select_one('.newsTitle').text
            link = news_info.select_one('.source a')['href']
            description = news_info.select_one('.desc').text.strip()
            author = news_info.select_one('.source').text.split()[0]
            date = news_info.select_one('.source span').text.strip()
            data.append({"date": date, "title": title, "link": link.split(
                '/r/')[1], "image_link": "", "author": author, "description": description})
        return data

    @staticmethod
    def annapurna_post(page=None, category=None, search=None):
        domain = "https://annapurnapost.com/"
        page = str(page)
        if category is None:
            category = "latest-news"
        if search is None:
            webpage = requests.get(
                domain+"category/latest-news/?page"+page, Scrap_news_owl.headers).text
        else:
            webpage = requests.get(
                domain+"search/?q="+search, Scrap_news_owl.headers).text
        soup = BeautifulSoup(webpage, "lxml")
        news_cards = soup.find_all("div", class_="grid__card")

        data = []

        for card in news_cards:
            title = card.select_one(".card__title a").text.strip()
            image_link = card.select_one(".card__img img")["src"]
            link = card.select_one(".card__title a")["href"]
            data.append({"date": "", "title": title, "link": domain+link,
                        "image_link": image_link, "author": domain, "description": ""})
        return data


export = Scrap_news_owl
