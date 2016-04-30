import subprocess
import sys
from itertools import groupby
from subprocess import  call
from createCW_latexHelper import *
from tkinter import *
master = Tk()
master.withdraw()
master.update()
width=0
height=0
index=0

ftypes = [('TEX files', '*.tex'), ('All files', '*')]
dlg = filedialog.Open(filetypes = ftypes)
ifil = dlg.show()
master.destroy()
# reads puzzle description from the LaTex file
with open(ifil,"r",encoding='utf-8') as ins:
    arr=[]
    i=-1
    inm=ins.read().splitlines()
    for line in inm:
        i=i+1
        x=[]
        x.append(line)
        if(len(x)==1):
            if(x[0]!=''):
                arr.append(x)
        else:
            arr.append(x)
        


array=[]
# splits the array based on the arguments (end of the argument is detected by '}') 
for j  in range(len(arr)):
    str1=arr[j][0]
    array.append(str1.split('}'))

# finds the width and height of the grid that are given as arguments to begin{Puzzle}
for i in range(0,len(array)):
    if("\\begin{Puzzle" in array[i]):
        ind=array[i].index("\\begin{Puzzle")
        while(ind+2<len(array[i])):
            temp=array[i][ind+1][1:len(array[i][ind+1])]
            temp1=array[i][ind+2][1:len(array[i][ind+2])] 
            if(temp.isdigit() and temp1.isdigit()):
                width=int(temp)
                height=int(temp1)
                index=i
                break
            else:
                ind=ind+1

# exits the program if width/height cannot be found
if(width==0 or height==0):
    sys.exit(0)

cellblock0=[]
cellno0=[]
row_cno=[]
col_cno=[]
# cellblock0 and cellno0 represents the grid and cellno for each cell present in the grid respectively
for i in range(height):   
    cellblock0.append([])
    cellno0.append([])
    for j in range(width):
        cellblock0[i].append("-")
        cellno0[i].append(0)
i=index+1
row=0
col=0
# finds the grid entries
while('\\end{Puzzle' not in array[i]):
    array[i][0].replace(" ","")
    temp=array[i][0].split('|')
    col=0
    for j in range(len(temp)):
        if(temp[j] not in ['','.']):
            temp[j]=temp[j].replace(" ","")
            if(temp[j]=='*'):
                cellblock0[row][col]="."
                col=col+1
            elif(temp[j][0]=='['):
                k=1
                temp_cell=""
                while(k<len(temp[j]) and temp[j][k]!=']'):
                    temp_cell=temp_cell+temp[j][k]
                    k=k+1
                k=k+1
                if(temp_cell.isdigit()):
                    cellno0[row][col]=int(temp_cell)
                    row_cno.append(row)
                    col_cno.append(col)
                if(k<len(temp[j]) and temp[j][k]=='['):           
                    while(k<len(temp[j]) and temp[j][k]!=']'):
                        k=k+1
                    k=k+1
                cellblock0[row][col]=temp[j][k:len(temp[j])]
                col=col+1
            else:
                cellblock0[row][col]=temp[j]
                col=col+1            
    row=row+1
    i=i+1
i=i+1
across0=[]
a=0
# filters the across cluelist from the array
while(['\\begin{PuzzleClues','{\\textbf{Across'] in array[i]):
    i=i+1
i=i+1
while('\\end{PuzzleClues' not in array[i]):
    if(len(array[i])!=1):
        j=0
        while(j<len(array[i])):
            if("Clue" in array[i][j]):
                across0.append([])
                k=len(array[i][j])-1
                while(k!=1 and array[i][j][k-1]!="{"):
                    k=k-1
                temp=""
                while(k<len(array[i][j]) and array[i][j][k].isdigit()):
                      temp=temp+array[i][j][k]
                      k=k+1
                across0[a].append(int(temp))
                j=len(array[i])-1
                while("{" not in array[i][j]):
                    j=j-1
                k=0
                while(k<len(array[i][j]) and array[i][j][k]!="{"):
                    k=k+1
                if(array[i][j][k]=="{"):
                    k=k+1
                    across0[a].append(array[i][j][k:len(array[i][j])])
                else:
                    across0[a].append("Across")
                a=a+1
            j=j+1               
    i=i+1
i=i+1
down0=[]
d=0
# filters the down cluelist from the array
while(['\\begin{PuzzleClues','{\\textbf{Down'] in array[i]):
    i=i+1
i=i+1    
while('\\end{PuzzleClues' not in array[i]):
    if(len(array[i])!=1):
        j=0
        while(j<len(array[i])):
            if("Clue" in array[i][j]):
                down0.append([])
                k=len(array[i][j])-1
                while(k!=1 and array[i][j][k-1]!="{"):
                    k=k-1
                temp=""
                while(k<len(array[i][j]) and array[i][j][k].isdigit()):
                      temp=temp+array[i][j][k]
                      k=k+1
                down0[d].append(int(temp))
                j=len(array[i])-1
                while("{" not in array[i][j]):
                    j=j-1
                k=0
                while(k<len(array[i][j]) and array[i][j][k]!="{"):
                    k=k+1
                if(array[i][j][k]=="{"):
                    k=k+1
                    down0[d].append(array[i][j][k:len(array[i][j])])
                else:
                    down0[d].append("Down")
                d=d+1
            j=j+1               
    i=i+1

# exits the program if across/down cluelist could not be found
if(len(across0)==0 or len(down0)==0):
    sys.exit(0)
else:
    initUI(width,height,cellblock0,across0,down0,cellno0,row_cno,col_cno)


