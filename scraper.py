import bs4 as bs
import urllib2 as request
import unicodedata
import os.path


def scrape_poet(poet_head, poem_head, poet, folder):

    sauce = request.urlopen(poet_head+poet).read()
    soup = bs.BeautifulSoup(sauce, 'lxml')
    body = soup.body

    links = []

    for i, poem_section in enumerate(body.find_all('div', class_='detail-assets')):
        if i:
            poem_list = poem_section.find('ul', class_='auxiliaryList')
            for poem in poem_list.find_all('li'):
                poem_link = poem.find('a').get('href')
                links.append(poem_link.split('/')[-1])

    if not os.path.isfile(folder + poet):
        f = open(folder + poet, 'w')
        for url in links:
            sauce = request.urlopen(poem_head + url).read()
            poem_content = bs.BeautifulSoup(sauce, 'lxml').body.find('div', class_='poem')
            poem = []
            for verse in poem_content.find_all('div'):
                ascii_verse = unicodedata.normalize('NFKD', verse.text).encode('ascii', 'ignore')
                poem.append(ascii_verse)
            poem_formatted = '\n'.join(poem)
            f.write(poem_formatted)
        f.close()
    else:
        print '{} already scraped!'.format(poet)
