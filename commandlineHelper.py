import sys
import struct
import functools
import operator
import math
import string
import array

ifil = input('Enter a file name along with path: ')
new_gext=[]
width=0
height=0
cellblock=[]
solnblock=[]
soln=[]
curn_state=[]
# 0 for black
cellno=[]
row_cellno=[]
col_cellno=[]
is_puz_rebus=False
rebus_no=[]
rebus_row_col=[]
rebus_content=[]
rebus_usr_content=[]
gext=[]
pencil=[]
valid=[]
lim=[]
BLACKSQUARE = '.'
time=0
time_state=0
checksum_sol=[]
checksum_sol.append(0)
soln_state=[]
soln_state.append(0)

# function that interacts with the binary (.puz) file
# if nth edit = 0: reads the puzzle description from the binary file
# else: writes the current state of the puzzle to the binary file
def filewrite(nth_edit):
    global ifil,Encoding_1,Encoding_2,Encoding_3,soln_state,puztype,soln,curn_state,b,ifile,valid_cksum,check_reveal_state,unlock_state,notes_state,checksum_sol
    global extra_sec_code,extra_sec_count,extra_sec_length,extra_sec_checksum,extra_sec_data,cluelist,ofile,ofile_txt
    global width,height,cellno,solnblock,across,down,acc,dwn,title,aut,cpyrt,notes,time,time_state
    if(nth_edit==0):
        ofile_txt=ifil
        ifile = open(ifil,'rb')
        Encoding_1 = "ascii"
        Encoding_2 = "ISO-8859-1"
        Encoding_3 = "utf-8"
        b1 = ifile.read();
        length=sys.getsizeof(b1)
        b=b1[0:length]
        ifile.close()
        # width and height of the crossword grid.    
        width=b[44]
        height=b[45]

        # 'a' denotes no. of clues present in the puzzle, no_of_clues is for accessing the last clue in the list.    
        clues=[]
        clues=struct.unpack('H',b[46:48])
        a=clues[0]
        cluelist = []
        no_of_clues=a-1
    
        # notes that come along with the puzzle.
        notes=""
        
        # list for storing across and down clues
        across=[]
        down=[]

        # count on clue number
        count=1    

        # no. of cells in the grid
        cells=width*height

        # counter variable to access cluelist
        num=0
        
        # number of clues in across and down clueliest respectively
        acc=0
        dwn=0

        # extra section list for rebus, timer, circled cells, incorrect and revealed cells.
        # extra_sec contains a list of valid section names    
        extra_sec=[b'GRBS',b'RTBL',b'RUSR',b'LTIM',b'GEXT']
        extra_sec_code=[]
        extra_sec_length=[]
        extra_sec_checksum=[]
        extra_sec_data=[]
        # counter variable for extra section
        extra_temp=0   
    
        # offset for the solution of the puzzle
        solun=52
        # curntsn stores the offset for the current state of the puzzle
        curntsn=solun+cells
        # n is the offset for string section that starts from title of the puzzle.
        n=curntsn+cells
        # binary form of solution of the puzzle
        soln=b[solun:curntsn]
        # binary form of current state of the puzzle
        curn_state=b[curntsn:n]
    
        # offset for title in the string section
        start=n
        # loop counter variable for string section
        k=0
        # offset for the components following title component in the string section. for eg, author,copyright,clues,etc.
        begn=0

        prevj=0
        previ=0
    
        # can be a normal or diagramless puzzle
        puzzletype=struct.unpack('H',b[48:50])   
        puztype=puzzletype[0]
   
        #  can have normal, scrambled or no solution
        solution_state=struct.unpack('H',b[50:52])
        soln_state[0]=solution_state[0]
        temp_cs=struct.unpack('H',b[30:32])
        if(soln_state[0]==4):
            temp_cs=struct.unpack('H',b[30:32])
            checksum_sol[0]=temp_cs[0]
            check_reveal_state="disabled"
            unlock_state="normal"
        else:
            check_reveal_state="normal"
            unlock_state="disabled"
            
    # to find the previous null value in the string section, from the given location 'loc'.
    def prevzero(loc):
        j=loc-1
        while j>=0 and b[j]!=0:
            j=j-1
        return j+1
    
    if(nth_edit==0):
        # finds the different components of the string section 
        i=start
        iterate=True
        while(iterate):
            if(b[i]==0):
                begn= prevzero(i)
                if k==0:
                    title = b[start:i]
                if k==1:
                    aut = b[begn:i]
                if k==2:
                    cpyrt = b[begn:i]
                if k>2:
                    # finds contents of each clue.
                    if no_of_clues>=0:
                        cluebegn=begn
                        cluelist.append(b[begn:i])
                        no_of_clues = no_of_clues-1
                    else:
                        # finds the notes that comes along with the puzzle
                        # notes=str(b[begn:i].decode('iso-8859-1'))
                        notes=b[begn:i]
                        if(notes.decode(Encoding_2)==""):
                            notes_state="disabled"
                        else:
                            notes_state="normal"
                        iterate=False
                k=k+1
            i=i+1
        
        # finds title,length,checksum and data of the components present in extra section 
        position=i
        while ((position+8)<=length):
            if(b[position:(position+4)] in extra_sec ):
                extra_sec_code.append(b[position:(position+4)])
                position=position+4
                temp_short=struct.unpack('H',b[position:(position+2)])
                temp_short1=temp_short[0]
                extra_sec_length.append(temp_short1)
                position=position+2
                temp_short=struct.unpack('H',b[position:(position+2)])
                temp_short1=temp_short[0]
                extra_sec_checksum.append(temp_short1)
                position=position+2
                temp_length=int(extra_sec_length[extra_temp])
                extra_sec_data.append(b[position:(position+temp_length)])
                # stores timer data -'time' finds how much time the user has taken, time_state denotes whether the timer is running or has stopped.
                if(extra_sec_code[extra_temp]==b'LTIM'):
                    lim_str=str(extra_sec_data[extra_temp].decode(Encoding_2))
                    lim=lim_str.split(',')
                    time=int(lim[0])
                    time_state=int(lim[1])
                position=position+temp_length+1
                extra_temp=extra_temp+1            
            else:
                position=position+1
                
        # block of bytes following extra section
        end_bytes=b[position:length]
       
        # no. of components in extra section
        extra_sec_count=extra_temp

        # stores solution of the puzzle
        n=solun
        for i in range(0,height):
            solnblock.append([])
            for j in range(0,width):
                sa=b[n:n+1]
                solnblock[i].append(sa.decode(Encoding_2))
                n=n+1
                j=j+1
            i=i+1
        
        # stores current state of the puzzle

        for i in range(0,height):
            cellblock.append([])
            for j in range(0,width):             
                sa=b[curntsn:curntsn+1]
                cellblock[i].append(sa.decode(Encoding_2))
                curntsn=curntsn+1
                j=j+1
            i=i+1
            


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
        
    if(nth_edit==0):
        # across,down[i]=[no,clue,curnt soln]
        # seperates across from down clues and finds cell no. associiated with each of these clues.
        for i in range(0,height):
            cellno.append([])
            gext.append([])
            pencil.append([])
            valid.append([])
            for j in range(0,width):
                cellno[i].append(0)
                gext[i].append(0)
                pencil[i].append(0)
                valid[i].append(0)
                # width-1 because last cell can't be the start of a clue.
                if j<width-1 and (cellblock[i][j+1]!="." and cellblock[i][j+1]!=":"):
                    if (cellblock[i][j]!="." and cellblock[i][j]!=":") and (j==0 or (cellblock[i][j-1]=="." or cellblock[i][j-1]==":")):
                        cellno[i][j]=count
                        # lists to keep track of row and column of each cell no. respecetively.
                        # count is 1 initially, so while searching use row_cellno[count-1]
                        temp_str=""
                        row_cellno.append(i)
                        col_cellno.append(j)
                        across.append([])
                        across[acc].append(count)
                        across[acc].append(str(cluelist[num].decode(Encoding_2)))
                        temp_str=findcurracross(i,j)
                        across[acc].append(len(temp_str)) 
                        across[acc].append(temp_str)                       
                        acc=acc+1
                        num=num+1
                        count=count+1
                if i<height-1 and (cellblock[i+1][j]!="." and cellblock[i+1][j]!=":")  :       
                    if (cellblock[i][j]!="." and cellblock[i][j]!=":") and (i==0 or (cellblock[i-1][j]=="." or cellblock[i-1][j]==":")):
                        down.append([])
                        temp_str=""
                        if j<width-1 and (cellblock[i][j]!="." and cellblock[i][j]!=":") and (j==0 or (cellblock[i][j-1]=="." or cellblock[i][j-1]==":")):
                        # if cell no. matches with across cell no., count won't be incremented.
                            down[dwn].append(count-1)
                        else:
                            down[dwn].append(count)
                            cellno[i][j]=count
                            count=count+1
                            row_cellno.append(i)
                            col_cellno.append(j)
                        down[dwn].append(str(cluelist[num].decode(Encoding_2)))
                        temp_str=findcurrdown(i,j)
                        down[dwn].append(len(temp_str))
                        down[dwn].append(temp_str)
                        num=num+1
                        dwn=dwn+1
                j=i+1
            i=i+1

    # calculates rebus values
    def calc_rebus():
        global is_puz_rebus
        for i in range(0,extra_sec_count):
            temp=0
            rebus_ind=0
            temp_s=""
            temp_str=""
            # finds the row and column of the rebus entry
            if(extra_sec_code[i]==b'GRBS'):
                for j in range (0,extra_sec_length[i]):
                    k= int(extra_sec_data[i][j])
                    if(k>0):
                        rebus_no.append(k-1)
                        temp_row=str(j//width)
                        temp_col=str(j%width)
                        rebus_row_col.append(temp_row+","+temp_col)
                        rebus_content.append("")
                        rebus_usr_content.append("")
                if(len(rebus_no)>0):
                    is_puz_rebus=True
            # finds the rebus solution for the corresponding rows and columns.
            if(extra_sec_code[i]==b'RTBL'):
                temp_s=extra_sec_data[i].decode(Encoding_3)
                j=0
                while(j<len(temp_s)):
                    if(temp_s[j]==':'):
                        temp_str=""
                        temp=j+1
                        while(temp_s[temp]!=';'):
                            temp_str=temp_str+str(temp_s[temp])
                            temp=temp+1
                        if(temp_s[j-2]==" "):
                            rebus_id=int(temp_s[j-1])
                        else:
                            rebus_id=int(temp_s[j-2:j])
                        for k in range (0,len(rebus_no)):
                            if(rebus_no[k]==rebus_id):
                                rebus_content[k]=temp_str
                        j=temp+1                        
                    else:
                        j=j+1     

            # finds the user entered value for the rebus entry          
            if(extra_sec_code[i]==b'RUSR'):
                j=0
                temp_col=0
                rebus_ind=0
                while(j<extra_sec_length[i]):
                    if(extra_sec_data[i][j]!=0):
                        temp=j
                        temp_str=""
                        while(extra_sec_data[i][j]!=0):
                            j=j+1
                        temp_str=extra_sec_data[i][temp:j].decode(Encoding_3)
                        cellblock[temp_col//width][temp_col%width]=temp_str                     
                    temp_col=temp_col+1
                    j=j+1

 
    # assigns extention code to each cell (it may be a circled, previously incorrect, incorrect or revealed cell)
    def calc_gext():
        for i in range(0,extra_sec_count):
            j=0
            if(extra_sec_code[i]==b'GEXT'):
                while(j<extra_sec_length[i]):
                                # PEN = used pencil
				# C = circled
				# PI = previously incorrect
				# I = incorrect
				# R = revealed
                    if(extra_sec_data[i][j:j+1]!=b'\x00'):
                    	# “PEN” = 1                                            
                        if(extra_sec_data[i][j:j+1]==b'\x08'):
                           gext[j//width][j%width]=1
                        # “PI” = 2 
                        if(extra_sec_data[i][j:j+1]==b'\x10'):
                           gext[j//width][j%width]=2                     
                        # “I” = 3 
                        if(extra_sec_data[i][j:j+1]==b'\x20'):
                           gext[j//width][j%width]=3                        
                        # “R” = 4
                        if(extra_sec_data[i][j:j+1]==b'\x40'):
                           gext[j//width][j%width]=4
                        # “C” = 5
                        if(extra_sec_data[i][j:j+1]==b'\x80'):
                           gext[j//width][j%width]=5
                        # “PEN+PI” = 6
                        if(extra_sec_data[i][j:j+1]==b'\x18'):
                           gext[j//width][j%width]=6
                        # "PEN+I” = 7 
                        if(extra_sec_data[i][j:j+1]==b'\x28'):
                           gext[j//width][j%width]=7                       
                        # "PEN+R” = 8
                        if(extra_sec_data[i][j:j+1]==b'\x48'):
                           gext[j//width][j%width]=8
                        # "PEN+C” = 9 
                        if(extra_sec_data[i][j:j+1]==b'\x88'):
                           gext[j//width][j%width]=9 
                        # “C+PI” = 10
                        if(extra_sec_data[i][j:j+1]==b'\x90'):
                           gext[j//width][j%width]=10
                        # "C+I” = 11
                        if(extra_sec_data[i][j:j+1]==b'\xa0'):
                           gext[j//width][j%width]=11                       
                        # "C+R” = 12
                        if(extra_sec_data[i][j:j+1]==b'\xc0'):
                           gext[j//width][j%width]=12
                        # "C+PEN+PI” = 13
                        if(extra_sec_data[i][j:j+1]==b'\x98'):
                           gext[j//width][j%width]=13
                        # “C+PEN+I” = 14
                        if(extra_sec_data[i][j:j+1]==b'\xa8'):
                           gext[j//width][j%width]=14
                        # "C+PEN+R” = 15
                        if(extra_sec_data[i][j:j+1]==b'\xc8'):
                           gext[j//width][j%width]=15
                    j=j+1

        # assigns a validity code for each cell
        for i in range(0,height):
            for j in range(0,width):
                if(gext[i][j] in [2,6,10,13]):
                   # previously incorrect (PI)
                   valid[i][j]=1
                if(gext[i][j] in [3,7,11,14]):
                   # incorrect (I)
                    valid[i][j]=2
                if(gext[i][j] in [4,8,12,15]):
                   # revealed (R)
                    valid[i][j]=3
                j=j+1
            i=i+1
    

    # finds the checksum for the data given as argument
    def cksum_region(data, cksum=0):
        for c in data:
            if (cksum & 0x0001):
                cksum = ((cksum >> 1) | 0x8000)
            else:
                cksum = (cksum >> 1)
            cksum = (cksum + c) & 0xffff
        return cksum

    # calculates cib checksum
    def cib_cksum(cksum=0):
        cksum = cksum_region(b[44:50],cksum)
        if(soln_state[0]==0):
            temp_soln_state=struct.pack('H',0x0000)
        else:
            temp_soln_state=b[50:52]  
        cksum = cksum_region(temp_soln_state,cksum)
        return cksum

    # calculates checksum for the string section
    def text_cksum(cksum=0):
        if(title):
            cksum = cksum_region(title+b'\0', cksum)
        if(aut):
            cksum = cksum_region(aut+b'\0', cksum)
        if(cpyrt):
            cksum = cksum_region(cpyrt+b'\0', cksum)
        for clue in cluelist:
            if(clue):
                cksum = cksum_region(clue, cksum)
        if(notes):
            cksum = cksum_region(notes+b'\0', cksum)
        return cksum
    

    # calculates overall checksum : cib + solution + current state + string section
    def overall_checksum():
        cksum = cib_cksum()
        cksum = cksum_region(soln, cksum)
        cksum = cksum_region(curn_state, cksum)
        cksum = text_cksum(cksum)
        return cksum
  
    # checksum of cib, solution, current state, string section XOR masked against the magic string 'ICHEATED'
    def magic_low_cksum():
        m1= ord('I') ^ (cib_cksum() & 0x00ff)
        m2= ord('C') ^ (cksum_region(soln) & 0x00ff)
        m3= ord('H') ^ (cksum_region(curn_state) & 0x00ff)
        m4= ord('E') ^ (text_cksum() & 0x00ff)
        calc_temp=struct.pack('4B',m1,m2,m3,m4)
        calc_magiclow_temp=struct.unpack('I',calc_temp)
        calc_magic_low=calc_magiclow_temp[0]
        return calc_magic_low


    def magic_high_cksum():
        m5= ord('A') ^ ((cib_cksum() & 0xff00) >> 8)
        m6= ord('T') ^ ((cksum_region(soln) & 0xff00) >> 8)
        m7= ord('E') ^ ((cksum_region(curn_state) & 0xff00) >> 8)
        m8= ord('D') ^ ((text_cksum() & 0xff00) >> 8)
        calc_temp=struct.pack('4B',m5,m6,m7,m8)
        calc_magichigh_temp=struct.unpack('I',calc_temp)
        calc_magic_high=calc_magichigh_temp[0]
        return calc_magic_high

    if(nth_edit==0):
    	# identifies rebus, circles and validity of cells
        calc_rebus()
        calc_gext()
        # checks the different checksums against the calculated value   
        calc_cib= True 
        temp_cib=struct.unpack('H',b[14:16])
        cib=temp_cib[0]
        calc_cib= calc_cib and (cib==cib_cksum())

        calc_gib= True 
        temp_gib=struct.unpack('H',b[0:2])
        gib=temp_gib[0]
        calc_gib= calc_gib and (gib==overall_checksum())

        calc_magic_low= magic_low_cksum()
        ml=struct.unpack('I',b[16:20])
        magic_low=ml[0]

        calc_magic_high= magic_high_cksum()
        mh=struct.unpack('I',b[20:24])
        magic_high=mh[0]
    
        calc_magic=((magic_low==calc_magic_low) and (magic_high==calc_magic_high))

        calc_extra_sec=True
        for i in range(0,extra_sec_count):
            calc_extra_sec = calc_extra_sec and (extra_sec_checksum[i]==cksum_region(extra_sec_data[i]))

        if (calc_cib and (calc_gib and (calc_magic and calc_extra_sec))):
            valid_cksum=True
        else:
            valid_cksum=False
        
 
    # if save request is given, updates the .puz file with current data
    if(nth_edit!=0):
        ofile=open(ifil,mode='wb')
        rebus_usr_entry=False
        new_curn=('').encode(Encoding_2)
        # updates current state of the puzzle
        for i in range(0,height):
            for j in range(0,width):   
                if(len(cellblock[i][j])>1):
                    rebus_usr_entry=True 
                    temp=cellblock[i][j][0]
                else:
                    temp=cellblock[i][j]
                if(pencil[i][j]==1):
                    temp=temp.lower()
                new_curn=new_curn+temp.encode(Encoding_2)       
                j=j+1
            i=i+1
        curn_state=new_curn
        new_soln=('').encode(Encoding_2)
        # updates solution block of the puzzle (if it has been unlocked in case of scrambled puzzles)
        for i in range(0,height):
            for j in range(0,width):   
                temp=solnblock[i][j]
                new_soln=new_soln+temp.encode(Encoding_2)       
                j=j+1
            i=i+1
        soln=new_soln
        gib=overall_checksum()
        cib=cib_cksum()
        # header section
        ofile.write(struct.pack('H',gib))
        ofile.write(("ACROSS&DOWN").encode(Encoding_2))
        ofile.write(b'\0')
        ofile.write(struct.pack('H',cib))   
        ml=magic_low_cksum()
        mh=magic_high_cksum()
        ofile.write(struct.pack('I',ml))
        ofile.write(struct.pack('I',mh))
        ofile.write(b[24:30])
        if(checksum_sol[0]==0):
            ofile.write(struct.pack('H',0x0000))
        else:
            ofile.write(b[30:32])
        ofile.write(b[32:50])
        if(soln_state[0]==0):
            ofile.write(struct.pack('H',0x0000))
        else:
            ofile.write(b[50:52])  
        ofile.write(soln)
        ofile.write(curn_state)
        # string section
        ofile.write(title)
        ofile.write(b'\0')
        ofile.write(aut)
        ofile.write(b'\0')
        ofile.write(cpyrt)
        ofile.write(b'\0')
        for i in range(0,len(cluelist)):
            ofile.write(cluelist[i])
            ofile.write(b'\0')
        ofile.write(notes)
        ofile.write(b'\0')
        # extra section
        if(is_puz_rebus==True):
            for i in range (0,extra_sec_count):
                if(extra_sec_code[i]==b'GRBS' or extra_sec_code[i]==b'RTBL'):
                    ofile.write(extra_sec_code[i])
                    ofile.write(struct.pack('H',extra_sec_length[i])) 
                    ofile.write(struct.pack('H',extra_sec_checksum[i])) 
                    ofile.write(extra_sec_data[i])
                    ofile.write(b'\0') 
        ofile.write(b'LTIM')
        new_time=str(time)
        new_time=new_time+","
        new_time=new_time+str(1)
        new_time_data=new_time.encode(Encoding_2)
        new_length=len(new_time_data)
        ofile.write(struct.pack('H',new_length))
        new_cksum=cksum_region(new_time_data)
        ofile.write(struct.pack('H',new_cksum))
        ofile.write(new_time_data)
        ofile.write(b'\0')
        new_gext=[]
        is_gext=False
        for i in range (0,height):
            for j in range (0,width):
                temp=0x00
                if(gext[i][j] in [5,9,10,11,12,13,14,15]):
                    temp=temp^0x80
                if(pencil[i][j]==1):
                    temp=temp^0x08
                if(valid[i][j]==1):
                    temp=temp^0x10
                if(valid[i][j]==2):          
                    temp=temp^0x20 
                if(valid[i][j]==3):          
                    temp=temp^0x40
                if(temp!=0x00):
                    is_gext=True
                new_gext.append(temp)
                j=j+1
            i=i+1

        if(is_gext==True):
            byte_gext=bytearray(new_gext)
            new_length=len(byte_gext)
            new_cksum=cksum_region(byte_gext)
            ofile.write(b'GEXT')
            ofile.write(struct.pack('H',new_length))    
            ofile.write(struct.pack('H',new_cksum))
            ofile.write(byte_gext)
            ofile.write(b'\0')
        if (rebus_usr_entry==True):
            new_usr=('').encode(Encoding_2)
            for i in range (0,height):
                for j in range (0,width):
                    if(len(cellblock[i][j])>1):
                        new_usr=new_usr+cellblock[i][j].encode(Encoding_2)
                    new_usr=new_usr+(b'\0')
            new_length=len(new_usr)
            new_cksum=cksum_region(new_usr)
            ofile.write(b'RUSR')
            ofile.write(struct.pack('H',new_length))    
            ofile.write(struct.pack('H',new_cksum))
            ofile.write(new_usr)
            ofile.write(b'\0')                   
        ofile.close()

filewrite(0)

# unscrambles the scrambled solution with 'key'   
def unscramble_solution(scrambled, width, height, key):
    sq = square(scrambled, width, height)
    data = restore(sq, unscramble_string(sq.replace('.', ''), key))
    return square(data, height, width)

# unscrambles the scrambled string with 'key'
def unscramble_string(s, key):
    key = key_digits(key)
    l = len(s)
    for k in key[::-1]:
        s = unshuffle(s)
        s = s[l-k:] + s[:l-k]
        s = unshift(s, key)
    return s

def key_digits(key):
    return [int(c) for c in str(key).zfill(4)]

def shift(s, key):
    atoz = string.ascii_uppercase
    if s:
        return ''.join(
            atoz[(atoz.index(c) + key[i % len(key)]) % len(atoz)]
            for i, c in enumerate(s)
        )
    else:
        return ''

def unshift(s, key):
    return shift(s, [-k for k in key])

def unshuffle(s):
    return s[1::2] + s[::2]
    
def square(data, w, h):
    aa = [data[i:i+w] for i in range(0, len(data), w)]
    return ''.join([''.join([aa[r][c] for r in range(0, h)]) for c in range(0, w)])

def restore(s, t):
    t = (c for c in t)
    return ''.join(next(t) if not is_blacksquare(c) else c for c in s)

def is_blacksquare(c):
    if isinstance(c, int):
        c = chr(c)
    return c == '.'

    



