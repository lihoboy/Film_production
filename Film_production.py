import min_heap as mh
import copy
import random
import time
import max_w_matching as mwm
def main():
    A=8
    for i in range(9,16):
        print("-----",A,"Actor ",i,"Days","-----")
        BB(A,i)
def BB(A,day):
    # print("main")
    # test_data=[23,56,34,78,9783,2,6,5,547,7,45345,3]
    # print(test_data)
    # mh.min_heap_buildheap(test_data)
    # print(test_data)
    # for i in range(len(test_data)):
    #     print(mh.min_heap_pop_min(test_data),end=" ")
    path="data_"+str(A)+"_"+str(day)
    print(path)
    data_list , weight_list=read_file(path)
    # '''if weight=1'''
    # for i in range(len(weight_list)):
    #     weight_list[i]=1

    # print(weight_list)
    '''data_list(Actor,Day)'''
    num_Actor=len(data_list)
    num_Day = len(data_list[0])
    # print(num_Actor," ",num_Day)
    '''variable for init'''
    list_init=[]
    for i in range(num_Day):
        list_init.append(i)
    # print(list_init)
    count_node=1
    count_prune=0
    '''root init'''
    root_init=Node(list_init,[],[],0)

    '''count init UB'''
    root_init.final_list=list_init
    root_init.final_cost=count_cost(data_list,weight_list,root_init.final_list)
    best_node=copy.deepcopy(root_init)

    Global_UB=best_node.final_cost
    # Global_UB=best_node.final_cost
    print("UB_init : ",Global_UB)
    tStart = time.time()
    '''init first layer'''
    # count=0
    BB_tree=[]
    for i in range(len(root_init.unschedule_list)):
        for j in range(len(root_init.unschedule_list)):
            if i!=j:
                indices = i,j
                '''init new node's list'''
                init_unschedule_list=copy.copy(root_init.unschedule_list)
                init_l_list=copy.copy(root_init.l_list)
                init_r_list = copy.copy(root_init.r_list)
                '''choose'''
                init_l_list.append(init_unschedule_list[i])
                init_r_list.append(init_unschedule_list[j])
                # print(init_unschedule_list)
                init_unschedule_list = [k for l, k in enumerate(init_unschedule_list) if l not in indices]
                # print(init_l_list)
                # print(init_unschedule_list)
                # print(init_r_list)
                # print(i," ",j," ",count)
                '''count LB here'''
                init_new_node=Node(init_unschedule_list,init_l_list,init_r_list,0)
                init_new_node.LB=count_LB(data_list,weight_list,init_new_node)
                BB_tree.append(init_new_node)
                count_node+=1
    mh.min_heap_buildheap(BB_tree)
    # for i in range(len(BB_tree)):
    #     print(mh.min_heap_pop_min(BB_tree).LB)
    '''start BB'''
    while(len(BB_tree)!=0):
        current_node=mh.min_heap_pop_min(BB_tree)
        if len(current_node.unschedule_list)<2:
            current_node.final_list=current_node.l_list+current_node.unschedule_list+current_node.r_list
            current_node.final_cost=count_cost(data_list,weight_list,current_node.final_list)
            if current_node.final_cost<Global_UB:
                Global_UB=current_node.final_cost
                best_node=copy.deepcopy(current_node)
                print("UB update:",Global_UB)
                continue
        else:
            for i in range(len(current_node.unschedule_list)):
                for j in range(len(current_node.unschedule_list)):
                    if i != j:
                        indices = i, j
                        '''init new node's list'''
                        init_unschedule_list = current_node.unschedule_list[:]
                        init_l_list = current_node.l_list[:]
                        init_r_list = current_node.r_list[:]
                        '''choose'''
                        init_l_list.append(init_unschedule_list[i])
                        init_r_list.insert(0,init_unschedule_list[j])

                        init_unschedule_list = [k for l, k in enumerate(init_unschedule_list) if l not in indices]

                        '''count LB here'''
                        init_new_node = Node(init_unschedule_list[:], init_l_list, init_r_list, 0)
                        init_new_node.LB = count_LB(data_list,weight_list, init_new_node)

                        if init_new_node.LB<Global_UB:
                            init_new_node.LB += count_LB_2(data_list, weight_list, init_new_node)
                            if init_new_node.LB < Global_UB:
                                BB_tree.append(init_new_node)
                                mh.min_heap_bottom_up(BB_tree,len(BB_tree)-1)
                                count_node += 1
                            else:
                                count_prune+=1
                        else:
                            count_prune += 1
    tEnd = time.time()
    print("----result----",A,"Actor ",day,"Days","-----")
    print("Sol:",best_node.final_cost)
    print("Schedule :",best_node.final_list)
    print("num_Node:",count_node)
    print("num_Prune:", count_prune)
    print("Time_cost:",tEnd-tStart)
    ''''''
    file = open("B&B.txt", "a")
    file.write("%s\t" % str(day))
    #file.write("%s\t" % Upper_BoundG)
    #file.write("%s\t" % Lower_BoundG)
    file.write("%s\t" % count_node)
    file.write("%s\t" % count_prune)
    file.write("%s\t" % count_cost(data_list,weight_list,best_node.final_list))
    file.write("%s\t" % str(tEnd-tStart))
    for i in range(0, len(best_node.final_list)):
        file.write("%s" % best_node.final_list[i])
        if i != len(best_node.final_list) - 1:
            file.write("->")
    file.write("\n")

    file.close()
    ''''''
    count_cost_1(data_list,weight_list,best_node.final_list)
    print_schedual(data_list,best_node.final_list)
