import nltk
import sys
import time as t
import  six.moves.cPickle as pickle
import threading
import math
from solveHelper import *
start_time = t.time()
Encoding_2 = "ISO-8859-1"
solved=cellblock
waitlist=[]

# loads the cluelist stored in clues.p
clues = pickle.load(open("/Users/Documents/clues.p",'rb'),encoding=Encoding_2)
print("--- %s seconds ---" % (t.time() - start_time))
al=[]
dl=[]
cost_dc=[]
cost_ac=[]
omit_list=['CC','DT','EX','IN','MD','JJR','PP','RP','TO','WDT','WP','WB','WRB','.']

# solution list corresponding to the across and down list that has to be found
for i in range(0,acc):
    al.append([])
    cost_ac.append([])
for i in range(0,dwn):
    dl.append([])
    cost_dc.append([])

# solves across clues (only if clue exactly matches any clue present in cluelist) 
def solve_across():
    for i in range(0,acc):
        al[i]=[]
        acc_length=len(across[i][2])
        temp_list=[]
        temp_cost=[]
        for element in clues[acc_length]:
            found=False
            for cl in element[1]:
                if cl==across[i][1]:
                    temp_list.append(element[0])
                    temp_cost.append(0)
                    break
        al[i]=temp_list
        cost_ac[i]=temp_cost

# solves down clues (only if clue exactly matches any clue present in cluelist) 
def solve_down():
    for i in range(0,dwn):
        dwn_length=len(down[i][2])
        temp_list=[]
        temp_cost=[]
        for element in clues[dwn_length]:
            for cl in element[1]:
                if cl==down[i][1]:
                    temp_list.append(element[0])
                    temp_cost.append(0)
                    break
        dl[i]=temp_list
        cost_dc[i]=temp_cost
    
# solve_across_1 and solve_down_1 solves unassigned across clues if constraints can be applied on the cells
# here entries with maximum cost are taken as the final solution entries

def solve_across_1():
    for i in range(0,acc):
        no_acc_down_hint=True
        print("across "+str(across[i][0]))
        if(("Down" in across[i][1] or "Across" in across[i][1]) and "-" in across[i][1]):
            no_acc_down_hint=False
        if(al[i]==[] and no_acc_down_hint):
            r_val=0
            c_val=0
            found_r_c=False
            for j in range(0,height):
                for k in range(0,width):
                    if(len(inter[j][k])!=0 and inter[j][k][0]==["across",across[i][0],0]):
                        found_r_c=True
                        r_val=j
                        c_val=k
                        break
                if(found_r_c==True):
                    break
            check_str=[]
            all_empty=True
            while(c_val!=width and solved[r_val][c_val]!="." and solved[r_val][c_val]!=":"):
                check_str.append(solved[r_val][c_val])
                if(solved[r_val][c_val]!="-"):
                    all_empty=False
                c_val=c_val+1
            acc_length=len(across[i][2])
            temp_thl=[]
            ta=[]
            ta=across[i][1].split()
            a_set = set((a) for a in ta)            
            max_cost=1
            max_list=[]
            max_c=[]
            if(not(all_empty)):
                for element in clues[acc_length]:
                    pattern_match=True
                    for j in range(0,len(check_str)):
                        if(check_str[j]!="-" and check_str[j]!=element[0][j]):
                            pattern_match=False
                            break
                    # checks whether the constraints are satisfied, if yes, proceeds to find maximum cost solutions
                    if(pattern_match==True):
                        found=False
                        for cl in element[1]:
                            text=[]
                            text = nltk.word_tokenize(cl)
                            tc=[]
                            tc=nltk.pos_tag(text)
                            new_tc = [k[0] for k in tc if k[1] not in omit_list]
                            cl_cet = set((a) for a in new_tc)
                            int_ln=len(a_set & cl_cet)
                            if(int_ln==max_cost and found==False):                        
                                max_list.append(element[0])
                                max_c.append(0)
                                found=True
                            if(int_ln>max_cost):
                                found=True
                                max_list=[]
                                max_list.append(element[0])
                                max_cost=int_ln
                                max_c=[]
                                max_c.append(0)
                al[i]=max_list                     
                cost_ac[i]=max_c
                
