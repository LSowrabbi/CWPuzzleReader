from tkinter import *
import subprocess
from createCW_pdf import *
from itertools import groupby
from subprocess import  call

master = Tk()
master.withdraw()
master.update()
width=15
height=15
max_cellno=0

# 'ifil' is the text file we get after implementing 'pdftotext' command
ftypes = [('Text files', '*.txt'), ('All files', '*')]
dlg = filedialog.Open(filetypes = ftypes)
ifil = dlg.show()
master.destroy()
# read puzzle data from 'ifil'
with open(ifil,"r",encoding='utf-8') as ins:
    array=[]
    i=-1
    for line in ins:
        i=i+1
        x=[]
        x.append(line)
        array.append(x)

# splits the read data based on its layout        
def splitWithIndices(s,c=' '):
    p = 0
    for k,g in groupby(s,lambda x:x==c):
        q = p+sum(1 for i in g)
        if not k:
            yield p,q
        p = q


array2=[]
array3=[]
for j  in range(len(array)):
    str1=array[j][0]
    ans1=list(splitWithIndices(str1))
    array2.append(ans1)
    array3.append(str1.split())

cellblock=[]
for j in range(15):
    row1=[]
    for jj in range(15):
        row1.append(0)
    cellblock.append(row1)


eog=0
str2=array[2][0]
# finds the position where the grid ends
for j in range(len(str2)):
    if (str2[j]=='\t'):
        eog=j
        break

for j in range(1,len(array)):
    strx=array[j][0]
    lst1=array2[j]
    lst2=array3[j]
    # finds the position where the cluelist begins
    if (len(lst1)-len(lst2) ==0):
        flag=0
        if ((j>5) and  (not lst2)):
            cluestart=j
            break
        # finds empty spaces
        if ((j > 5) and (lst1[0][0]<10) and (not (lst2[0].isdigit())) ):
            cluestart=j
            break

# quits the program if cluestart position cannot be found     
if (cluestart==0):
    sys.exit(0)
    
if (eog==0):
    eog=78

endofgrid=[]

# end of grid array maintains the end position for each row in the grid
for i in range(0,cluestart):
    endofgrid.append(eog)
num=1
clnum=[]
temp_cl=[]
count=0
temp_eog=[]

# finds the endofgrid and cellnumbers present in each row of the grid  
for j in range(1,cluestart):
        l=[]
        as2=array2[j]
        as3=array3[j]
        for i in range(len(as2)):
            ii=as2[i][0]
            ij =as2[i][1]
            ip=as3[i]
            if(ip.isdigit()):
                if(int(ip)==num):
                    l.append([num,ii])
                    num=num+1
                else:
                    endofgrid[j]=ii
                    break
            else:
                    endofgrid[j]=ii
                    break
        if(l!=[]):            
            temp_cl.append(l)
            temp_eog.append(endofgrid[j])
            temp_s=endofgrid[j]/15
            for i in range(len(temp_cl[count])):
                # denotes the width of each cell
                temp_cl[count][i][1]=round(temp_cl[count][i][1]/temp_s)
            count=count+1

max_eog=min(endofgrid)   
# sometimes a single cellno. (at the beginning or end of any row) might be printed on a new line
# this step appends such cells to the corresponding row's list
if(count!=15):
    for i in range(0,len(temp_cl)):
        if(len(temp_cl[i])==1 and temp_eog[i]>50):
            if(i==0):
                temp_cl[i+1].append(temp_cl[i][0])
            else:
                if(temp_cl[i+1][0]>temp_cl[i][0]):
                    temp_cl[i-1].append(temp_cl[i][0])
                else:
                     temp_cl[i+1].append(temp_cl[i][0])
        if(len(temp_cl[i])==1 and temp_eog[i]<50):
            if(i==0):
                temp_cl[i+1].insert(0,temp_cl[i][0])
            else:
                if(temp_cl[i-1][0]<temp_cl[i][0]):
                    temp_cl[i+1].insert(0,temp_cl[i][0])
                else:
                     temp_cl[i-1].insert(0,temp_cl[i][0])

# 'clnum' holds all cellnos corresponding to each row after the above filtering step                     
for i in range(0,len(temp_cl)):
    if(len(temp_cl[i])>1):
        clnum.append(temp_cl[i])
        
