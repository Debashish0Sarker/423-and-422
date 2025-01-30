#task1
import random
def alpha_beta(depth,node,maximizing,value,alpha,beta):
    if depth==0:
        return value[node]
    if maximizing==1:
        max_val=float('-inf')
        for i in range(2):
            val=alpha_beta(depth-1,node*2+i,0,value,alpha,beta)
            max_val=max(max_val,val)
            alpha=max(alpha,val)
            # if alpha>=beta:
            #     break
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

def mortal_kombat(start):
    depth=5
    total_rounds=3
    round_winners=[]

    current_player=start 
    for k in range(total_rounds):
        utility_values=[random.choice([-1,1]) for i in range(2**depth)]
        winner= alpha_beta(5,0,current_player,utility_values, float('-inf'), float('inf'))
        if winner==1:
            round_winner='Sub-Zero'
        else:
            round_winner='Scorpion'
        round_winners.append(round_winner)
        current_player = 1-current_player
        if round_winners.count("Sub-Zero")>1 or round_winners.count("Scorpion")>1:
            break

    game_winner=round_winners[-1]
    return game_winner,len(round_winners),round_winners
start=int(input("Enter 0 for Scorpion 1 for Sub-Zero: "))

game_winner,total_rounds_played,round_winners=mortal_kombat(start)

print(f"Game Winner: {game_winner}")
print(f"Total Rounds Played: {total_rounds_played}")
for i in range(len(round_winners)):
    print(f"Winner of Round {i+1}: {round_winners[i]}")

#task2
'''
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
'''