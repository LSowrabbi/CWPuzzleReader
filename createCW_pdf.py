from tkinter import *
from createCW_pdfHelper import *
import tkinter.filedialog
master = Tk()
cellblock=[]
master.destroy()
class File():
    title=None
    author=None
    cpyrt=None
    notes=None
    width=0
    height=0
    solnblock=[]
    acc=0
    dwn=0
    across=[]
    down=[]
    loc=""

def highlightclue(c_row,c_col):
    # if across_down = "Across" then dull clue = down and cur_clue = across, else vice versa
    d_col=c_col
    global dull_clue,cur_clue,dull_clue_ad,cur_clue_ad,cur_bool
    # clears previous dull and current clues
    cur_bool=True
    if(dull_clue_ad=="across"):
        if(acc!=0):
            listbox.selection_clear(dull_clue)
    else:
        if(dwn!=0):
            listbox1.selection_clear(dull_clue)
    if(cur_clue_ad=="across"):
        if(acc!=0):
            listbox.selection_clear(cur_clue)
    else:
        if(dwn!=0):
            listbox1.selection_clear(cur_clue)
    # reconfigures the foreground color of dull clues to red
    if(dull_clue_ad=="across"):
        if(acc!=0):
            listbox.itemconfig(dull_clue,selectbackground="gray",selectforeground="red")
    else:
        if(dwn!=0):
            listbox1.itemconfig(dull_clue,selectbackground="gray",selectforeground="red")
    if across_down=="across":
        cur_clue_ad="across"
        dull_clue_ad="down"
    else:
        cur_clue_ad="down"
        dull_clue_ad="across"
    # finds new dull and current clues
    while(c_col!=0 and cellblock[c_row][c_col]!='.'):
        c_col=c_col-1
    if(cellblock[c_row][c_col]=='.'):
        c_col=c_col+1
    for i in range(0,acc+1):
        if(i!=acc):
            if(cellno[c_row][c_col]==across[i][0]):
                if across_down=="across":
                    cur_clue=i
                else:
                    dull_clue=i
                break
    if i==acc:
        if across_down=="across":
            cur_bool=False
            cur_clue=0
        else:
            dull_clue=0
    while(c_row!=0 and cellblock[c_row][d_col]!='.'):
        c_row=c_row-1
    if(cellblock[c_row][d_col]=='.'):
        c_row=c_row+1
    for i in range(0,dwn+1):
        if(i!=dwn):
            if(cellno[c_row][d_col]==down[i][0]):
                if across_down=="down":
                    cur_clue=i
                else:
                    dull_clue=i
                break
    if i==dwn:
        if across_down=="down":
            cur_bool=False
            cur_clue=0
        else:
            dull_clue=0
   
    # highlights dull and current clues and reconfigures foreground color of dull clue
    if(cur_clue_ad=="across"):
        if(acc!=0):
            listbox.selection_set(first=cur_clue)
            disp_clue=across[cur_clue][1]
            listbox.see(cur_clue)
    else:
        if(dwn!=0):
            listbox1.selection_set(first=cur_clue)
            disp_clue=down[cur_clue][1]
            listbox1.see(cur_clue)
    if(dull_clue_ad=="across"):
        if(acc!=0):
            listbox.itemconfig(dull_clue,selectbackground="gray",selectforeground="black")
            listbox.selection_set(first=dull_clue)
            listbox.see(dull_clue)
    else:
        if(dwn!=0):
            listbox1.itemconfig(dull_clue,selectbackground="gray",selectforeground="black")
            listbox1.selection_set(first=dull_clue)
            listbox1.see(dull_clue)
    text.delete("1.0",END)
    if cur_bool==True:
        if(across_down=="across"):
            labelE.config(text="Enter clue for  "+ str(across[cur_clue][0])+".  Across : ")
        else:
            labelE.config(text="Enter clue for  "+ str(down[cur_clue][0])+".  Down : ")                         
        text.insert(INSERT,disp_clue)
    else:
        if across_down=="across":
            labelE.config(text="No across clue for this block")
        else:
            labelE.config(text="No down clue for this block")