# assigns each cell, its cellno. (if it has one)        
for i in range(0,len(clnum)):
    for j in range(0,len(clnum[i])):
        val=clnum[i][j][0]
        col=clnum[i][j][1]
        if(cellblock[i][col]>0):
            jj=col
            while((cellblock[i][jj]!=0 and cellblock[i][jj]<val) and jj!=14):
                jj=jj+1
            if(jj!=14 and cellblock[i][jj]==0):
                cellblock[i][jj]=val
            if(jj!=14 and cellblock[i][jj]>val):
                temp=cellblock[i][jj]
                cellblock[i][jj]=val
                jj=jj+1
                while(jj!=14 and cellblock[i][jj]!=0):
                    temp_s=cellblock[i][jj]
                    cellblock[i][jj]=temp
                    temp=temp_s
                    jj=jj+1
                cellblock[i][jj]=temp
            if(jj==14):
                while(jj!=0 and cellblock[i][jj]!=0):
                    jj=jj-1
                if(jj!=0):
                    while(jj<14):
                        cellblock[i][jj]=cellblock[i][jj+1]
                        jj=jj+1
                    cellblock[i][jj]=val
        else:
            cellblock[i][col]=val

# 'max_cell' holds the maximum cellno.
max_cell=0
for i in range(15):
    max_cell=max(max_cell,max(cellblock[i]))

len1=0
# finds the rightmost position of any entry in the cluelist
for i in range(len(array)):
    if (len(array[i][0])>len1):
        len1=len(array[i][0])
title=""
author=""
title_set=False
found_across=False
colspace1=int(max_eog/3)-1
colspace2=int((len1-max_eog)/2)-1
# firstcolumn,secondcolumn and thirdcolumn denotes the cluelist entries present below the grid in the pdf file
firstcolumn=[]
secondcolumn=[]
thirdcolumn=[]
for i in range(cluestart,len(array)):
    ax=array2[i]
    bx=array3[i]
    if(len(ax)==len(bx) and i!=(len(array)-1)):
        # checks whether the last row of the document has been reached
        if(ax[0][0]==4 and array2[i+1][0][0]==0 and array2[i+1][0][1]==2 and array3[i+1][0]=="s"):
           break
        for j in range(len(ax)):
            # finds the title and author that would be present just before the rows containing across cluelist
            if(found_across!=True):
                if(bx[0]=="Across"):
                    found_across=True
                else:
                    # title is separated from the author by '|'
                    if(title_set==True and ax[j][0]<max_eog):
                        author=author+" "+bx[j]
                    if(title_set==False and bx[j]=='|' and ax[j][0]<max_eog):
                        for k in range(j):
                            title=title+bx[k]+" "
                        title_set=True
            if (ax[j][0]<colspace1):
                if(j+1<len(bx) and ax[j+1][1]>colspace1 and bx[j].isdigit()):
                    if(int(bx[j])<max_cell):
                        secondcolumn.append(bx[j])
                    else:
                        firstcolumn.append(bx[j])
                else:
                    firstcolumn.append(bx[j])
            else:
                # stores the cluelist to the respective columns to which they belong to
                if (ax[j][0]<2*colspace1):
                    if(j+1<len(bx) and ax[j+1][1]>(2*colspace1) and bx[j].isdigit()):
                        if(int(bx[j])<max_cell):
                            thirdcolumn.append(bx[j])
                        else:
                            secondcolumn.append(bx[j])
                    else:
                        secondcolumn.append(bx[j])
                else:
                    if(ax[j][0]<3*colspace1):
                        thirdcolumn.append(bx[j])


rowend=0
# 'rowend' represents the position to the right of the grid's endpoint
for i in range(cluestart+1,len(array)-10):
    ax=array2[i]
    bx=array3[i]
    if (len(ax)==len(bx)):
        for j in range(len(ax)):
            if (ax[j][0]>=3*colspace1):
                if(bx[j]=="Previous"):
                    rowend=i
                    break

# fourthcolumn and fifthcolumn denotes the cluelist entries present to the right of the grid in pdf file
fourthcolumn=[]
fifthcolumn=[]
gridend=max_eog