def solve_down_1():
    for i in range(0,dwn):
        no_acc_down_hint=True
        print("down "+str(down[i][0]))
        if(("Down" in down[i][1] or "Across" in down[i][1]) and "-" in down[i][1]):
            no_acc_down_hint=False
        if(dl[i]==[] and no_acc_down_hint):
            r_val=0
            c_val=0
            found_r_c=False
            for j in range(0,height):
                for k in range(0,width):
                    if((len(inter[j][k])==1 and inter[j][k][0]==["down",down[i][0],0]) or (len(inter[j][k])==2 and inter[j][k][1]==["down",down[i][0],0])):
                        found_r_c=True
                        r_val=j
                        c_val=k
                        break
                if(found_r_c==True):
                    break
            check_str=[]
            all_empty=True
            while(r_val!=height and solved[r_val][c_val]!="." and solved[r_val][c_val]!=":"):
                check_str.append(solved[r_val][c_val])
                if(solved[r_val][c_val]!="-"):
                    all_empty=False
                r_val=r_val+1
            dwn_length=len(down[i][2])
            temp_thl=[]
            ta=[]
            ta=down[i][1].split()
            a_set = set((a) for a in ta)            
            max_cost=1
            max_list=[]
            max_c=[]
            cle=""
            if(not(all_empty)):
                for element in clues[dwn_length]:
                    pattern_match=True
                    for j in range(0,len(check_str)):
                        if(check_str[j]!="-" and check_str[j]!=element[0][j]):
                            pattern_match=False
                            break
                    # checks whether the constraints are satisfied, if yes, proceeds to find maximum cost solutions
                    if(pattern_match==True):
                        found=False
                        for cl in element[1]:
                            text=[]
                            text = nltk.word_tokenize(cl)
                            tc=[]
                            tc=nltk.pos_tag(text)
                            new_tc = [k[0] for k in tc if k[1] not in omit_list]
                            cl_cet = set((a) for a in new_tc)
                            int_ln=len(a_set & cl_cet)
                            if(int_ln==max_cost and found==False):                        
                                max_list.append(element[0])
                                max_c.append(0)
                                found=True
                            if(int_ln>max_cost):
                                found=True
                                max_list=[]
                                max_c=[]
                                max_list.append(element[0])
                                max_c.append(0)
                                cle=cl
                                max_cost=int_ln
                dl[i]=max_list              
                cost_dc[i]=max_c

# deletes all the inconsistent entries to a solution entry for any clue whose size is 1      
def propagate():
    global waitlist
    waitlist=[]
    for i in range(0,len(al)):
        if(len(al[i])==1):
            found=False
            i_r=0
            i_c=0
            for j in range(0,height):
                for k in range(0,width):
                    if(len(inter[j][k])==2 and across[i][0]==inter[j][k][0][1]):
                        i_r=j
                        i_c=k
                        found=True
                        break
                    else:
                        if(len(inter[j][k])==1 and inter[j][k][0][0]=="across" and across[i][0]==inter[j][k][0][1]):
                            i_r=j
                            i_c=k
                            found=True
                            break
                if(found==True):
                    break
            l=0
            while(l<len(al[i][0])):
                if(len(inter[i_r][i_c])==2):
                    for j in range(0,dwn):
                        if(down[j][0]==inter[i_r][i_c][1][1]):
                            char=inter[i_r][i_c][1][2]
                            for el in dl[j]:
                                if(al[i][0][l]!=el[char]):
                                    ind=dl[j].index(el)
                                    if(len(dl[j])>1):
                                        del dl[j][ind]
                                        del cost_dc[j][ind]
                                    else:
                                        # if the inconsistent entry is also of size one, it gets added to the waitlist
                                        # the entry is deleted if it is already in the waitlist
                                        if(("down",j,dl[j][ind]) in waitlist):
                                            del_ind=waitlist.index(("down",j,dl[j][ind]))
                                            del waitlist[del_ind]
                                            del dl[j][ind]
                                            del cost_dc[j][ind]
                                        else:
                                            waitlist.append(("down",j,dl[j][ind]))
                            break
                    i_c=i_c+1
                    l=l+1

    for i in range(0,len(dl)):
        if(len(dl[i])==1):
            found=False
            i_r=0
            i_c=0
            for j in range(0,height):
                for k in range(0,width):
                    if(len(inter[j][k])==2 and down[i][0]==inter[j][k][1][1]):
                        i_r=j
                        i_c=k
                        found=True
                        break
                    else:
                        if(len(inter[j][k])==1 and inter[j][k][0][0]=="down" and down[i][0]==inter[j][k][0][1]):
                            i_r=j
                            i_c=k
                            found=True
                            break
                if(found==True):
                    break
            l=0
            while(l<len(dl[i][0])):
                if(len(inter[i_r][i_c])==2):
                    for j in range(0,acc):
                        if(across[j][0]==inter[i_r][i_c][0][1]):
                            char=inter[i_r][i_c][0][2]
                            for el in al[j]:
                                if(dl[i][0][l]!=el[char]):
                                    ind=al[j].index(el)
                                    if(len(al[j])>1):
                                        del al[j][ind]
                                        del cost_ac[j][ind]
                                    else:
                                        if(("across",j,al[j][ind]) in waitlist):
                                            del_ind=waitlist.index(("across",j,al[j][ind]))
                                            del waitlist[del_ind]
                                            del al[j][ind]
                                            del cost_ac[j][ind]
                                        else:
                                            waitlist.append(("across",j,al[j][ind]))
                            break
                    i_r=i_r+1
                    l=l+1



