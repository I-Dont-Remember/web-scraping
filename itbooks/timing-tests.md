
### Testing with the multiprocessing.dummy thread library:
#### Running with supposed 116 Mbps down
  - page 1-5 scraped for test, no write to file
    - Finished in 64s with 1 threads.
    - Finished in 37s with 2 threads.
    - Finished in 25s with 3 threads.
    - Finished in 20s with 4 threads.
    - Finished in 15s with 5 threads.
    - Finished in 12s with 6 threads.
    - Finished in 11s with 7 threads.
    - Finished in 11s with 8 threads.


  - page 1 - 20 for test, no write to file
      - Finished in 268s with 1 threads.
      - Finished in 145s with 2 threads.
      - Finished in 94s with 3 threads.
      - Finished in 70s with 4 threads.
      - Finished in 54s with 5 threads.
      - Finished in 54s with 6 threads.
      - Finished in 46s with 7 threads.
      - Finished in 43s with 8 threads.
      - Finished in 32s with 9 threads.
      - Finished in 32s with 10 threads.
      - Finished in 30s with 11 threads.
      - Finished in 29s with 12 threads.

      -> And just for fun...confirm the plateau and valley
      - Finished in 28s with 15 threads.
      - Finished in 23s with 30 threads.
      - Finished in 26s with 50 threads.

### Key takeaways
 * Wow, multiprocessing makes life suck less.
 * Like a lot less, cutting these times by huge amounts since the script spends most of the
time waiting on the I/O from requests, so threads work well.
 * Have to be careful with printing output, threading made it garbled, which makes sense but
messes up nice looking plans.


#### First run no threading...
`
Writing list of 7342 pdfs to itebooks_pdfs_links.txt...
Finished writing to itebooks_pdfs_links.txt
Finished in 9375s.
`

#### Final quick run for all 735 pages...
`
Writing list of 7350 pdfs to itebooks_pdfs_links.txt...
Finished writing to itebooks_pdfs_links.txt
Finished in 824s with 14 threads.
`


### Now for the fun times, actual downloads of the pdfs...
  - Acquired 7350 pdf links in 0 s.
Culled to 20 pdf links
100% [........................................................................] 26913695 / 26913695
Finished download in 23 s

  - Acquired 7350 pdf links in 0 s.
Culled to 20 pdf links
100% [........................................................................] 20545253 / 20545253
Finished download in 23 s

  - Culled to 20 pdf links
100% [........................................................................] 15984588 / 15984588
Finished download in 30 s


### Final download run
  - 
Acquired 7350 pdf links in 0 s.
Culled to 7350 pdf links
100% [..........................................................................] 7542493 / 7542493
Finished download in 6682 s

