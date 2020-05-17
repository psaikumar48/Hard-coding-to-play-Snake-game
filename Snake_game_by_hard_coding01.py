import pygame
import random
from scipy.spatial import distance

M,N,grid_size=20,20,20
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
    snake_body=Snake[1:-1]
    display()
def prediction():
    global action
    (x,y)=Snake[0]
    [r,l,t,b]=[(x+1,y),(x-1,y),(x,y-1),(x,y+1)]
    block=[0 if (i not in grids or i in Snake[:-1]) else 1 for i in [t,r,b,l]]
    dist=[distance.euclidean(i,Food) for i in [t,r,b,l]]   
    op=[dist[i] if block[i]==1 else 100 for i in range(4)]
    right_label=op.index(min(op))
    action=Actions[right_label]

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
                if event.key == pygame.K_DOWN:
                    snake_wait_time+=25
                elif event.key == pygame.K_UP:
                    if snake_wait_time>=25:
                        snake_wait_time-=25