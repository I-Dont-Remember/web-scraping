#! /usr/bin/env python3
import requests
import sys
import os
import time
import wget
import pdb
from multiprocessing.dummy import Pool as ThreadPool


def main():
    dest_name = 'pdf_books'
    if len(sys.argv) == 1:
        print('./downloader num_threads file_of_pdf_links [num_to_run:optional]')
        raise SystemExit

    num_threads = int(sys.argv[1])
    file_name = sys.argv[2]

    if sys.argv[3]:
        num_pdfs = int(sys.argv[3])

    start = time.time()
    pdf_links = []
    try:
        with open(file_name, 'r') as f:
            for line in f:
                pdf_links.append(line.strip('\n'))
                print(line)
    except IOError:
        print('Problem reading from file %s' % file_name)
        raise SystemExit

    total = time.time() - start
    print('Acquired %d pdf links in %d s.' % (len(pdf_links), total))

    if sys.argv[3]:
        print('Culled to %d pdf links' % num_pdfs)
        pdf_links = pdf_links[:num_pdfs]
    start = time.time()

    pool = ThreadPool(num_threads)

    # create folder so we don't have files everywhere
    cwd = os.getcwd()
    dest = os.path.join(cwd, dest_name)
    if not os.path.exists(dest):
        new_dir = os.mkdir(dest)

    os.chdir(dest)
    # concatenates results, but we want to download them so don't care a ton about response
    logf = open('download.log', 'w')
    try:
        results = pool.map(wget.download, pdf_links)
    except Exception as e:
        logf.write('-> Error during download: %s' % e)
        pass

    pool.close()
    pool.join()
    logf.close()

    total = time.time() - start
    print('\nFinished download in %d s' % total)
    return 0




if __name__ == '__main__':
    main()
