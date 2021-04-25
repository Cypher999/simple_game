import pygame
import random

class Main_game:
    def __init__(this,panjang,lebar):
        pygame.init()
        pygame.font.init()
        this.panjang=panjang
        this.lebar=lebar
        this.layar=pygame.display.set_mode((this.panjang,this.lebar))
        pygame.display.set_caption("Game")
        this.font=pygame.font.Font("freesansbold.ttf",12)
        this.selesai=False
        this.hero_pos_x=10
        this.hero_pos_y=550
        this.enemy=[]
        this.hr=Hero(this.hero_pos_x,this.hero_pos_y,50,10,this)
        this.key={
            "fire":False,
            }
        this.score=0
        while not this.selesai:
            this.score_display=this.font.render("Score :"+str(this.score),True,(0,100,100))
            this.mouse_pos_x, this.mouse_pos_y=pygame.mouse.get_pos()
            this.hr.pos_x=int(this.mouse_pos_x)-20
            this.hr.pos_y=this.mouse_pos_y
            this.layar.fill((0,0,0))
            this.hr.make_sprite()
            this.layar.blit(this.score_display,(4,4))
            for kejadian in pygame.event.get():
                this.check_keypress(kejadian)
                if kejadian.type==pygame.QUIT:
                    this.selesai=True            
            this.hr.check_movement()
            enemy_showup=random.randint(0,100)
            enemy_pos=random.randint(0,(int(this.panjang)-50))
            if enemy_showup==15:
                this.enemy.append(Enemy(enemy_pos,0,20,20,this))
            for enemy in this.enemy:
                enemy.make_sprite()
                enemy.check_fire()
            if len(this.hr.fire)>0:
                for hero_fire in this.hr.fire:
                    hero_fire.make_sprite()
            pygame.display.flip()
    def check_keypress(this,kejadian):
        if kejadian.type==pygame.KEYDOWN:
            if kejadian.key==pygame.K_SPACE:
                this.key["fire"]=True
        if kejadian.type==pygame.KEYUP:
            if kejadian.key==pygame.K_SPACE:
                this.key["fire"]=False
        if kejadian.type==pygame.MOUSEBUTTONDOWN:
            if kejadian.button==1:
                this.key["fire"]=True
        if kejadian.type==pygame.MOUSEBUTTONUP:
            if kejadian.button==1:
                this.key["fire"]=False

class Fire:
    def __init__(this,pos_x,pos_y,panjang,lebar,game,speed):
        this.panjang=panjang
        this.lebar=lebar
        this.game=game        
        this.pos_x=pos_x
        this.pos_y=pos_y
        this.speed=speed
    def make_sprite(this):
        pygame.draw.rect(this.game.layar,(0,125,230),pygame.Rect(this.pos_x,this.pos_y,this.panjang,this.lebar))
        this.pos_y-=this.speed
        if this.pos_y<=0:
            if this in this.game.hr.fire:
                this.game.hr.fire.remove(this)


class Enemy:
    def __init__(this,pos_x,pos_y,panjang,lebar,game):
        this.panjang=panjang
        this.lebar=lebar
        this.game=game        
        this.pos_x=pos_x
        this.pos_y=pos_y        
    def check_fire(this):
        for hero_fire in this.game.hr.fire:
            max_enemy_x=this.pos_x+this.panjang
            max_enemy_y=this.pos_y+this.lebar
            max_fire_x=hero_fire.pos_x+hero_fire.panjang
            max_fire_y=hero_fire.pos_y+hero_fire.lebar
            if (((hero_fire.pos_x>=this.pos_x)and(hero_fire.pos_x<=max_enemy_x))or ((max_fire_x>=this.pos_x)and(max_fire_x<=max_enemy_x))):
                if (((hero_fire.pos_y>=this.pos_y)and(hero_fire.pos_y<=max_enemy_y))or ((max_fire_y>=this.pos_x)and(max_fire_y<=max_enemy_y))):
                    if hero_fire in this.game.hr.fire:
                        this.game.hr.fire.remove(hero_fire)
                    if this in this.game.enemy:
                        this.game.enemy.remove(this)
                        this.game.score+=10
    def make_sprite(this):
        pygame.draw.rect(this.game.layar,(0,125,255),pygame.Rect(this.pos_x,this.pos_y,this.panjang,this.lebar))
        this.pos_y+=1
        if this.pos_y>this.game.lebar:
            if this in this.game.enemy:
                this.game.enemy.remove(this)
    


class Hero:
    def __init__(this,pos_x,pos_y,panjang,lebar,game):
        this.panjang=panjang
        this.lebar=lebar
        this.game=game        
        this.pos_x=pos_x
        this.pos_y=pos_y
        this.fire=[]
    def make_sprite(this):
        x_tengah=(int(this.pos_x)-5)+(float(this.panjang)/2)
        pygame.draw.rect(this.game.layar,(0,125,125),pygame.Rect(this.pos_x,this.pos_y,this.panjang,this.lebar))
        pygame.draw.rect(this.game.layar,(0,125,125),pygame.Rect(x_tengah,int(this.pos_y)-10,10,10))
    def check_movement(this):
        x_tengah=(int(this.pos_x)-5)+(float(this.panjang)/2)
        if this.game.key["fire"]==True:
            if len(this.fire)<10:
                this.fire.append(Fire(x_tengah,int(this.pos_y)-10,3,1,this.game,5))
Main_game(600,600)
