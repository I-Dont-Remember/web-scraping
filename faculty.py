#! /usr/bin/env python
import bs4
import requests


class Person(object):

    def __init__(self, last_name, first_name, dept, email):
        if not last_name:
            last_name = ''
        if not first_name:
            first_name = ''
        if not dept:
            dept = ''
        if not email:
            email = ''
        self.name = first_name + ' ' +  last_name
        self.email = email
        self.dept = dept

    def displayPerson(self):
        print('Name:', self.name, ', Email:', self.email, ', Dept:', self.dept)


    
def get_pages_researchers(soup, selector):
    researchers = []
    rows = soup.select(selector)
    for person in rows:
        td_list = person.find_all('td')
        researchers.append(Person(get_last_name(td_list[0]),
                           get_first_name(td_list[1]),
                           get_dept(td_list[2]),
                           get_email(td_list[3])))
    return researchers


def get_email(td):
    # comes as 'name | email'
    string = td['title']
    pieces = string.split('|')
    return pieces[1].strip()


def get_last_name(td):
    return td.string


def get_first_name(td):
    return td.string


def get_dept(td):
    return td.string


def main():
    researchers = []
    page_num = "5000"
    web_link = 'http://discoveryportal.org/faculty.aspx?&page='
    researchers_selector = 'tr.researcherList'
    
    print('Preparing to scrape "%s"...' % web_link) 
    response = requests.get(web_link + page_num)
    soup = bs4.BeautifulSoup(response.text, 'html.parser')
    print(soup)
    return 0
    # Can't just check return code cuz idiot site returns an empty list but
    # functional page even if page is out of the "true" range
    while response:
        print('-->Scraping page %s...' % page_num)
        soup = bs4.BeautifulSoup(response.text, 'html.parser')
        researchers += get_pages_researchers(soup, researchers_selector)

    print('-->Page returned bad status...')
    for r in researchers:
        r.displayPerson()

    print('...done')


if __name__ == '__main__':
    main()

