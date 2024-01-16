from pygame import *
from random import randint
from sys import exit
import data

init()


#Constants
WD,HT=1050,770
HERO_VEL=6
ENEMY_VEL=1
MISSILE_VEL=6
AMMO=20
HERO_HIT=USEREVENT+1
ENEMY_HIT=USEREVENT+2
HERO_BULLET_HIT=USEREVENT+3
game_activity='user'
mu=0

#Images
icon_=transform.rotate(
image.load('Assets\spaceship_red.png'),180)
hero_i=transform.rotate(transform.scale(
image.load('Assets\App-kspaceduel-spaceship-icon.png'),
(100,100)),180)
missile=transform.rotate(transform.scale(
image.load('Assets\missile.png'),
(32,32)),45)
bullet=transform.rotate(transform.scale(
image.load('Assets/bullet.png'),
(32,32)),180)
wp=transform.scale(
image.load(r'Assets\wp3205652.jpg'),(WD,HT))
space1=transform.scale(
image.load('Assets\photo-1570284613060-766c33850e00.jpeg'),(WD,HT))
space2=transform.scale(
image.load('Assets\Space_purple.jpg'),(WD,HT))
space3=transform.scale(
image.load('Assets\photo-1502134249126-9f3755a50d78.jpeg'),(WD,HT))
space4=transform.scale(transform.rotate(
image.load('Assets/529040.jpg'),90),(WD,HT))

enemy1=transform.scale(
image.load('Assets\spaceship_red.png'),(64,64))

#Music
mixer.music.load("Assets\cornfield_chase.mp3")
mixer.music.set_volume(0.25)

Hit_Sound=mixer.Sound("Assets\hit_sound.mp3")
Fire_Sound=mixer.Sound('Assets\Gun_Sound.mp3')
Hit_Sound.set_volume(0.5)
Fire_Sound.set_volume(0.5)
#Fonts
score_f=font.SysFont('arial', 30)
GameOver_f=font.SysFont('arial', 100)
starter_font=font.SysFont('arial', 60)
game_f=font.SysFont('arial', 120)

#Text
play_again=starter_font.render('Press Enter To Play Again',True,(255,255,255))
Game_Over_txt=GameOver_f.render('Game Over',True,(255,255,255))
login_txt=starter_font.render('Login',True,(255,255,255))
signup_txt=starter_font.render('Sign Up',True,(255,255,255))
enter_txt=starter_font.render('Enter',True,(255,255,255))
enter_rect=enter_txt.get_rect(center=(500,700))
login_rect=login_txt.get_rect(center=(300,600))
signup_rect=signup_txt.get_rect(center=(675,600))
username=starter_font.render('Username:',True,(255,255,255))
passwd=starter_font.render('Password:',True,(255,255,255))
txt1=''
txt2=''
txt1s=game_f.render(txt1,True,'white')
txt2s=txt2s=game_f.render(txt2,True,'white')
txt1_rect=Rect(400,210,630,138)
txt2_rect=Rect(400,400,630,138)
wp_txt=starter_font.render('Space War',True,(255,255,255))
#Lists
enemy_l=[]
enemy_li=[]
missile_l=[]
bullet_l=[]
bullet_li=[]
starter_l=[]
tb=[]
Space=[space1,space2,space3,space4]

#Screen
screen=display.set_mode((WD,HT))
display.set_caption('Space War')
display.set_icon(icon_)



#All the functions
def values():
    global hero,alpha,Score,Lives,Health,max_enemy,space,beta,iit
    iit=0
    Health=10
    max_enemy=2
    Lives=5
    Score=0
    alpha=0
    beta=AMMO
    hero=hero_i.get_rect(center=(500,600))
    space=space1
    mixer.music.rewind() 

values()
def change():
    global space,iit
    if iit<3:
        iit+=1
    else:
        iit=0
    space=Space[iit]


