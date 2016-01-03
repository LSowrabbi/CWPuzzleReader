from commandlineHelper import *

for i in range(0,height):
        for j in range(0,width):
                if(cellblock[i][j]!="." and cellblock[i][j]!=":" and pencil[i][j]==0):
                        cellblock[i][j]=cellblock[i][j].upper()
                        
# calc_across and calc_down are for calculating current state of the across and down clues respectively
def calc_across():
        for i in range(0,acc):
            temp=across[i][0]
            c_row=row_cellno[temp-1]
            c_col=col_cellno[temp-1]
            curstr=""
            while((c_col<width) and  (cellblock[c_row][c_col]!="." and cellblock[c_row][c_col]!=":")):
                curstr=curstr+cellblock[c_row][c_col]
                c_col=c_col+1
            across[i][3]=curstr

def calc_down():            
        for i in range(0,dwn):
            temp=down[i][0]
            c_row=row_cellno[temp-1]
            c_col=col_cellno[temp-1]
            curstr=""
            while(c_row<height and (cellblock[c_row][c_col]!="." and cellblock[c_row][c_col]!=":")):
                curstr=curstr+cellblock[c_row][c_col]
                c_row=c_row+1            
            down[i][3]=curstr

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
        print("Congratulations, You have successfully completed the puzzle") 

# displays clue and asks user to enter a solution for the corresponding clue            
def disp_clue(clue):         
    if ('across' in clue):
        num=acc
        user_no=int(clue.replace(' across',''))
        for i in range(0,acc):
            if(user_no==int(across[i][0])):
                num=i
        if(num==acc):
            print("No such clue number exists in across cluelist")
            return
        c_row=row_cellno[user_no-1]
        c_col=col_cellno[user_no-1]
        print(str(across[num][0])+". "+across[num][1]+" ("+str(across[num][2])+") : "+across[num][3])
        getstr=input('Enter word : ')
        for char in getstr:
            if(cellblock[c_row][c_col]!="." and cellblock[c_row][c_col]!=":"):
                if(char not in "," and valid[c_row][c_col]!=3 ):
                    if char in "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz":
                        pencil[c_row][c_col]=0
                        cellblock[c_row][c_col]=char.upper()
                    else:
                        cellblock[c_row][c_col]="-"
                    if(valid[c_row][c_col]==2):
                        valid[c_row][c_col]=1
                c_col=c_col+1
                if(c_row==height or c_col==width):
                    break
            else:
                break
        curstr=""
        c_row=row_cellno[user_no-1]
        c_col=col_cellno[user_no-1]
        while((c_col<width) and  (cellblock[c_row][c_col]!="." and cellblock[c_row][c_col]!=":")):
            curstr=curstr+cellblock[c_row][c_col]
            c_col=c_col+1
        across[num][3]=curstr
        calc_down()
        return

    if ('down' in clue):
        num=dwn
        user_no=int(clue.replace(' down',''))
        for i in range(0,dwn):
            if(user_no==int(down[i][0])):
                num=i
        if(num==dwn):
            print("No such clue number exists in down cluelist")
            return
        c_row=row_cellno[user_no-1]
        c_col=col_cellno[user_no-1]
        print(str(down[num][0])+". "+down[num][1]+" ("+str(down[num][2])+") : "+down[num][3])
        getstr=input('Enter word : ')
        for char in getstr:
            if(cellblock[c_row][c_col]!="." and cellblock[c_row][c_col]!=":"):
                if(char not in "," and valid[c_row][c_col]!=3 ):
                    if char in "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz":
                        pencil[c_row][c_col]=0
                        cellblock[c_row][c_col]=char.upper()
                    else:
                        cellblock[c_row][c_col]="-"
                    if(valid[c_row][c_col]==2):
                        valid[c_row][c_col]=1
                c_row=c_row+1
                if(c_row==height or c_col==width):
                    break
            else:
                break
        curstr=""
        c_row=row_cellno[user_no-1]
        c_col=col_cellno[user_no-1]
        while(c_row<height and (cellblock[c_row][c_col]!="." and cellblock[c_row][c_col]!=":")):
            curstr=curstr+cellblock[c_row][c_col]
            c_row=c_row+1            
        down[num][3]=curstr        
        calc_across()
        return
    print("Sorry wrong format")

