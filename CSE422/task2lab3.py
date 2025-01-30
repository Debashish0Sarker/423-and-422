def alpha_beta(depth,node,maximizing,value,alpha,beta):
    if depth==0:
        return value[node]
    if maximizing==1:
        max_val=float('-inf')
        for i in range(2):
            val=alpha_beta(depth-1,node*2+i,0,value,alpha,beta)
            max_val=max(max_val,val)
            alpha=max(alpha,val)
            if alpha>=beta:
                break
        return max_val
    else:
        min_val=float('inf')
        for i in range(2):
            val=alpha_beta(depth-1,node*2+i,1,value,alpha,beta)
            min_val=min(min_val,val)
            beta=min(beta,val)
            if beta<=alpha:
                break
        return min_val
def dark_magic(depth,node,value,alpha,beta):#only maximizing
    if depth==0:
        return value[node]
    max_val=float('-inf')
    for i in range(2):
        val=dark_magic(depth-1,node*2+i,value,alpha,beta)
        max_val=max(max_val,val)
        alpha=max(alpha,val)
        if alpha>=beta:
            break
    return max_val

def pac_man(c):
    utility_values=[3, 6, 2, 3, 7, 1, 2, 0]
    alpha=float('-inf')
    beta=float('inf')
    depth=3
    alphabeta=alpha_beta(depth,0,1,utility_values,alpha,beta)#starts with maximizing
    darkmagic=dark_magic(depth,0,utility_values,alpha,beta)
    #utility_values = [3, 6, 2, 3, 7, 1, 2, 0]
    mid=len(utility_values)//2
    left_subtree=utility_values[:mid]
    right_subtree=utility_values[mid:]
    max_left=max(left_subtree)
    max_right=max(right_subtree)
    direction=''
    if max_left >= max_right:
        direction='left'
    else:
        direction='right'
    aftermagic=darkmagic-c
    if alphabeta<aftermagic:
        print(f'The new minimax value is {aftermagic}. Pacman goes {direction} and uses dark magic')
    else:
        print(f'The minimax value is {alphabeta}. Pacman does not use dark magic')
c=int(input())
a=pac_man(c)