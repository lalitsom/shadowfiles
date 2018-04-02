import urllib
from HTMLParser import HTMLParser
import os

try:
    from urllib import unquote
except ImportError:
    from urllib.parse import unquote

print '\n Welcome to Shadow Files :: \n'
print ':::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::: \n'
print  'Need help: File an issue  on https://github.com/lalitsom/shadowfiles/issues'
print ':::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::: \n'
print 'copy paste the link of an online directory \n'
rooturl = raw_input()
print 'Enter a folder name (eg. downloads)\n'
rootdir = unquote(raw_input())

def createdir(dirpath):
    if not os.path.exists(dirpath):
        os.makedirs(dirpath)

def linkisparent(link):    
	parentlinks = ['../','Parent','root','Directory']
	for keyword in parentlinks:
		if keyword in link:			            
			return True
	return False		

# append / if not present
if rooturl[-1] != '/':
    rooturl += '/'


# append / if not present
if rootdir[-1] != '/':
    rootdir += '/'

# folders to traverse... BFS QUEUE
folders = []


template = open('vlctemplate.xspf').read()

class MyHTMLParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        global folders
        global rooturl
        global rootdir
        if tag=='a':
            for ats in attrs:
                try:                    
                    if ats[0] == 'href':
                        lnkname = ats[1]
                        if lnkname[-1] == '/':
                            folders.append([rooturl+lnkname,rootdir+unquote(lnkname)])
                            createdir(rootdir+unquote(lnkname))
                        else:
                            print rooturl+lnkname +" ---> "+rootdir+lnkname
                            outfile=open('./'+rootdir+unquote(lnkname)+".xspf", 'w+')
                            outfile.write(template.replace("##sourcelink##",rooturl+lnkname))
                            outfile.close()
                except:
                    print 'error occured, continuing.......'            

    def handle_endtag(self, tag):
        tmp = 6  # this line is useless, just like your existence.

    def handle_data(self, data):
        tmp = 6  # on second thoughts, your life is more usless.



def traverse(link, _dir):
    global rootdir
    global rooturl
    rootdir = unquote(_dir)
    rooturl = link
    parser = MyHTMLParser()
    createdir(_dir)
    response = urllib.urlopen(link)
    htmldata = response.read()
    parser.feed(htmldata)
    parser.close()

traverse(rooturl,rootdir)

while folders:
    link,folder = folders.pop()    
    if linkisparent(link):
    	print link,' skipped'        
        continue
    print link,' saved'
    traverse(link,folder)
