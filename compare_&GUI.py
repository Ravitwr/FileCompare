import PySimpleGUI as sg
import re, time
import datacompy
import datetime
import pandas as pd
import csv

sg.theme('Dark blue 4')
layoutprefile = [
    [sg.Text('Select two files to proceed')],
    [sg.Text('Folder 1'), sg.InputText(size=(75,2),change_submits=True), sg.FilesBrowse()],
    [sg.Text('Folder 2'), sg.InputText(size=(75,2),change_submits=True), sg.FilesBrowse()],
    [sg.Output(size=(101, 5))],
    [sg.Submit('Proceed'), sg.Cancel('Exit')]
]
window = sg.Window('File Compare', layoutprefile,resizable=True)
while True:    # The Event Loop
    event, values = window.read()
    # print(event, values)  # debug
    if event in (None, 'Exit', 'Cancel'):
        secondwindow = 0
        break
    elif event == 'Proceed':
#do some checks if valid directories have been provided
        file1test = file2test = isitago = proceedwithfindcommonkeys = None
        file1, file2 = values[0], values[1]
        if file1 and file2:
            file1test = re.findall('.+:\/.+\.+.', file1)
            file2test = re.findall('.+:\/.+\.+.', file2)
            isitago = 1
            if not file1test and file1test is not None:
                print('Error: File 1 path not valid.')
                isitago = 0
            elif not file2test and file2test is not None:
                print('Error: File 2 path not valid.')
                isitago = 0

            elif file1 == file2:
                print('Error: The files need to be different')
                isitago = 0

            elif isitago == 1:
                print('Info: Filepaths correctly defined.')
# check if files exist
                try:
                    print('Info: Attempting to access files.')
                    if re.findall('/.+?/.+\.(.+)',file1)[0]  in  ['csv', 'txt']:
                        df1, df2 = pd.read_csv(file1,sep=None, header=None,encoding='cp932', engine="python"), pd.read_csv(file2,sep=None, header=None,encoding='cp932', engine="python")
                    elif re.findall('/.+?/.+\.(.+)',file1)[0] == 'json':
                        df1, df2 = pd.read_json(file1), pd.read_json(file2)
                    elif re.findall('/.+?/.+\.(.+)',file1)[0] in  ['xlsx', 'xlsm']:
                        df1, df2 = pd.read_excel(file1), pd.read_excel(file2)
                    else:
                        pd.options.display.max_rows = None
                        pd.options.display.max_columns = None
                        #df1, df2 = pd.read_table(file1,sep=None, header=None,encoding='cp932', engine="python", quotechar='"'), pd.read_csv(file2,sep=None, header=None,encoding='cp932', engine="python")
                        with (
                               open("file1", "r", encoding='cp932', newline="\n") as f1,
                               open("file2", "r", encoding='cp932', newline="\n") as f2,
                            ):
                               lst1,lst2 = csv.reader(f1, delimiter=',',quotechar='"'), csv.reader(f2, delimiter=',', quotechar='"')
                               df1, df2 = pd.DataFrame(lst1), pd.DataFrame(lst2)

                    proceedwithfindcommonkeys = 1
                except IOError:
                    print("Error: File not accessible.")
                    proceedwithfindcommonkeys = 0
                except UnicodeDecodeError:
                    print("Error: File includes a unicode character that cannot be decoded with the default UTF decryption.")
                    proceedwithfindcommonkeys = 0
                except Exception as e:
                    print('Error: ', e)
                    proceedwithfindcommonkeys = 0
        else:
            print('Error: Please choose 2 files.')
        if proceedwithfindcommonkeys == 1:
            keyslist1 = [] #This will be the list of headers from first file
            keyslist2 = [] #This will be the list of headers from second file
            keyslist = [] #This will be the list of headers that are the intersection between the two files
            formlists = [] #This will be the list to be displayed on the UI
            for header in df1.columns:
                if header not in keyslist1:
                    keyslist1.append(header)
            for header in df2.columns:
                if header not in keyslist2:
                    keyslist2.append(header)
            for item in keyslist1:
                if item in keyslist2:
                    keyslist.append(item)
            if len(keyslist) == 0:
                print('Error: Files have no common headers.')
                secondwindow = 0
            else:
                window.close()
                secondwindow = 1
                break
