import sys
import struct
import functools
import operator
import math
import string
Encoding_2 = "ISO-8859-1" 
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
    cksum = cksum_region(cib_text,cksum)
    return cksum

# calculates checksum for the string section
def text_cksum(cksum=0):
    global cktrial
    if(f.title!=""):
        cksum = cksum_region(f.title.encode(Encoding_2)+b'\0',cksum)
    if(f.author!=""):
        cksum = cksum_region(f.author.encode(Encoding_2)+b'\0',cksum)
    if(f.cpyrt!=""):
        cksum = cksum_region(copy_sym+f.cpyrt.encode(Encoding_2)+b'\0',cksum)
    for clue in cl:
        if(clue):
            cksum = cksum_region(clue, cksum) 
    if(f.notes!=""):
        cksum = cksum_region(f.notes.encode(Encoding_2)+b'\0',cksum)
    return cksum
    

# calculates overall checksum : cib + solution + current state + string section
def overall_checksum():
    cksum = cib_cksum()
    cksum = cksum_region(new_soln, cksum)
    cksum = cksum_region(new_curn, cksum)
    cksum = text_cksum(cksum)
    return cksum
  
# checksum of cib, solution, current state, string section XOR masked against the magic string 'ICHEATED'
def magic_low_cksum():
    m1= ord('I') ^ (cib_cksum() & 0x00ff)
    m2= ord('C') ^ (cksum_region(new_soln) & 0x00ff)
    m3= ord('H') ^ (cksum_region(new_curn) & 0x00ff)
    m4= ord('E') ^ (text_cksum() & 0x00ff)
    calc_temp=struct.pack('4B',m1,m2,m3,m4)
    calc_magiclow_temp=struct.unpack('I',calc_temp)
    calc_magic_low=calc_magiclow_temp[0]
    return calc_magic_low

def magic_high_cksum():
    m5= ord('A') ^ ((cib_cksum() & 0xff00) >> 8)
    m6= ord('T') ^ ((cksum_region(new_soln) & 0xff00) >> 8)
    m7= ord('E') ^ ((cksum_region(new_curn) & 0xff00) >> 8)
    m8= ord('D') ^ ((text_cksum() & 0xff00) >> 8)
    calc_temp=struct.pack('4B',m5,m6,m7,m8)
    calc_magichigh_temp=struct.unpack('I',calc_temp)
    calc_magic_high=calc_magichigh_temp[0]
    return calc_magic_high

# stores the puzzle description in the binary file
def filewrite(t):
    global f,cib_text,new_soln,new_curn,cluelist,cl,copy_sym
    f=t
    ofile=open(f.loc,mode='wb')
    new_soln=('').encode(Encoding_2)
    # solution block of the puzzle
    for i in range(0,f.height):
        for j in range(0,f.width):   
            if(len(f.solnblock[i][j])>1):
                rebus_usr_entry=True 
                temp=f.solnblock[i][j][0]
            else:
                temp=f.solnblock[i][j]
            new_soln=new_soln+temp.encode(Encoding_2)       
            j=j+1
        i=i+1
    new_curn=('').encode(Encoding_2)
     # current state of the puzzle : all the unshaded cells are set to null value (represented by "-") 
    for i in range(0,f.height):
        for j in range(0,f.width):
            if(f.solnblock[i][j]=="."):
                temp="."
            else:
                temp="-"
            new_curn=new_curn+temp.encode(Encoding_2)       
            j=j+1
        i=i+1
    temp_acc=0
    temp_dwn=0
    cl=[]
    cluelist=('').encode(Encoding_2)
    while(temp_acc!=f.acc and temp_dwn!=f.dwn):
        if(f.across[temp_acc][0]<=f.down[temp_dwn][0]):
            cl.append(f.across[temp_acc][1].encode(Encoding_2))
            cluelist=cluelist+(f.across[temp_acc][1].encode(Encoding_2))+b'\0'               
            temp_acc=temp_acc+1
        else:
            cl.append(f.down[temp_dwn][1].encode(Encoding_2))
            cluelist=cluelist+(f.down[temp_dwn][1].encode(Encoding_2))+b'\0'
            temp_dwn=temp_dwn+1
    if(temp_acc==f.acc  and temp_dwn!=f.dwn):
        while(temp_dwn!=f.dwn):
            cl.append(f.down[temp_dwn][1].encode(Encoding_2))
            cluelist=cluelist+(f.down[temp_dwn][1].encode(Encoding_2))+b'\0'
            temp_dwn=temp_dwn+1                
    if(temp_acc!=f.acc and temp_dwn==f.dwn):
        while(temp_acc!=f.acc):
            cl.append(f.across[temp_acc][1].encode(Encoding_2))
            cluelist=cluelist+(f.across[temp_acc][1].encode(Encoding_2))+b'\0'
            temp_acc=temp_acc+1
    no_clues=f.acc+f.dwn
    byte_width=struct.pack('B',f.width)
    byte_height=struct.pack('B',f.height)
    byte_clues=struct.pack('H',no_clues)
    scrambled=struct.pack('H',0x0000)
    diagramless=struct.pack('H',0x0001)
    copy_sym=struct.pack("B",0xa9)
    copy_sym=copy_sym+struct.pack("B",0x20)
    cib_text=byte_width+byte_height+byte_clues+diagramless+scrambled
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
    ofile.write(("1.3").encode(Encoding_2))               
    ofile.write(b'\0')
    ofile.write(b'\0\0')
    ofile.write(struct.pack('H',0x0000))
    ofile.write(bytes(12))
    ofile.write(struct.pack('B',f.width))
    ofile.write(struct.pack('B',f.height))
    ofile.write(struct.pack('H',no_clues))
    ofile.write(diagramless)  
    ofile.write(scrambled)
    ofile.write(new_soln)
    ofile.write(new_curn)
    # string section
    ofile.write((f.title).encode(Encoding_2))
    ofile.write(b'\0')
    ofile.write((f.author).encode(Encoding_2))
    ofile.write(b'\0')
    ofile.write(copy_sym)
    ofile.write((f.cpyrt).encode(Encoding_2))
    ofile.write(b'\0')
    ofile.write(cluelist)
    ofile.write(b'\0')  
    ofile.close()