# decides whether the clue belongs to fourth or fifth column, for each entry in the cluelist present to the right of the grid
for i in range(1,rowend):
    ax=array2[i]
    bx=array3[i]
    if(len(ax)==len(bx)):
        for j in range(len(ax)):
            if (ax[j][0]>=max_eog and ax[j][1]<(max_eog+colspace2)):
                if(j+1<len(bx) and ax[j+1][1]>(gridend+colspace2) and bx[j].isdigit() and not(bx[j+1].isdigit())):
                    if(int(bx[j])<max_cell):
                        fifthcolumn.append(bx[j])
                    else:
                        fourthcolumn.append(bx[j])
                else:
                    fourthcolumn.append(bx[j])
            if (ax[j][1]>(max_eog+colspace2)):
                fifthcolumn.append(bx[j])

xrows={}
xcols={}
xmax=0
# stores the row and column corresponding to each cell in the grid that has a cellno. 
for i in range(15):
    for j in range(15):
        if (cellblock[i][j]>0):
            xrows[str(cellblock[i][j])]=i
            xcols[str(cellblock[i][j])]=j
            if (cellblock[i][j]>xmax):
                xmax=cellblock[i][j]


across0=[]
xacross=[]
xdown=[]
down0=[]
flag=0
xcount=0
strc=""
clue1=[]
direction=0
cur_no=0


for i in range(len(firstcolumn)):
    if (firstcolumn[i]=="Across"):
        cur_no=0
        direction=1
    else:
        # when a new clue is encountered
        if (firstcolumn[i].isdigit() and direction==1 and int(firstcolumn[i])>cur_no and int(firstcolumn[i])<=max_cell):
            cur_no=int(firstcolumn[i])
            if (flag>0):
                clue1.insert(1,strc)
                across0.append(clue1)
            flag=0
            clue1=[]
            strc=""
            clue1.insert(0,int(firstcolumn[i]))
            xacross.insert(xcount,int(firstcolumn[i]))
            xcount=xcount+1
        else:
            # checks whether the clueno. has been merged with the clue entry present to the right of it
            j=0
            while(j<len(firstcolumn[i])):
                if(firstcolumn[i][j].isdigit()):
                    j=j+1
                else:
                    break
            # if yes, separates the clueno. from the clue entry to the right of it
            if(j>0 and int(firstcolumn[i][0:j])>cur_no and direction==1  and int(firstcolumn[i][0:j])<=max_cell and ("Across" not in firstcolumn[i][j:]) and ("Down" not in firstcolumn[i][j:]) and ("-" not in firstcolumn[i][j:])):                
                cur_no=int(firstcolumn[i][0:j])
                if (flag>0):
                    clue1.insert(1,strc)
                    across0.append(clue1)
                clue1=[]
                strc=firstcolumn[i][j:]+" "
                clue1.insert(0,cur_no)
                xacross.insert(xcount,cur_no)
                xcount=xcount+1
            else:
                strc=strc+firstcolumn[i]+" "
                flag=1

for i in range(len(secondcolumn)):
    if (secondcolumn[i]=="Across"):
        direction=1
    else:
        # when a new clue is encountered
        if (secondcolumn[i].isdigit() and direction==1 and int(secondcolumn[i])>cur_no and int(secondcolumn[i])<=max_cell):
            cur_no=int(secondcolumn[i])
            if (flag>0):
                clue1.insert(1,strc)
                across0.append(clue1)
            flag=0
            clue1=[]
            strc=""
            clue1.insert(0,int(secondcolumn[i]))
            xacross.insert(xcount,int(secondcolumn[i]))
            xcount=xcount+1
        else:
            # checks whether the clueno. has been merged with the clue entry present to the right of it
            j=0
            while(j<len(secondcolumn[i])):
                if(secondcolumn[i][j].isdigit()):
                    j=j+1
                else:
                    break
            # if yes, separates the clueno. from the clue entry to the right of it
            if(j>0 and int(secondcolumn[i][0:j])>cur_no and direction==1  and int(secondcolumn[i][0:j])<=max_cell and ("Across" not in secondcolumn[i][j:]) and ("Down" not in secondcolumn[i][j:]) and ("-" not in secondcolumn[i][j:])):                
                cur_no=int(secondcolumn[i][0:j])
                if (flag>0):
                    clue1.insert(1,strc)
                    across0.append(clue1)
                clue1=[]
                strc=secondcolumn[i][j:]+" "
                clue1.insert(0,cur_no)
                xacross.insert(xcount,cur_no)
                xcount=xcount+1
            else:
                strc=strc+secondcolumn[i]+" "
                flag=1
                
