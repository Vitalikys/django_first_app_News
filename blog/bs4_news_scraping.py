''' для сайту News  Scraping - Parsing
https://it4each.com/blog/dropshipping-internet-magazin-na-django-chast-6/
https://www.crummy.com/software/BeautifulSoup/bs4/doc/#css-selectors
'''
from .models import News
import requests
from bs4 import BeautifulSoup

class ScrapingError(Exception):
    pass


class ScrapingTimeoutError(ScrapingError):
    pass


class ScrapingHTTPError(ScrapingError):
    pass


class ScrapingOtherError(ScrapingError):
    pass
def scraping_fun():
    url = 'https://portal.lviv.ua/article'
    resp = requests.get(url, timeout=10.0)
    resp.raise_for_status()
    if resp.status_code != 200:
        raise Exception('HTTP err access!')
    data_list = []
    html = resp.text
    soup = BeautifulSoup(resp.text, 'lxml')
    blocks = soup.select('.item_article')
    # print(blocks)
    for block in blocks:
        data = {}
        title = block.select_one('.sidebar-news-desc').text
        data['title'] = title
        # now open each Article page to get full_content
        # find and open detail page
        url_detail = block.select_one('a')
        url_detail = 'https://portal.lviv.ua' + url_detail['href']
        html_detail = requests.get(url_detail).text
        soup_d = BeautifulSoup(html_detail, 'html.parser')
        content = soup_d.select_one('p').text + url_detail
        # content = soup_d.select('.article-content'> 'p').text
        data['content'] = content
        photo = soup_d.select_one('img')['src']
        if photo:
            data['photo'] = photo
        data_list.append(data)
        # print(data)
        for item in data_list:
            if not News.objects.filter(title=item['title']).exists():
                News.objects.create(
                title=item['title'],
                content=item['content'],
                photo=item['photo'],
                category_id =5,
            )

    return data_list


if __name__ == '__main__':
    scraping_fun()
