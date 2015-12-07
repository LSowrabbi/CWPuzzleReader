from commandlineHelper import *

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
            across[i][2]=curstr

def calc_down():            
        for i in range(0,dwn):
            temp=down[i][0]
            c_row=row_cellno[temp-1]
            c_col=col_cellno[temp-1]
            curstr=""
            while(c_row<height and (cellblock[c_row][c_col]!="." and cellblock[c_row][c_col]!=":")):
                curstr=curstr+cellblock[c_row][c_col]
                c_row=c_row+1            
            down[i][2]=curstr
            
# displays clue and asks user to enter a solution for the corresponding clue
            
def disp_clue(clue):    
    if ('across' in clue):
        num=acc
        user_no=int(clue.replace(' across',''))
        for i in range(0,acc):
            if(user_no==int(across[i][0])):
                num=i
        if(num==acc):
            print("No such clue number exists in Across clues")
            return
        c_row=row_cellno[user_no-1]
        c_col=col_cellno[user_no-1]
        print(str(across[num][0])+". "+across[num][1]+" ("+str(len(across[num][2]))+") : "+across[num][2])
        getstr=input('Enter word : ')
        text=""
        for char in getstr:
            if(cellblock[c_row][c_col]!="." and cellblock[c_row][c_col]!=":"):
                if char in "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz":
                    pencil[c_row][c_col]=0
                    cellblock[c_row][c_col]=char.upper()
                else:
                    cellblock[c_row][c_col]="-"
                text=text+cellblock[c_row][c_col]
                c_col=c_col+1
                if(c_row==height or c_col==width):
                    break
            else:
                break
        across[num][2]=text
        calc_down()
        return

    if ('down' in clue):
        num=dwn
        user_no=int(clue.replace(' down',''))
        for i in range(0,dwn):
            if(user_no==int(down[i][0])):
                num=i
        if(num==dwn):
            print("No such clue number exists in Down clues")
            return
        c_row=row_cellno[user_no-1]
        c_col=col_cellno[user_no-1]
        print(str(down[num][0])+". "+down[num][1]+" ("+str(len(down[num][2]))+") : "+down[num][2])
        getstr=input('Enter word : ')
        text=""
        for char in getstr:
            if(cellblock[c_row][c_col]!="." and cellblock[c_row][c_col]!=":"):
                if char in "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz":
                    cellblock[c_row][c_col]=char.upper()
                else:
                    cellblock[c_row][c_col]="-"
                text=text+cellblock[c_row][c_col]
                c_row=c_row+1
                if(c_row==height or c_col==width):
                    break
            else:
                break
        down[num][2]=text
        calc_across()
        return
    print("Sorry wrong format")

# displays solution for a clue number given by the user

def disp_sol(clue):    
    if ('across' in clue):
        num=acc
        user_no=int(clue.replace(' across',''))
        for i in range(0,acc):
            if(user_no==int(across[i][0])):
                num=i
        if(num==acc):
            print("No such clue number exists in Across clues")
            return
        c_row=row_cellno[user_no-1]
        c_col=col_cellno[user_no-1]
        text=""
        while(solnblock[c_row][c_col]!="." and solnblock[c_row][c_col]!=":"):
            cellblock[c_row][c_col]=solnblock[c_row][c_col]
            text=text+solnblock[c_row][c_col]
            c_col=c_col+1
        print(str(across[num][0])+". "+across[num][1]+" ("+str(len(text))+") : "+text)
        across[num][2]=text
        calc_down()
        return

    if ('down' in clue):
        num=dwn
        user_no=int(clue.replace(' down',''))
        for i in range(0,dwn):
            if(user_no==int(down[i][0])):
                num=i
        if(num==dwn):
            print("No such clue number exists in Across clues")
            return
        c_row=row_cellno[user_no-1]
        c_col=col_cellno[user_no-1]
        text=""
        while(solnblock[c_row][c_col]!="." and solnblock[c_row][c_col]!=":"):
            cellblock[c_row][c_col]=solnblock[c_row][c_col]
            text=text+solnblock[c_row][c_col]
            c_row=c_row+1
        print(str(down[num][0])+". "+down[num][1]+" ("+str(len(text))+") : "+text)
        down[num][2]=text
        calc_across()
        return
    print("Sorry wrong format")

# view all across and down clues along with their current state

def view_acc():
    for i in range(0,acc):
        temp=str(across[i][0])+". "+across[i][1]+" ("+str(len(across[i][2]))+") : "+across[i][2]
        print(temp)

def view_dwn():
    for i in range(0,dwn):
        temp=str(down[i][0])+". "+down[i][1]+" ("+str(len(down[i][2]))+") : "+down[i][2]
        print(temp)

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

# view solution grid of the puzzle
def view_soln():
        temp=""
        for i in range(0,height):
            temp=""
            for j in range(0,width):
                temp=temp+" "+solnblock[i][j]
                cellblock[i][j]=solnblock[i][j]
                j=j+1
            print(temp)
            i=i+1
        calc_across()
        calc_down()

         
# clears all the cells
def clear_cells():
        for i in range(0,height):
            for j in range(0,width):
                if(cellblock[i][j]!="." and cellblock[i][j]!=":"):
                    cellblock[i][j]="-"
                j=j+1
            i=i+1
        calc_across()
        calc_down()



            
ip=1
# quits program if checksum does not match
if(valid_cksum==False):
        print("Sorry, the file has been corrupted")
        sys.exit(0)
        
print('Enter 1 to Display the option menu anytime\n')
print('Enter your option: ')
print(" 2 : Enter word for a clue\n 3 : View Solution for a clue\n 4 : View current solution grid\n 5 : View entire solution grid\n 6 : View all across clues\n 7 : View all down clues\n 8 : Clear cells\n 9 : Save\n 0 : Exit")
while(ip!=0):
        ip = input('Enter your option: ')
        if(ip=="1"):
            print(" 2 : Enter word for a clue\n 3 : Display Solution for a clue\n 4 : View current solution grid\n 5 : View entire solution grid\n 6 : View all across clues\n 7 : View all down clues\n 8 : Clear cells\n 9 : Save\n 0: Exit") 
        if(ip=="2"):
            clue= input('Enter clue number (for e.g "1 across") :')
            disp_clue(clue)
        if(ip=="3"):
            clue= input('Enter clue number (for e.g "1 across"):')            
            disp_sol(clue)
        if(ip=="4"):
            print('Current Block:')
            view_cur()
        if(ip=="5"):
            print('Solution Block:')
            view_soln()
        if(ip=="6"):
            print('Across:')
            view_acc()
        if(ip=="7"):
            print('Down:')
            view_dwn()
        if(ip=="8"):
            clear_cells()
            print('Cells Cleared!!')
        if(ip=="9"):
            filewrite(1)
            print("Saved Work Succesfully!")
        if(ip=="0"):
            print("Thank you!!")
            break
        