# calculates cost of each entry in the down list
def calc_cost():
    for i in range(0,height):
        for j in range(0,width):
            if(len(inter[i][j])==2):
                #print(str(i)+str(j))
                for l in range(0,acc):
                    if(across[l][0]==inter[i][j][0][1]):
                        ai=l
                aj=inter[i][j][0][2]
                for l in range(0,dwn):
                    if(down[l][0]==inter[i][j][1][1]):
                        di=l
                dj=inter[i][j][1][2]
                for acc_element in al[ai]:
                    k=0
                    for dwn_element in dl[di]:
                        #print(acc_element+dwn_element+str(aj)+" "+str(dj))
                        if acc_element[aj]==dwn_element[dj]:
                            cost_dc[di][k]=cost_dc[di][k]+1
                        k=k+1

# finds entry with maximum cost for each element in down list
# calculates cost of across list based on this final down list entries
# finds entry with maximum cost for each element in across list
def final_list():
    global final_dl,final_al
    final_dl=[]
    final_al=[]
    for i in range (0,len(dl)):
        if(dl[i]!=[]):
            ind=cost_dc[i].index(max(cost_dc[i]))
            final_dl.append(dl[i][ind])
        else:
            final_dl.append("-")

    for k in range (0,len(dl)):
        if(final_dl[k]!="-"):
            for i in range(0,height):
                for j in range(0,width):
                    if(len(inter[i][j])==2):
                        if(down[k][0]==inter[i][j][1][1]):
                            dj=inter[i][j][1][2]
                            for l in range(0,acc):
                                if(across[l][0]==inter[i][j][0][1]):
                                    ai=l
                                    aj=inter[i][j][0][2]
                            for acc_element in al[ai]:
                                m=0
                                if acc_element[aj]==final_dl[k][dj]:
                                    cost_ac[ai][m]=cost_ac[ai][m]+1
                                m=m+1

    for i in range (0,len(al)):
        if(al[i]!=[]):
            ind=cost_ac[i].index(max(cost_ac[i]))
            final_al.append(al[i][ind])
        else:
            final_al.append("-")

# assigns values to variables in grid based on the final across and down list containing entries with maximum cost           
def solve_list():
    for j in range(0,width):
        for i in range(0,height):
            if cellno[i][j]!=0 and len(inter[i][j])>0:
                if len(inter[i][j])==2 or  inter[i][j][0][0]=="down":
                    for l in range(0,dwn):
                        if(cellno[i][j]==down[l][0] and final_dl[l]!="-"):
                            for k in range(0,len(final_dl[l])):
                                solved[i+k][j]=final_dl[l][k]
                            break

    for i in range(0,height):
        for j in range(0,width):
            if solved[i][j]=="-" and len(inter[i][j])>0 and inter[i][j][0][0]=="across":
                c_no=inter[i][j][0][1]
                pos=inter[i][j][0][2]
                for l in range(0,acc):
                    if(c_no==across[l][0] and final_al[l]!="-"):
                        solved[i][j]=final_al[l][pos]
                        break                  

solve_across()
solve_down()
for i in range(0,len(al)):
    print(str(al[i]))
for i in range(0,len(dl)):
    print(str(dl[i]))    
propagate()
calc_cost()
final_list()
solve_list()
for i in range(0,height):
    print(solved[i]) 
solve_across_1()
solve_down_1()
propagate()
calc_cost()
final_list()
solve_list()
for i in range(0,len(al)):
    print(str(al[i]))
for i in range(0,len(dl)):
    print(str(dl[i])) 
for i in range(0,height):
    print(solved[i]) 
                       
    
print("--- %s seconds ---" % (t.time() - start_time))