# creates temporary text for highlighted cells
def create_txt(row,col):
    global temp_str
    if (cellblock[row][col]!="-" and cellblock[row][col]!="."):
        if str(row)+","+str(col) in taglist:
            x=(ex0[row][col]+ex1[row][col])/2+3
            y=(ey0[row][col]+ey1[row][col])/2+3
            temp_str.append("temp_str"+str(row)+","+str(col))
            temp_text=cellblock[row][col]
            if(len(temp_text)==1):
                size=16
            else:
                size=10
            # checks for rebus
            if(len(temp_text)>2):
                temp_text=temp_text[0:2]+".."
            canvas.create_text(x, y, text=temp_text,font=("Arial",size,"bold"), tag=("temp_str"+str(row)+","+str(col)), fill="black" )

# creates temporary cellno,if any, for highlighted cells
def create_cellno(row,col):
    global temp_cellno
    if (cellno[row][col]!=0):
        x=ex0[row][col]+5
        y=ey0[row][col]+5
        temp_cellno.append(("temp_cell"+str(row)+","+str(col)))
        canvas.create_text(x, y, text=str(cellno[row][col]),tag=("temp_cell"+str(row)+","+str(col)),font=("Times New Roman",9), fill="black")
        
def create_rect(c_row,c_col):
    # highlights word corresponding to the currently active row and col
    global temp_str,temp_cellno
    # deletes previously highlighted circles,cell nos,entries showing validity and texts.
    canvas.delete("cursor")
    for element in temp_str:
        canvas.delete(element)
    del temp_str[:]
    for element in temp_cellno:
        canvas.delete(element)
    del temp_cellno[:]
    # highlights cell of the clicked letter to red
    if cellblock[c_row][c_col]!=".":
        canvas.create_rectangle(ex0[c_row][c_col],ey0[c_row][c_col], ex1[c_row][c_col], ey1[c_row][c_col],fill="red", tags=("cursor"))
        highlightclue(c_row,c_col)
        # creates temporary entries for the highlighted cell
        create_txt(c_row,c_col)      
        if(cellno[c_row][c_col]!=0):
            create_cellno(c_row,c_col)
        row=c_row
        col=c_col
        # highlights and creates temporary entires for the cells to the left/up, that form the word along with the letter in the highlighted cell
        if (across_down=="down"):
            row=c_row-1
        else:
            col=c_col-1
        if(row >=0 and col >=0):
            while(cellblock[row][col]!="."):
                canvas.create_rectangle(ex0[row][col], ey0[row][col], ex1[row][col], ey1[row][col],fill="#A6A6A6", tags=("cursor"))
                create_txt(row,col)
                if(cellno[row][col]!=0):
                    create_cellno(row,col)
                if across_down=="down":
                    row=row-1
                else:
                    col=col-1
                if (row <0 or col<0):
                    break
        # highlights and creates temporary entires for the cells to the right/down, that form the word along with the letter in highlighted cell
        if (across_down=="down"):
            row=c_row+1
        else:
            col=c_col+1
        if(row <height and col <width):
            while(cellblock[row][col]!="." and cellblock[row][col]!=":"):
                canvas.create_rectangle(ex0[row][col], ey0[row][col], ex1[row][col], ey1[row][col],fill="#A6A6A6", tags=("cursor"))
                create_txt(row,col)
                if(cellno[row][col]!=0):
                    create_cellno(row,col)
                if across_down=="down":
                    row=row+1
                else:
                    col=col+1
                if (row == height or col==width):
                    break

def list_clicked(no_clicked):
    # highlights  word associated with the clue selected
    global row,col
    if(is_multi==0):
        row=row_cellno[no_clicked-1]
        col=col_cellno[no_clicked-1]
        create_rect(row,col)
    

# when any clue in  across list box is clicked :
def box_clickedA(event):
    global across_down
    if(is_multi==0):
        across_down="across"
        firstIndex = listbox.curselection()[0]
        list_clicked(across[firstIndex][0])

# when any clue in the down list box is clicked :      
def box_clickedD(event):
    global across_down
    if(is_multi==0):
        across_down="down"
        firstIndex = listbox1.curselection()[0]
        list_clicked(down[firstIndex][0])
        
        
def cell_clicked(event):
    # changes the focus word to the corresponding mouse click position
    global row,col,across_down,temp_str,taglist,temp_str     
    x, y = event.x, event.y
    if(is_multi==0):
        if (MARGIN < x < WIDTH - MARGIN and MARGIN < y < HEIGHT - MARGIN):
            canvas.focus_set()
            # get row and col numbers from x,y coordinates
            c_row, c_col = int((y - MARGIN) / SIDE), int((x - MARGIN) / SIDE)
            if c_row >= 0 and c_col >= 0:
                if cellblock[c_row][c_col]!=".":
                    row,col=c_row,c_col
                    create_rect(row,col)

 
