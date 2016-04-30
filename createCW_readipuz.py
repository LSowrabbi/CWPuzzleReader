import sys
import ipuz
import struct
import json
across=[]
down=[]
solnblock=[]
# reads the puzzle description from the IPUZ file (path of the file is given by 'loc' attribute of the file instance)
def read_ipuz(f):
    data_file = open(f.loc,'r')   
    data = data_file.read()
    data_file.close()
    try:
        puzzle = ipuz.read(data)
    except ipuz.IPUZException:
        master.withdraw()
        messagebox.showinfo("Sorry!", "File corrupted")
        sys.exit(0)
    # 'block' represents the shaded cells in the grid
    if 'block' in puzzle:
        block=puzzle['block']
    else:
        block="#"
    # 'empty' represents the unshaded cells in the grid that does not hold any value currently
    if 'empty' in puzzle:
        empty=puzzle['empty']
        try:
            empty=int(empty)
        except ValueError:
            pass  
    else:
        empty=0
    if 'title' in puzzle:
        title=puzzle['title']
    else:
        title='title'        
    if 'author' in puzzle:
        author=puzzle['author']
    else:
        author='author'
    if 'copyright' in puzzle:
        cpyrt=puzzle['copyright']
    else:
        cpyrt='copyright'
    if 'notes' in puzzle:
        notes=puzzle['notes']
    else:
        notes=''
    # Across and Down cluelist
    if 'Across' in puzzle['clues'] and 'Down' in puzzle['clues']:      
        for i in range(0,len(puzzle['clues']['Across'])):
            l=puzzle['clues']['Across'][i]
            if isinstance(l,dict):
                across.append(l['clue'])
            else:
                across.append(l[1])
        acc=len(across)
        for i in range(0,len(puzzle['clues']['Down'])):
            l=puzzle['clues']['Down'][i]
            if isinstance(l,dict): 
                down.append(l['clue'])
            else:
                down.append(l[1])
        dwn=len(down)
    if isinstance(puzzle['dimensions']['height'],str):
        height=int(puzzle['dimensions']['height'])
    else:
        height=puzzle['dimensions']['height']
    if isinstance(puzzle['dimensions']['width'],str):
        width=int(puzzle['dimensions']['width'])
    else:
        width=puzzle['dimensions']['width']
    # solnblock represents the solution grid of the puzzle
    for i in range(0,height):
        solnblock.append([])
        for j in range(0,width):
            if isinstance(puzzle['puzzle'][i][j],dict):
                solnblock[i].append(puzzle['puzzle'][i][j]['cell'])
            else:
                solnblock[i].append(puzzle['puzzle'][i][j])           
            if solnblock[i][j]==block or solnblock[i][j]=="null" or solnblock[i][j]==None:
                solnblock[i][j]="."
            else:
                if 'solution' in puzzle:
                    if isinstance(puzzle['solution'][i][j],dict):
                        solnblock[i][j]=puzzle['solution'][i][j]['value'].upper()
                    else:
                        solnblock[i][j]=puzzle['solution'][i][j].upper()
                else:
                    solnblock[i][j]="-"
    f.title=title
    f.author=author
    f.cpyrt=cpyrt
    f.notes=notes
    f.width=width
    f.height=height
    f.solnblock=solnblock
    f.across=across
    f.down=down
    return f

# creates an IPUZ file with the help of object 'f' that contains the complete puzzle description 
def write_ipuz(f):
    puzzle = {'version': "http://ipuz.org/v1", 'kind': ["http://ipuz.org/crossword#1"], 'title': f.title, 'author': f.author, 'copyright': f.cpyrt, 'notes':f.notes};
    puzzle['dimensions']={}
    puzzle['dimensions']['height']=f.height
    puzzle['dimensions']['width']=f.width
    puzzle['clues']={}
    puzzle['clues']['Across']=f.across
    puzzle['clues']['Down']=f.down
    for i in range(0,f.height):
        for j in range(0,f.width):
            if f.solnblock[i][j]==".":
                f.solnblock[i][j]="#"
    puzzle['solution']=f.solnblock
    temp=[]
    for i in range(0,f.height):
        temp.append([])
        for j in range(0,f.width):
            if f.solnblock[i][j]=="#":
                temp[i].append("#")
            else:
                temp[i].append(f.cellno[i][j])
    puzzle['puzzle']=temp
    data = ipuz.write(puzzle, jsonp=True, callback_name="ipuz_function")
    ofile=open(f.loc,mode='w')
    ofile.write(data)
    ofile.close()    
                                
