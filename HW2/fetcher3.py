#!/usr/bin/env python
"""
A simple program to extract links in a web page, by Minghong Lin, for CMS/CS/EE 144.
Remade for Python 3 by: Catherine Ma (cmma@caltech.edu)
If you use Python, you can import this file and simply call the function
"fetch_links(URL)" to get a (may be empty) list, which contains all hyperlinks
in the web page specified by the URL. It returns None if the URL is not a valid
HTML page or some error occurred.
If you use another programming language, you can make a system call to execute this
file and pipe the output to your program. The command is
"python fetcher.py http://..."
The output is a list (may be empty "[]") of hyperlinks which looks like:
"['http://today.caltech.edu', 'http://www.caltech.edu/copyright/', ...]"
The output is "None" if the URL is not a valid HTML page or some error occurred.

Note: Updated urllib request to avoid 403 errors (Andrew Ma, ama2@caltech.edu)
"""

from html.parser import HTMLParser
from urllib.parse import urljoin
from urllib import request
from urllib.error import URLError
from typing import Dict, Tuple, List, Set
import urllib
import queue
import csv

# Our version of the HTMLParser, which handles start tags differently than Python's
# own HTMLParser. We overwrite the handle_starttag method to look for the desired
# hyperlinks.
class MyHTMLParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.urls = []

    def handle_starttag(self, tag, attrs):
        if tag == 'a' or tag == 'area': # extract href links from "a" and "area" tags
            href = [v for (k, v) in attrs if k == 'href']
            self.urls.extend(href)
        if tag == 'frame' or tag == 'iframe': # extra src links from "frame" and "iframe" tags
            src = [v for (k, v) in attrs if k == 'src']
            self.urls.extend(src)

    # Refine the hyperlinks: ignore the parameters in dynamic URLs, convert
    # all hyperlinks to absolute URLs, and remove duplicated URLs.
    def get_links(self, current_url):
        res = set()       # use a set to avoid duplicated URLs
        for url in self.urls:
            url = url.split('?')[0]   # extract the part before '?' if any
            url = url.split('#')[0]   # extract the part before '#' if any
            url = urljoin(current_url, url.strip())   # convert to absolute URL
            if url.startswith("http://") or url.startswith("https://"):
                res.add(url)
        res.discard(current_url)    # self-link is removed
        return list(res)

# Fetch an HTML file and return the real (redirected) URL and the content.
def fetch_html_page(url):
    content = None
    real_url = url
    req = urllib.request.Request(
        url=url,
        headers={'User-Agent': 'Mozilla/5.0'}
    )
    try:
        with urllib.request.urlopen(req, timeout=2) as usock:
            real_url = usock.url   # real_url will be changed if there is a redirection
            if "text/html" in usock.info()['content-type']:
                content=usock.read().decode('utf-8')    # only fetch it if it is html (not mp3/avi/...)
    # Terminate on CTRL+C sequences, and pass URLError up the stack.
    except KeyboardInterrupt:
        raise
    except:
        pass
    return (real_url, content)

# Fetch the hyperlinks by first fetching the content then using our HTMLParser to
# parse them.
def fetch_links(url):
    links = None
    try:
        parser = MyHTMLParser()
        real_url, content = fetch_html_page(url)
        if content is not None:
            parser.urls = []
            parser.feed(content)
            parser.close()
            links = parser.get_links(real_url)
    # Terminate on CTRL+C sequences, and pass URLError up the stack.
    except (KeyboardInterrupt, URLError):
        raise
    except:
        pass
    return links


def crawl(): 
    RESTRICTED_DOMAIN = "caltech.edu"
    START = "http://www.caltech.edu/"
    start_links = fetch_links(START)
    history: Set[Tuple[int, int]] = set() # set of tuples that contains all connections 
    # between sites in the caltech domain. Each tuple contains two ints, 
    # the first being the integer ID of the start site and the second being
    # the integer ID of the second
    links: queue.Queue[Tuple[str, str]] = queue.Queue() # queue of links to crawl
    # Implementation of BFS to crawl the network: iterate through all links from our
    # start page and enqueue each subsequent site's data

    last_idx = 1 # current integer ID for sites
    links_to_ints: Dict[str, int] = {START: 1} # mapping of links to their IDs
    crawled: List[int] = [1] # integers corresponding to IDs that 
    # should be included in our network

    MIN_CRAWLS = 75

    for link in start_links: 
        if RESTRICTED_DOMAIN in link: 
            links.put((START, link))
            if link not in links_to_ints: 
                last_idx += 1
                links_to_ints[link] = last_idx
                history.add((1, last_idx))

    def find_next_links(add_to_queue: bool):
        """
        Dequeue a link and find its neighbors. If add_to_queue, add the neighbors
        as nodes to query in the links queue. In all cases, create edges between 
        the current link and its neighbors. 
        """ 
        nonlocal last_idx

        _, curr = links.get()
        # Ensure that we don't repeat a crawl
        while True:        
            if links_to_ints[curr] not in crawled: 
                break
            else: 
                if links.empty(): 
                    return
                _, curr = links.get() # BFS: Get first pair in queue

        next_links = fetch_links(curr)
        curr_ID = links_to_ints[curr] # get ID of current link
        crawled.append(curr_ID) # note that we visited the current site
        if next_links is None: 
            return 

        for link in next_links: 
            if RESTRICTED_DOMAIN in link: # check if in caltech domain
                if add_to_queue: 
                    links.put((curr, link)) # add new and next link to queue
                    # if we have already identified this node
                if link in links_to_ints: 
                    # add new connection to network
                    history.add((curr_ID, links_to_ints[link]))
                else:
                    # we haven't seen this site before, add it to our dict and 
                    # log the connection
                    last_idx += 1
                    links_to_ints[link] = last_idx
                    history.add((curr_ID, links_to_ints[link]))

    for i in range(MIN_CRAWLS):
        if i % 5 == 0: 
            print(f"Iteration: {i}")
        find_next_links(True)

    while not links.empty():
        if links.qsize() % 10 == 0: 
            print(f"Clearing queue: {links.qsize()} remaining")
        find_next_links(False)

    # Clean dataset to only include sites we crawled
    print("Cleaning data")
    cleaned_history = set()
    for start, end in history: 
        if start in crawled and end in crawled: 
            cleaned_history.add((start, end))

    print(cleaned_history)

    cw = csv.writer(open("HW2/network.csv", "w"))
    cw.writerow(["source", "target"])
    cw.writerows(list(cleaned_history))


if __name__ == "__main__":
    crawl()