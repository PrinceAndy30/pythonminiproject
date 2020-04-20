#meteorBrown_big1.png,laserGreen10.png,laserRed03.png,sfx_laser2.ogg,sfx_lose.ogg and explosion sounds from kenney.nl
#spacecraft_enemy.png from redhulimachinelearning.com 
#villain.png from flaticon.com 
#Game Type C.mp3 from vgmdownloads.com 
#FrostbiteBossFight-dL0Z.ttf from fontspace.co
#star-wars-jedi-starfighter.png from nicepng.com
import pygame 
import sys 
import random 
import math 
pygame.mixer.pre_init(44100,16,2,4096)#pygame module for loading and playing sounds
pygame.init()  #initialize all imported pygame modules
FPS=20

#screen width and height
WIDTH=1500 
HEIGTH=750  

Fontcolour=[184, 25, 4]
scorecolor=[50, 168, 82]
BLACK=[0,0,0] 
Fontcolour2=[245,144,66]

#size of the sprites 
player_size=60  
enemy_size=40 
lazer_size=10

#loading player image 
ship=pygame.image.load('star-wars-jedi-starfighter.png') 
ship=pygame.transform.scale(ship,(player_size,player_size))
 

#loading alien image
alienship=pygame.image.load('spacecraft_enemy.png') 
alienship=pygame.transform.scale(alienship,(player_size,player_size))
 

#loading meteor image
meteor=pygame.image.load('meteorBrown_big1.png') 
meteor=pygame.transform.scale(meteor,(enemy_size,enemy_size))

#various font definitions
font0=pygame.font.Font('kenvector_future_thin.ttf',40)
font1=pygame.font.Font('FrostbiteBossFight-dL0Z.ttf',150) 
font2=pygame.font.Font('FrostbiteBossFight-dL0Z.ttf',44) 
font3=pygame.font.Font('FrostbiteBossFight-dL0Z.ttf',70) 
font4=pygame.font.Font('FrostbiteBossFight-dL0Z.ttf',60) 

#score count
score=0

#loading laser image
lazer=pygame.image.load('laserGreen10.png') 
lazer=pygame.transform.scale(lazer,(lazer_size,40))

#loading alien laser image
a_lazer=pygame.image.load('laserRed03.png') 
a_lazer=pygame.transform.scale(a_lazer,(lazer_size,40))


#getting display screen
screen=pygame.display.set_mode((WIDTH,HEIGTH))  

#background image
background_pic=pygame.image.load('starwars.png').convert() 
background_pic=pygame.transform.scale(background_pic,(WIDTH,HEIGTH)) 
back_gnd=background_pic

#Game title and icon
pygame.display.set_caption('Battlestar Galactica') 
icon=pygame.image.load('villain.png')
pygame.display.set_icon(icon)

#setting frames per second
clock= pygame.time.Clock()  

#loading background music
pygame.mixer.music.load('Game Type C.mp3') 
pygame.mixer.music.set_volume(0.15) 
pygame.mixer.music.play(-1)#music plays,'-1' indicates that music is looped indefinitely

#loading different sound effcts
shot=pygame.mixer.Sound('sfx_laser2.ogg') 
shot.set_volume(0.4)
lose=pygame.mixer.Sound('sfx_lose.ogg') 
lose.set_volume(1)
explo1=pygame.mixer.Sound('Explosion+1.wav') 
explo1.set_volume(0.25)
explo2=pygame.mixer.Sound('Torpedo+Explosion.wav') 
explo2.set_volume(0.2)

#game running conditions
game_over= False  
main_scn=True

#defining and loading explosion effects
explo_anima={} 
explo_anima['large']=[] 
explo_anima['small']=[] 
for i in range(4): 
	filename='tank_explosion{}.png'.format(i) 
	imag=pygame.image.load(filename).convert()
	imag_lg=pygame.transform.scale(imag,(75,75)) 
	explo_anima['large'].append(imag_lg)
	imag_sm=pygame.transform.scale(imag,(32,32)) 
	explo_anima['small'].append(imag_sm)

#player bullet as sprite
class Bullets(pygame.sprite.Sprite): 
	def __init__ (self,x,y): 
		pygame.sprite.Sprite .__init__(self) 
		self.image=lazer
		self.rect=self.image.get_rect() 
		self.rect.bottom=y
		self.rect.centerx=x 
		self.speedy=-10 
	def update(self): 
		self.rect.y+=self.speedy
		if self.rect.bottom<0 : 
			self.kill()	

