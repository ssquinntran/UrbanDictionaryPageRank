# -*- coding: utf-8 -*-
import re
import sys
import urllib
import urlparse
import random
import pickle
from bs4 import BeautifulSoup

from random import randrange

class MyOpener(urllib.FancyURLopener):
    version = 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.2.15) Gecko/20110303 Firefox/3.6.15'

def domain(url):
    """
    Parse a url to give you the domain.
    """
    # urlparse breaks down the url passed it, and you split the hostname up 
    # ex: hostname="www.google.com" becomes ['www', 'google', 'com']
    hostname = urlparse.urlparse(url).hostname.split(".")
    hostname = ".".join(len(hostname[-2]) < 4 and hostname[-3:] or hostname[-2:])
    return hostname
    
def parse_links(url, url_start):
    """
    Return all the URLs on a page and return the start URL if there is an error or no URLS.
    """
    url_list = []
    myopener = MyOpener()

    # open, read, and parse the text using beautiful soup
    page = myopener.open(url)
    text = page.read()
    page.close()
    soup = BeautifulSoup(text, "html.parser")

    # find all hyperlinks using beautiful soup
    for tag in soup.findAll('a', href=True):
        # concatenate the base url with the path from the hyperlink
        urlstring = urlparse.urljoin(url, tag['href']).lower()

        # we want to stay in the berkeley EECS domain (more relevant later)...
        # if domain(tmp).endswith('berkeley.edu') and 'eecs' in tmp:
        try:
            parseresult = urlparse.urlparse(urlstring)
            prefix = parseresult.netloc.split(".")[0]
            # expect that parseresult.query[0:4] == "term"
            if prefix == "www" and domain(urlstring) == domain(url) and "term=" in urlstring:
                if not urlstring == url and not "page=" in urlstring and not "defid=" in urlstring:
                    if not "alphabetical" in tag.parent.parent["class"] and not "trending" in tag.parent.parent["class"]:
                        url_list.append(urlstring)
        except Exception as e:
            print "EXCEPTION", urlstring
            exc_type, exc_obj, exc_tb = sys.exc_info()
            print exc_type, exc_obj, exc_tb.tb_lineno

    if len(url_list) == 0:
        # print "OH FUCK WE'RE OUT OF WORDS"
        print "reached a sink"
        # return [url_start]
        return []
    return url_list
  

assert len(sys.argv) == 3
numseeds = int(sys.argv[1])
numclicks = int(sys.argv[2])
print "num seeds", numseeds
print "num clicks/seed", numclicks
print ""

filtered_out = {}
sorted_dict = {}
word_related = {}

seed = "http://www.urbandictionary.com/random.php"
hits = {} # words to counts
pagelinks = {} # words to links to counts
cache = {} # words to lists of links
counter = 0
myopener = MyOpener()
reseed = False
cached = False
damping_factor = .05
go_random = .05

# BEGIN ALT IMPLEMENTATION
for i in range(numseeds):
    start = myopener.open(seed)
    curr = start.geturl().lower()
    print "[SEED]", curr
    current_seed = curr.split("=")[1]
    if current_seed not in word_related.keys():
        print "added %s" % current_seed
        word_related[current_seed] = set()

    if not curr in hits:
        hits[curr] = 1
    else:
        hits[curr] += 1
    counter += 1
    j = 1
    while j < numclicks:
        if random.random() >= damping_factor:
            if random.random() < go_random:
                start = myopener.open(seed)
                curr = start.geturl().lower()
                print ""
                print cached, "[RESEEDED]", curr
            currword = curr.split("=")[1]

            if currword != current_seed:
                word_related[current_seed].add(currword)

            if currword in cache: # url list already cached
                urllist = cache[currword]
                cached = True
            else: # not cached
                while True:
                    try: # try to open the page and extract relevant links
                        urllist = parse_links(curr, curr) # ONLY LOOKS AT FIRST PAGE OF DEFINITIONS
                        break
                    except: # if it fails, just keep trying until it works
                        print "failure, trying again"

                linkcounts = {}
                for url in urllist:
                    nextword = url.split("=")[1]
                    if nextword in linkcounts:
                        linkcounts[nextword] += 1
                    else:
                        linkcounts[nextword] = 1
                pagelinks[currword] = linkcounts
                cache[currword] = urllist
                cached = False

            if urllist: # use a random link from the url list of the current page
                rand_index = randrange(0, len(urllist))
                curr = urllist[rand_index]
                print cached, rand_index, "/", len(urllist), curr

            else: # just terminate (or reseed)
                print cached, "no available links; terminating"
                break
                # ----------------
                # RESEED CODE:
                # ----------------
                # start = myopener.open(seed)
                # curr = start.geturl().lower()
                # print ""
                # print cached, "[RESEEDED]", curr

            if not curr in hits:
                hits[curr] = 1
            else:
                hits[curr] += 1
            counter += 1
        j += 1

    print j, "/", numclicks, "links visited in this seed"
    print "completed seed:", i + 1, "/", numseeds
    print ""
# END ALT IMPLEMENTATION

print ""

sorteddict = sorted(hits, key=hits.get, reverse=True)
# print sorteddict
for url in sorteddict:
    word = url.split("=")[1]
    print hits[url], word
    #updated filtered_out
    if word in filtered_out.keys():
        filtered_out[word] += hits[url]
    else:
        filtered_out[word] = hits[url]
    #updated sorted_dict
    if word in sorted_dict.keys():
        sorted_dict[word] += hits[url]
    else:
        sorted_dict[word] = hits[url]
#always keep number of filtered_out words to be <= 100
while len(filtered_out) > 100:
    min_word = min(filtered_out, key=filtered_out.get)
    filtered_out.pop(min_word, None)


print "words scoured", counter, "/", numseeds*numclicks
print ""


fwrite = open("medium_demo_filtered_out", "w")
fwrite1 = open("medium_demo_sorted_dict", "w")
fwrite2 = open("medium_demo_word_related", "w")

pickle.dump(filtered_out, fwrite)
pickle.dump(sorted_dict, fwrite1)
pickle.dump(word_related, fwrite2)

fwrite.close()
fwrite1.close()
fwrite2.close()