def change_state(c_state):
    filemenu.entryconfig(0,state=c_state)
    filemenu.entryconfig(1,state=c_state)
    filemenu.entryconfig(2,state=c_state)
    return

def key_pressed(event):         
    # associates character key pressed to the currently active cell in the grid
    global row,col,across_down,taglist,temp_str,is_multi,multi
    if(is_multi==1):
        # for rebus entries
        if(len(multi)<8):
            if event.keysym in 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz' and cellblock[row][col]!="." :
                canvas.delete("mults")
                x=(ex0[row][col]+ex1[row][col])/2+10
                y=(ey0[row][col]+ey1[row][col])/2+10
                strn=event.char
                multi.append(strn)
                canvas.create_text(x, y, text=''.join(multi),font=("Arial",10),tag="mults", fill="black")
    else:
        if row>=0 and col>=0 and event.keysym in 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz' and cellblock[row][col]!=".":
            if str(row)+","+str(col) in taglist:
                canvas.delete(str(row)+","+str(col))
                canvas.delete("temp_str"+str(row)+","+str(col))
            else:
                taglist.append(str(row)+","+str(col))
            x=(ex0[row][col]+ex1[row][col])/2+3
            y=(ey0[row][col]+ey1[row][col])/2+3
            strn=event.char
            cellblock[row][col]=strn.upper()                       
            canvas.create_text(x, y, text=strn.upper(),font=("Arial",16,"bold"), tag=(str(row)+","+str(col)), fill="black")
            if(across_down=="across" and col+1<width and cellblock[row][col+1]!="." and cellblock[row][col+1]!=":"):
                col=col+1
            if(across_down=="down" and row+1<height and cellblock[row+1][col]!="." and cellblock[row+1][col]!=":"):
                row=row+1
            create_rect(row,col)

# makes cell to the left as the currently active cell and current mode to across           
def key_pressedL(event):
    global row,col,across_down
    if(is_multi==0 and across_down=="across"):
        if col-1>=0:
            c_col=col-1
            if cellblock[row][c_col]==".":
                while(cellblock[row][c_col]=="."):
                    if c_col-1<0:
                        break
                    else:
                        c_col=c_col-1
            if (cellblock[row][c_col]!="."):
                col=c_col
        create_rect(row,col)
    if(is_multi==0 and across_down=="down"):
        across_down="across"
        create_rect(row,col)
           
# makes cell to the right as the currently active cell and current mode to across  
def key_pressedR(event):
    global row,col,across_down
    if(is_multi==0 and across_down=="across"):
        if col+1<width:
            c_col=col+1
            if cellblock[row][c_col]==".":
                while(cellblock[row][c_col]=="."):
                    if c_col+1==width:
                        break
                    else:
                        c_col=c_col+1
            if (cellblock[row][c_col]!="."):
                col=c_col
        create_rect(row,col)
    if(is_multi==0 and across_down=="down"):
        across_down="across"
        create_rect(row,col)
                  
# makes cell upper to the highlighted cell as the currently active cell  and current mode to down
def key_pressedU(event):
    global row,col,across_down
    if(is_multi==0 and across_down=="down"):
        if row-1>=0:
            c_row=row-1
            if cellblock[c_row][col]==".":
                while(cellblock[c_row][col]=="."):
                    if c_row-1<0:
                        break
                    else:
                        c_row=c_row-1
            if (cellblock[c_row][col]!="."):
                row=c_row
        create_rect(row,col)
    if(is_multi==0 and across_down=="across"):
        across_down="down"
        create_rect(row,col)

# makes cell below the highlighted cell as the currently active cell  and current mode to down
def key_pressedD(event):
    global row,col,across_down
    if(is_multi==0 and across_down=="down"):
        if row+1<height:
            c_row=row+1
            if cellblock[c_row][col]==".":
                while(cellblock[c_row][col]=="."):
                    if c_row+1==height:
                        break
                    else:
                        c_row=c_row+1
            if (cellblock[c_row][col]!="."):
                row=c_row
        create_rect(row,col)
    if(is_multi==0 and across_down=="across"):
        across_down="down"
        create_rect(row,col)


