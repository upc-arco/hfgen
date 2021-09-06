#!/usr/bin/python3

import argparse
import operator
import re
import codecs
import sys
from lxml import etree


pageRegex = re.compile("([0-9]+)-([0-9]+)")
startYear = 1995
endYear = 2021
xmlFolder = "./xml"
outputFile = "out.txt"

def printOutInfo(container, authorNames, rankings, filename, numRange=0):
    text_file = codecs.open(filename, mode='w+', encoding='utf-8')
    if numRange == 0:
        numRange = len(rankings)
    for num in range(numRange):
        id = rankings[num][0]
        author = authorNames[id]
        line = author + " (total=" + str(rankings[num][1]) + "): "
        for y in range(startYear, endYear+1):
            year = str(y)
            numPapers = container[id].get(year, 0)
            line = "%s%d," % (line, numPapers)
        text_file.write(line+"\n")


def addToCount(container, key):
    count = container.get(key, 0) + 1
    container[key] = count


def addAuthorInfo(container, author, year):
    if author not in container:
        container[author] = {}
    addToCount(container[author], year)

def addAuthorName(container, id, name):
    if id not in container:                 # if this author haven't been accounted yet, add it
        container[id] = name
    else:
        if len(name) > len(container[id]):   # use the 'longest' name ever found
            container[id] = name

def processElement(authorCount, authorData, authorNames, paper):

    if (paper.find('type').text == "Editorship"):
        return False

    #checking for invalid matches
    pages = paper.xpath('pages')[0].text
    regexResult = pageRegex.match(pages)
    if(not regexResult):
        return False
    year = paper.xpath('year')[0].text
    yearNum = int(year)
    if(yearNum < startYear or yearNum > endYear):
        return False

    authors = paper.find('authors').xpath('author')
    pageLength = int(regexResult.group(2)) - int(regexResult.group(1)) + 1
    # adding this because some workshops are included and had 8 page papers
    criteria = ((pageLength > 6 and yearNum < 2015) or
                 (pageLength >=3 and yearNum == 1999) or
                 (pageLength >=10 and yearNum >= 2015))
    if(not criteria):
        print("found paper not meeting criteria")
        print("pageLength:  ", pageLength)
        print("year: ", year)
        print("attribute: ", paper.find('key').text)
        output = "authors: "
        for author in authors:
            output += author.text + ", "
        print(output)
        return False

    for author in authors:
        author_id = author.get('pid')   # avoid problems if the name appears different (e.g., Michael G. Scott vs. Michael Gary Scott). Also, primary key should be unique.
        author_name = author.text
        addToCount(authorCount, author_id)
        addAuthorInfo(authorData, author_id, year)
        addAuthorName(authorNames, author_id, author_name)
    return True

def eventDrivenParsing():
    count = 0
    #map contains number of papers for author
    authorCount = {}
    #map containing number of papers for author in each year
    authorData = {}
    #mao containing the id and name of each author
    authorNames = {}
    fileName = "%s/dblp.xml" % (xmlFolder)
    for _, element in etree.iterparse(fileName, load_dtd=False,
                                          dtd_validation=False):
        if(element.tag == "info"):
            if(processElement(authorCount, authorData, authorNames, element)):
                count += 1
            #since no longer needed, free up memory allocated to element
            element.clear()

    print("total count = ", count)
    sortedResult = sorted(authorCount.items(), key=operator.itemgetter(1),
                           reverse=True)
    printOutInfo(authorData, authorNames, sortedResult, outputFile)


def parseArgs():
    global xmlFolder, startYear, endYear, outputFile
    parser = argparse.ArgumentParser(prog='HPCA HOF List Generator')
    parser.add_argument('--xmlFolder',
                        default=xmlFolder,
                        help='location of xml folder')
    parser.add_argument('--startYear',
                        default=startYear,
                        help='first year to count')
    parser.add_argument('--endYear',
                        default=endYear,
                        help='last year to count')
    parser.add_argument('--outputFile',
                        default=outputFile,
                        help='where to write results')

    args = parser.parse_args()
    xmlFolder = args.xmlFolder
    outputFile = args.outputFile
    startYear = int(args.startYear)
    endYear = int(args.endYear)

def main():
    parseArgs()
    eventDrivenParsing()

if __name__ == '__main__':
    main()