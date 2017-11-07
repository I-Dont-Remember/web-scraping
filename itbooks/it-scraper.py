#! /usr/bin/env python3
import requests
import bs4
import time
import sys
from multiprocessing.dummy import Pool as ThreadPool

error404_class = '.error404'

def get_soup_from_link(link):
    response = requests.get(link)
    response.raise_for_status()
    return bs4.BeautifulSoup(response.text, 'html.parser')


def has_error404_class(soup):
    # returns empty list/ None if it doesn't find it
    if soup.select(error404_class):
        return True
    else:
        return False


def scrape_for_bookmarks(url):
    bookmarks = []
    soup = get_soup_from_link(url)
    headers = soup.findAll('header', {'class': 'entry-header'})
    for header in headers:
        if header.a:
            link = header.a['href']
            print('---> found %s' % link)
            bookmarks.append(link)
    return bookmarks


# Map concatenates into a list of lists, flatten after return
def get_bookmark_links(page_range, base_link, pool):
    actual_links = [base_link + str(num) for num in page_range]
    bookmarks = pool.map(scrape_for_bookmarks, actual_links)
    return bookmarks


def send_list_to_file(a_list, file_name):
    try:
        with open(file_name, 'w') as f:
            for item in a_list:
                f.write('%s\n' % item)
    except IOError:
        print('Issue writing to %s, exiting' % file_name)
        raise SystemExit

    print('Finished writing to %s' % file_name)


def get_pdf_links(bookmarks, pool):
    pdfs = []
    print('Getting pdf links from bookmarks...')
    pdfs = pool.map(get_pdf_from_bookmark, bookmarks)
    return pdfs


def get_pdf_from_bookmark(link):
    print('---> %s...' % link, end='')
    try:
        response = requests.get(link)
        response.raise_for_status()
        soup = bs4.BeautifulSoup(response.text, 'html.parser')
    except requests.exceptions.ConnectionError:
        print('Problem connecting to page %s...' % link)
        return ''

    try:
        pdf_link = soup.find('span', class_='download-links').a['href']
    except (KeyError, AttributeError) as e:
        print('%s had no pdf link...' % link)
        return ''

    return pdf_link


def flatten(outer_list):
    flatlist = []
    for l in outer_list:
        if type(l) == list:
            for e in l:
                flatlist.append(e)
        else:
            flatlist.append(l)
    return flatlist


def main():
    last_page = 735
    page_range = list(range(1,last_page + 1))
    pool_size = int(sys.argv[1])
    base_link = 'http://www.allitebooks.com/page/'
    file_name = 'itebooks_pdfs_links.txt'
    pool = ThreadPool(pool_size)
    # Run until class 'error404'
    start = time.time()
    print('Preparing to scrape "%s"...' % base_link)

    try:
        bookmark_links = flatten(get_bookmark_links(page_range, base_link, pool))
    except requests.exceptions.ConnectionError:
        print('Problem connecting to page %s%d, exiting.' % (base_link, page_num))
        raise SystemExit
    print('Scraped %d pages for bookmarks...' % (last_page))

    try:
        pdf_links = get_pdf_links(bookmark_links, pool)
    except requests.exceptions.ConnectionError:
        print('Problem connecting to pdf_links, exiting.')
        raise SystemExit

    print('Writing list of %d pdfs to %s...' % (len(pdf_links), file_name))
    send_list_to_file(pdf_links, file_name)

    end = time.time() - start
    print('Finished in %ds with %d threads.' % (end, pool_size))
    return 0


if __name__ == '__main__':
    main()