class Node:
    def __init__(self,unschedule_list,l_list,r_list,LB):
        self.unschedule_list=unschedule_list
        self.l_list=l_list
        self.r_list=r_list
        self.LB=LB
        self.final_list=[]
        self.final_cost=0

def read_file(path):
    file=open(path,"r")
    list_out=[]
    first_line=[]
    first_line=file.readline().split(" ")
    for i in range (len(first_line)):
        first_line[i]=int(first_line[i])
    # print(first_line)
    for i in file:
        list=i.split(" ")
        list_out.append(list)

    for i in range(len(list_out)):
        for j in range(len(list_out[0])):
            list_out[i][j]=int(list_out[i][j])
    # print(list_out)
    return list_out,first_line
def count_LB(data_list,weight_list,node):
    ''''''
    all_cost=0
    num_Actor = len(data_list)
    num_Day = len(data_list[0])
    list_for_LB2=[]
    for a in range(num_Actor):
        '''left has one'''
        l_has_one=0
        for i in range(len(node.l_list)):
            if data_list[a][node.l_list[i]]==1:
                l_has_one=1
                break
        '''right has one'''
        r_has_one = 0
        for i in range(len(node.r_list)):
            if data_list[a][node.r_list[i]] == 1:
                r_has_one = 1
                break
        if l_has_one and r_has_one:
            '''case 1'''
            zero_at_l=0
            zero_at_r=0
            zero_at_m = 0
            for l_index in range(len(node.l_list)-1,-1,-1):
                if data_list[a][node.l_list[l_index]]==0:
                    zero_at_l+=1
                else:
                    break
            for r_index in range(len(node.r_list)):
                if data_list[a][node.r_list[r_index]]==0:
                    zero_at_r+=1
                else:
                    break
            '''count zero in mid'''
            for m_index in range(len(node.unschedule_list)):
                if data_list[a][node.unschedule_list[m_index]]==0:
                    zero_at_m+=1

            all_cost+=(zero_at_l+zero_at_r+zero_at_m)*weight_list[a]

    return all_cost