# function for rebus entry at a particular location in a word
def disp_rebus_clue(clue):         
    if ('across' in clue):
        num=acc
        user_no=int(clue.replace(' across',''))
        for i in range(0,acc):
            if(user_no==int(across[i][0])):
                num=i
        if(num==acc):
            print("No such clue number exists in across cluelist")
            return
        c_row=row_cellno[user_no-1]
        c_col=col_cellno[user_no-1]
        print(str(across[num][0])+". "+across[num][1]+" ("+str(across[num][2])+") : "+across[num][3])
        getstr=input('Enter the location where rebus has to be placed (for eg. in the word ABCDE, press 1 to place rebus at position A) : ')
        loc=int(getstr)
        if (loc>across[num][2] or loc<1):
            print("Sorry location index is out of range")
            return
        c_col=c_col+(loc-1)
        if (valid[c_row][c_col]==3):
            print("Sorry the cellblock at this location has already been revealed")
            return
        getstr=input('Enter the rebus word  : ')
        text=""
        for char in getstr:
            if char in "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz":
                text=text+char.upper()
        if(text==""):
            text="-"
        pencil[c_row][c_col]=0
        cellblock[c_row][c_col]=text
        if(valid[c_row][c_col]==2):
            valid[c_row][c_col]=1
        c_row=row_cellno[user_no-1]
        c_col=col_cellno[user_no-1]
        curstr=""
        while((c_col<width) and  (cellblock[c_row][c_col]!="." and cellblock[c_row][c_col]!=":")):
            curstr=curstr+cellblock[c_row][c_col]
            c_col=c_col+1
        across[num][3]=curstr
        calc_down()
        return

    if ('down' in clue):
        num=dwn
        user_no=int(clue.replace(' down',''))
        for i in range(0,dwn):
            if(user_no==int(down[i][0])):
                num=i
        if(num==dwn):
            print("No such clue number exists in down cluelist")
            return
        c_row=row_cellno[user_no-1]
        c_col=col_cellno[user_no-1]
        print(str(down[num][0])+". "+down[num][1]+" ("+str(down[num][2])+") : "+down[num][3])
        getstr=input('Enter the location where rebus has to be placed (for eg. in the word ABCDE, press 1 to place rebus at position A) : ')
        loc=int(getstr)
        if (loc>down[num][2] or loc<1):
            print("Sorry location index is out of range")
            return
        c_row=c_row+(loc-1)
        if (valid[c_row][c_col]==3):
            print("Sorry the cellblock at this location has already been revealed")
            return
        getstr=input('Enter the rebus word  : ')
        text=""
        for char in getstr:
            if char in "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz":
                text=text+char.upper()
        if(text==""):
            text="-"
        pencil[c_row][c_col]=0
        cellblock[c_row][c_col]=text
        if(valid[c_row][c_col]==2):
            valid[c_row][c_col]=1
        c_row=row_cellno[user_no-1]
        c_col=col_cellno[user_no-1]
        curstr=""
        while(c_row<height and (cellblock[c_row][c_col]!="." and cellblock[c_row][c_col]!=":")):
            curstr=curstr+cellblock[c_row][c_col]
            c_row=c_row+1
        down[num][3]=curstr        
        calc_across()
        return
    print("Sorry wrong format")

# view all across and down clues along with their current state
def view_acc():
    for i in range(0,acc):
        temp=str(across[i][0])+". "+across[i][1]+" ("+str(across[i][2])+") : "+across[i][3]
        print(temp)

def view_dwn():
    for i in range(0,dwn):
        temp=str(down[i][0])+". "+down[i][1]+" ("+str(down[i][2])+") : "+down[i][3]
        print(temp)

# clears all the entries in the cells       
def clear_cells():
    for i in range(0,height):
        for j in range(0,width):
            valid[i][j]=0
            pencil[i][j]=0
            if cellblock[i][j]!="." and cellblock[i][j]!=":":
                cellblock[i][j]="-"
            j=j+1
        i=i+1
    calc_across()
    calc_down()

# view current state of the puzzle
def view_cur():
        temp=""
        for i in range(0,height):
            temp=""
            for j in range(0,width):
                temp=temp+" "+cellblock[i][j]
                j=j+1
            print(temp)
            i=i+1
            
# checks the letter in the given row and column of grid with the corresponding letter in the solution                        
def check(c_row,c_col):
    global valid
    valid_count=True
    if(cellblock[c_row][c_col]!="." and cellblock[c_row][c_col]!=":" and valid[c_row][c_col]!=3):
        if((is_puz_rebus==True) and (str(c_row)+","+str(c_col) in rebus_row_col)):
            rebus_index=rebus_row_col.index(str(c_row)+","+str(c_col))
            temp_text=rebus_content[rebus_index]
        else:
            temp_text=solnblock[c_row][c_col]
        if(cellblock[c_row][c_col]==temp_text or cellblock[c_row][c_col]=="-"):  
            valid_count=True
        else:
            valid_count=False
            valid[c_row][c_col]=2                   
    return valid_count            
     
    
