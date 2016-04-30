import sys
import struct

# to find the previous null value in the string section, from the given location 'loc'.
def prevzero(loc):
    j=loc-1
    while j>=0 and b[j]!=0:
        j=j-1
    return j+1

# reads the puzzle description from the binary file (path of the file is given by 'loc' attribute of the file instance)
def readpuz(f):
    global b
    title=""
    aut=""
    cpyrt=""
    notes="" 
    width=0
    height=0
    solnblock=[]
    soln=[]
    is_puz_rebus=False
    rebus_no=[]
    rebus_row_col=[]
    rebus_content=[]
    ifile = open(f.loc,'rb')
    Encoding_2 = "ISO-8859-1"
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
    # no. of cells in the grid
    cells=width*height        
    # extra section list for rebus, timer, circled cells, incorrect and revealed cells.
    # extra_sec contains a list of valid section names    
    extra_sec=[b'GRBS',b'RTBL']
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
    # offset for title in the string section
    start=n
    # loop counter variable for string section
    k=0
    # offset for the components following title component in the string section. for eg, author,copyright,clues,etc.
    begn=0
    prevj=0
    previ=0       
    # finds the different components of the string section 
    i=start
    iterate=True
    while(iterate):
        if(b[i]==0):
            begn = prevzero(i)
            if k==0:
                title = b[start:i].decode(Encoding_2)
            if k==1:
                aut = b[begn:i].decode(Encoding_2)
            if k==2:
                cpyrt_bytes = b[begn:i]
                cs=struct.pack('H',0x20a9)
                if(cs in cpyrt_bytes):
                    cpyrt_bytes=cpyrt_bytes.replace(cs,b'')
                cpyrt=cpyrt_bytes.decode(Encoding_2)
            if k>2:
                # finds contents of each clue.
                if no_of_clues>=0:
                    cluebegn=begn
                    cluelist.append(b[begn:i].decode(Encoding_2))
                    no_of_clues = no_of_clues-1
                else:
                    # finds the notes that comes along with the puzzle
                    # notes=str(b[begn:i].decode('iso-8859-1'))
                    notes=b[begn:i].decode(Encoding_2)
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
            position=position+temp_length+1
            extra_temp=extra_temp+1
        else:
            position=position+1
       
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
          
    # assigns all rebus cells in the grid with their corresponding rebus solution          
    for i in range(0,height):
        for j in range(0,width):
            if(is_puz_rebus==True):
               if (str(i)+","+str(j) in rebus_row_col):
                    rebus_index=rebus_row_col.index(str(i)+","+str(j))
                    temp_text=rebus_content[rebus_index]
                    solnblock[i][j]=rebus_content[rebus_index]
            if (solnblock[i][j]==":"):
                   solnblock[i][j]="."
    f.title=title
    f.author=aut
    f.cpyrt=cpyrt
    f.notes=notes
    f.width=width
    f.height=height
    f.solnblock=solnblock
    f.across=cluelist       
    return f
   