# assigns rebus entry to the corresponding cellblock when 'enter' key is pressed
def key_pressedE(event):
    global row,col,across_down,taglist,multi,is_multi
    if(is_multi==1):
        if str(row)+","+str(col) in taglist:
            canvas.delete(str(row)+","+str(col))
            canvas.delete("temp_str"+str(row)+","+str(col))
        else:
            taglist.append(str(row)+","+str(col))
        canvas.delete("mults")
        canvas.delete("mult")
        x=(ex0[row][col]+ex1[row][col])/2+3
        y=(ey0[row][col]+ey1[row][col])/2+3
        cellblock[row][col]=''.join(multi)
        cellblock[row][col]=cellblock[row][col].upper()
        temp_text=cellblock[row][col]
        if(len(temp_text)==1):
            size=16
        else:
            size=10
        if(len(temp_text)>2):
            temp_text=temp_text[0:2]+".."
        canvas.create_text(x, y, text=temp_text,font=("Arial",size,"bold"), tag=(str(row)+","+str(col)), fill="black")
        del multi[:]
        is_multi=0
        listbox.config(state=NORMAL)
        listbox1.config(state=NORMAL)
        change_state("normal")

# deletes a letter from the cell when 'backspace' key is pressed        
def key_pressedB(event):
    global row,col,across_down,taglist,multi,is_multi
    if(is_multi==1 and len(multi)>0):         
        canvas.delete("mults")
        x=(ex0[row][col]+ex1[row][col])/2
        y=(ey0[row][col]+ey1[row][col])/2+10
        del multi[len(multi)-1]
        canvas.create_text(x, y, text=''.join(multi),font=("Arial",11),tag="mults", fill="black")
    else:
        if(cellblock[row][col] not in [".","-"]):
            canvas.delete(str(row)+","+str(col))
            canvas.delete("temp_str"+str(row)+","+str(col))
            temp_str.remove("temp_str"+str(row)+","+str(col))
            cellblock[row][col]="-"

# clears all the entries in the cells and temporary lists        
def clear_cells():
    global temp_str,taglist
    for element in taglist:
        canvas.delete(element)
    for element in temp_str:
        canvas.delete(element)
    del temp_str[:]
    del taglist[:]
    for i in range(0,height):
        for j in range(0,width):
            if cellblock[i][j]!=".":
                cellblock[i][j]="-"

# when a multiple entry has to be placed in a cell, can be exited only when 'enter' key is prressed.
def multiple_sol():
    global multi,is_multi
    canvas.focus_set()
    if (cellblock[row][col]!="." and is_multi==0):
        is_multi=1
        change_state("disabled")
        y0=(ey0[row][col]+ey1[row][col])/2
        x1=(ex1[row][col])+24
        canvas.create_rectangle(ex0[row][col],y0,x1,ey1[row][col],fill="white",tag="mult",outline="#0088B5")            
        if(cellblock[row][col]!='-'):
            for element in cellblock[row][col]:
                multi.append(element)
            x=(ex0[row][col]+ex1[row][col])/2+10
            y=(ey0[row][col]+ey1[row][col])/2+10
            canvas.create_text(x, y, text=cellblock[row][col],font=("Arial",10), tag="mults", fill="black")
        listbox.config(state=DISABLED)
        listbox1.config(state=DISABLED)

# finds current state of an across or down word, taking the starting row and column for that word as the input
def findcurracross(i,j):
    curstr=""
    while((j<width) and  (cellblock[i][j]!="." and cellblock[i][j]!=":")):
        curstr=curstr+cellblock[i][j]
        j=j+1
    return curstr

def findcurrdown(i,j):
    curstr=""
    while((i<height) and (cellblock[i][j]!="." and cellblock[i][j]!=":")):
        curstr=curstr+cellblock[i][j]
        i=i+1
    return curstr

# stores the value for the clue entered by the user in the corresponding cluelist
def textentered(event=0):
    ip=text.get("1.0",'end-1c')
    if(cur_bool==True and ip!=""):
        if(across_down=="across"):
            across[cur_clue][1]=ip
            listbox.delete(cur_clue)
            listbox.insert(cur_clue,("  "+str(across[cur_clue][0])+".  "+ip))
        if(across_down=="down"):
            down[cur_clue][1]=ip
            listbox1.delete(cur_clue)
            listbox1.insert(cur_clue,("  "+str(down[cur_clue][0])+".  "+ip))            
    else:
        if(ip==""):
            msg="Clue cannot be a null string"
        else:
            msg=across_down+" clue cannot be entered for this block"
        messagebox.showinfo("Sorry!", msg)
    canvas.focus_set()
    create_rect(row,col)