def win_display(hero,Health,Lives,Score,highscore,username):
    if Score%50!=0:
        score_str='Score: {}'.format((Score-1))
    elif Score%50==0:
        score_str='Score: {}'.format((Score))
    health_txt=score_f.render('Health: {}'.format(Health),True,(255,255,255))
    lives_txt=score_f.render('Lives: {}'.format(Lives),True,(255,255,255))
    HS_txt=score_f.render(f'High Score: {highscore}',True,(255,255,255))
    score_txt=score_f.render(score_str,True,(255,255,255))
    us_name_txt=score_f.render(f'User: {username}',True,(255,255,255))
    
    screen.blit(space,(0,0))
    screen .blit(hero_i,hero.topleft)
    screen.blit(HS_txt,(325,20))
    screen.blit(health_txt,(10,20))
    screen.blit(lives_txt,(550,20))
    screen.blit(score_txt,(175,20))
    screen.blit(us_name_txt,(675,20))

    if alpha==AMMO:
        ammo_txt=score_f.render('Ammo: Reloading...',True,(255,255,255))
    else:
        ammo_txt=score_f.render('Ammo: {}'.format(beta),True,(255,255,255))
        
    
    for j in range(len(enemy_l)):
        screen .blit(enemy_li[j],(enemy_l[j].x,enemy_l[j].y))
        if enemy_l[j].y>starter_l[j] and Lives!=0 and bullet_l[j].y>enemy_l[j].y:
            screen .blit(bullet_li[j],(bullet_l[j].x,bullet_l[j].y))
    
    screen.blit(ammo_txt,(850,20))


def hero_movement(key_):
    if Lives!=0:
        if key_[K_LEFT] and hero.x>-10:    #LEFT
            hero.x-=HERO_VEL
        if key_[K_RIGHT] and hero.x<(WD-90):   #RIGHT
            hero.x+=HERO_VEL
        if key_[K_UP] and hero.y>(3*(HT/4))-40:  #UP
            hero.y-=HERO_VEL
        if key_[K_DOWN] and hero.y<(HT-101):    #DOWN
            hero.y+=HERO_VEL

def Ammunition_Movement(t):
    global tb
    for i in missile_l:
        if i.y<=1:
            missile_l.remove(i)
    for i in missile_l:
        a=Rect.collidelist(i,enemy_l)
        if a!=-1:
            Hit_Sound.play()
            missile_l.remove(i)
            event.post(event.Event(ENEMY_HIT))
            enemy_l.pop(a)
            enemy_li.pop(-1)
            bullet_l.pop(a)
            tb.pop(a)
            bullet_li.pop(-1)
            starter_l.pop(-1)
        i.y-=MISSILE_VEL
        screen.blit(missile,i.topleft)
        
            

    for i in range(len(bullet_l)):
        if Lives!=0:
            if enemy_l[i].y>starter_l[i] and (t-tb[i])>3000 and bullet_l[i].y<HT+1000:
                bullet_l[i].y+=MISSILE_VEL
            else:
                bullet_l[i].y=enemy_l[i].y
            collide=Rect.collidelist(bullet_l[i],missile_l)
            if Rect.colliderect(bullet_l[i],hero):
                event.post(event.Event(HERO_BULLET_HIT))
                bullet_l[i].y=enemy_l[i].y
                Hit_Sound.play()
                tb[i]=time.get_ticks()
            elif collide!=(-1):
                Hit_Sound.play()
                bullet_l[i].y=enemy_l[i].y
                tb[i]=time.get_ticks()
                missile_l.pop(collide)
    

def enemy():
    while len(enemy_l)+1<=max_enemy:
        enemy_rect=Rect(randint(0,WD-65),randint(-500,-65),64,64)
        bullet_rect=Rect(enemy_rect.x+15,enemy_rect.y,32,32)
        starter=randint(0,100)
        enemy_l.append(enemy_rect)
        bullet_l.append(bullet_rect)
        bullet_li.append(bullet)
        tb.append(0)
        starter_l.append(starter)
        enemy_li.append(enemy1)


