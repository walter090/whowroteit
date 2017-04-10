import bs4 as bs
import urllib2 as request
import unicodedata
import os.path


def scrape_poet(poet,
                poet_head='https://www.poetryfoundation.org/poems-and-poets/poets/detail/',
                poem_head='https://www.poetryfoundation.org/poems-and-poets/poems/detail/',
                folder='poems/'):

    poet_folder = folder + poet + '/'

    if os.path.exists(poet_folder):
        print '{} already scraped!'.format(poet)
        return
    else:
        os.mkdir(poet_folder)

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

    for url in links:
        sauce = request.urlopen(poem_head + url).read()
        poem_content = bs.BeautifulSoup(sauce, 'lxml').body.find('div', class_='poem')
        poem = []
        for verse in poem_content.find_all('div'):
            ascii_verse = unicodedata.normalize('NFKD', verse.text).encode('ascii', 'ignore')
            poem.append(ascii_verse)
        poem_formatted = '\n'.join(poem)

        poem_path = poet_folder+url
        if not os.path.isfile(poem_path):
            with open(poem_path, 'w') as f:
                f.write(poem_formatted)