#  checks the validity of a single letter in a word for a given clue   
def check_one():
    clue= input('Enter clue number (for e.g "1 across"): ')            
    if ('across' in clue):
        num=acc
        user_no=int(clue.replace(' across',''))
        for i in range(0,acc):
            if(user_no==int(across[i][0])):
                num=i
        if(num==acc):
            print("No such clue number exists in across cluelist")
            return
        c_row=row_cellno[user_no-1]
        c_col=col_cellno[user_no-1]
        print(str(across[num][0])+". "+across[num][1]+" ("+str(across[num][2])+") : "+across[num][3])
        getstr=input('Enter the location which has to be checked in the word (for eg. in the word ABCDE, press 1 to check the letter in position A) : ')
        loc=int(getstr)
        if (loc>across[num][2] or loc<1):
            print("Sorry location index is out of range")
            return
        c_col=c_col+(loc-1)
        v=check(c_row,c_col)
        if (v==True):
            print("The letter is correct")
        else:
            print("Sorry, the letter seems to be incorrect")
        return
    if ('down' in clue):
        num=dwn
        user_no=int(clue.replace(' down',''))
        for i in range(0,dwn):
            if(user_no==int(down[i][0])):
                num=i
        if(num==dwn):
            print("No such clue number exists in down cluelist")
            return
        c_row=row_cellno[user_no-1]
        c_col=col_cellno[user_no-1]
        print(str(down[num][0])+". "+down[num][1]+" ("+str(down[num][2])+") : "+down[num][3])
        getstr=input('Enter the location which has to be checked in the word (for eg. in the word ABCDE, press 1 to check the letter in position A) : ')
        loc=int(getstr)
        if (loc>down[num][2] or loc<1):
            print("Sorry location index is out of range")
            return
        c_row=c_row+(loc-1)
        v=check(c_row,c_col)
        if (v==True):
            print("The letter is correct")
        else:
            print("Sorry, the letter seems to be incorrect")
        return
    print("Sorry wrong format")        
            
# checks the validity of a word for a given clue 
def check_word():
    ck_val=True
    ad=0
    clue = input('Enter clue number (for e.g "1 across"): ') 
    if ('across' in clue):
        num=acc
        user_no=int(clue.replace(' across',''))
        for i in range(0,acc):
            if(user_no==int(across[i][0])):
                num=i
        if(num==acc):
            print("No such clue number exists in across cluelist")
            return
        ad=1
    if ('down' in clue):
        num=dwn
        user_no=int(clue.replace(' down',''))
        for i in range(0,dwn):
            if(user_no==int(down[i][0])):
                num=i
        if(num==dwn):
            print("No such clue number exists in down cluelist")
            return
        ad=2
    if (ad==0):
        print("Sorry wrong format!")
        return
    c_row=row_cellno[user_no-1]
    c_col=col_cellno[user_no-1]
    text=""
    while(cellblock[c_row][c_col]!="." and cellblock[c_row][c_col]!=":"):
        val=check(c_row,c_col)
        if (val==True):
            if (cellblock[c_row][c_col]=="-"):
                text=text+" - "
            else:
                text=text+" "+cellblock[c_row][c_col]+","+"Correct "
        else:
            text=text+" "+cellblock[c_row][c_col]+","+"Wrong "
        ck_val=ck_val and val
        if(ad==1):
            c_col=c_col+1
        else:
            c_row=c_row+1
        if (c_row == height or c_col==width):
            break
    if(ck_val==True):
        print("No incorrect letters found!")
    else:
        print("Sorry there are some incorrect letters in the word")
        print(text)
    return
             

# checks the validity of the entire grid         
def check_all():
    ck_val=True
    text=""
    for i in range(0,height):
        for j in range(0,width):
            val=check(i,j)
            if (val==True):
                if (cellblock[i][j]=="-" or (cellblock[i][j]=="." or cellblock[i][j]==":" )):
                    text=text+" "+cellblock[i][j]+" "
                else:
                    text=text+" "+cellblock[i][j]+","+"Correct "
            else:
                text=text+" "+cellblock[i][j]+","+"Wrong "
            ck_val=ck_val and val
            j=j+1
        text=text+"\n"
        i=i+1
    if(ck_val==True):
        print("No incorrect letters found!")
    else:
        print("Sorry there are some incorrect entries in the grid")
        print(text)
    return

