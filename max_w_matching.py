import copy
def main():
    # a = [0, 1, 2, 3]
    # G={}
    G = [[0, 1400, 2100, 700],
         [1400, 0, 0, 850],
         [2100, 0, 0, 750],
         [700, 850, 750, 0]]
    print(greedy(G))
def mwm(G):
    a=[]
    for i in range(len(G)):
        a.append(i)
    max_f=0
    for i in range(len(a)-1):
        for j in range(i+1,len(a)):

            a_prime=a[:]
            v_i=a_prime[i]
            v_j=a_prime[j]
            # print("v_i ", v_i, "v_j_r ", v_j)
            a_prime=[x for x in a_prime if x != v_i]
            a_prime = [x for x in a_prime if x != v_j]
            crr=f(a_prime, v_i, v_j, G)
            # crr+=G[a[i]][a[j]]
            if max_f<crr:
                max_f=crr
#                 print("max_f= ",max_f)
    # print("max_f_all",max_f)
    return max_f
def f(a,v_i,v_j,G):
    if len(a)==0:
        return G[v_i][v_j]
    else:
        max_f=0
        for i in range(len(a)-1):
            for j in range(i + 1, len(a)):
                #if i != j:
                # print("i",i,"j",j)
                a_prime = copy.copy(a)
                v_i_r = a_prime[i]
                v_j_r = a_prime[j]
                # print(a_prime)
                # print("v_i_r ",v_i_r ,"v_j_r ",v_j_r )
                a_prime = [x for x in a_prime if x != v_i_r]
                a_prime = [x for x in a_prime if x != v_j_r]
                # print(a_prime)
                crr = f(a_prime, v_i_r, v_j_r, G)
                if max_f < crr:
                    max_f = crr
        # print(G[v_i][v_j],"+",max_f,"=",G[v_i][v_j]+max_f)
        return  G[v_i][v_j]+max_f

def greedy(G):
    a = []

    for i in range(len(G)):
        a.append(i)
    # print(a)

    sum_weight=0
    is_all_0=1
    for i in range(len(a) - 1):
        for j in range(i + 1, len(a)):
            if G[a[i]][a[j]]!=0:
                is_all_0=0
                break
        if is_all_0:
            break
    if is_all_0:
        return 0
    # print(G)
    while len(a)>1:

        v1 = -1
        v2 = -1
        max_edge = -1
        for i in range(len(a)-1):
            for j in range(i+1,len(a)):
                if G[a[i]][a[j]]>max_edge:
                    max_edge=G[a[i]][a[j]]
                    v1=a[i]
                    v2=a[j]
        sum_weight+=max_edge
        # print(max_edge)
        a.remove(v1)
        a.remove(v2)
    return sum_weight
if __name__ == "__main__":
    main()