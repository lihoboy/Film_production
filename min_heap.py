def min_heap_heapify(heap_list,n):
    l=2*n+1
    r=2*n+2

    size=len(heap_list)-1
    if l<=size and heap_list[l].LB<heap_list[n].LB:
        min_index=l
    else:
        min_index = n
    if r <= size and heap_list[r].LB < heap_list[min_index].LB:
        min_index=r
    if min_index!=n:
        heap_list[min_index].LB,heap_list[n].LB=heap_list[n].LB,heap_list[min_index].LB
        min_heap_heapify(heap_list, min_index)

def min_heap_buildheap(heap_list):
    # print("heap")
    size=len(heap_list)-1
    # print(size)
    for i in range (int(size/2)-1,-1,-1):
        # print(i)
        min_heap_heapify(heap_list,i)
def min_heap_pop_min(heap_list):
    size=len(heap_list)
    if size==0:
        print("is_empty")
        return
    else:
        heap_list[size-1],heap_list[0]=heap_list[0],heap_list[size-1]
        temp=heap_list.pop(size-1)
        min_heap_heapify(heap_list, 0)
        return temp
def min_heap_bottom_up(heap_list,n):
    if n==0:
        return
    # size=len(heap_list)-1
    is_even=0
    if n%2==0:
        is_even=1
    parent=int(n/2)-is_even
    if heap_list[n].LB<heap_list[parent].LB:
        heap_list[n],heap_list[parent]=heap_list[parent],heap_list[n]
        min_heap_bottom_up(heap_list, parent)
    else:
        return