#alien bullet as sprite
class ABullets(pygame.sprite.Sprite): 
		def __init__ (self,x,y): 
			pygame.sprite.Sprite .__init__(self) 
			self.image=a_lazer
			self.rect=self.image.get_rect() 
			self.rect.bottom=y
			self.rect.centerx=x 
			self.speedy=5 
		def update(self): 
			self.rect.y+=self.speedy
			if self.rect.bottom>HEIGTH : 
				self.kill()	

#alien as sprite
class Alien(pygame.sprite.Sprite):
	
	def __init__ (self): 
		pygame.sprite.Sprite .__init__(self) 
		self.image=alienship
		self.rect=self.image.get_rect() 
		self.rect.centerx=random.randrange(0,WIDTH/2) 
		self.rect.top=0
		self.spd=1 
		self.shoot_delay = 1000
		self.last_shot=pygame.time.get_ticks()	
		self.num_of_shots = 1#s
	def shoot(self):
		current_time = pygame.time.get_ticks()
		if current_time - self.last_shot > self.shoot_delay:
			shot.play()
			self.last_shot = current_time
			a_bullets=ABullets(self.rect.centerx,self.rect.bottom) 
			all_sprites.add(a_bullets)
			a_bullet.add(a_bullets)


	def update(self): 
		self.rect.x+=self.spd  
		if self.rect.right>WIDTH: 
			self.rect.centerx=random.randrange(0,WIDTH/2) 
		if self.rect.left > 0 and self.rect.right < WIDTH:
			for i in range(self.num_of_shots):
				self.shoot()
					

#player as sprite
class myPlayer(pygame.sprite.Sprite): 
	def __init__ (self): 
		pygame.sprite.Sprite .__init__(self) 
		self.image=ship
		self.rect=self.image.get_rect() 
		self.rect.centerx=WIDTH/2 
		self.rect.bottom=HEIGTH-2*player_size
		self.spd1=0 
		self.spd2=0	
		self.shoot_delay = 250
		self.last_shot=pygame.time.get_ticks()
	
	def update(self): 
		self.spd1=0 
		self.spd2=0
		key=pygame.key.get_pressed() 
		if key[pygame.K_LEFT]: 
			self.spd1= -3
		if key[pygame.K_RIGHT]: 
			self.spd1= 3 
		if key[pygame.K_UP]: 
			self.spd2= -3 
		if key[pygame.K_DOWN]: 
			self.spd2= 3 
		if key[pygame.K_SPACE]: 
			self.shoot()
		self.rect.x +=self.spd1
		self.rect.y +=self.spd2 
		if self.rect.right>WIDTH: 
			self.rect.right=WIDTH
		if self.rect.left<0: 
			self.rect.left=0 
		if self.rect.top<0: 
			self.rect.top=0 
		if self.rect.bottom>HEIGTH: 
			self.rect.bottom=HEIGTH	

	def shoot(self): 
		now = pygame.time.get_ticks() 
		if now-self.last_shot>self.shoot_delay: 
			self.last_shot=now
			bullets=Bullets(self.rect.centerx,self.rect.top) 
			all_sprites.add(bullets)
			shot.play()
			bullet.add(bullets) 

#meteors
class Enemies(pygame.sprite.Sprite): 
	def __init__ (self): 
		pygame.sprite.Sprite .__init__(self) 
		self.image=meteor
		self.rect=self.image.get_rect() 
		self.rect.x=random.randrange(0,WIDTH-enemy_size)
		self.rect.y=random.randrange(-100,-40) 
		self.espd=random.randrange(1,3) 
		self.speedx=random.randrange(-2,2)
		
	def update(self): 
		self.rect.y+=self.espd 
		self.rect.x+=self.speedx
		if self.rect.top>HEIGTH : 
			
			self.rect.x=random.randrange(0,WIDTH-enemy_size)
			self.rect.y=random.randrange(-100,-10) 
			self.espd=random.randrange(1,3) 

#explosion as sprite
class Explosion(pygame.sprite.Sprite): 
	def __init__(self,center,size): 
		pygame.sprite.Sprite.__init__(self) 
		self.size=size 
		self.image=explo_anima[self.size][0] 
		self.rect=self.image.get_rect() 
		self.rect.center=center 
		self.frame=0 
		self.last_update=pygame.time.get_ticks() 
		self.frame_rate=50

	def update(self): 
		now=pygame.time.get_ticks() 
		if now-self.last_update > self.frame_rate: 
			self.last_update=now 
			self.frame+=1 
			if self.frame==len(explo_anima[self.size]): 
				self.kill() 
			else:
				center=self.rect.center 
				self.image=explo_anima[self.size][self.frame] 
				self.rect=self.image.get_rect() 
				self.rect.center=center 

