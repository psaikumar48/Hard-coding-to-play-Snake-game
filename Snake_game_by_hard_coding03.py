import pygame
import random
import copy
from scipy.spatial import distance

M,N,grid_size=10,10,20
grids=[(i,j) for i in range(M) for j in range(N)]
Actions=['Top','Right','Bottum','Left']
Episode,High_score,snake_wait_time= 1,0,0

def food():
    global Food
    snake_no_grids= [i for i in grids if i not in Snake]
    Food = random.choice(snake_no_grids)
def display():
    pygame.draw.rect(screen,(0,0,0), (0,0,M*grid_size,N*grid_size))
    pygame.draw.rect(screen,(255,255,255), (Snake[0][0]*grid_size,Snake[0][1]*grid_size,grid_size,grid_size))
    for i in Snake[1:]:
        pygame.draw.rect(screen,(255,255,255), (i[0]*grid_size,i[1]*grid_size,grid_size,grid_size),1)
    pygame.draw.rect(screen,(0,255,0), (Food[0]*grid_size,Food[1]*grid_size,grid_size,grid_size))
    pygame.display.update()
def update_snake():
    global snake_tail,snake_head,snake_body,right_label
    x,y=Snake[0][0],Snake[0][1]
    if action == 'Right' :
        Snake.insert(0,(x+1,y))
    elif action == 'Left' :
        Snake.insert(0,(x-1,y))
    elif action == 'Top' :
        Snake.insert(0,(x,y-1))
    elif action == 'Bottum' :
        Snake.insert(0,(x,y+1))
    snake_tail=Snake.pop()
    snake_head=Snake[0]
    snake_body=Snake[1:len(Snake)]
    display()
    
def picking_one_from_two(lst,values=[1],n=0):
    if n<len(lst):
        (x,y)=lst[n]
        t,r,b,l=(x,y-1),(x+1,y),(x,y+1),(x-1,y)
        for i in [t,r,b,l]:
            if i in grids and i not in lst and i not in blocks:
                lst.append(i)
                values.append(values[n]+1)
        n+=1
        return picking_one_from_two(lst,values,n)
    else:
        return max(values),lst
    
def picking_one_from_three(ip):
    (x,y)=ip
    [t,r,b,l] =[(x,y-1),(x+1,y),(x,y+1),(x-1,y)]
    block=[0 if (i not in grids or i in Snake[:-1]) else 1 for i in [t,r,b,l]]
    if sum(block)==0:
        return (0,0)
    elif sum(block)==1:
        plc=block.index(1)
        a1=[t,r,b,l][plc]
        a2,lst=picking_one_from_two([a1],values=[1],n=0)
        return (a2,0)
    elif sum(block)==2:
        plc1=block.index(1)
        block[plc1]=0
        plc2=block.index(1)
        a2,b2=[t,r,b,l][plc1],[t,r,b,l][plc2]
        a3,lst=picking_one_from_two([a2],values=[1],n=0)
        a4,lst=picking_one_from_two([b2],values=[1],n=0)
        return (max(a3,a4),0)
    elif sum(block)==3:
        return (len(grids)-len(Snake),1)
    
def prediction():
    global action,block,blocks
    (x,y)=Snake[0]
    [t,r,b,l] =[(x,y-1),(x+1,y),(x,y+1),(x-1,y)]
    block=[0 if (i not in grids or i in Snake) else 1 for i in [t,r,b,l]]
    dist=[distance.euclidean(i, Food) for i in [t,r,b,l]]
    op=[dist[i] if block[i]==1 else 100 for i in range(4)]
    plc1=op.index(min(op))
    op[plc1]=101
    plc2=op.index(min(op))
    op[plc2]=101
    plc3=op.index(min(op))
    op[plc3]=101
    plc4=op.index(min(op))
    order=[[t,r,b,l][plc1],[t,r,b,l][plc2],[t,r,b,l][plc3],[t,r,b,l][plc4]]
    if sum(block)==4 or sum(block)==1 or len(Snake)==1:
        action=Actions[[t,r,b,l].index(order[0])]
    elif sum(block)==2:
        blocks=Snake[:-1]
        a1,lst=picking_one_from_two([order[0]],values=[1],n=0)
        if order[1] in lst:
            action=Actions[[t,r,b,l].index(order[0])]
        else:
           a2,lst=picking_one_from_two([order[1]],values=[1],n=0)
           if a1>a2:
               action=Actions[[t,r,b,l].index(order[0])]
           else:
               action=Actions[[t,r,b,l].index(order[1])]
    elif sum(block)==3:
        blocks=Snake[:-1]
        rn=[picking_one_from_three(k) for k in order]
        star=[rn[i][0] for i in range(3)]
        bk=[rn[i][1] for i in range(3)]
        if sum(bk)==3 or bk[0]==1 or sum(bk)==0:
            new_star=star
        elif sum(bk)==2 or sum(bk)==1:
            new_star=[star[_] if bk[_]==0 else 0.5 for _ in range(3)]
        plc=new_star.index(max(new_star))
        action=Actions[[t,r,b,l].index(order[plc])] 

mloop=True
while mloop:
    pygame.init()
    screen = pygame.display.set_mode((M*grid_size,N*grid_size))
    Snake=[random.choice(grids)]
    food()
    loop=True
    while loop:
        pygame.time.wait(snake_wait_time)
        prediction()
        update_snake()
        if snake_head==Food:
            food()
            Snake.append(snake_tail)
        elif snake_head not in grids or snake_head in snake_body:
            score=len(Snake)-1
            if score > High_score:
                High_score=score
            print('Episodes :',Episode,', High_score :',High_score,', Score :',score)
            Episode+=1
            loop=False
        ev=pygame.event.get()
        for event in ev:
            if event.type == pygame.QUIT:
                pygame.quit()
                loop=False
                mloop=False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    snake_wait_time+=25
                elif event.key == pygame.K_DOWN:
                    if snake_wait_time>=25:
                        snake_wait_time-=25