for i in range(len(thirdcolumn)):
    # direction is set to 1 while going through across cluelist
    # direction is set to 2 while going through down cluelist
    # checks if the end of across cluelist has been reached
    if (thirdcolumn[i]=="Down"):
        cur_no=0
        direction=2
        xcount=0
        clue1.insert(1,strc)
        across0.append(clue1)
        strc=""
        clue1=[]
        flag=0
    else:
        if (thirdcolumn[i].isdigit() and int(thirdcolumn[i])>cur_no and int(thirdcolumn[i])<=max_cell):
            cur_no=int(thirdcolumn[i])
            if (flag>0):
                clue1.insert(1,strc)
                if (direction==1):
                    across0.append(clue1)
                else:
                    down0.append(clue1)
            flag=0
            clue1=[]
            strc=""
            clue1.insert(0,int(thirdcolumn[i]))
            if (direction==1):
                xacross.insert(xcount,int(thirdcolumn[i]))
                xcount=xcount+1
            else:
                xdown.insert(xcount,int(thirdcolumn[i]))
                xcount=xcount+1
        else:
            j=0
            while(j<len(thirdcolumn[i])):
                if(thirdcolumn[i][j].isdigit()):
                    j=j+1
                else:
                    break
            if(j>0 and int(thirdcolumn[i][0:j])>cur_no and int(thirdcolumn[i][0:j])<=max_cell and ("Across" not in thirdcolumn[i][j:]) and ("Down" not in thirdcolumn[i][j:]) and ("-" not in thirdcolumn[i][j:])):                
                cur_no=int(thirdcolumn[i][0:j])
                if (flag>0):
                    clue1.insert(1,strc)
                    if (direction==1):
                        across0.append(clue1)
                    else:
                        down0.append(clue1)
                clue1=[]
                strc=thirdcolumn[i][j:]+" "
                clue1.insert(0,cur_no)
                if (direction==1):
                    xacross.insert(xcount,cur_no)
                    xcount=xcount+1
                else:
                    xdown.insert(xcount,cur_no)
                    xcount=xcount+1
            else:
                strc=strc+thirdcolumn[i]+" "
                flag=1          

for i in range(len(fourthcolumn)):
    if (fourthcolumn[i]=="Down"):
        cur_no=0
        direction=2
        xcount=0
        clue1.insert(1,strc)
        across0.append(clue1)
        strc=""
        clue1=[]
        flag=0
    else:
        if (fourthcolumn[i].isdigit() and int(fourthcolumn[i])>cur_no and int(fourthcolumn[i])<=max_cell):
            cur_no=int(fourthcolumn[i])            
            if (flag>0):
                clue1.insert(1,strc)
                if (direction==1):
                    across0.append(clue1)
                else:
                    down0.append(clue1)
            flag=0
            clue1=[]
            strc=""
            clue1.insert(0,int(fourthcolumn[i]))
            if (direction==1):
                xacross.insert(xcount,int(fourthcolumn[i]))
                xcount=xcount+1
            else:
                xdown.insert(xcount,int(fourthcolumn[i]))
                xcount=xcount+1
        else:
            j=0
            while(j<len(fourthcolumn[i])):
                if(fourthcolumn[i][j].isdigit()):
                    j=j+1
                else:
                    break
            if(j>0 and int(fourthcolumn[i][0:j])>cur_no and int(fourthcolumn[i][0:j])<=max_cell and ("Across" not in fourthcolumn[i][j:]) and ("Down" not in fourthcolumn[i][j:]) and ("-" not in fourthcolumn[i][j:])):                
                cur_no=int(fourthcolumn[i][0:j])
                if (flag>0):
                    clue1.insert(1,strc)
                    if (direction==1):
                        across0.append(clue1)
                    else:
                        down0.append(clue1)
                clue1=[]
                strc=fourthcolumn[i][j:]+" "
                clue1.insert(0,cur_no)
                if (direction==1):
                    xacross.insert(xcount,cur_no)
                    xcount=xcount+1
                else:
                    xdown.insert(xcount,cur_no)
                    xcount=xcount+1
            else:
                strc=strc+fourthcolumn[i]+" "
                flag=1           


