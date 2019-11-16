# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import requests
import sys


DBLP_URL_PREFIX = "https://dblp.org/rec/"
DBLP_URL_PREFIX_SIZE = len(DBLP_URL_PREFIX)
DBLP_PUB_API = "https://dblp.org/search/publ/api?"

ARXIV = 'CoRR'


def query_db(title):
    query = '+'.join(title.lower().split())
    resp = requests.get(DBLP_PUB_API, params={'q':query})    
    return BeautifulSoup(resp.content, 'lxml')


def normalize_pub_title(title):
    title = title.lower()
    if title.endswith('.'):
        title = title[:-1]
    return title


def normalize_input_title(title):
    title = title.lower()
    return title.replace(': ', ' - ')


def accio_pub(title):
    print('Accio article \"{}\"'.format(title))
    soup = query_db(title)
    pub_hits = soup.find_all("hits")    
    for hits in pub_hits:
        venue_hash = dict()
        for pub_hit in hits.find_all("hit"):        
            pub_info = pub_hit.find("info")
            pub_title = pub_info.find("title").text.strip()
            if normalize_pub_title(pub_title) != normalize_input_title(title):
                continue
            venue = pub_info.find("venue").text
            dblp_url = pub_info.find("url").text
            assert(dblp_url.startswith(DBLP_URL_PREFIX))
            bib_url = dblp_url[:DBLP_URL_PREFIX_SIZE] + 'bib2/' + dblp_url[DBLP_URL_PREFIX_SIZE:]
            venue_hash[venue] = bib_url
            if venue != ARXIV:
                break
        if venue_hash:
            bib_url = venue_hash[venue]
            bib_resp = requests.get(bib_url)
            # check for cross reference
            bib_content = bib_resp.text.split('\n\n')
            print('Success!')
            return [item.strip() for item in bib_content if item.strip()]
        else:
            print('Warning: no publication data found!')
        break


def accio():
    in_txt = sys.argv[1]
    out_bib = sys.argv[2]
   
    num_read, num_failed = 0, 0
    with open(in_txt) as f:
        bib_output = set()
        for line in f:
            num_read += 1
            bib_items = accio_pub(line.strip())
            if bib_items:
                for item in bib_items:
                    bib_output.add(item)
            else:
                num_failed += 1

    with open(out_bib, 'w') as o_f:
        for item in sorted(list(bib_output)):
            o_f.write(item + '\n\n')
    print('*** Completed ***')
    print('{} Succeeded, {} Failed'.format(num_read - num_failed, num_failed))
    print('Bibtex saved to {}'.format(out_bib))


if __name__ == '__main__':
    # title = 'NL2Bash: A Corpus and Semantic Parser for Natural Language Interface to the Linux Operating System'
    # accio_pub(title)
    accio() 
    