def count_LB_2(data_list,weight_list,node):
    all_cost = 0
    num_Actor = len(data_list)
    num_Day = len(data_list[0])
    list_for_LB2 = []
    for a in range(num_Actor):
        '''left has one'''
        l_has_one = 0
        for i in range(len(node.l_list)):
            if data_list[a][node.l_list[i]] == 1:
                l_has_one = 1
                break
        '''right has one'''
        r_has_one = 0
        for i in range(len(node.r_list)):
            if data_list[a][node.r_list[i]] == 1:
                r_has_one = 1
                break
        if l_has_one and r_has_one==0:
            '''get actor of case 2.1'''
            list_for_LB2.append(a)
        if l_has_one==0 and r_has_one:
            '''get actor of case 2.2'''
            list_for_LB2.append(a)
    list_G=[]
    for a1 in range(len(list_for_LB2)):
        list_each_a1=[]
        for a2 in range(len(list_for_LB2)):

            if a1==a2:
                list_each_a1.append(0)
            else:
                count_01 = 0
                count_10 = 0
                for d in range (len(node.unschedule_list)):
                    if data_list[list_for_LB2[a1]][node.unschedule_list[d]] ==0 and data_list[list_for_LB2[a2]][node.unschedule_list[d]] :
                        count_01+=1
                    if data_list[list_for_LB2[a1]][node.unschedule_list[d]]  and data_list[list_for_LB2[a2]][node.unschedule_list[d]] ==0:
                        count_10+=1
                cost_min_a1a2=min(count_01*weight_list[list_for_LB2[a1]],count_10*weight_list[list_for_LB2[a2]])
                list_each_a1.append(cost_min_a1a2)
        list_G.append(list_each_a1)
    # print (list_G)
    return mwm.greedy(list_G)



    # return all_cost
def count_cost_1(data_list,weight_list,schedule_list):
    '''print demo schedule'''
    all_cost=0
    num_Actor = len(data_list)
    num_Day = len(data_list[0])
    # for a in range(num_Actor):
    #     print("actor",a,":",end=" ")
    #     for d in range(num_Day):
    #         print(data_list[a][schedule_list[d]],end=" ")
    #     print()

    for a in range (num_Actor):
        flag_after_one=0
        last_one_index=0
        count_zero=0
        '''last 1 index'''
        for l in range(num_Day-1,-1,-1):
            if data_list[a][schedule_list[l]]==1:
                last_one_index=l
                break
        for d in range (num_Day):
            if d==last_one_index:
                break
            if data_list[a][schedule_list[d]] ==1:
                flag_after_one=1
            if flag_after_one==1 and data_list[a][schedule_list[d]]==0:
                count_zero += 1
        print ("a",a,"->",count_zero,end="*")
        all_cost+=count_zero*weight_list[a]
        print(weight_list[a]," = ",count_zero*weight_list[a])
    print("=",all_cost)
    return all_cost
def count_cost(data_list,weight_list,schedule_list):
    '''print demo schedule'''
    all_cost=0
    num_Actor = len(data_list)
    num_Day = len(data_list[0])
    # for a in range(num_Actor):
    #     print("actor",a,":",end=" ")
    #     for d in range(num_Day):
    #         print(data_list[a][schedule_list[d]],end=" ")
    #     print()

    for a in range (num_Actor):
        flag_after_one=0
        last_one_index=0
        count_zero=0
        '''last 1 index'''
        for l in range(num_Day-1,-1,-1):
            if data_list[a][schedule_list[l]]==1:
                last_one_index=l
                break
        for d in range (num_Day):
            if d==last_one_index:
                break
            if data_list[a][schedule_list[d]] ==1:
                flag_after_one=1
            if flag_after_one==1 and data_list[a][schedule_list[d]]==0:
                count_zero += 1
        # print ("a",a,"cost=",count_zero)
        all_cost+=count_zero*weight_list[a]
    #     print(count_zero*weight_list[a],"+",end="")
    # print("=",all_cost)
    return all_cost
def print_schedual(data_list,schedule_list):
    num_Actor = len(data_list)
    num_Day = len(data_list[0])
    for a in range(num_Actor):
        print("actor", a, ":", end=" ")
        for d in range(num_Day):
            print(data_list[a][schedule_list[d]], end=" ")
        # print()
        print()
if __name__ == "__main__":
    main()