for i in range(len(fifthcolumn)):    
    if (fifthcolumn[i]=="Down"):
        #cur_no=int(fifthcolumn[i+1])
        cur_no=0
        direction=2
        xcount=0
        clue1.insert(1,strc)
        across0.append(clue1)
        strc=""
        clue1=[]
        flag=0
    else:
        if (fifthcolumn[i].isdigit() and int(fifthcolumn[i])>cur_no and int(fifthcolumn[i])<=max_cell and ("-" not in fifthcolumn[i][j:])):
            cur_no=int(fifthcolumn[i])
            if (flag>0):
                clue1.insert(1,strc)
                if (direction==1):
                    across0.append(clue1)
                else:
                    down0.append(clue1)
            flag=0
            clue1=[]
            strc=""
            clue1.insert(0,int(fifthcolumn[i]))
            if (direction==1):
                xacross.insert(xcount,int(fifthcolumn[i]))
                xcount=xcount+1
            else:
                xdown.insert(xcount,int(fifthcolumn[i]))
                xcount=xcount+1
        else:      
            if(j>0 and int(fifthcolumn[i][0:j])>cur_no and int(fifthcolumn[i][0:j])<=max_cell and ("Across" not in fifthcolumn[i][j:]) and ("Down" not in fifthcolumn[i][j:])):                
                cur_no=int(fifthcolumn[i][0:j])
                if (flag>0):
                    clue1.insert(1,strc)
                    if (direction==1):
                        across0.append(clue1)
                    else:
                        down0.append(clue1)
                clue1=[]
                strc=fifthcolumn[i][j:]+" "
                clue1.insert(0,cur_no)
                if (direction==1):
                    xacross.insert(xcount,cur_no)
                    xcount=xcount+1
                else:
                    xdown.insert(xcount,cur_no)
                    xcount=xcount+1
            else:
                strc=strc+fifthcolumn[i]+" "
                flag=1
                
clue1.insert(1,strc)
down0.append(clue1)

# finds the shaded cells in the grid based on across clue numbers   
for i in range(len(xacross)):
    xi=str(xacross[i])
    if (xi in xrows):
        ir=xrows[xi]
        ic=xcols[xi]
        if ((ic>0) and cellblock[ir][ic-1] ==0):
            cellblock[ir][ic-1]='.'

# finds the shaded cells in the grid based on down clue numbers   
for i in range(len(xdown)):
    xi=str(xdown[i])
    if (xi in xrows):
        ir=xrows[xi]
        ic=xcols[xi]
        if ((ir>0) and (cellblock[ir-1][ic] ==0)):
            cellblock[ir-1][ic]='.'

# assigns null value ('-') for all unshaded cells 
for i in range(0,height):
    for j in range(0,width):
        if(cellblock[i][j]==0):
            cellblock[i][j]="-"


# applies rotational symmetry               
def symmetry():
    global row,col
    for i in range(0,height):   
        for j in range(0,width):
            if(cellblock[i][j]=="."):
                rvalue=i
                cvalue=j
                row=(height-1)-rvalue
                col=(width-1)-cvalue
                if row >= 0 and col >= 0:
                    x0 = ex0[row][col]
                    y0 = ey0[row][col]
                    x1 = ex1[row][col]
                    y1 = ey1[row][col]
                    if(cellblock[row][col]!="."):
                        cellblock[row][col]="."
                        canvas.create_rectangle(x0, y0, x1, y1,fill="black", tags=str(row)+","+str(col))

# once the grid has been designed, proceeds to the next step of reviewing clues and assigning solution to the puzzle
def nxts():
    if val==1:
        master.destroy()
        initUI(width,height,cellblock,across0,down0,xacross,xdown,cn,title,author)

# calculates cell no. based on the shaded/unshaded cells        
def calc_cellno():
    global max_cellno,cn
    cellno=[]
    row_cellno=[]
    col_cellno=[]
    count=1
    for k in range(0,max_cellno):        
        canvas.delete("cell"+str(k))
    max_cellno=0
    for i in range(0,height):
        cellno.append([])       
        for j in range(0,width):
            cellno[i].append(0)
            # width-1 because last cell can't be the start of a clue.
            if j<width-1 and cellblock[i][j+1]!=".":
                if (cellblock[i][j]!="." and (j==0 or cellblock[i][j-1]==".")):
                    cellno[i][j]=count
                    # lists to keep track of row and column of each cell no. respecetively.
                    # count is 1 initially, so while searching use row_cellno[count-1]
                    row_cellno.append(i)
                    col_cellno.append(j)
                    count=count+1
            if i<height-1 and cellblock[i+1][j]!=".":       
                if (cellblock[i][j]!="." and (i==0 or cellblock[i-1][j]==".")):
                    if ((j<width-1 and cellblock[i][j+1]!=".")  and (j==0 or cellblock[i][j-1]==".")):
                        pass
                    else:
                        cellno[i][j]=count
                        count=count+1
                        row_cellno.append(i)
                        col_cellno.append(j)
            x=ex0[i][j]+5
            y=ey0[i][j]+5
            if(cellno[i][j]!=0):
                canvas.create_text(x, y, text=str(cellno[i][j]), tags="cell"+str(cellno[i][j]), font=("Times New Roman",9), fill="black")
            j=i+1
        i=i+1
    max_cellno=count
    cn=cellno