def enemy_movement():
    for i in range(len(enemy_l)):
        if Lives!=0:
            enemy_l[i].y+=ENEMY_VEL
    for i in enemy_l:
        if i.y>HT+2 or hero.colliderect(i):
            if hero.colliderect(i):
                Hit_Sound.play()
            a=enemy_l.index(i)
            enemy_l.remove(i)
            bullet_l.pop(a)
            tb.pop(a)
            enemy_li.pop(-1)
            bullet_li.pop(-1)
            starter_l.pop(-1)
            event.post(event.Event(HERO_HIT))


def Start():
    screen.fill((0,0,0))
    starter_game=game_f.render('Space Wars',True,(0,96,255))
    starter_start=starter_font.render('Press Enter To Begin',True,(0,96,255))
    starter_txtins=score_f.render("How to Play",True,(0,96,255))
    starter_txt1=score_f.render('1. Prevent the enemies from reaching your base.',True,(0,96,255))
    starter_txt2=score_f.render('2. Shoot them using the SPACE BAR.',True,(0,96,255))
    starter_txt3=score_f.render('3. When your health becomes zero, you lose one life',True,(0,96,255))
    starter_txt4=score_f.render('4. Crashing with enemy will decrease your life.',True,(0,96,255))
    starter_txt5=score_f.render('5. Move the hero using ARROW KEYS.',True,(0,96,255))
    starter_txt6=score_f.render('6. Be careful of the enemy firearms',True,(0,96,255))
    starter_txt7=score_f.render('7. Press R to reload',True,(0,96,255))

    screen.blit(starter_game,(WD/2-starter_game.get_width()/2,100))
    screen.blit(starter_start,(WD/2-starter_start.get_width()/2,HT/2-100))
    screen.blit(starter_txtins,(WD/2-starter_start.get_width()/2,HT/2-10))
    screen.blit(starter_txt1,(WD/2-starter_start.get_width()/2,HT/2+35))
    screen.blit(starter_txt2,(WD/2-starter_start.get_width()/2,HT/2+70))
    screen.blit(starter_txt3,(WD/2-starter_start.get_width()/2,HT/2+105))
    screen.blit(starter_txt4,(WD/2-starter_start.get_width()/2,HT/2+140))
    screen.blit(starter_txt5,(WD/2-starter_start.get_width()/2,HT/2+175))
    screen.blit(starter_txt6,(WD/2-starter_start.get_width()/2,HT/2+210))
    screen.blit(starter_txt7,(WD/2-starter_start.get_width()/2,HT/2+245))

def user():
    screen.blit(wp,(0,0))
    draw.rect(screen,"red",login_rect,7,4)
    draw.rect(screen,'green',signup_rect,7,4)
    draw.rect(screen,"red",login_rect,0,4)
    draw.rect(screen,"green",signup_rect,0,4)
    screen.blit(login_txt,login_rect.topleft)
    screen.blit(wp_txt,(350,100))
    screen.blit(signup_txt,signup_rect.topleft)

def enter(txt1s,txt1_rect,txt2s,txt2_rect):
    screen.blit(wp,(0,0))
    screen.blit(username,(100,200))
    screen.blit(passwd,(100,400))
    draw.rect(screen,'yellow',txt1_rect,0,7)
    draw.rect(screen,'yellow',txt2_rect,0,7)
    screen.blit(txt1s,txt1_rect.topleft)
    screen.blit(txt2s,txt2_rect.topleft)
    draw.rect(screen,'orange',enter_rect,7,4)
    draw.rect(screen,"orange",enter_rect,0,4)
    screen.blit(enter_txt,enter_rect.topleft)


