#This python code will basically visit the website
#Parses out all the links looking for .csv, .xml, and .zip files
#and downloads them to the directory this .py file sits in
import urllib2
import re
import sys
from HTMLParser import HTMLParser

#only need to get href=... for our purposes
class MyHTMLParser(HTMLParser):
    csvFiles = []
    xmlFiles = []
    zipFiles = []
    csvRe = re.compile('.*\.csv.*', re.IGNORECASE)
    xmlRe = re.compile('.*\.xml.*', re.IGNORECASE)
    zipRe = re.compile('.*\.zip.*', re.IGNORECASE)
    
    def handle_starttag(self, tag, attrs):
        for t in attrs:
            if t[0] == "href":
                fileName = t[1]
                if self.csvRe.match(fileName):
                    self.csvFiles.append(fileName)
                elif self.xmlRe.match(fileName):
                    self.xmlFiles.append(fileName)
                elif self.zipRe.match(fileName):
                    self.zipFiles.append(fileName)
    
    def getCsvFiles(self):
        return self.csvFiles
    
    def getXmlFiles(self):
        return self.xmlFiles
    
    def getZipFiles(self):
        return self.zipFiles

if __name__ == "__main__":
    url = "http://www.repole.com/sun4cast/data.html"
    website = "http://www.repole.com/sun4cast/"
    
    #open the website and get html file
    response = urllib2.urlopen(url)
    html = response.read()
    lines = html.split("\n")
    
    #search for .csv, .xml and .zip files and keep a list of file
    parser = MyHTMLParser()
    parser.feed(html)
    
    csvFiles = parser.getCsvFiles()
    xmlFiles = parser.getXmlFiles()
    zipFiles = parser.getZipFiles()
    
    for fileName in csvFiles:
        file = urllib2.urlopen(website + fileName)
        output = open(fileName.split("/")[-1],'wb')
        output.write(file.read())
        output.close()

    for fileName in xmlFiles:
        file = urllib2.urlopen(website + fileName)
        output = open(fileName.split("/")[-1],'wb')
        output.write(file.read())
        output.close()
    
    for fileName in zipFiles:
        file = urllib2.urlopen(website + fileName)
        output = open(fileName.split("/")[-1],'wb')
        output.write(file.read())
        output.close()
        
    #computes the cumulative scoreOff per team in nfl2012stats.csv
    headerIndex = {}
    scoreOffs = {}
    teams = []
    
    file = open("nfl2012stats.csv", "r")
    #get headder info
    line = file.readline().strip()
    items = line.split(",")
    for i in range(0, len(items)):
        headerIndex[items[i]] = i
    for line in file:
        line = line.strip()
        items = line.split(",")
        
        teamName = items[headerIndex["TeamName"]]
        scoreOff = 0
        try:
            scoreOff = int(items[headerIndex["ScoreOff"]])
        except Exception:
            scoreOff = 0
            
        if not teamName in teams:
            teams.append(teamName)
            scoreOffs[teamName] = 0
        
        scoreOffs[teamName] = scoreOffs[teamName] + scoreOff
        
    file.close()
    
    #print the cumulative score offs
    for team in teams:
        print team + ": " + str(scoreOffs[team])