#! /usr/bin/env python
import bs4
import requests
import csv
import time

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


    def getCSVformat(self):
        return (self.dept, self.name, self.email)

def get_pages_researchers(rows, ignored_depts):
    researchers = []
    for person in rows:
        td_list = person.find_all('td')
        dept = get_dept(td_list[2])
        if dept not in ignored_depts:
            researchers.append(Person(get_last_name(td_list[0]),
                               get_first_name(td_list[1]),
                               dept,
                               get_email(td_list[3])))

    print('----> Found %d researchers on this page...' % (len(researchers)))
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

def convert_to_csv_data(people):
    data = []
    for person in people:
        data.append(person.getCSVformat())
    return data


def write_to_csv(person_list, file_name):
    data = convert_to_csv_data(person_list)
    try:
        with open(file_name, 'w') as fp:
            writer = csv.writer(fp, delimiter=',')
            writer.writerows(data)
    except Exception as e:
        # Need to find out what exceptions to check for
        print('Exception thrown during csv writing')
        print(e)
        raise SystemExit


def main():
    researchers = []
    ignored_depts = []
    page_num = 0
    file_name = 'researchers.csv'
    ignore_file = 'ignored_depts.txt'
    web_link = 'http://discoveryportal.org/faculty.aspx?&page='
    researchers_selector = 'tr.researcherList'

    start = time.time()
    print('--> Getting ignored list from %s' %  ignore_file)
    try:
        with open(ignore_file, 'r') as fp:
            lines = fp.readlines()
    except Exception as e:
        print('exception: %s' % e)
        raise SystemExit

    for line in lines:
        ignored_depts.append(line.rstrip())
    print('--> Fetched %s as ignored list in %d seconds...' %(ignore_file, time.time() - start))

    start = time.time()
    print('--> Preparing to scrape "%s"...' % web_link)
    response = requests.get(web_link + str(page_num))
    soup = bs4.BeautifulSoup(response.text, 'html.parser')
    rows = soup.select(researchers_selector)

    # Can't just check return code cuz idiot site returns an empty list but
    # functional page even if page is out of the "true" range
    while rows:
        print('--> Scraping page %s...' % page_num)
        researchers += get_pages_researchers(rows, ignored_depts)

        # handle next page
        page_num += 1
        response = requests.get(web_link + str(page_num))
        soup = bs4.BeautifulSoup(response.text, 'html.parser')
        rows = soup.select(researchers_selector)

    print('--> Page %s returned empty list...' % page_num)
    researchers.sort(key = lambda x: x.dept)
    print('--> Found %d total researchers on %d pages...' % (len(researchers), page_num + 1))
    print('--> Scraping done in %d seconds...' % (time.time() - start))

    start = time.time()
    print('--> Writing to %s...' % file_name)
    write_to_csv(researchers, file_name)
    print('...Writing done in %d seconds' % (time.time() - start))


if __name__ == '__main__':
    main()