# reveals the solution for the given row and column of grid        
def reveal(i,j):
    global valid
    correct_entry=False
    if((is_puz_rebus==True) and (str(i)+","+str(j) in rebus_row_col)):
        rebus_index=rebus_row_col.index(str(i)+","+str(j))
        correct_entry=(rebus_content[rebus_index]==cellblock[i][j])
    else:
        correct_entry=(solnblock[i][j]==cellblock[i][j])
    if(not(correct_entry)):
        if solnblock[i][j]!="." and solnblock[i][j]!=":":
            pencil[i][j]=0
            valid[i][j]=3
            if((is_puz_rebus==True) and (str(i)+","+str(j) in rebus_row_col)):
                rebus_index=rebus_row_col.index(str(i)+","+str(j))
                cellblock[i][j]=rebus_content[rebus_index]
            else:
                cellblock[i][j]=solnblock[i][j]

# reveals a single letter in a word for a given clue   
def reveal_one():
    clue = input('Enter clue number (for e.g "1 across"): ')            
    if ('across' in clue):
        num=acc
        user_no=int(clue.replace(' across',''))
        for i in range(0,acc):
            if(user_no==int(across[i][0])):
                num=i
        if(num==acc):
            print("No such clue number exists in across cluelist")
            return
        c_row=row_cellno[user_no-1]
        c_col=col_cellno[user_no-1]
        print(str(across[num][0])+". "+across[num][1]+" ("+str(across[num][2])+") : "+across[num][3])
        getstr=input('Enter the location which has to be revealed in the word (for eg. in the word ABCDE, press 1 to reveal the letter in position A) : ')
        loc=int(getstr)
        if (loc>across[num][2] or loc<1):
            print("Sorry location index is out of range")
            return
        c_col=c_col+(loc-1)
        reveal(c_row,c_col)
        print("The letter at the given location is : "+cellblock[c_row][c_col])
        curstr=""
        c_row=row_cellno[user_no-1]
        c_col=col_cellno[user_no-1]
        while((c_col<width) and  (cellblock[c_row][c_col]!="." and cellblock[c_row][c_col]!=":")):
            curstr=curstr+cellblock[c_row][c_col]
            c_col=c_col+1
        across[num][3]=curstr
        calc_down()
        return
    if ('down' in clue):
        num=dwn
        user_no=int(clue.replace(' down',''))
        for i in range(0,dwn):
            if(user_no==int(down[i][0])):
                num=i
        if(num==dwn):
            print("No such clue number exists in down cluelist")
            return
        c_row=row_cellno[user_no-1]
        c_col=col_cellno[user_no-1]
        print(str(down[num][0])+". "+down[num][1]+" ("+str(down[num][2])+") : "+down[num][3])
        getstr=input('Enter the location which has to be checked in the word (for eg. in the word ABCDE, press 1 to reveal the letter in position A): ')
        loc=int(getstr)
        if (loc>down[num][2] or loc<1):
            print("Sorry location index is out of range")
            return
        c_row=c_row+(loc-1)
        reveal(c_row,c_col)
        print("The letter at the given location is : "+cellblock[c_row][c_col])
        curstr=""
        c_row=row_cellno[user_no-1]
        c_col=col_cellno[user_no-1]
        while(c_row<height and (cellblock[c_row][c_col]!="." and cellblock[c_row][c_col]!=":")):
            curstr=curstr+cellblock[c_row][c_col]
            c_row=c_row+1            
        down[num][3]=curstr        
        calc_across()
        return
    print("Sorry wrong format") 

                            
# reveals the word for a given clue                          
def reveal_word():
    ck_val=True
    ad=0
    clue = input('Enter clue number (for e.g "1 across"):') 
    if ('across' in clue):
        num=acc
        user_no=int(clue.replace(' across',''))
        for i in range(0,acc):
            if(user_no==int(across[i][0])):
                num=i
        if(num==acc):
            print("No such clue number exists in across cluelist")
            return
        ad=1
    if ('down' in clue):
        num=dwn
        user_no=int(clue.replace(' down',''))
        for i in range(0,dwn):
            if(user_no==int(down[i][0])):
                num=i
        if(num==dwn):
            print("No such clue number exists in down cluelist")
            return
        ad=2
    if (ad==0):
        print("Sorry wrong format!")
        return
    c_row=row_cellno[user_no-1]
    c_col=col_cellno[user_no-1]
    text=""
    while(cellblock[c_row][c_col]!="." and cellblock[c_row][c_col]!=":"):
        reveal(c_row,c_col)
        text=text+cellblock[c_row][c_col]
        if(ad==1):
            c_col=c_col+1
        else:
            c_row=c_row+1
        if (c_row == height or c_col==width):
            break
    if(ad==1):
        print("The word for the clue '"+across[num][1]+"' is : "+text)
    else:
        print("The word for the clue '"+down[num][1]+"' is : "+text)
    c_row=row_cellno[user_no-1]
    c_col=col_cellno[user_no-1]
    if(ad==1):
        across[num][3]=text
        calc_down()
    else:           
        down[num][3]=text        
        calc_across()
    return