# stores the puzzle description in binary format       
def save_sol():
    global location
    location=StringVar()
    check_block=True
    check_acc_clue=True
    check_dwn_clue=True
    for i in range(0,acc):
        if(across[i][1]==""):
            check_acc_clue=False
            break
    for i in range(0,dwn):
        if(down[i][1]==""):
            check_dwn_clue=False
            break
    if(check_acc_clue==False):
        messagebox.showinfo("Sorry!", "Across cluelist has not been filled completely")
    if(check_dwn_clue==False):
        messagebox.showinfo("Sorry!", "Down cluelist has not been filled completely")
    if(check_acc_clue==True and check_dwn_clue==True):
        file_opt=opt = {}
        opt['filetypes'] = [('all files', '.*'), ('binary files', '.puz')]
        #options['initialfile'] = 'My_CW_File.puz'
        opt['parent'] = master
        fileloc = filedialog.asksaveasfilename(filetypes=opt['filetypes'])
        File.title=title
        File.author=author
        File.cpyrt=cpyrt
        File.notes=notes
        File.width=width
        File.height=height
        File.solnblock=cellblock
        File.acc=acc
        File.dwn=dwn
        File.across=across
        File.down=down
        File.loc=fileloc
        filewrite(File)
        master.destroy()
        sys.exit(0)


# stores the puzzle description as a text file
def save_txt():
    file_opt=opt = {}
    col_space=[]
    max_col=0
    Encoding_2 = "ISO-8859-1"
    opt['filetypes'] = [('all files', '.*'), ('text files', '.txt')]
    opt['parent'] = master
    fileloc = filedialog.asksaveasfilename(filetypes=opt['filetypes'])
    ofil=fileloc
    ofl=open(ofil,mode='wb')
    ofl.write(("\n  ").encode(Encoding_2))
    ofl.write(title.encode(Encoding_2))    
    for j in range (0,width):
        for i in range (0,height):
            if (len(cellblock[i][j])>max_col):
                max_col=len(cellblock[i][j])
        col_space.append(max_col)
        max_col=0
    ofl.write(("\n\n\n Current State of the puzzle:\n\n  ").encode(Encoding_2))        
    for i in range(0,height):
        ofl.write(("\n  ").encode(Encoding_2))
        ad_space=0
        for j in range(0,width):
            if(cellblock[i][j]!=":"):
                ofl.write(cellblock[i][j].encode(Encoding_2))
            else:
                ofl.write(".".encode(Encoding_2))                    
            ad_space=col_space[j]-len(cellblock[i][j])
            if ad_space>0:
                for k in range(0,ad_space):
                    ofl.write((" ").encode(Encoding_2))                                          
            ofl.write((" ").encode(Encoding_2))                
    ofl.write(("\n\n CLUES\n").encode(Encoding_2))
    ofl.write("\n Across :  \n".encode(Encoding_2))        
    for i in range(0,acc):
        ct=across[i][0]
        r=row_cellno[ct-1]
        c=col_cellno[ct-1]
        temp_st=findcurracross(r,c)
        if(across[i][1]!=""):
            temp=str(across[i][0])+". "+across[i][1]+" <"+temp_st+">"
        else:
            temp=str(across[i][0])+". Across <"+temp_st+">"            
        ofl.write(("\n  ").encode(Encoding_2))
        ofl.write(temp.encode(Encoding_2))
            
    ofl.write("\n\n Down :\n".encode(Encoding_2))    
    for i in range(0,dwn):
        ct=down[i][0]
        r=row_cellno[ct-1]
        c=col_cellno[ct-1]
        temp_st=findcurrdown(r,c)
        ofl.write(("\n  ").encode(Encoding_2))
        if(down[i][1]!=""):
            temp=str(down[i][0])+". "+down[i][1]+" <"+temp_st+">"
        else:
            temp=str(down[i][0])+". Down <"+temp_st+">" 
        ofl.write(temp.encode(Encoding_2))
    ofl.close()
        
