import csv
import os
import re

#appends newText to file at location path
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

raw_input('press enter to continue otherwise close window to exit...\n')
print 'Running...'

exportCSV = open('TestCases.csv','rb')  
#parses CSV
dataCSV = csv.reader(exportCSV)         
#only execute first 'if' statement once
i = 0                                   

for r in dataCSV:

    #only execute on the first line   
    if not i:                           
        testHead = str(r)[1:-1]     
        testHead = re.sub("[']","",testHead)
        for cN in range(0,len(r)):
            if r[cN] == 'Folder Name':
                folderCol = cN
        i = 1

    #execute on all following lines of csv
    else:                               
        #file path location
        path = r[folderCol]
        #only allow first 120 chars
        path = path[:120]               
        #strip spaces
        path = path.strip()             

        #if no filename make directory 'No Path'
        if path == '':
            path = 'No Path'
            if not os.path.exists(path): 
                os.makedirs(path)

        #if file name exists, make new directory
        else:
            if not os.path.exists(path):
                os.makedirs(path)

        #initialize testContent
        testContent = ''
        #combine all columns in row to 1 string
        for c in r:
            testContent = testContent+'"'+c+'",'
        
        #strip off last char ','
        testContent = testContent[:-1]
        #gets lastchild of folder name,
        j = path.rfind('/')             
        name = path[j+1:]                
        #only allow first 60 chars
        name = name[:60]
        #strips spaces
        name = name.strip()
        #adds '/' and '.csv'
        name = '/'+name+'.csv'
        #combines folder name and file name
        path = path + name
        
        #if <last_child>.csv doesn't exist write column titles and nl
        if not os.path.isfile(path):
            fileAppend(path,testHead)
        testCase = '\n'+testContent
        fileAppend(path,testCase)

exportCSV.close()
raw_input('\nFinished, press enter to close this window...')
