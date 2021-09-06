#!/usr/bin/python3


# Previous (working) script to generate the hpca hall of fame was here https://github.com/teshull/hpca_hof
# however it required the complete dblp database (more than 3GB) to fetch hpca data only (which is really just some KB).
# this script uses the dblp api to filter hpca papers. the obtained xml differs from the full dblp database, so I had to do some small changes
# over the original script. 
# The obtained list of authors in the hall of fame is the same as the previous script, so I guess it's all good.

# Understanding the process

# If we go to dplb, search for HPCA and select the proper conference, i.e., "International Symposium on High-Performance Computer Architecture (HPCA)"
# the web will redirect to the conference index: https://dblp.org/db/conf/hpca/index.html
# if we ask to download the data it will create a URL query (the url itself) like this:
# https://dblp.org/search/publ/api?q=stream%3Astreams%2Fconf%2Fhpca%3A&h=1000&format=xml
# this query already filters results for publications in HPCA only (the correct conference 'conf/hpca'; others such as 'conf/hpcasia' would not match the query)
# the query is (as expected) in accordance with the query API https://dblp.org/faq/How+to+use+the+dblp+search+API.html
# also notice that there is a limit in the amount of 1000 entries. So it was necessary to fetch data in chunks and append to the resulting xml file.
# we can thus issue more queries, based on the base query, to collect all chunks that matches the HPCA conference.

# E.g., try out pasting the following url queries on your browser to see how the dblp api works
# https://dblp.org/search/publ/api?q=stream%3Astreams%2Fconf%2Fhpca%3A&h=10&format=xml&f=0
# https://dblp.org/search/publ/api?q=stream%3Astreams%2Fconf%2Fhpca%3A&h=2&format=xml&f=1
# https://dblp.org/search/publ/api?q=stream%3Astreams%2Fconf%2Fhpca%3A&h=100&format=xml&f=1000


from xml.etree import ElementTree as ET
import requests
import os

base_api_query = "https://dblp.org/search/publ/api?q=stream%3Astreams%2Fconf%2Fhpca%3A&h={0}&format=xml&f={1}"
BATCH_SIZE = 1000

def unify_entries(aux_tree, tree):
    "Merge multiple chunks into a single xml tree."
    for hit in aux_tree.iter('hit'):
        tree.find('hits').append(hit)
    pass


def get_hpca_papers_with_api():
    "Issue queries to dblp api to fetch all hpca publications."
    batch_initial_index = 0
    query = base_api_query.format(BATCH_SIZE, batch_initial_index)      # we can ask for the #papers (max of 1000 per query) and initial index 
    
    # query the api
    response = requests.get(query)

    # get content and check if query worked
    tree = ET.fromstring(response.content)
    assert tree.find('status').text == "OK"
    assert tree.find('status').get('code') == '200'

    # check if more chunks are needed
    total_papers = int(tree.find('hits').get('total'))
    remaining_papers = total_papers - BATCH_SIZE
    
    while (remaining_papers > 0):
        batch_initial_index += BATCH_SIZE   # advances fetch index
        query = base_api_query.format(BATCH_SIZE, batch_initial_index)  # get a new batch of papers
        
        # query the api
        response = requests.get(query)
        aux_tree = ET.fromstring(response.content)  

        # get content and check if query worked
        assert aux_tree.find('status').text == "OK"
        assert aux_tree.find('status').get('code') == '200'

        # merge this batch with all previous data
        unify_entries(aux_tree, tree)
        
        # update control variable to know if more batches are necessary
        remaining_papers = remaining_papers - BATCH_SIZE  # discount acquired papers from the remaining

    return tree

def main():
    tree = get_hpca_papers_with_api() # get tree of papers from dblp, using their api (read the header of this file)
    doc =  ET.ElementTree(tree)     # https://stackoverflow.com/questions/56682486/xml-etree-elementtree-element-object-has-no-attribute-write
    os.makedirs('./xml', exist_ok=True)
    doc.write("./xml/dblp.xml")
    pass

if __name__ == '__main__':
    main()