#################################################
# First screen completed, moving on to second one
if secondwindow != 1:
    exit()
#To align the three columns on the UI

maxlen = 0
for header in keyslist:
    if len(str(header)) > maxlen:
        maxlen = len(str(header))
if maxlen > 25:
    maxlen = 25
elif maxlen < 10:
    maxlen = 15
#Split the keys to four columns
for index,item in enumerate(keyslist):
    if index == 0: i =0
    if len(keyslist) >= 4 and i == 0:
        formlists.append([sg.Checkbox(keyslist[i], size=(maxlen,None)),sg.Checkbox(keyslist[i+1], size=(maxlen,None)),sg.Checkbox(keyslist[i+2], size=(maxlen,None)),sg.Checkbox(keyslist[i+3], size=(maxlen,None))])
        i += 4
    elif len(keyslist) > i:
        if len(keyslist) - i - 4>= 0:
            formlists.append([sg.Checkbox(keyslist[i], size=(maxlen,None)),sg.Checkbox(keyslist[i+1], size=(maxlen,None)),sg.Checkbox(keyslist[i+2], size=(maxlen,None)),sg.Checkbox(keyslist[i+3], size=(maxlen,None))])
            i += 4
        elif len(keyslist) - i - 3>= 0:
            formlists.append([sg.Checkbox(keyslist[i], size=(maxlen,None)),sg.Checkbox(keyslist[i+1], size=(maxlen,None)),sg.Checkbox(keyslist[i+2], size=(maxlen,None))])
            i += 3
        elif len(keyslist)- i - 2>= 0:
            formlists.append([sg.Checkbox(keyslist[i], size=(maxlen,None)),sg.Checkbox(keyslist[i+1], size=(maxlen,None))])
            i += 2
        elif len(keyslist) - i - 1>= 0:
            formlists.append([sg.Checkbox(keyslist[i], size=(maxlen,None))])
            i += 1
        else:
            sg.Popup('Error: Uh-oh, something\'s gone wrong!')

#The second UI
sg.theme('Dark blue 4')
layoutpostfile = [
    [sg.Text('File 1'), sg.InputText(file1,disabled = True, size = (75,2))],
    [sg.Text('File 2'), sg.InputText(file2,disabled = True, size = (75,2))],
    #[sg.Text('Select the data key for the comparison:')],
    [sg.Frame(layout=[
        *formlists],title = 'Select the Data Key for Comparison',relief=sg.RELIEF_RIDGE
    )],
    [sg.Output(size=(maxlen*6, 20))],
    [sg.Submit('Compare'), sg.Cancel('Exit')]
]
window2 = sg.Window('File Compare', layoutpostfile,resizable=True, use_custom_titlebar=True)
datakeydefined = 0
definedkey = []
while True:  # The Event Loop
    event, values = window2.read()
    # print(event, values)  # debug
    if event in (None, 'Exit', 'Cancel'):
        break
    elif event == 'Compare':
        definedkey.clear()
        file1test = file2test = isitago = None
        starttime=datetime.datetime.now()
        #print('Event', event, '\n', 'Values', values)
        for index, value in enumerate(values):
            if index not in [0,1]:
                if values[index] == True:
                    datakeydefined = 1
                    definedkey.append(keyslist[index-2])
            #print(index, values[index], keyslist[index-2])
        if len(definedkey) > 0:
            compare = datacompy.Compare(
                    df1,
                    df2,
                    on_index=True,
                    abs_tol=0,
                    rel_tol=0,
                    df1_name='IF1',
                    df2_name='IF2'
            )
            print('########################################################################################################')
            endtime=datetime.datetime.now()-starttime
            print('Elapsed time : '+str(endtime))
            print(' ')
            #print(compare.report())
        else:
            print('Error: You need to select at least one attribute as a data key')
           

