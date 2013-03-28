import csv
import os
import re

#appends newText to file at location: path
def fileAppend(path, newText):
    dataSource = open(path, 'a')
    dataSource.write(newText)
    dataSource.close()
    return

print 'This program will only work if this script and exported CSV file are\n'+\
      'in the same directory.  Also the exported CSV file must have the\n'    +\
      'name "TestCases.csv".\n\n'+\
      'Note: Windows paths are limited to 256 characters, this script will\n' +\
      'shorten relative path names to 120 chars and limit the csv file\n'     +\
      'names created to 60 chars.  This means that the absolute path to\n'    +\
      'the directory that contains this script must be shorter than 60ish\n'  +\
      'chars.\n'
raw_input('press enter to continue otherwise close window to exit...')
print '\nRunning...'

exportCSV = open('TestCases.csv','rb')  #opens CSV file
dataCSV = csv.reader(exportCSV)         #parses CSV
i = 0                                   #only execute first if statement once
for r in dataCSV:
        
    if not i:                           #only execute on the first line
        testHead = str(r)[1:-1]     
        testHead = re.sub("[']","",testHead)
        for cN in range(0,len(r)):
            if r[cN] == 'Folder Name':
                folderCol = cN
        i = 1
    else:                               #execute on all following lines of csv
        path = r[folderCol]             #file path location
        path = path[:120]               #only allow first 120 chars
        path = path.strip()             #and strip spaces
            
        if path == '':                  #if no filename make directory 'No Path'
            path = 'No Path'
            if not os.path.exists(path): 
                os.makedirs(path)
        else:                           #if file name exists, make new directory
            if not os.path.exists(path):
                os.makedirs(path)

        testContent = ''                #initialize testContent
        for c in r:                     #combine all columns in row to 1 string
            testContent = testContent+'"'+c+'",'
        
        testContent = testContent[:-1]  #strip off last char ','
        j = path.rfind('/')             #find last '/' in path
        name = path[j+1:]               #gets lastchild of folder name, 
        name = name[:60]                #only allow first 60 chars
        name = name.strip()             #strips spaces
        name = '/'+name+'.csv'          #adds '/' and '.csv'
        path = path + name              #combines folder name and file name
        
        if not os.path.isfile(path):    #if <last_child>.csv doesn't exist
            fileAppend(path,testHead)   #write column titles and nl
        testCase = '\n'+testContent
        fileAppend(path,testCase)

exportCSV.close()
raw_input('\nFinished, press enter to close this window...')
