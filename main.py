import os, sys
import requests
from html.parser import HTMLParser
import random
import pdfkit

class ZcsHtmlParser(HTMLParser):
    def __init__(self):
        super(ZcsHtmlParser, self).__init__()

        self.article_url_start = False
        self.require_title = False
        self.article_urls = []
        self.article_titles = []

    def feed(self, data):
        self.article_url_start = False
        self.require_title = False
        self.article_urls = []
        self.article_titles = []

        super().feed(data)

    def handle_starttag(self, tag, attrs):
        #print(tag, attrs)
        if tag == 'article' and len(attrs) > 0:
            for key, val in attrs:
                if key == 'class':
                    if val == 'blog-list-box': #'article-list':
                        self.article_url_start = True
        
        if tag == 'a' and self.article_url_start is True:
            self.article_url_start = False
            self.require_title = True
            for key, val in attrs:
                if key == 'href':
                    self.article_urls.append(val)
    
    def handle_endtag(self, tag):
        if tag == 'h4' and self.require_title is True:
            self.require_title = False
            # print('[%s]' % self.data.replace(' ', '').replace('\n', ''))
            self.article_titles.append(self.data.replace(' ', '').replace('\n', ''))

    def handle_data(self, data):
        self.data = data

    def check(self):
        assert len(self.article_titles) == len(self.article_urls)
        print('find %d artilces' % len(self.article_urls))

    def random_choose(self):
        idx = random.randint(0, len(self.article_urls)-1)
        return self.article_titles[idx], self.article_urls[idx]

    def get(self, idx):
        return self.article_titles[idx], self.article_urls[idx]

def get_user_agent():
    user_agents = [ \
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1', \
        'Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11', \
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6', \
        'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6', \
        'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1', \
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5', \
        'Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5', \
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3', \
        'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3', \
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3', \
        'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3', \
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3', \
        'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3', \
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3', \
        'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3', \
        'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3', \
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24', \
        'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24']
    user_agent = random.choice(user_agents)
    return user_agent
    # return user_agents[0]

def get_blog_titles_and_urls(root_url='https://blog.csdn.net/weixin_39228381?type=blog'):
    user_agent = get_user_agent()
    response = requests.get(root_url, headers={'user-agent':user_agent})
    text = response.content.decode('utf-8')

    #with open('./articles.txt', 'w') as fp:
    #    fp.write(text)

    # cookies = response.cookies
    # print(cookies)
    # cookies = requests.utils.dict_from_cookiejar(cookies)
    # print(cookies)

    #with open('./articles.txt', 'r') as fp:
    #    text = fp.read()
    # print(text)

    zhp = ZcsHtmlParser()
    zhp.feed(text)
    zhp.check()
    return zhp
    # print(title, url)

def save_pdf(htmls, file_name):  
    options = {
            'page-size': 'Letter',
            'margin-top': '0.75in',
            'margin-right': '0.75in',
            'margin-bottom': '0.75in',
            'margin-left': '0.75in',
            'encoding': "UTF-8",
            'custom-header': [
                ('Accept-Encoding', 'gzip')
                ],
            'cookie': [
                ('cookie-name1', 'cookie-value1'),
                ('cookie-name2', 'cookie-value2'),
                ],
            'outline-depth': 10,
            }
    pdfkit.from_file(htmls, file_name, options=options) 

if __name__ == '__main__':
    zhp = get_blog_titles_and_urls()
    #sys.exit()
    user_agent = get_user_agent()
    for title, url in zip(zhp.article_titles, zhp.article_urls):
        print(title, url)
        title = title.replace('\&', '\\\&')
        #title = title.encode('utf-8').decode('utf-8')
        #pdfkit.from_url(url, u'\"pdf/%s.pdf\"' % title)
        #os.system(u'touch \"pdf/%s.pdf\"' % title)
        os.system(u'wkhtmltopdf %s pdf/tmp.pdf' % url)
        os.system(u'mv pdf/tmp.pdf \"pdf/%s.pdf\"' % title)
        #break