# shaded/unshades the cell that has been clicked
def cell_clicked0(event):
    x, y = event.x, event.y
    if (MARGIN < x < WIDTH - MARGIN and MARGIN < y < HEIGHT - MARGIN):
        canvas.focus_set()
        # gets row and col numbers from x,y coordinates
        row, col = int((y - MARGIN) / SIDE), int((x - MARGIN) / SIDE)
        if row >= 0 and col >= 0:
            x0 = ex0[row][col]
            y0 = ey0[row][col]
            x1 = ex1[row][col]
            y1 = ey1[row][col]
            if(cellblock[row][col]=="."):
                cellblock[row][col]="-"
                canvas.delete(str(row)+","+str(col))
            else:
                cellblock[row][col]="."
                canvas.create_rectangle(x0, y0, x1, y1,fill="black", tags=str(row)+","+str(col))
        calc_cellno()

# UI that allows user to review and edit the grid design
def initUI0(cb,w,h):
    global val,master,canvas,cellblock,MARGIN,WIDTH,SIDE,HEIGHT,ex0,ex1,ey0,ey1,width,height,max_cellno
    val=0
    cellblock=cb
    width=w
    height=h
    master = Tk()
    screen_height = master.winfo_screenheight()
    MARGIN=10
    HEIGHT=screen_height-200
    SIDE=(HEIGHT - (MARGIN*2))/height
    WIDTH=MARGIN*2+SIDE*width
    canvas= Canvas(master,width=WIDTH,height=HEIGHT)
    canvas.pack(fill=BOTH, side=TOP)
    ex0=[]
    ex1=[]
    ey1=[]
    ey0=[]
    for i in range(0,(width+1)):
        color="black" if (i==width or i==0) else "gray"
        x0 = MARGIN + i * SIDE
        y0 = MARGIN
        x1 = MARGIN + i * SIDE
        y1 = HEIGHT - MARGIN
        canvas.create_line(x0, y0, x1, y1, fill=color)
    for i in range(0,(height+1)):
        color="black" if (i==height or i==0) else "gray"
        x0 = MARGIN
        y0 = MARGIN + i * SIDE
        x1 = WIDTH - MARGIN
        y1 = MARGIN + i * SIDE
        canvas.create_line(x0, y0, x1, y1, fill=color)                
    for row in range (0,height):
        c=0
        ex0.append([])
        ex1.append([])
        ey0.append([])
        ey1.append([])
        for col in range (0,width):
            if(row==0):
                len1=MARGIN+(col*SIDE)
                ex0[row].append(len1)
                ey0[row].append(MARGIN)
                len2=MARGIN+((col+1)*SIDE)
                ex1[row].append(len2)
                ey1[row].append(MARGIN+SIDE)
            else:
                ex0[row].append(ex0[(row-1)][col])
                ey0[row].append(ey0[(row-1)][col]+SIDE)
                ex1[row].append(ex1[(row-1)][col])
                ey1[row].append(ey1[(row-1)][col]+SIDE)
    for i in range(0,height):
        for j in range(0,width):
            if(cellblock[i][j]=="."):
                x0 = ex0[i][j]
                y0 = ey0[i][j]
                x1 = ex1[i][j]
                y1 = ey1[i][j]
                canvas.create_rectangle(x0, y0, x1, y1,fill="black", tags=str(i)+","+str(j))
            x=ex0[i][j]+5
            y=ey0[i][j]+5
    calc_cellno()
    max_cellno=max_cell
    apply_symmetry=Button(master,text="Apply rotational symmetry", command=symmetry)
    apply_symmetry.pack(fill=Y, side=LEFT)
    nexts=Button(master,text="Next", command=nxts)
    nexts.pack(fill=Y, side=LEFT)
    val=1
    canvas.bind("<Button-1>", cell_clicked0)
    master.mainloop()

initUI0(cellblock,width,height)

