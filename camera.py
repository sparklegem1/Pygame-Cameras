import pygame, sys
from random import randint

class Tree(pygame.sprite.Sprite):
	def __init__(self,pos,group):
		super().__init__(group)
		self.image = pygame.image.load('graphics/tree.png').convert_alpha()
		self.rect = self.image.get_rect(topleft = pos)

class Player(pygame.sprite.Sprite):
	def __init__(self,pos,group):
		super().__init__(group)
		self.image = pygame.image.load('graphics/player.png').convert_alpha()
		self.rect = self.image.get_rect(center = pos)
		self.direction = pygame.math.Vector2()
		self.speed = 5

	def input(self):
		keys = pygame.key.get_pressed()

		if keys[pygame.K_w]:
			self.direction.y = -1
		elif keys[pygame.K_s]:
			self.direction.y = 1
		else:
			self.direction.y = 0

		if keys[pygame.K_d]:
			self.direction.x = 1
		elif keys[pygame.K_a]:
			self.direction.x = -1
		else:
			self.direction.x = 0

	def update(self):
		self.input()
		self.rect.center += self.direction * self.speed
  
class CameraGroup(pygame.sprite.Group):
	def __init__(self):
		super().__init__()
		self.display_surface = pygame.display.get_surface()
		
		self.offset = pygame.math.Vector2(-300, 100)
		self.half_width = self.display_surface.get_size()[0] // 2
		self.half_height = self.display_surface.get_size()[1] // 2
		
		self.ground_surf = pygame.image.load('graphics/ground.png').convert_alpha()
		self.ground_rect = self.ground_surf.get_rect(topleft=(0,0))
	
	def center_camera_target(self, target):
		self.offset.x = target.centerx - self.half_width
		self.offset.y = target.centery - self.half_height
  
	def custom_draw(self, player):
		self.center_camera_target(player)
		ground_offest = self.ground_rect.topleft - self.offset
		self.display_surface.blit(self.ground_surf, ground_offest)
		for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
			offset_pos = sprite.rect.topleft + self.offset
			self.display_surface.blit(sprite.image, offset_pos)
			
  
pygame.init()
screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
clock = pygame.time.Clock()
pygame.event.set_grab(True)

# setup 
camera_group = CameraGroup()
player = Player((640,360),camera_group)

for i in range(20):
	random_x = randint(0,1000)
	random_y = randint(0,1000)
	Tree((random_x,random_y),camera_group)
 


while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				pygame.quit()
				sys.exit()

	screen.fill('#71ddee')

	camera_group.update()
	camera_group.custom_draw(player)

	pygame.display.update()
	clock.tick(60)
