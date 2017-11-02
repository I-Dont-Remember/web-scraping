#! /usr/bin/env python3
import requests
import bs4
import time

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


def get_bookmark_links(soup):
    # list = soup.findAll('a', {'rel': 'bookmark'})
    # still need to get rid of child elements
    bookmarks = []
    headers = soup.findAll('header', {'class': 'entry-header'})
    for header in headers:
        print(header.a['href'])
        bookmarks.append(header.a['href'])
    return bookmarks

def send_list_to_file(a_list, file_name):
    print('%d bookmark links found..' % len(a_list))


def get_pdf_links(bookmarks):
    print('for every bookmark print pdf')


def get_pdf_from_bookmark():
    print('get pdf')


def main():
    page_num = 735
    bookmark_links = []
    base_link = 'http://www.allitebooks.com/page/'
    file_name = 'bookmarks_file.txt'
    # Run until class 'error404'
    start = time.time()
    print('Preparing to scrape "%s"...' % base_link)

    soup = get_soup_from_link(base_link + str(page_num))

    # while not has_error404_class(soup):
    #     # valid page
    try:
        while True:
            bookmark_links += get_bookmark_links(soup)
            print('Grabbed links from page %d...' % page_num)

            page_num += 1
            soup = get_soup_from_link(base_link + str(page_num))
    except requests.exceptions.HTTPError as err:
        print('404 at page %s%d...' % (base_link, page_num))
        pass
    except requests.exceptions.ConnectionError:
        print('Problem connecting to page %s%d, exiting.' % (base_link, page_num))

    print('Scraped %d pages...' % (page_num - 1))
    print('Writing list of %d bookmark links to %s...' % (len(bookmark_links), file_name))
    send_list_to_file(bookmark_links, file_name)

    end = time.time() - start
    print('Finished in %ds.' % end)
    return 0


if __name__ == '__main__':
    main()