# constructs the initial state for the crossword grid
def initUI(w,h,cb,across0,down0,xacross,xdown,cell,titl,aut):
    global master,MARGIN,SIDE,HEIGHT,WIDTH,row,col,n,height,width,title,author,cpyrt,notes,listbox,listbox1,first_row_col,canvas,is_multi,multi,across,down,row_cellno,col_cellno,cur_bool
    global cellno,cellblock,taglist,temp_str,temp_cellno,across_down,cur_clue,dull_clue,cur_clue_ad,dull_clue_ad,found_cur,found_dull,acc,dwn,filemenu,labelE,B,text,x,ex0,ex1,ey0,ey1
    cur_bool=False
    width=w
    height=h
    cellblock=cb
    title=titl
    author=aut
    cpyrt="WSJ Puzzles"
    notes=""
    master = Tk()
    master.title(title)
    for i in range(0,height):
        for j in range(0,width):
            if(cb[i][j]!="." and cb[i][j]!="-"):
                cellblock[i][j]="-"
    MARGIN=10
    screen_width = master.winfo_screenwidth()
    screen_height = master.winfo_screenheight()
    sw=int(screen_width/6)-30
    HEIGHT=screen_height-200
    SIDE=(HEIGHT - (MARGIN*2))/height
    WIDTH=MARGIN*2+SIDE*width
    fmB=Frame(master,width=WIDTH,height=200,bg="#D9DADA")
    fmB.pack(side=TOP, anchor=NW, fill=BOTH)
    labelE = Label(fmB,text="Enter your clue here:", font=("Arial",17), anchor=NW,bg="#D9DADA")
    labelE.pack(side=TOP,anchor=NW)
    text = Text(fmB,height=2,width=70)
    text.insert(INSERT, "")
    text.pack(side=LEFT,fill=X)
    fmB1=Frame(fmB,width=10,bg="#D9DADA")
    fmB1.pack(side=LEFT,fill=BOTH)
    B = Button(fmB, text ="Enter", command =textentered,bg="#D9DADA",highlightbackground="#D9DADA")
    B.pack(side=LEFT)
    listbox_width=screen_width-(WIDTH+30)
    fm2=Frame(master,width=WIDTH+30,height=HEIGHT+30,bg="#D9DADA")
    fm2.pack(side=LEFT, anchor=NW, fill=Y)
    # canvas for the crossword grid
    canvas= Canvas(fm2,width=WIDTH,height=HEIGHT,scrollregion=(0,0,WIDTH,HEIGHT),relief=RAISED,bg="white")
    canvas.config(highlightbackground="#D9DADA",highlightcolor="#D9DADA")
    canvas.create_rectangle(0, 0, WIDTH, 10,fill="#D9DADA",width=0)
    canvas.create_rectangle(0, 0, 10, HEIGHT,fill="#D9DADA",width=0)
    canvas.create_rectangle((WIDTH-MARGIN),0, WIDTH, HEIGHT,fill="#D9DADA",width=0)
    canvas.create_rectangle(0,(HEIGHT-MARGIN), WIDTH, HEIGHT,fill="#D9DADA",width=0)
    canvas.pack(side=LEFT)
    fm1=Frame(master,width=listbox_width,height=HEIGHT,relief=FLAT,bg="#D9DADA")
    fm1.pack(side=LEFT, anchor=NW, fill=BOTH,expand=TRUE)
    fmS=Frame(fm1,width=30,height=HEIGHT,bg="#D9DADA")
    fmS.pack(side=LEFT,anchor=NW)
    fm3=Frame(fm1,height=10,relief=FLAT,bg="#D9DADA")
    fm3.pack(side=TOP,anchor=NW, fill=Y)
    # Across clue list
    label = Label( fm1,text="Across",relief=GROOVE,font=("Arial",17), anchor=NW,bg="#F2F2F2") 
    label.pack(side=TOP,anchor=NW,fill=X)
    canvas1= Canvas(fm1,height=(HEIGHT-10)/2,relief=FLAT,bg="#D9DADA")
    canvas1.pack(side=TOP,anchor=NW, fill=BOTH,expand=TRUE)
    fmS1= Frame(fm1,width=10,height=10,relief=FLAT,bd=0,bg="#D9DADA")
    fmS1.pack(side=TOP,anchor=NW)
    # Down clue list
    labelD = Label(fm1,relief=GROOVE,text="Down", font=("Arial",17), anchor=NW,bg="#D9DADA")
    labelD.pack(side=TOP,anchor=NW,fill=X)
    canvas2= Canvas(fm1,height=(HEIGHT-10)/2,relief=FLAT,bg="#D9DADA")
    canvas2.pack(side=TOP,anchor=NW, fill=BOTH,expand=TRUE)
    across=[]
    down=[]
    acc,dwn=0,0
    cellno=[]
    row_cellno=[]
    col_cellno=[]
    taglist=[]
    temp_str=[]
    temp_cellno=[]
    first_row_col=True
    across_down="across"
    cur_clue=0
    dull_clue=0
    cur_clue_ad="across"
    dull_clue_ad="down"
    found_cur=0
    found_dull=0