#main screen
def main_screen(): 
	screen.blit(back_gnd,(0,0)) 
	game=font1.render('BATTLESTAR GALACTICA',1,(Fontcolour)) 
	screen.blit(game,(WIDTH/12,HEIGTH/5)) 
	game=font2.render('Arrow keys to move & hold Space to shoot',1,Fontcolour2) 
	screen.blit(game,(WIDTH/3.5,HEIGTH/1.5)) 
	game=font2.render('Press R to play',1,Fontcolour2) 
	screen.blit(game,(WIDTH/2.5,HEIGTH/1.2))
	pygame.display.flip() 
	waiting=True 
	#waiting till player presses R or quits
	while waiting : 
		clock.tick(FPS) 
		for event in pygame.event.get() : 
			if event.type == pygame.QUIT: 
				pygame.quit() 
			if event.type == pygame.KEYUP: 
				if event.key==pygame.K_r: 
					waiting=False 


##################### MAIN GAME LOOP #################################
while not game_over: 
	#game over screen condition
	if main_scn : 
		main_screen() #calling main screen
		main_scn=False 
		score=0
		all_sprites = pygame.sprite.Group()# creating sprite group for all sprites
		player=myPlayer() #creating player sprite
		player_group=pygame.sprite.Group() #player sprite group
		player_group.add(player)
		a_group=pygame.sprite.Group()#alien sprite group
		a_bullet=pygame.sprite.Group()#alien bullet sprite group
		enemy=pygame.sprite.Group()#meteor sprite group
		bullet=pygame.sprite.Group()#player bullet sprite group
		for i in range(6): #spawning aliens
					alien=Alien() #alien sprite
					all_sprites.add(alien) 
					a_group.add(alien)
					
		all_sprites.add(player) 
		
		for i in range(10):#spawing enemies 
			e=Enemies()
			all_sprites.add(e) 
			enemy.add(e)

	for event in pygame.event.get():
		
	
		if event.type==pygame.QUIT: #quiting game condition
			sys.exit()
		
	
	all_sprites.update()	#updating all sprites	

	#conditions to draw and update all sprites
	screen.fill(BLACK) 
	screen.blit(back_gnd,(0,0))
	all_sprites.draw(screen) 
	
	#all collution conditions
	hit1=pygame.sprite.spritecollide(player,enemy,False)#player with meteors
	hit2=pygame.sprite.groupcollide(enemy,bullet,True,True)#meteor with player bullets
	hit3=pygame.sprite.groupcollide(player_group,a_group,True,True)#player with aliens
	hit4=pygame.sprite.groupcollide(a_group,bullet,True,True)#aliens with player bullets
	hit5=pygame.sprite.spritecollide(player,a_bullet,False)#player with alien bullets

	#condition to destroy meteor
	for hit in hit2: 
		explo1.play()
		e=Enemies()
		all_sprites.add(e) 
		expl1=Explosion(hit.rect.center,'small')#small explosion sprite
		all_sprites.add(expl1)
		enemy.add(e)
	
	#score condition
	if hit2: 
		score+=1
	if hit4: 
		score+=5
	
	#condtion to destroy aliens
	for hit in hit4: 
		explo2.play()
		alien=Alien() 
		all_sprites.add(alien) 
		expl2=Explosion(hit.rect.center,'large')#large explotion sprite
		all_sprites.add(expl2)
		a_group.add(alien)


	if hit1 or hit3 or hit5: 
		lose.play() #play game over effect
		
		#condition for game over screen
		screen.fill(BLACK)
		screen.blit(back_gnd,(0,0)) 
		game=font3.render('Bears',1,(Fontcolour)) 
		screen.blit(game,(WIDTH/15,HEIGTH/5))
		game=font3.render('beets',1,(Fontcolour)) 
		screen.blit(game,(WIDTH/15,HEIGTH/3))
		game=font3.render('battlestar galactica!!',1,(Fontcolour)) 
		screen.blit(game,(WIDTH/15,HEIGTH/2))	
		text1='Your Score: '+ str(score)  
		label1=font4.render(text1,1,scorecolor) 
		screen.blit(label1,(WIDTH/10,HEIGTH/1.2))
		pygame.display.flip() 
		pygame.time.wait(2000)
		main_scn=True 

	#display and update score in main game
	text='Score:'+ str(score)  
	label=font0.render(text,1,scorecolor) 
	screen.blit(label,(WIDTH-250,HEIGTH-40))
 	

	pygame.display.flip()
	pygame.display.update() 
######################################################################	
