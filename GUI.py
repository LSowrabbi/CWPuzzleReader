#assigning clues and reveal solutions
from tkinter import *
from GUI_Helper import *
from tkinter.messagebox import *
master = Tk()
# quits program if given checksum does not match the calculated checksum
if(valid_cksum==False):
    master.withdraw()
    messagebox.showinfo("Sorry!", "File corrupted")
    sys.exit(0)

MARGIN=10
cells=height
screen_width = master.winfo_screenwidth()
screen_height = master.winfo_screenheight()
sw=int(screen_width/6)-30
HEIGHT=screen_height-200
SIDE=(HEIGHT - (MARGIN*2))/height
WIDTH=MARGIN*2+SIDE*width
fmM=Frame(master,width=800,height=250,bg="#D9DADA")
fmM.pack(side=TOP, anchor=NW, fill=BOTH,expand=TRUE)
fmB=Frame(fmM,height=150,bg="#D9DADA",width=sw)
fmB.pack(side=TOP, anchor=NW, fill=NONE)
fmB1=Frame(fmM,height=20)
fmB1.pack(side=TOP, anchor=NW, fill=BOTH,expand=TRUE)
row,col,n=0,0,0
listbox_width=screen_width-(WIDTH+30)
fm2=Frame(master,width=WIDTH+30,height=HEIGHT+30,bg="#D9DADA")
fm2.pack(side=LEFT, anchor=NW, fill=Y)
sec=time

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
elements=[]
ex0=[]
ey0=[]
ex1=[]
ey1=[]
taglist=[]
temp_str=[]
temp_cellno=[]
temp_circ=[]
temp_valid=[]
prevx0,prevy0,prevx1,prevy1=0,0,0,0
first_row_col=True
across_down="across"
a=0
cur_clue=0
dull_clue=0
cur_clue_ad="across"
dull_clue_ad="down"
found_cur=0
found_dull=0
# is_multi is set to 1 in order to input rebus entries for a cell; it can be turned off only after 'enter' key is pressed
is_multi=0
multi=[]
class UI():
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
    
    # finds solution for an across or down word, taking the starting row and column for that word as the input
    def findsolacross(i,j):
        curstr=""
        while((j<width) and  (cellblock[i][j]!="." and cellblock[i][j]!=":")):
            curstr=curstr+solnblock[i][j]
            j=j+1
        return curstr

    def findsoldown(i,j):
        curstr=""
        while((i<height) and (cellblock[i][j]!="." and cellblock[i][j]!=":")):
            curstr=curstr+solnblock[i][j]
            i=i+1
        return curstr
        
    # creates temporary text for highlighted cells
    def create_txt(row,col):
        global temp_str
        if cellblock[row][col]!="-" and (cellblock[row][col]!="." and cellblock[row][col]!=":"):
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
                if(pencil[row][col]==1):
                   canvas.create_text(x, y, text=temp_text.upper(),font=("Arial",size,"bold"), tag=("temp_str"+str(row)+","+str(col)), fill="#4D4D4D")
                else:
                   canvas.create_text(x, y, text=temp_text,font=("Arial",size,"bold"), tag=("temp_str"+str(row)+","+str(col)), fill="black" )

   # creates temporary cellno,if any, for highlighted cells
    def create_cellno(row,col):
        global temp_cellno
        if(cellno[row][col]!=0):
                x=ex0[row][col]+5
                y=ey0[row][col]+5
                temp_cellno.append(("temp_cell"+str(row)+","+str(col)))
                canvas.create_text(x, y, text=str(cellno[row][col]),tag=("temp_cell"+str(row)+","+str(col)),font=("Times New Roman",9), fill="black")
    
    # creates temporary circle ,if any, for highlighted cells            
    def create_cir(i,j):
        global temp_circ
        canvas.create_oval(ex0[i][j], ey0[i][j], ex1[i][j], ey1[i][j],tag=("temp_circ"+str(i)+","+str(j)),outline="#333333")
        temp_circ.append(("temp_circ"+str(i)+","+str(j)))

    # creates temporary validity entries, if any, for highlighted cells     
    def create_pol(i,j,value):
        global temp_valid
        temp_valid.append("temp_valid"+str(i)+","+str(j))
        if value==1:
            canvas.create_polygon(ex1[i][j]-8,ey0[i][j],ex1[i][j],ey0[i][j],ex1[i][j],ey0[i][j]+8,tag=("temp_valid"+str(i)+","+str(j)),fill="black")
        if value==2:
            canvas.create_line(ex0[i][j],ey0[i][j],ex1[i][j],ey1[i][j],fill="#4D4D4D",tag=("temp_valid"+str(i)+","+str(j)),width=0.1)
            canvas.create_line(ex1[i][j],ey0[i][j],ex0[i][j],ey1[i][j],fill="#4D4D4D",tag=("temp_valid"+str(i)+","+str(j)),width=1) 
        if value==3:
            canvas.create_polygon(ex1[i][j]-8,ey0[i][j]+1,ex1[i][j],ey0[i][j]+1,ex1[i][j],ey0[i][j]+8,tag=("temp_valid"+str(i)+","+str(j)),fill="red")

    def highlightclue(c_row,c_col):
        # if across_down = "Across" then dull clue = down and cur_clue = across, else vice versa
        d_col=c_col
        disp_clue=""
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
        while(c_col!=0 and (cellblock[c_row][c_col]!='.' and cellblock[c_row][c_col]!=':')):
            c_col=c_col-1
        if(cellblock[c_row][c_col]=='.' or cellblock[c_row][c_col]==':'):
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
        while(c_row!=0 and (cellblock[c_row][d_col]!='.' and cellblock[c_row][d_col]!=':')):
            c_row=c_row-1
        if(cellblock[c_row][d_col]=='.' or cellblock[c_row][d_col]==':'):
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
        UI.labelc.config(text=disp_clue)

                
    def create_rect(c_row,c_col):
        # highlights word corresponding to the currently active row and col
         global temp_str,taglist
         # deletes previously highlighted circles,cell nos,entries showing validity and texts.
         canvas.delete("cursor")
         for element in temp_str:
             canvas.delete(element)
         del temp_str[:]
         for element in temp_cellno:
             canvas.delete(element)
         del temp_cellno[:]
         for element in temp_circ:
             canvas.delete(element)
         del temp_circ[:]
         for element in temp_valid:
             canvas.delete(element)
         del temp_valid[:]
         # highlights cell of the clicked letter to red
         if cellblock[c_row][c_col]!="." and cellblock[c_row][c_col]!=":":
            canvas.create_rectangle(ex0[c_row][c_col],ey0[c_row][c_col], ex1[c_row][c_col], ey1[c_row][c_col],fill="red", tags=("cursor"))
            UI.highlightclue(c_row,c_col)
            # creates temporary entries for the highlighted cell
            UI.create_txt(c_row,c_col)      
            if(cellno[c_row][c_col]!=0):
                UI.create_cellno(c_row,c_col)
            if(gext[c_row][c_col] in [5,9,10,11,12,13,14,15]):
               UI.create_cir(c_row,c_col)
            if(valid[c_row][c_col]!=0):
               UI.create_pol(c_row,c_col,valid[c_row][c_col])
            row=c_row
            col=c_col
           # highlights and creates temporary entires for the cells to the left/up, that form the word along with the letter in the highlighted cell
            if (across_down=="down"):
                row=c_row-1
            else:
                col=c_col-1
            if(row >=0 and col >=0):
                while(cellblock[row][col]!="." and cellblock[row][col]!=":"):
                    canvas.create_rectangle(ex0[row][col], ey0[row][col], ex1[row][col], ey1[row][col],fill="#A6A6A6", tags=("cursor"))
                    UI.create_txt(row,col)
                    if(gext[row][col] in [5,9,10,11,12,13,14,15]):
                        UI.create_cir(row,col)
                    if(valid[row][col]!=0):
                        UI.create_pol(row,col,valid[row][col])
                    if(cellno[row][col]!=0):
                        UI.create_cellno(row,col)
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
            if(row <cells and col <width):
                while(cellblock[row][col]!="." and cellblock[row][col]!=":"):
                    canvas.create_rectangle(ex0[row][col], ey0[row][col], ex1[row][col], ey1[row][col],fill="#A6A6A6", tags=("cursor"))
                    UI.create_txt(row,col)
                    if(gext[row][col] in [5,9,10,11,12,13,14,15]):
                        UI.create_cir(row,col)
                    if(valid[row][col]!=0):
                        UI.create_pol(row,col,valid[row][col])
                    if(cellno[row][col]!=0):
                        UI.create_cellno(row,col)
                    if across_down=="down":
                        row=row+1
                    else:
                        col=col+1
                    if (row == cells or col==width):
                        break

        

    def cell_clicked(event):
            # changes the focus word to the corresponding mouse click position
             global row,col,n,cells,across_down,temp_str,taglist,temp_str     
             x, y = event.x, event.y
             if(is_multi==0):
                 if (MARGIN < x < WIDTH - MARGIN and MARGIN < y < HEIGHT - MARGIN):
                    canvas.focus_set()
                    # get row and col numbers from x,y coordinates
                    c_row, c_col = int((y - MARGIN) / SIDE), int((x - MARGIN) / SIDE)
                    if c_row >= 0 and c_col >= 0:
                       if cellblock[c_row][c_col]!="." and cellblock[c_row][c_col]!=":":
                           row,col=c_row,c_col
                           UI.create_rect(row,col)

    def list_clicked(no_clicked):
             # highlights  word associated with the clue selected
             global row,col,n,cells,row_cellno,col_cellno,temp_str
             if(is_multi==0):
                 row=row_cellno[no_clicked-1]
                 col=col_cellno[no_clicked-1]
                 UI.create_rect(row,col)

    # changes state of the entries in the menubar
    def change_state(c_state):
        if(c_state=="disabled"):
            UI.solnmenu.entryconfig(0,state=c_state)
            UI.solnmenu.entryconfig(1,state=c_state)
            UI.solnmenu.entryconfig(3,state=c_state)
        else:
            UI.solnmenu.entryconfig(0,state=check_reveal_state)
            UI.solnmenu.entryconfig(1,state=check_reveal_state)
            UI.solnmenu.entryconfig(3,state=unlock_state)
        UI.filemenu.entryconfig(0,state=c_state)
        UI.filemenu.entryconfig(1,state=c_state)
        UI.filemenu.entryconfig(2,state=c_state)            
        UI.filemenu.entryconfig(3,state=c_state) 
        UI.filemenu.entryconfig(4,state=c_state) 
        UI.viewmenu.entryconfig(0,state=c_state)
        return
    
    # displays dialog box if entire grid is filled with correct entries              
    def is_sol_complete():
        for i in range(0,height):
            for j in range(0,width):
                if(cellblock[i][j]=="-"):
                    return       
                if(cellblock[i][j]!="." and cellblock[i][j]!=":" and valid[i][j]!=3):
                    if((is_puz_rebus==True) and (str(i)+","+str(j) in rebus_row_col)):
                        rebus_index=rebus_row_col.index(str(i)+","+str(j))
                        temp_text=rebus_content[rebus_index]
                    else:
                        temp_text=solnblock[i][j]
                    if(cellblock[i][j]!=temp_text):
                        return           
        messagebox.showinfo("Congratulations!", "You have successfully completed the puzzle") 
              
    def key_pressed(event):         
            # associates character key pressed to the currently active cell in the grid
            global row,col,across_down,taglist,temp_str,is_multi,multi,is_pencil,pencil,valid,temp_valid
            if(is_multi==1):
                # for rebus entries
                if(len(multi)<8):
                    if event.keysym in 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz' and cellblock[row][col]!="." and cellblock[row][col]!=":":
                        canvas.delete("mults")
                        x=(ex0[row][col]+ex1[row][col])/2+10
                        y=(ey0[row][col]+ey1[row][col])/2+10
                        strn=event.char
                        multi.append(strn)
                        canvas.create_text(x, y, text=''.join(multi),font=("Arial",10),tag="mults", fill="black")
            else:
                if row>=0 and col>=0 and event.keysym in 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz' and cellblock[row][col]!="." and cellblock[row][col]!=":":
                    # proceeds if solution hasen't been revealed yet
                    if(valid[row][col]!=3):
                       prev_str=cellblock[row][col]
                       if str(row)+","+str(col) in taglist:
                           canvas.delete(str(row)+","+str(col))
                           canvas.delete("temp_str"+str(row)+","+str(col))
                       else:
                           taglist.append(str(row)+","+str(col))
                       x=(ex0[row][col]+ex1[row][col])/2+3
                       y=(ey0[row][col]+ey1[row][col])/2+3
                       strn=event.char
                       cellblock[row][col]=strn.upper()                       
                       if(is_pencil.get()==1):
                         pencil[row][col]=1
                         canvas.create_text(x, y, text=strn.upper(),font=("Arial",16,"bold"), tag=(str(row)+","+str(col)), fill="#4D4D4D")
                       else:
                         pencil[row][col]=0
                         canvas.create_text(x, y, text=strn.upper(),font=("Arial",16,"bold"), tag=(str(row)+","+str(col)), fill="black")
                       if(valid[row][col]==2):
                           canvas.delete("temp_valid"+str(row)+","+str(col))
                           canvas.delete("valid"+str(row)+","+str(col))
                           if("temp_valid"+str(row)+","+str(col) in temp_valid):
                              temp_valid.remove("temp_valid"+str(row)+","+str(col))
                           canvas.create_polygon(ex1[row][col]-8,ey0[row][col]+1,ex1[row][col],ey0[row][col]+1,ex1[row][col],ey0[row][col]+8,tag=("valid"+str(row)+","+str(col)),fill="black")
                           valid[row][col]=1
                       if(prev_str!=cellblock[row][col]):
                           UI.is_sol_complete()
                    if(across_down=="across" and col+1<width and cellblock[row][col+1]!="." and cellblock[row][col+1]!=":"):
                        col=col+1
                    if(across_down=="down" and row+1<cells and cellblock[row+1][col]!="." and cellblock[row+1][col]!=":"):
                        row=row+1
                    UI.create_rect(row,col)

                        

    # makes cell to the left as the currently active cell and current mode to across           
    def key_pressedL(event):
       global row,col,across_down,taglist
       if(is_multi==0 and across_down=="across"):
           if col-1>=0:
               c_col=col-1
               if cellblock[row][c_col]=="." or cellblock[row][c_col]==":":
                   while(cellblock[row][c_col]=="." or cellblock[row][c_col]==":"):
                       if c_col-1<0:
                           break
                       else:
                           c_col=c_col-1
               if (cellblock[row][c_col]!="." and cellblock[row][c_col]!=":"):
                        col=c_col
           UI.create_rect(row,col)
       if(is_multi==0 and across_down=="down"):
           across_down="across"
           UI.create_rect(row,col)
           
    # makes cell to the right as the currently active cell and current mode to across  
    def key_pressedR(event):
        global row,col,across_down,taglist
        if(is_multi==0 and across_down=="across"):
            if col+1<width:
                c_col=col+1
                if cellblock[row][c_col]=="." or cellblock[row][c_col]==":":
                    while(cellblock[row][c_col]=="." or cellblock[row][c_col]==":"):
                        if c_col+1==width:
                            break
                        else:
                            c_col=c_col+1
                if (cellblock[row][c_col]!="." and cellblock[row][c_col]!=":"):
                    col=c_col
            UI.create_rect(row,col)
        if(is_multi==0 and across_down=="down"):
           across_down="across"
           UI.create_rect(row,col)
           
    # makes cell upper to the highlighted cell as the currently active cell  and current mode to down
    def key_pressedU(event):
        global row,col,across_down,taglist
        if(is_multi==0 and across_down=="down"):
            if row-1>=0:
                c_row=row-1
                if cellblock[c_row][col]=="." or cellblock[c_row][col]==":":
                    while(cellblock[c_row][col]=="." or cellblock[c_row][col]==":"):
                        if c_row-1<0:
                            break
                        else:
                            c_row=c_row-1
                if (cellblock[c_row][col]!="." and cellblock[c_row][col]!=":"):
                    row=c_row
            UI.create_rect(row,col)
        if(is_multi==0 and across_down=="across"):
           across_down="down"
           UI.create_rect(row,col)

    # makes cell below the highlighted cell as the currently active cell  and current mode to down
    def key_pressedD(event):
        global row,col,across_down,taglist
        if(is_multi==0 and across_down=="down"):
            if row+1<cells:
                c_row=row+1
                if cellblock[c_row][col]=="." or cellblock[c_row][col]==":":
                    while(cellblock[c_row][col]=="." or cellblock[c_row][col]==":"):
                        if c_row+1==cells:
                            break
                        else:
                            c_row=c_row+1
                if (cellblock[c_row][col]!="." and cellblock[c_row][col]!=":"):
                    row=c_row
            UI.create_rect(row,col)
        if(is_multi==0 and across_down=="across"):
           across_down="down"
           UI.create_rect(row,col)

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
           if(is_pencil.get()==1):
               pencil[row][col]=1   
               canvas.create_text(x, y, text=temp_text,font=("Arial",size,"bold"), tag=(str(row)+","+str(col)), fill="#4D4D4D")
           else:
               pencil[row][col]=0
               canvas.create_text(x, y, text=temp_text,font=("Arial",size,"bold"), tag=(str(row)+","+str(col)), fill="black")
           del multi[:]
           is_multi=0
           listbox.config(state=NORMAL)
           listbox1.config(state=NORMAL)
           UI.change_state("normal")
           if(valid[row][col]==2):
               canvas.delete("temp_valid"+str(row)+","+str(col))
               canvas.delete("valid"+str(row)+","+str(col))
               temp_valid.remove("temp_valid"+str(row)+","+str(col))
               canvas.create_polygon(ex1[row][col]-8,ey0[row][col]+1,ex1[row][col],ey0[row][col]+1,ex1[row][col],ey0[row][col]+8,tag=("valid"+str(row)+","+str(col)),fill="black")
               valid[row][col]=1
               UI.create_rect(row,col)
           UI.is_sol_complete()
        
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
           if(cellblock[row][col] not in [":",".","-"] and valid[row][col]!=3):
              canvas.delete(str(row)+","+str(col))
              canvas.delete("temp_str"+str(row)+","+str(col))
              temp_str.remove("temp_str"+str(row)+","+str(col))
              cellblock[row][col]="-"
           if(valid[row][col]==2):
               canvas.delete("temp_valid"+str(row)+","+str(col))
               canvas.delete("valid"+str(row)+","+str(col))
               temp_valid.remove("temp_valid"+str(row)+","+str(col))
               canvas.create_polygon(ex1[row][col]-8,ey0[row][col]+1,ex1[row][col],ey0[row][col]+1,ex1[row][col],ey0[row][col]+8,tag=("valid"+str(row)+","+str(col)),fill="black")
               valid[row][col]=1
               UI.create_rect(row,col)
    
    # clears all the entries in the cells and temporary lists        
    def clear_cells():
            global temp_str
            if(is_multi==0):
                global taglist
                for element in taglist:
                    canvas.delete(element)
                for element in temp_str:
                    canvas.delete(element)
                for element in temp_valid:
                    canvas.delete(element)
                del temp_valid[:]
                del temp_str[:]
                del taglist[:]
                for i in range(0,cells):
                    for j in range(0,width):
                        canvas.delete("valid"+str(i)+","+str(j))
                        valid[i][j]=0
                        pencil[i][j]=0
                        if cellblock[i][j]!="." and cellblock[i][j]!=":":
                            cellblock[i][j]="-"
 
    # checks the letter in the given row and column of grid with the corresponding letter in the solution                        
    def check(c_row,c_col):
        global valid,row,col
        valid_count=True
        if(cellblock[c_row][c_col]!="." and cellblock[c_row][c_col]!=":" and valid[c_row][c_col]!=3 and is_multi==0):
           if((is_puz_rebus==True) and (str(c_row)+","+str(c_col) in rebus_row_col)):
              rebus_index=rebus_row_col.index(str(c_row)+","+str(c_col))
              temp_text=rebus_content[rebus_index]
           else:
              temp_text=solnblock[c_row][c_col]
           if(cellblock[c_row][c_col]==temp_text or cellblock[c_row][c_col]=="-"):  
              valid_count=True
           else:
              valid_count=False
              if(valid[c_row][c_col]==1):
                 canvas.delete("temp_valid"+str(c_row)+","+str(c_col))
                 canvas.delete("valid"+str(c_row)+","+str(c_col))
                 if("temp_valid"+str(row)+","+str(col) in temp_valid):
                    temp_valid.remove("temp_valid"+str(c_row)+","+str(c_col))             
              canvas.create_line(ex0[c_row][c_col],ey0[c_row][c_col],ex1[c_row][c_col],ey1[c_row][c_col],fill="#4D4D4D",tag=("valid"+str(c_row)+","+str(c_col)),width=0.1)
              canvas.create_line(ex1[c_row][c_col],ey0[c_row][c_col],ex0[c_row][c_col],ey1[c_row][c_col],fill="#4D4D4D",tag=("valid"+str(c_row)+","+str(c_col)),width=1)
              valid[c_row][c_col]=2                   
        return valid_count            
     
    # checks all the letters in the grid         
    def check_all():
          ck_val=True
          for i in range(0,cells):
             for j in range(0,width):
                #print(str(i)+str(j))
                val=UI.check(i,j)
                ck_val=ck_val and val
                j=j+1
             i=i+1
          if(ck_val==True):
             messagebox.showinfo("", "No incorrect letters found!!")
    
    # checks for the currently highlighted letter    
    def check_one():
        v=UI.check(row,col)
        if(v==True and is_multi==0):
           messagebox.showinfo("", "No incorrect letters found!!")
           
    # checks all the letters in the highlighted word
    def check_word():
        global across_down
        i=row
        j=col
        ck_val=True
        if cellblock[row][col]!="." and cellblock[row][col]!=":" and is_multi==0:       
            val=UI.check(row,col)
            ck_val=ck_val and val
            if (across_down=="down"):
                i=row-1
            else:
                j=col-1
            if(i >=0 and j >=0):
                while(cellblock[i][j]!="." and cellblock[i][j]!=":"):
                    val=UI.check(i,j)
                    ck_val=ck_val and val
                    if across_down=="down":
                        i=i-1
                    else:
                        j=j-1
                    if (i <0 or j<0):
                        break
            if (across_down=="down"):
                i=row+1
            else:
                j=col+1
            if(i <cells and j <width):
                while(cellblock[i][j]!="." and cellblock[i][j]!=":"):
                    val=UI.check(i,j)
                    ck_val=ck_val and val
                    if across_down=="down":
                        i=i+1
                    else:
                        j=j+1
                    if (i == cells or j==width):
                        break
            if(ck_val==True):
               messagebox.showinfo("", "No incorrect letters found!!")        
             

    # when any clue in  across list box is clicked :
    def box_clickedA(event):
        global across_down
        if(is_multi==0):
            across_down="across"
            firstIndex = listbox.curselection()[0]
            UI.list_clicked(across[firstIndex][0])

    # when any clue in the down list box is clicked :      
    def box_clickedD(event):
        global across_down
        if(is_multi==0):
            across_down="down"
            firstIndex = listbox1.curselection()[0]
            UI.list_clicked(down[firstIndex][0])

    # reveals the solution for the given row and column of grid        
    def reveal_letter(i,j):
           global valid
           correct_entry=False
           if((is_puz_rebus==True) and (str(i)+","+str(j) in rebus_row_col)):
               rebus_index=rebus_row_col.index(str(i)+","+str(j))
               correct_entry=(rebus_content[rebus_index]==cellblock[i][j])
           else:
               correct_entry=(solnblock[i][j]==cellblock[i][j])
           if(not(correct_entry)):
              canvas.delete("temp_str"+str(i)+","+str(j))
              if "temp_str"+str(i)+","+str(j) in temp_str:
                  temp_str.remove("temp_str"+str(i)+","+str(j))
              if (str(i)+","+str(j)) in taglist:
                 canvas.delete(str(i)+","+str(j))
              else:
                 taglist.append(str(i)+","+str(j))
              x=((ex0[i][j]+ex1[i][j])/2)+3
              y=((ey0[i][j]+ey1[i][j])/2)+3
              if solnblock[i][j]!="." and solnblock[i][j]!=":":
                 pencil[i][j]=0
                 if(valid[i][j]!=0):
                    canvas.delete("temp_valid"+str(i)+","+str(j))
                    canvas.delete("valid"+str(i)+","+str(j))
                 canvas.create_polygon(ex1[i][j]-8,ey0[i][j]+1,ex1[i][j],ey0[i][j]+1,ex1[i][j],ey0[i][j]+8,tag=("valid"+str(i)+","+str(j)),fill="red")
                 valid[i][j]=3
                 if((is_puz_rebus==True) and (str(i)+","+str(j) in rebus_row_col)):
                    rebus_index=rebus_row_col.index(str(i)+","+str(j))
                    temp_text=rebus_content[rebus_index]
                    if(len(temp_text)>2):
                       temp_text=temp_text[0:2]+".."
                       size=11
                    canvas.create_text(x, y, text=temp_text, tag=(str(i)+","+str(j)), font=("Arial",11,"bold"), fill="black")
                    cellblock[i][j]=rebus_content[rebus_index]
                 else:
                    canvas.create_text(x, y, text=solnblock[i][j], tag=(str(i)+","+str(j)), font=("Arial",16,"bold"), fill="black")
                    cellblock[i][j]=solnblock[i][j]

    # reveals the currently highlighted letter in the grid   
    def reveal_one():
        UI.reveal_letter(row,col)
        UI.is_sol_complete()

    # reveals the complete solution  
    def reveal_sol():
        for i in range(0,cells):
            for j in range(0,width):
                UI.reveal_letter(i,j)
        UI.is_sol_complete()

    # reveals solution for incorrect entries 
    def reveal_incorrect():
        for i in range(0,cells):
            for j in range(0,width):
                if cellblock[i][j]!="-" and (cellblock[i][j]!="." and cellblock[i][j]!=":"):
                    UI.reveal_letter(i,j)
        UI.is_sol_complete()
        
    # reveals solution for all the cells in the highlighted word                           
    def reveal_word():
        global across_down
        i=row
        j=col
        if cellblock[row][col]!="." and cellblock[row][col]!=":":       
            UI.reveal_letter(row,col)
            if (across_down=="down"):
                i=row-1
            else:
                j=col-1
            if(i >=0 and j >=0):
                while(cellblock[i][j]!="." and cellblock[i][j]!=":"):
                    UI.reveal_letter(i,j)
                    if across_down=="down":
                        i=i-1
                    else:
                        j=j-1
                    if (i <0 or j<0):
                        break
            if (across_down=="down"):
                i=row+1
            else:
                j=col+1
            if(i <cells and j <width):
                while(cellblock[i][j]!="." and cellblock[i][j]!=":"):
                    UI.reveal_letter(i,j)
                    if across_down=="down":
                        i=i+1
                    else:
                        j=j+1
                    if (i == cells or j==width):
                        break
        UI.is_sol_complete()
        
    # when a multiple entry has to be placed in a cell, can be exited only when 'enter' key is prressed.
    def multiple_sol():
        global multi,is_multi
        if (cellblock[row][col]!="." and cellblock[row][col]!=":" and is_multi==0 and valid[row][col]!=3):
            is_multi=1
            UI.change_state("disabled")
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


    # displays notes, if any, that comes along with the puzzle
    def show_notes():
       global notes
       txt=notes.decode(Encoding_2)
       messagebox.showinfo("Notes", txt)

    # can be used to start or stop the timer
    def time_modify(self):
        global time_state
        if(is_multi==0):
            if(time_state==1):           
                time_state=0
                UI.labelt.config(foreground="green")
                UI.update_clock()
            else:
                time_state=1        
                UI.labelt.config(foreground="red")

    # constructs the initial state for the crossword grid
    def initUI():
            global row,col,n,cells,width,title,Encoding_2,listbox,listbox1,first_row_col,is_pencil,cur_clue_ad,dull_clue_ad
            master.title(title.decode(Encoding_2))
            is_pencil=IntVar()
            # creates grid
            for i in range(0,(width+1)):
                color="black"
                x0 = MARGIN + i * SIDE
                y0 = MARGIN
                x1 = MARGIN + i * SIDE
                y1 = HEIGHT - MARGIN
                canvas.create_line(x0, y0, x1, y1, fill=color)
            for i in range(0,(cells+1)):
                x0 = MARGIN
                y0 = MARGIN + i * SIDE
                x1 = WIDTH - MARGIN
                y1 = MARGIN + i * SIDE
                canvas.create_line(x0, y0, x1, y1, fill=color)
            # x0,y0,x1 and y1 position for each cell in the canvas
            for row in range(cells):
                c=0
                ex0.append([])
                ex1.append([])
                ey0.append([])
                ey1.append([])
                for col in range (width):
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
            x0=ex1[0][(width-1)]
            y0=ey0[0][(width-1)]
            x1=ex1[(cells-1)][(width-1)]
            y1=ey1[(cells-1)][(width-1)]
            canvas.create_line(x0, y0, x1, y1, fill=color)
            for i in range(0,cells):
                for j in range(0,width):
                    x=ex0[i][j]+5
                    y=ey0[i][j]+5
                    if(cellno[i][j]!=0):
                        canvas.create_text(x, y, text=str(cellno[i][j]), font=("Times New Roman",9), fill="black")
                        if(first_row_col):
                             row=i
                             col=j
                             if((j+1<width) and cellblock[i][j+1]!="." and cellblock[i][j+1]!=":"):
                                 across_down="across"
                                 cur_clue_ad="across"
                                 dull_clue_ad="down"
                             else:
                                 across_down="down"
                                 cur_clue_ad="down"
                                 dull_clue_ad="across"
                             first_row_col=False
                    if cellblock[i][j]=="." or cellblock[i][j]==":":
                        canvas.create_rectangle(ex0[i][j], ey0[i][j], ex1[i][j], ey1[i][j],fill="black")
                    # circled cells
                    if(gext[i][j] in [5,9,10,11,12,13,14,15]):
                        canvas.create_oval(ex0[i][j], ey0[i][j], ex1[i][j], ey1[i][j],outline="#333333")                      
                    x=((ex0[i][j]+ex1[i][j])/2)+3
                    y=((ey0[i][j]+ey1[i][j])/2)+3
                    if cellblock[i][j]!="-" and (cellblock[i][j]!="." and cellblock[i][j]!=":"):
                        taglist.append(str(i)+","+str(j))
                        temp_text=cellblock[i][j]
                        # rebus cells
                        if(len(temp_text)>2):
                           temp_text=temp_text[0:2]+".."
                        # pencil entry
                        if(gext[i][j] in [1,6,7,8,9,13,14,15] or cellblock[i][j] in 'abcdefghijklmnopqrstuvwxyz'):
                           pencil[i][j]=1
                           cellblock[i][j]=cellblock[i][j].upper()
                           canvas.create_text(x, y, text=temp_text.upper(), tag=(str(i)+","+str(j)), font=("Arial",16,"bold"), fill="#4D4D4D")
                        else:
                           canvas.create_text(x, y, text=temp_text, tag=(str(i)+","+str(j)), font=("Arial",16,"bold"), fill="black")
                    if (valid[i][j]!=0):
                        if valid[i][j]==1:
                           canvas.create_polygon(ex1[i][j]-8,ey0[i][j],ex1[i][j],ey0[i][j],ex1[i][j],ey0[i][j]+8,tag=("valid"+str(i)+","+str(j)),fill="black")
                        if valid[i][j]==2:
                           canvas.create_line(ex0[i][j],ey0[i][j],ex1[i][j],ey1[i][j],fill="#4D4D4D",tag=("valid"+str(i)+","+str(j)),width=0.1)
                           canvas.create_line(ex1[i][j],ey0[i][j],ex0[i][j],ey1[i][j],fill="#4D4D4D",tag=("valid"+str(i)+","+str(j)),width=1) 
                        if valid[i][j]==3:
                           canvas.create_polygon(ex1[i][j]-8,ey0[i][j]+1,ex1[i][j],ey0[i][j]+1,ex1[i][j],ey0[i][j]+8,tag=("valid"+str(i)+","+str(j)),fill="red")                           


            # attaches scrollbars to across and down listboxes
            scrollbar = Scrollbar(canvas1)
            scrollbar.pack(side=RIGHT, fill=Y)
            listbox = Listbox(canvas1,selectbackground="gray",activestyle="none",selectforeground="red",exportselection=0,selectmode='SINGLE')
            listbox.pack(side=LEFT, fill=BOTH,expand=TRUE)
            for i in range(0,acc):
                listbox.insert(END,("  "+str(across[i][0])+".  "+str(across[i][1])))
                i=i+1
            listbox.config(yscrollcommand=scrollbar.set)
            scrollbar.config(command=listbox.yview)
            scrollbar1 = Scrollbar(canvas2)
            scrollbar1.pack(side=RIGHT, fill=Y)
            listbox1 = Listbox(canvas2,selectbackground="gray",activestyle="none",selectforeground="red",exportselection=0,selectmode='SINGLE')
            listbox1.pack(side=LEFT, fill=BOTH,expand=TRUE)
            for i in range(0,dwn):
                listbox1.insert(END,("  "+str(down[i][0])+".  "+str(down[i][1])))
                i=i+1
            listbox1.config(yscrollcommand=scrollbar1.set)
            scrollbar1.config(command=listbox1.yview)

    # saves the current state of the puzzle in the binary file
    def save_sol():
        filewrite(1,sec,time_state)
        messagebox.showinfo("", "saved successfully")
    
    # saves the current state of the puzzle as a text file     
    def save_txt():
        file_opt=opt = {}
        col_space=[]
        max_col=0
        opt['filetypes'] = [('all files', '.*'), ('text files', '.txt')]
        opt['parent'] = master
        fileloc = filedialog.asksaveasfilename(filetypes=opt['filetypes'])
        ofil=fileloc
        ofl=open(ofil,mode='wb')
        ofl.write(("\n  ").encode(Encoding_2))
        ofl.write(title)       
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
            temp_st=UI.findcurracross(r,c)
            temp=str(across[i][0])+". "+across[i][1]+" <"+temp_st+">"
            ofl.write(("\n  ").encode(Encoding_2))
            ofl.write(temp.encode(Encoding_2))
            
        ofl.write("\n\n Down :\n".encode(Encoding_2))    
        for i in range(0,dwn):
            ct=down[i][0]
            r=row_cellno[ct-1]
            c=col_cellno[ct-1]
            temp_st=UI.findcurrdown(r,c)
            ofl.write(("\n  ").encode(Encoding_2))
            temp=str(down[i][0])+". "+down[i][1]+" <"+temp_st+">"
            ofl.write(temp.encode(Encoding_2))
        ofl.close()

    # inserts a prefix '\' to special characters in Latex in order to print them like any other character
    def replace_spl_char(tex_str):
        tex_str=tex_str.replace("_","\_")
        tex_str=tex_str.replace("&","\&")
        tex_str=tex_str.replace("~","\~")
        tex_str=tex_str.replace("^","\^")
        tex_str=tex_str.replace(repr("\\"),repr("\\\\"))
        tex_str=tex_str.replace("#","\#")
        tex_str=tex_str.replace("$","\$")
        tex_str=tex_str.replace("%","\%")
        tex_str=tex_str.replace("{","\{")
        tex_str=tex_str.replace("}","\}")
        return tex_str
    
    # saves puzzle in LaTex format 
    def save_latex():
        file_opt=opt = {}
        col_space=[]
        max_col=0
        opt['filetypes'] = [('all files', '.*'), ('tex files', '.tex')]
        opt['parent'] = master
        fileloc = filedialog.asksaveasfilename(filetypes=opt['filetypes'])
        ofil=fileloc
        ofl=open(ofil,mode='wb')
        ofl.write(("\\documentclass{article}\n").encode(Encoding_2))
        ofl.write(("\\usepackage[unboxed]{cwpuzzle}\n").encode(Encoding_2))       
        ofl.write(("\\begin{document}\n").encode(Encoding_2))
        ofl.write(("\\begin{PuzzleClues}{\\textbf{Across}}\n").encode(Encoding_2))
        for i in range(0,acc):
            ct=across[i][0]
            r=row_cellno[ct-1]
            c=col_cellno[ct-1]
            temp_st=UI.findsolacross(r,c)
            temp_st1=UI.replace_spl_char(across[i][1])
            temp="\\Clue{"+str(across[i][0])+"}{"+temp_st+"}{"+temp_st1+"}"
            ofl.write((temp+"\n").encode(Encoding_2))
        ofl.write(("\\end{PuzzleClues}\n\n").encode(Encoding_2))
        ofl.write(("\\begin{PuzzleClues}{\\textbf{Down}}\n").encode(Encoding_2))
        for i in range(0,dwn):
            ct=down[i][0]
            r=row_cellno[ct-1]
            c=col_cellno[ct-1]
            temp_st=UI.findsoldown(r,c)
            temp_st1=UI.replace_spl_char(down[i][1])
            temp="\\Clue{"+str(down[i][0])+"}{"+temp_st+"}{"+temp_st1+"}"
            ofl.write((temp+"\n").encode(Encoding_2))
        ofl.write(("\\end{PuzzleClues}\n").encode(Encoding_2)) 
        ofl.write(("\\newline\n").encode(Encoding_2)) 
        ofl.write(("\\PuzzleSolution\n").encode(Encoding_2))
        ofl.write(("\\begin{Puzzle}{"+str(width)+"}{"+str(height)+"}\n").encode(Encoding_2))
        for i in range (0,height):
            temp=""
            for j in range (0,width):
                temp=temp+"|"               
                if(cellblock[i][j] in [".",":"]):
                    temp=temp+"*  "
                elif(cellblock[i][j]=="-"):
                    temp=temp+"\ "
                else:
                    if(cellno[i][j]!=0):
                        temp=temp+"["+str(cellno[i][j])+"]"                     
                    temp=temp+cellblock[i][j]+" "
            temp=temp+"|."
            ofl.write((temp+"\n").encode(Encoding_2))
        ofl.write(("\\end{Puzzle}\n").encode(Encoding_2))
        ofl.write(("\\end{document}\n").encode(Encoding_2))
        ofl.close()

    # unlocks the solution if the key entered by the user is valid key
    def check_key():
        global check_reveal_state,unlock_state,soln_state,checksum_sol
        ab=unscramble_solution(soln.decode(Encoding_2), width, height, int(key.get()))
        window.destroy()
        temp=""
        c=0
        for j in range(0,width):
            c=j
            for i in range(0,height):
                if(ab[c]!=":" and ab[c]!="."):
                    temp=temp+ab[c]
                c=c+width
        data=temp.encode(Encoding_2)
        cksum=0
        for c in data:
            if (cksum & 0x0001):
                cksum = ((cksum >> 1) | 0x8000)
            else:
                cksum = (cksum >> 1)
            cksum = (cksum + c) & 0xffff
        if (cksum==checksum_sol[0]):
            messagebox.showinfo("", "The solution for the puzzle has been unlocked")
            check_reveal_state="normal"
            unlock_state="disabled"                      
            UI.solnmenu.entryconfig(0,state=check_reveal_state)
            UI.solnmenu.entryconfig(1,state=check_reveal_state)
            UI.solnmenu.entryconfig(3,state=unlock_state)
            soln_state[0]=0
            checksum_sol[0]=0
            temp=0
            for i in range(0,height):
                for j in range(0,width):
                    solnblock[i][j]=ab[temp]
                    temp=temp+1
        else:
            messagebox.showinfo("Sorry", "Wrong key")

    # allows user to enter the key inorder to unlock the puzzle   
    def unlock_soln():
        global window,key
        key=StringVar()
        window = Toplevel(master)
        Label(window, text="Enter the 4 digit key").pack()
        e = Entry(window,textvariable=key)
        e.pack(padx=5)
        b = Button(window, text="Unlock", command=UI.check_key)
        b.pack(pady=5)

       

    initUI()

    # menubar
    menubar = Menu(master)
    filemenu = Menu(menubar, tearoff=0)
    filemenu.add_command(label="Save", command=save_sol)
    filemenu.add_command(label="Save as Text File", command=save_txt)
    filemenu.add_command(label="Save as Latex File", command=save_latex)
    filemenu.add_command(label="Clear Puzzle", command=clear_cells)
    filemenu.add_command(label="Multiple Entry", command=multiple_sol)
    filemenu.add_checkbutton(label="Use Pencil", variable = is_pencil, onvalue = 1, offvalue = 0)
    menubar.add_cascade(label="Edit", menu=filemenu)
    solnmenu = Menu(menubar, tearoff=0)
    checkmenu = Menu(solnmenu, tearoff=0)
    checkmenu.add_command(label="Check Letter", command=check_one)
    checkmenu.add_command(label="Check Word", command=check_word)
    checkmenu.add_command(label="Check Solution", command=check_all)
    solnmenu.add_cascade(label="Check", menu=checkmenu,state=check_reveal_state)
    revealmenu = Menu(solnmenu, tearoff=0)
    revealmenu.add_command(label="Reveal Letter", command=reveal_one)
    revealmenu.add_command(label="Reveal Word", command=reveal_word)
    revealmenu.add_command(label="Reveal Incorrect Letters", command=reveal_incorrect)
    revealmenu.add_separator()
    revealmenu.add_command(label="Reveal Solution", command=reveal_sol)
    solnmenu.add_cascade(label="Reveal", menu=revealmenu,state=check_reveal_state)
    solnmenu.add_separator()
    solnmenu.add_command(label="Unlock",command=unlock_soln,state=unlock_state)   
    menubar.add_cascade(label="Solution", menu=solnmenu)
    viewmenu = Menu(menubar, tearoff=0)
    viewmenu.add_command(label="Notes", command=show_notes, state=notes_state)
    menubar.add_cascade(label="View", menu=viewmenu)
    master.config(menu=menubar,background="#D9DADA")   

    # labels to display title, author, copyright followed by the currently highlighted clue
    labela = Label(fmB,text=title.decode((Encoding_2)),width=int(sw/3)+10,relief=RIDGE,font=("Arial",10),bg="#F2F2F2",padx=10,pady=4)
    labela.config(anchor=W,justify=LEFT)
    labela.pack(side=LEFT, fill=BOTH, expand =TRUE)
    labela = Label(fmB,text=aut.decode((Encoding_2)),width=int(sw/3)-5,relief=RIDGE,font=("Arial",10),bg="#F2F2F2",padx=10,pady=4)
    labela.config(justify=CENTER)
    labela.pack(side=LEFT, fill=BOTH, expand =TRUE)
    labela = Label(fmB,text=cpyrt.decode((Encoding_2)),width=int(sw/3)-5,relief=RIDGE,font=("Arial",10),bg="#F2F2F2",padx=10,pady=4)
    labela.config(justify=CENTER)
    labela.pack(side=LEFT, fill=BOTH, expand =TRUE)

    # timer
    m, s = divmod(sec, 60)
    h, m = divmod(m, 60)
    now = "%d:%02d:%02d" % (h, m, s)
    labelt = Label(fmB,text=now,relief=RIDGE,font=("Arial",14),bg="black",padx=5,pady=4)
    labelt.pack(side=LEFT,fill=BOTH, expand =TRUE)
    labelt.config(anchor=W,justify=CENTER)
    labelt.bind("<Button-1>",time_modify)
    if(time_state==0):
       labelt.config(foreground="green")
    else:
       labelt.config(foreground="red")

    # clue for the selected text
    labelc = Label(fmB1,text="",relief=RIDGE,font=("Arial",15,"bold"),bg="#F2F2F2",foreground="#660000",padx=10,pady=4)
    labelc.config(justify=CENTER)
    labelc.pack(side=LEFT, fill=BOTH, expand =TRUE)

    # binds events to the corresponding methods
    listbox.bind("<<ListboxSelect>>", box_clickedA)
    listbox1.bind("<<ListboxSelect>>", box_clickedD)
    canvas.bind("<Button-1>", cell_clicked)
    master.bind("<Key>", key_pressed)
    master.bind("<Left>", key_pressedL)
    master.bind("<Right>", key_pressedR)
    master.bind("<Up>", key_pressedU)
    master.bind("<BackSpace>",key_pressedB)
    master.bind("<Return>",key_pressedE)
    master.bind("<Down>",key_pressedD)
    row,col=0,0


    # updates clock every 1000 milliseconds
    def update_clock():
        global sec,time_state
        if(time_state!=1):
           sec=sec+1
           m, s = divmod(sec, 60)
           h, m = divmod(m, 60)
           now = "%d:%02d:%02d" % (h, m, s)
           UI.labelt.configure(text=now)
           master.after(1000, UI.update_clock)


UI.create_rect(row,col)
UI.update_clock()
master.mainloop()
