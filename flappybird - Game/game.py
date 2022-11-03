import pygame  
import random as rn



pygame.font.init()
WINDOW_H=924  
WINDOW_W=575
FONT=pygame.font.SysFont("comicsans",50)
BIRD_IMGS = [pygame.transform.scale2x(pygame.image.load('data\\bird1.png')),pygame.transform.scale2x(pygame.image.load('data\\bird2.png')),pygame.transform.scale2x(pygame.image.load('data\\bird3.png'))]

PIPE_IMGS=pygame.transform.scale2x(pygame.image.load('data\\pipe.png'))
BASE_IMGS=pygame.transform.scale2x(pygame.image.load('data\\base.png'))
BG_IMGS=pygame.transform.scale2x(pygame.image.load('data\\bg.png'))     


pygame.init()
global win
win=pygame.display.set_mode((WINDOW_W,WINDOW_H))
pygame.display.set_caption("Flappy-bird-BY RAMZEY")

class Bird():
    def __init__(self,x,y,radius):
        self.x=x
        self.y=y
        self.radius=radius
        self.alive=True
        self.timecount=0
        self.isjumb=False
        self.way=1
        self.movecount=0
        self.img=BIRD_IMGS[0]
        self.tilt=0

    def draw(self,win):
        if self.movecount<10 :
           self.img=BIRD_IMGS[0]
        elif self.movecount<15:
           self.img=BIRD_IMGS[1]
        elif self.movecount<20:
            self.img=BIRD_IMGS[2]
        else:
            self.img=BIRD_IMGS[0]
            self.movecount=0

        rotared_img = pygame.transform.rotate(self.img,self.tilt)
        new_rect=rotared_img.get_rect(center=self.img.get_rect(topleft=(self.x,self.y)).center)
        win.blit( rotared_img,new_rect)
        self.movecount+=1
    def move(self):
        if(self.isjumb==False):
            self.y+=((self.timecount**2)*0.5)/10
            self.timecount+=1
        
        else:
            self.y-=((self.timecount**2)*0.5)/75
            self.timecount+=1
            if(self.timecount>-10):
                self.isjumb=False
                self.timecount=1
                
        if self.timecount<-10:
            self.tilt=25   
        elif self.timecount<5:
            self.tilt=0 
        elif self.timecount>10 and self.timecount<20:
            self.tilt=-20
        elif self.timecount>20:
            self.tilt=-60
    def jumb(self):
        if(self.timecount>-10):
            self.isjumb=True
            self.timecount=-40 
    def getMask(self):
        return pygame.mask.from_surface(self.img)
class Pipe():
    space=400  
    
    def __init__(self,height) :
        self.x=Pipe.space
        self.height=height
        self.speed=5
        self.img_down=PIPE_IMGS
        self.img_up=pygame.transform.flip(self.img_down,False,True)
        self.passed=False
        Pipe.space+=400

        
    def draw(self,win):
        win.blit(self.img_up,(self.x,(self.height-640)))
        win.blit(self.img_down ,(self.x,(self.height+200)))
        self.x-=self.speed
    def collide(self,bird):
        bird_mask=bird.getMask()
        down_mask=pygame.mask.from_surface(self.img_down)
        down_offset=(self.x-bird.x,(self.height+200)-round(bird.y))
        down_point=bird_mask.overlap(down_mask,down_offset)
        if down_point!=None:
            return True
        return False

    def collide_up(self,bird):
        bird_mask=bird.getMask()
        up_mask=pygame.mask.from_surface(self.img_up)
        up_offset=(int(self.x-bird.x+40),int((self.height-50)-(bird.y)))
        up_point=up_mask.overlap(bird_mask,up_offset)
        if up_point !=None:
            return True
        return False
class Base():
    def __init__(self):
        self.img1=BASE_IMGS
        self.img2=BASE_IMGS
        self.x1=0
        self.x2=WINDOW_W
        self.speed=5
    def draw(self,win):
        win.blit(self.img1,(self.x1,WINDOW_H-124))
        win.blit(self.img2,(self.x2,WINDOW_H-124))
    def move(self):
        if self.x1+WINDOW_W<0:
            self.x1=WINDOW_W
            
        elif self.x2+WINDOW_W<0:
            self.x2=WINDOW_W
        self.x1-=self.speed
        self.x2-=self.speed
    def collide(self,bird):
        if bird.y>WINDOW_H-124:
            return True
        return False

def generate_pipes():
    pipe1=rn.randrange(150,450,20)
    return pipe1


    
global Run
Run=True    





def draw_game(bird,pipes,base,score):
    global win,Run
    win.blit(BG_IMGS,(0,0))
    bird.draw(win)
    text=FONT.render("Score:"+str(score),True,(255,255,255))

    bird.move()
    for pipe in pipes:
        pipe.draw(win)
        if pipe.collide(bird):Run=False
        if pipe.collide_up(bird):Run=False 
        
    win.blit(text,(WINDOW_W-10-text.get_width(),10))
        
            
    base.draw(win)
    base.move()

    pygame.display.update()
    

def main():
    global pipes_x,Run
    score=0
    clock=pygame.time.Clock()
    bird=Bird(120,80,20)
    pipes=[]
    for i in range(0,100):
        pipes.append(Pipe(generate_pipes()))
    pipes.count
    base=Base()
    while Run:
        clock.tick(30)
        events=pygame.event.get()
        for e in events :
            if e.type == pygame.QUIT:
                quit()
        kyes=pygame.key.get_pressed()
        if kyes[pygame.K_SPACE]:
            bird.jumb()
        if base.collide(bird):
            Run=False
        draw_game(bird,pipes,base,score)
        for pipe in pipes:
            if bird.x>pipe.x+PIPE_IMGS.get_width() and pipe.passed==False:
                score+=1
                pipe.passed=True
            if pipe.x+PIPE_IMGS.get_width()<0:
                pipes.remove(pipe)

              
 
main()






