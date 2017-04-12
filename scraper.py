import bs4 as bs
import urllib2 as request
import unicodedata
import os.path
import time


def scrape_by_century(*centuries):
    """
    A more effective way to scrape poems, finds all the poets in the
    specified century. Since the web page that displays the list of
    poets is non-static, and cannot be scraped with beautifulsoup, here an
    alternative solution is used to scape the list of poets by century from 
    Wikipedia
    :param century: code for the target school or period
    :return: 
    """
    for century in centuries:
        url = 'https://en.wikipedia.org/wiki/Category:{}th-century_English_poets'
        poet_names = []

        try:
            sauce = request.urlopen(url.format(century))
            time.sleep(5)
            sauce = sauce.read()
        except request.HTTPError:
            print 'no poet found in given century'
            return

        soup = bs.BeautifulSoup(sauce, 'lxml')

        try:
            for poet in soup.find('div', {'id': 'mw-subcategories'}).find_all('a'):
                poet_name = poet.text
                poet_names.append('-'.join(poet_name.lower().split(' ')))
        except AttributeError:
            print 'not poets listed in {}th century'.format(century)

        print poet_names

        scrape_poet(poet_names)


def scrape_poet(poets):
    poet_head = 'https://www.poetryfoundation.org/poems-and-poets/poets/detail/'
    poem_head = 'https://www.poetryfoundation.org/poems-and-poets/poems/detail/'
    folder = 'poems/'

    for poet in poets:
        poet_folder = folder + poet + '/'

        try:
            sauce = request.urlopen(poet_head + poet).read()
        except request.HTTPError:
            print '{} does not exist in the database!'.format(poet)
            continue

        if os.path.exists(poet_folder):
            print '{} already scraped!'.format(poet)
            continue
        else:
            os.mkdir(poet_folder)

        soup = bs.BeautifulSoup(sauce, 'lxml')
        body = soup.body

        links = []

        for i, poem_section in enumerate(body.find_all('div', class_='detail-assets')):
            if i:
                poem_list = poem_section.find('ul', class_='auxiliaryList')
                for poem in poem_list.find_all('li'):
                    try:
                        poem_link = poem.find('a').get('href')
                    except AttributeError:
                        print 'no poem found of this poet'
                        continue
                    links.append(poem_link.split('/')[-1])

        for url in links:
            try:
                sauce = request.urlopen(poem_head + url).read()
            except request.HTTPError:
                pass

            poem_content = bs.BeautifulSoup(sauce, 'lxml').body.find('div', class_='poem')
            try:
                [s.extract() for s in poem_content('span', {'style': 'display: none;'})]
            except TypeError:
                pass
            # if the text format does not exist, skip the poem and move on
            if poem_content is None:
                continue
            poem = []
            for verse in poem_content.find_all('div'):
                ascii_verse = unicodedata.normalize('NFKD', verse.text).encode('ascii', 'ignore')
                poem.append(ascii_verse)
            poem_formatted = '\n'.join(poem)

            poem_path = poet_folder + url
            if not os.path.isfile(poem_path):
                with open(poem_path, 'w') as f:
                    f.write(poem_formatted)

        if not os.listdir(poet_folder):
            os.rmdir(poet_folder)
            print '{} does not have any poem in text format'.format(poet)
        else:
            print '{} added to collection!'.format(poet)