def main():
    global Health,Lives,Score,alpha,max_enemy,beta,game_activity,txt1,txt2,txt1s,txt2s,mu
    FPS=time.Clock()
    gamma=0
    t=0
    s=0
    h=0
    static_time=0
    while True:
        FPS.tick(60)
        t=time.get_ticks()
        for i in event.get():
            if i.type==QUIT:
                quit()
                exit()

            if game_activity=='user':
                if i.type==MOUSEBUTTONDOWN:
                    if login_rect.collidepoint(i.pos):
                        game_activity='login'
                        print(game_activity)
                    elif signup_rect.collidepoint(i.pos):
                        game_activity='signup'
                        print(game_activity)

            elif game_activity=='login' or game_activity=='signup':
  
                txt1s=game_f.render(txt1,True,'white')
                txt2s=game_f.render(txt2,True,'white')
                mo=mouse.get_pos()
                if i.type==KEYDOWN:
                    if txt1_rect.collidepoint(mo):
                        if i.key==K_BACKSPACE:
                            txt1=txt1[:-1]
                        elif len(txt1)<=10 and i.key!=K_BACKSPACE:
                            txt1+=i.unicode
                    elif txt2_rect.collidepoint(mo):
                        if i.key==K_BACKSPACE:
                            txt2=txt2[:-1]
                        elif len(txt2)<=10 and i.key!=K_BACKSPACE:
                            txt2+=i.unicode
                elif enter_rect.collidepoint(mo):
                    if i.type==MOUSEBUTTONDOWN:
                        if game_activity=='login':
                            if data.check(txt1,txt2):
                                username=txt1
                                password=txt2
                                game_activity='instruction'
                            else:
                                txt1='Try'
                                txt2='Again'
                        elif game_activity=='signup':
                            a=data.new(txt1,txt2)
                            if a==-1:
                                txt1='Username'
                                txt2='Taken'
                            else:
                                username=txt1
                                game_activity='instruction'
            
            elif game_activity=='start':
                if i.type==KEYDOWN:                
                    if i.key==K_SPACE and alpha<AMMO and Lives!=0 :
                        missile_rect=Rect(hero.x+25,hero.y-20,32,32)
                        missile_l.append(missile_rect)
                        alpha+=1
                        beta-=1
                    if i.key==K_r and alpha!=0:
                        alpha=AMMO
                if i.type==HERO_BULLET_HIT and Lives!=0:
                    Health-=1
                if i.type==HERO_HIT and Lives!=0:
                    Lives-=1
                if i.type==ENEMY_HIT and Lives!=0:
                    Score+=50
            
            elif game_activity=='gameover':
                if i.type==KEYDOWN:
                    if i.key==K_RETURN:
                        enemy_l.clear()
                        enemy_li.clear()
                        bullet_l.clear()
                        bullet_li.clear()
                        game_activity='start'
                        values()
            elif game_activity=="instruction":
                if i.type==KEYDOWN:
                    if i.key==K_RETURN:
                        game_activity='start' 


        if game_activity=='instruction':
            Start()            
        elif game_activity=="user":
            user()
        elif game_activity=="login" or game_activity=='signup':
            enter(txt1s,txt1_rect,txt2s,txt2_rect)
        elif game_activity=='start':
            if mu==0:
                mixer.music.play(-1)
                mu+=1
            key_=key.get_pressed()
            highscore=data.give(username)

            if Health==0 and Lives!=0:
                Health=10
                Lives-=1 
            if alpha==AMMO and static_time==0:
                    s=time.get_ticks()
                    static_time=1
            if (t-s)>5000 and alpha==AMMO:
                alpha=0
                beta=AMMO
                static_time=0
            if Score%500==0 and Score!=0:
                Score+=100
                max_enemy+=1
                change()
            if Score>=highscore:
                data.update(username,Score)
            if Lives==0:
                game_activity='gameover'            
            enemy()
            win_display(hero,Health,Lives,Score,highscore,username )
            Ammunition_Movement(t)
            hero_movement(key_)
            enemy_movement()
        elif game_activity=='gameover':
            screen.fill('black')
            screen.blit(Game_Over_txt,((WD/2-Game_Over_txt.get_width()/2),HT/2-100))
            screen.blit(play_again,((WD/2-play_again.get_width()/2),HT/2+30))
            mixer.music.pause()
            mu=0
        display.update()


if __name__=='__main__':
    main()
