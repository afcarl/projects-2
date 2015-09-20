#!/usr/bin/env python

# File for publishing project pages to the web.

import os
import sys
import re
import shutil
import time
import string
import httplib
import posix
import yaml

sys.path.append(os.path.join(posix.environ['HOME'], 'public_html', 'cgi-bin'))
import ndltext
import ndlfile
import ndlhtml


homeDir = os.getenv('HOME')

#projectHeader.txt contains the pages' headers
fileNameBase = os.path.join(homeDir, 'SheffieldML', 'projects');
projectHeader = ndlfile.readTxtFile('projectHeader.txt', fileNameBase)
#projectFooter.txt contains the pages' footers
projectFooter = ndlfile.readTxtFile('projectFooter.txt', fileNameBase)
#projectStyle.txt contains the pages' style
projectStyle = ndlfile.readTxtFile('projectStyle.txt', fileNameBase)
# projectNavigation contains navigation bar.
projectNavigation = ndlfile.readTxtFile('projectNavigation.txt', fileNameBase)

# arguments PROJECTNAME
sheffieldPersonBase = 'http://www.dcs.sheffield.ac.uk/cgi-bin/makeperson?'
sheffieldBase = 'http://ml.sheffield.ac.uk/'
if len(sys.argv) < 2:
    raise "There should be an input argument (project name)."
year = time.strftime('%Y')
timeStamp = time.strftime('%A %d %b %Y at %H:%M')
projectName = sys.argv[1];
lowerProject = projectName.lower();
f = open('project.yml', 'r')
project = yaml.load(f)

# personnel.txt contains staff/students information
personnelDetails = ndlfile.extractFileDetails('personnel.txt')

# publication.txt contains details of the publications.
publicationDetails = ndlfile.extractFileDetails('publications.txt')

overview=''
fileHandle = open('overview.md', 'r');
fileLines = fileHandle.readlines()
fileHandle.close()
for line in fileLines:
    overview += line

outputString="# " + project['shortname'] + " Project\n\n"
outputString += "## Overview"
outputString+= "\n\n" + overview


if len(project['sponsors'])>0:
    outputString += "The project is sponsored by "
    for sponsor in project['sponsors']:
        outputString += "[" + sponsor['name'] + " Project Ref " + str(sponsor['ref']) + "](" + sponsor['url'] + ")"
        if len(project['sponsors'])>1:
            if i==len(project['sponsors'])-1:
                outputString += ", "
            else:
                outputString += " and "
    if len(project['collaborators'])>0:
        outputString += " and is a collaboration with "
    else:
        outputString += ".\n\n" 
       
else:
    if len(project['collaborators'])>0:
        outputString += "The project is a collaboration with "

if len(project['collaborators'])>0:
    for i, collaborator in enumerate(project['collaborators']):
        outputString += "[" + collaborator['name'] + "](" + collaborator['url'] + ") of " + collaborator['institute']
        if len(project['collaborators'])>1:
            if i==len(project['collaborators'])-2:
                outputString += " and "
            elif i==len(project['collaborators'])-1:
                outputString += "."
            else:
                outputString += ", "
        else:
            outputString += ".\n\n"

if len(project['personnel'])>0:
    outputString+= "\n\n<a name=\"personnel\"></a>## Personnel from ML@SITraN\n\n"
    for person in project['personnel']:
        outputString += "- [" + person['name'] + "](" + person['url'] + ") " + person['role'] + "\n\n"

    outputString += "\n\n"

# Give information about software.
if len(project['software'])>1:
    outputString+= "<a name=\"software\"></a>## Software\n\n"
    outputString+= "The following software has been made available either wholly or partly as a result of work on this project:"
    for i, software in enumerate(project['software']):
        if software['url']=='local':
            outputString += "- [" + software['name'] + "](http://inverseprobability.com/" + software['name'] + ") " + software['tagline'] + "\n\n"
        elif software['url']=='SheffieldML':
            outputString += "- Github: [" + software['name'] + "](https://github.com/SheffieldML/" + software['name'] + ") " + software['tagline'] + "\n\n"
        else:
            outputString += "- [" + software['name'] + "](" + software['url'] + ") " + software['tagline'] + "\n\n"



# Give information about publications
outputString+="<a name=\"publications\"></a>## Publications\n\n"
for key in project['publications']:
    print key
    if key == 'conference':
        outputString+="The following conference publications were made associated with this project.\n\n"
    elif key == 'chapters':
        outputString+="The following edited chapters were published as part of this project.\n\n"
    elif key == 'journal':
        outputString+="The journal papers were published as part of this project.\n\n"
    elif key == 'books':
        outputString+="The following books were published as part of this project.\n\n"
    elif key == 'patents':
        outputString+="The patents were applied for as part of this project.\n\n"

    elif key == 'related':
        outputString+="The following publications have provided background to our work in this project.\n\n"

    for publicationkey in project['publications'][key]:
        outputString += ndlhtml.getMdReference(publicationkey)
        outputString += '\n\n'

# Now create a web page
publishBase=os.path.expanduser(os.path.join("~", "public_html", "projects", lowerProject));

if not os.path.exists(publishBase):
    os.mkdir(publishBase)



ndlhtml.mdWriteToFile('index.md', outputString, projectStyle, project['shortname'], projectHeader, projectFooter, projectNavigation)

shutil.copyfile('index.md', os.path.join(publishBase, 'index.md'))
