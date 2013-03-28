#imports for gui
import Tkinter
import tkFileDialog

#imports for backup script
import csv
import os
import re

class gui:
    def __init__(self,root):
        self.fileName = ''
        self.makeLabel(root)
        self.makeGoButton(root)
        self.makeBrowseButton(root)
        self.makeMessage(root)
        return
    def makeLabel(self,root):
        msg = 'Instructions:\n\n'+\
              '1. On the "Test Cases" tab of QA Complete select the Project you would\n'+\
              '   like to backup.\n\n'+\
              '2. Select the root node "Test Cases", you can select any other folder\n'+\
              "   in the hierarchy if you don't want to backup the whole test case library\n"+\
              '   for the chosen project all at once\n\n'+\
              '3. Click Actions > Export Test Cases (all fields) to download your test\n'+\
              '   cases as a single CSV file.\n\n'+\
              '4. Click the browse button in this window and select the downloaded CSV file.\n'+\
              '\n\n'+\
              'Note: Windows paths are limited to 256 characters, this script will\n' +\
              'shorten relative path names to 120 chars and limit the csv file\n'     +\
              'names created to 60 chars.  This means that the absolute path to\n'    +\
              'the directory that contains this script must be shorter than 60ish\n'  +\
              'chars.\n'
        Tkinter.Label(root,text=msg,justify=Tkinter.LEFT).pack(side=Tkinter.TOP,padx=10,pady=10)
        return
    def makeBrowseButton(self,root):
        Tkinter.Button(root,text="Browse",command=self.fileOpen).pack(side=Tkinter.RIGHT,padx=10,pady=10)
        return
    def makeGoButton(self,root):
        Tkinter.Button(root,text='Start', width=10).pack(side=Tkinter.RIGHT,padx=10,pady=10)
        return
    def makeMessage(self,root):
        Tkinter.Message(root,text='message',relief=Tkinter.SUNKEN, width=100).pack(side=Tkinter.RIGHT,padx=10,pady=10)
        return
    def printFileName(self):
        print self.fileName

    #opens the selected file name
    def fileOpen(self):
        self.fileName = tkFileDialog.askopenfilename(filetypes=[("CSV Files","*.csv")])
        return

    #appends newText to file at location: path
    def fileAppend(self, path, newText):
        dataSource = open(path, 'a')
        dataSource.write(newText)
        dataSource.close()
        return

    def backupScript(self):
        exportCSV = open(self.fileName,'rb')  #opens CSV file
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
                    self.fileAppend(path,testHead)   #write column titles and nl
                testCase = '\n'+testContent
                self.fileAppend(path,testCase)

        exportCSV.close()
        return


def main():
    root = Tkinter.Tk()
    k = gui(root)
    root.title('QAC Backup')
    root.mainloop()

main()