# is_multi is set to 1 in order to input rebus entries for a cell; it can be turned off only after 'enter' key is pressed
    is_multi=0
    multi=[]
    count=1
    num=0
    ex0=[]
    ex1=[]
    ey1=[]
    ey0=[]
    for i in range(0,height):
        ex0.append([])
        ex1.append([])
        ey0.append([])
        ey1.append([])
        for j in range(0,width):
            ex0[i].append(0)
            ex1[i].append(0)
            ey0[i].append(0)
            ey1[i].append(0)
    # seperates across from down clues and finds cell no. associiated with each of these clues.
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
                    across.append([])
                    across[acc].append(count)
                    across[acc].append("")
                    acc=acc+1
                    count=count+1
            if i<height-1 and cellblock[i+1][j]!=".":       
                if (cellblock[i][j]!="." and (i==0 or cellblock[i-1][j]==".")):
                    down.append([])
                    if ((j<width-1 and cellblock[i][j+1]!=".")  and (j==0 or cellblock[i][j-1]==".")):
                        # if cell no. matches with across cell no., count won't be incremented.
                         down[dwn].append(count-1)
                    else:
                        down[dwn].append(count)
                        cellno[i][j]=count
                        count=count+1
                        row_cellno.append(i)
                        col_cellno.append(j)
                    down[dwn].append("")
                    dwn=dwn+1
            j=i+1
        i=i+1
        

    for i in range(0,acc):
        for j in range(0,len(across0)):
            if (across[i][0]==across0[j][0]):              
                across[i][1]=across0[j][1]
    for i in range(0,dwn):
        for j in range(0,len(down0)):
            if (down[i][0]==down0[j][0]):              
                down[i][1]=down0[j][1]
            
    # creates grid
    for i in range(0,(width+1)):
        color="black"
        x0 = MARGIN + i * SIDE
        y0 = MARGIN
        x1 = MARGIN + i * SIDE
        y1 = HEIGHT - MARGIN
        canvas.create_line(x0, y0, x1, y1, fill=color)
    for i in range(0,(height+1)):
        x0 = MARGIN          
        y0 = MARGIN + i * SIDE
        x1 = WIDTH - MARGIN
        y1 = MARGIN + i * SIDE
        canvas.create_line(x0, y0, x1, y1, fill=color)
    # x0,y0,x1 and y1 position for each cell in the canvas
    for row in range(height):
        c=0
        for col in range (width):
            if(row==0):
                len1=MARGIN+(col*SIDE)
                ex0[row][col]=len1
                ey0[row][col]=MARGIN
                len2=MARGIN+((col+1)*SIDE)
                ex1[row][col]=len2
                ey1[row][col]=MARGIN+SIDE
            else:
                ex0[row][col]=ex0[(row-1)][col]
                ey0[row][col]=ey0[(row-1)][col]+SIDE
                ex1[row][col]=ex1[(row-1)][col]
                ey1[row][col]=ey1[(row-1)][col]+SIDE
    x0=ex1[0][(width-1)]
    y0=ey0[0][(width-1)]
    x1=ex1[(height-1)][(width-1)]
    y1=ey1[(height-1)][(width-1)]
    canvas.create_line(x0, y0, x1, y1, fill=color)
    for i in range(0,height):
        for j in range(0,width):
            x=ex0[i][j]+5
            y=ey0[i][j]+5
            if(cellno[i][j]!=0):
                canvas.create_text(x, y, text=str(cellno[i][j]), font=("Times New Roman",9), fill="black")
                if(first_row_col):
                    row=i
                    col=j
                    if((j+1)<width and cellblock[i][j+1]!="."):
                        across_down="across"
                        cur_clue_ad="across"
                        dull_clue_ad="down"
                    else:
                        across_down="down"
                        cur_clue_ad="down"
                        dull_clue_ad="across"
                    first_row_col=False
            if cellblock[i][j]==".":
                canvas.create_rectangle(ex0[i][j], ey0[i][j], ex1[i][j], ey1[i][j],fill="black")
            if cellblock[i][j]!="-" and cellblock[i][j]!=".":
                    x=((ex0[i][j]+ex1[i][j])/2)+3
                    y=((ey0[i][j]+ey1[i][j])/2)+3
                    taglist.append(str(i)+","+str(j))
                    temp_text=cellblock[i][j]                 
                    canvas.create_text(x, y, text=temp_text, tag=(str(i)+","+str(j)), font=("Arial",16,"bold"), fill="black")

    # attaches scrollbars to across and down listboxes
    scrollbar = Scrollbar(canvas1)
    scrollbar.pack(side=RIGHT, fill=Y)
    listbox = Listbox(canvas1,selectbackground="gray",activestyle="none",selectforeground="red",exportselection=0,selectmode='SINGLE')
    listbox.pack(side=LEFT, fill=BOTH,expand=TRUE)
    for i in range(0,acc):
        if(across[i][1]!=""):
            listbox.insert(END,("  "+str(across[i][0])+".  "+across[i][1]))
        else:
            listbox.insert(END,("  "+str(across[i][0])+".  Across"))
        i=i+1
    listbox.config(yscrollcommand=scrollbar.set)
    scrollbar.config(command=listbox.yview)
    scrollbar1 = Scrollbar(canvas2)
    scrollbar1.pack(side=RIGHT, fill=Y)
    listbox1 = Listbox(canvas2,selectbackground="gray",activestyle="none",selectforeground="red",exportselection=0,selectmode='SINGLE')
    listbox1.pack(side=LEFT, fill=BOTH,expand=TRUE)
    for i in range(0,dwn):
        if(down[i][1]!=""):
            listbox1.insert(END,("  "+str(down[i][0])+".  "+down[i][1]))
        else:
            listbox1.insert(END,("  "+str(down[i][0])+".  Down"))
        i=i+1
    listbox1.config(yscrollcommand=scrollbar1.set)
    scrollbar1.config(command=listbox1.yview)
    # menubar
    menubar = Menu(master)
    filemenu = Menu(menubar, tearoff=0)
    filemenu.add_command(label="Create Puzzle", command=save_sol)   
    filemenu.add_command(label="Copy work to a text file", command=save_txt)
    filemenu.add_command(label="Clear Puzzle", command=clear_cells)
    menubar.add_cascade(label="File", menu=filemenu) 
    master.config(menu=menubar,background="#D9DADA")   
    text.bind("<Button-1>", canvas.focus())
    text.bind("<Key>", canvas.focus())
    # binds events to the corresponding methods
    listbox.bind("<<ListboxSelect>>", box_clickedA)
    listbox1.bind("<<ListboxSelect>>", box_clickedD)
    canvas.bind("<Button-1>", cell_clicked)
    canvas.bind("<Key>", key_pressed)
    listbox.bind("<Key>", key_pressed)
    listbox1.bind("<Key>", key_pressed)
    canvas.bind("<Left>", key_pressedL)
    listbox.bind("<Left>", key_pressedL)
    listbox1.bind("<Left>", key_pressedL)
    canvas.bind("<Right>", key_pressedR)
    listbox.bind("<Right>", key_pressedR)
    listbox1.bind("<Right>", key_pressedR)
    canvas.bind("<Up>", key_pressedU)
    listbox.bind("<Up>", key_pressedU)
    listbox1.bind("<Up>", key_pressedU)
    canvas.bind("<BackSpace>",key_pressedB)
    listbox.bind("<BackSpace>", key_pressedB)
    listbox1.bind("<BackSpace>", key_pressedB)
    canvas.bind("<Return>",key_pressedE)
    text.bind("<Return>", textentered)
    listbox.bind("<Return>", key_pressedE)
    listbox1.bind("<Return>", key_pressedE)
    canvas.bind("<Down>",key_pressedD)
    listbox.bind("<Down>", key_pressedD)
    listbox1.bind("<Down>", key_pressedD)    
    row,col=0,0
    canvas.focus_set()
    create_rect(row,col)
    master.mainloop()



