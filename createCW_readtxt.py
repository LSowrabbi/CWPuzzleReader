# reads the partially created puzzle's description (path of the file is given by 'loc' attribute of object 'f')
def readtext(f):
    with open(f.loc,encoding="ISO-8859-1") as k:
        content = k.read().splitlines()
    i=0
    width=0
    height=0
    acc=0
    across=[]
    dwn=0
    down=[]
    solnblock=[]
    title=""
    author=""
    cpyrt=""
    notes=""
    Encoding_2 = "ISO-8859-1"
    while(content[i]!="<TITLE>"):
        i=i+1
    i=i+1
    temp=""
    # reads the puzzle description and saves in the respective variables mentioned above
    while(content[i]!="</TITLE>"):
        temp=temp+content[i]
        i=i+1
    title=temp
    i=i+1
    if(content[i]=="<AUTHOR>"):
        i=i+1
        temp=""
        while(content[i]!="</AUTHOR>"):
            temp=temp+content[i]
            i=i+1
        author=temp
        i=i+1
    if(content[i]=="<COPYRIGHT>"):
        i=i+1
        temp=""
        while(content[i]!="</COPYRIGHT>"):
            temp=temp+content[i]
            i=i+1
        cpyrt=temp
        i=i+1
    if(content[i]=="<WIDTH>"):
        i=i+1
        temp=""
        while(content[i]!="</WIDTH>"):
            temp=temp+content[i]
            i=i+1
        width=int(temp)
        i=i+1
    if(content[i]=="<HEIGHT>"):
        i=i+1
        temp=""
        while(content[i]!="</HEIGHT>"):
            temp=temp+content[i]
            i=i+1
        height=int(temp)
        i=i+1
    if(content[i]=="<GRID>"):
        i=i+1
        r=0
        while(content[i]!="</GRID>"):
            j=0
            solnblock.append([])
            # each entry in the solution grid is seperated by a ',')
            while(True):
                temp=""
                while(content[i][j]!=","):
                    temp=temp+content[i][j]
                    j=j+1
                solnblock[r].append(temp)
                j=j+1
                if(j==len(content[i])):
                   break
            r=r+1
            i=i+1
    i=i+1   
    # stores the across and down clues that are already input by the user in the respective cluelists
    if(content[i]=="<ACROSS>"):
        i=i+1
        while(content[i]!="</ACROSS>"):
            if(content[i]!="<NULL>"):
                across.append(content[i])
            else:
                across.append("")
            i=i+1
        acc=len(across)
        i=i+1
    if(content[i]=="<DOWN>"):
        i=i+1
        while(content[i]!="</DOWN>"):
            if(content[i]!="<NULL>"):
                down.append(content[i])
            else:
                down.append("")
            i=i+1
        dwn=len(down)
        i=i+1
    if(content[i]=="<NOTEPAD>"):
        i=i+1
        temp=""
        while(content[i]!="</NOTEPAD>"):
            temp=temp+content[i]
            i=i+1
        notes=temp
    # stores the read puzzle description in the corrresponding object attributes
    f.title=title
    f.author=author
    f.cpyrt=cpyrt
    f.notes=notes
    f.width=width
    f.height=height
    f.solnblock=solnblock
    f.acc=acc
    f.dwn=dwn
    f.across=across
    f.down=down
    f.loc=""
    return f

# writes the data corresponding to the partially complete puzzle to a text file
def writetext(f):
    Encoding_2 = "ISO-8859-1" 
    ofile=open(f.loc,mode='wb')
    #  title of the puzzle
    ofile.write(("<TITLE>"+"\n").encode(Encoding_2))
    msg=f.title+"\n"
    ofile.write(msg.encode(Encoding_2))
    ofile.write(("</TITLE>"+"\n").encode(Encoding_2))
    #  author of the puzzle
    ofile.write(("<AUTHOR>"+"\n").encode(Encoding_2))
    msg=f.author+"\n"
    ofile.write(msg.encode(Encoding_2))
    ofile.write(("</AUTHOR>"+"\n").encode(Encoding_2))
    #  puzzle's copyright
    ofile.write(("<COPYRIGHT>"+"\n").encode(Encoding_2))
    msg=f.cpyrt+"\n"
    ofile.write(msg.encode(Encoding_2))
    ofile.write(("</COPYRIGHT>"+"\n").encode(Encoding_2))
    #  width of the puzzle
    ofile.write(("<WIDTH>"+"\n").encode(Encoding_2))
    msg=str(f.width)+"\n"
    ofile.write(msg.encode(Encoding_2))
    ofile.write(("</WIDTH>"+"\n").encode(Encoding_2))
    #  height of the puzzle
    ofile.write(("<HEIGHT>"+"\n").encode(Encoding_2))
    msg=str(f.height)+"\n"
    ofile.write(msg.encode(Encoding_2))
    ofile.write(("</HEIGHT>"+"\n").encode(Encoding_2))
    # solution grid of the puzzle
    ofile.write(("<GRID>"+"\n").encode(Encoding_2))
    for i in range(0,f.height):
        for j in range(0,f.width):
            msg=f.solnblock[i][j]+","
            ofile.write(msg.encode(Encoding_2))
        ofile.write(("\n").encode(Encoding_2))
    ofile.write(("</GRID>"+"\n").encode(Encoding_2))
    # across and down cluelist
    # if the user has not yet entered a clue for a specific across or down clue, the corresponding clue value is represented by "NULL"
    ofile.write(("<ACROSS>"+"\n").encode(Encoding_2))
    for i in range(0,f.acc):
        if(f.across[i][1]==""):
            msg="<NULL>"+"\n"
        else:
            msg=f.across[i][1]+"\n"
        ofile.write(msg.encode(Encoding_2))
    ofile.write(("</ACROSS>"+"\n").encode(Encoding_2))
    ofile.write(("<DOWN>"+"\n").encode(Encoding_2))
    for i in range(0,f.dwn):
        if(f.down[i][1]==""):
            msg="<NULL>"+"\n"
        else:
            msg=f.down[i][1]+"\n"
        ofile.write(msg.encode(Encoding_2))
    ofile.write(("</DOWN>"+"\n").encode(Encoding_2))
    # notes related to the puzzle (optional)
    ofile.write(("<NOTEPAD>"+"\n").encode(Encoding_2))
    msg=f.notes+"\n"
    ofile.write(msg.encode(Encoding_2))
    ofile.write(("</NOTEPAD>"+"\n").encode(Encoding_2))
    ofile.close()
    