# reveals the complete solution  
def reveal_sol():
    text=""
    for i in range(0,height):
        for j in range(0,width):
            reveal(i,j)
            text=text+" "+cellblock[i][j]
            j=j+1
        text=text+"\n"
        i=i+1
    print("Solution Grid : ")
    print(text)
    calc_across()
    calc_down()
    return

# in locked puzzles, this function checks the validity of the key entered by the user.        
def check_key(key):
    global check_reveal_state,unlock_state,soln_state,checksum_sol
    ab=unscramble_solution(soln.decode(Encoding_2), width, height, int(key))
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
        print("The solution for the puzzle has been unlocked")
        check_reveal_state="normal"
        unlock_state="disabled"                      
        soln_state[0]=0
        checksum_sol[0]=0
        temp=0
        for i in range(0,height):
            for j in range(0,width):
                solnblock[i][j]=ab[temp]
                temp=temp+1
    else:
       print("Sorry, Wrong key!")

# in locked puzzles, this function gets the key from the user, to unlock the solution.        
def unlock_soln():
    global key
    key = input("Enter the 4 digit key : ") 
    check_key(key)



# quits program if checksum does not match
if(valid_cksum==False):
        print("Sorry, the file has been corrupted")
        sys.exit(0)


time_state=1
ip=1
calc_across()
calc_down()
print('Enter 1 to Display the option menu anytime')
while(ip!=0):
        ip = input('Enter your option: ')
        if(ip=="1"):
            if(unlock_state=="disabled"):
                print(" 2 : Enter word for a clue (While entering letters for the word, press ',' key to repeat letters from the previous entry of the word eg. A,,DE)\n 3 : Enter rebus for a cell\n 4 : View all across clues\n 5 : View all down clues\n 6 : Clear cells\n 7 : Save\n 8 : View current state of the grid\n 9 : Check a letter, word or entire grid\n 10 : Reveal letter, word or entire solution grid") 
            else:
                print(" 2 : Enter word for a clue\n 3 : Enter rebus for a cell\n 4 : View all across clues\n 5 : View all down clues\n 6 : Clear cells\n 7 : Save\n 8 : View current state of the grid\n 11 : Unlock solution")
            if(notes_state=="normal"):
                print(" 12 : Display notepad\n 0 : Exit")
            else:
                print(" 0 : Exit")                
        if(ip=="2"):
            clue= input('Enter clue number (for e.g "1 across"): ')
            disp_clue(clue)
            is_sol_complete()
        if(ip=="3"):
            clue= input('Enter clue number (for e.g "1 across"): ')            
            disp_rebus_clue(clue)
            is_sol_complete()
        if(ip=="4"):
            print('Across:')
            view_acc()
        if(ip=="5"):
            print('Down:')
            view_dwn()
        if(ip=="6"):
            clear_cells()
            print('Cells Cleared!!')
        if(ip=="7"):
            filewrite(1)
            print("Saved Work Succesfully!")
        if(ip=="8"):
            print('Current Block:')
            view_cur()
        if(ip=="9"):
            if(unlock_state=="disabled"):
                print('Enter your choice for checking blocks:')
                choice=input(' 1 : Check letter\n 2 : Check word\n 3 : Check entire grid\n')  
                if choice=="1":
                    check_one()
                if choice=="2":
                    check_word()
                if choice=="3":
                    check_all()
            else:
                print("Sorry you must unlock the solution first to check or reveal the grid")
        if(ip=="10"):
            if(unlock_state=="disabled"):
                print('Enter your choice for revealing blocks:')
                choice=input(' 1 : Reveal letter\n 2 : Reveal word\n 3 : Reveal entire grid\n')  
                if choice=="1":
                    reveal_one()
                    is_sol_complete()
                if choice=="2":
                    reveal_word()
                    is_sol_complete()
                if choice=="3":
                    reveal_sol()
                    is_sol_complete()
            else:
                print("Sorry you must unlock the solution first to check or reveal the grid")
        if(ip=="11"):
            if(unlock_state=="normal"):
                print('Unlock Solution:')
                unlock_soln()
            else:
                print("The solution has already been unlocked!")
        if(ip=="12"):
            if(notes_state=="normal"):
                print(notes.decode(Encoding_2))
            else:
                print("There are no notes available for this puzzle")
        if(ip=="0"):
            print("Thank you!!")
            break
