import pygame 
import time
import math

def scale_image(img, factor):
    size = round(img.get_width() * factor), round(img.get_height() * factor)
    return pygame.transform.scale(img, size)

def blit_rotate_center(win, image, top_left, angle):
    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center=image.get_rect(topleft = top_left).center)
    win.blit(rotated_image, new_rect.topleft)

TRACK_WIDTH, TRACK_HEIGHT = 675, 650

GRASS = scale_image(pygame.image.load('imgs/grass.jpg'), 2.5)
TRACK_IMAGE = pygame.image.load('imgs/track.png')
TRACK = pygame.transform.scale(
    TRACK_IMAGE, (TRACK_WIDTH, TRACK_HEIGHT))

TRACK_BORDER_IMAGE = pygame.image.load('imgs/track-border.png')
TRACK_BORDER = pygame.transform.scale(
    TRACK_BORDER_IMAGE, (TRACK_WIDTH, TRACK_HEIGHT))
TRACK_BORDER_MASK = pygame.mask.from_surface(TRACK_BORDER)
FINISH = pygame.image.load('imgs/finish.png')
FINISH_MASK = pygame.mask.from_surface(FINISH)
FINISH_POSITION = (102, 225)


RED_CAR =  scale_image(pygame.image.load('imgs/red-car.png'), 0.46)
GREEN_CAR =  scale_image(pygame.image.load('imgs/green-car.png'), 0.46)

WIDTH, HEIGHT = TRACK.get_width(), 650
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Racing Game!")

FPS = 60

class AbstractCar:
    def __init__(self, max_vel, rotation_vel):
        self.img = self.IMG
        self.max_vel = max_vel
        self.vel= 0
        self.rotation_vel = rotation_vel
        self.angle = 0
        self.x, self.y = self.START_POS
        self.acceleration = 0.1

    def rotate_red(self, left=False, right=False):
        if left:
            self.angle += self.rotation_vel
        elif right:
            self.angle -= self.rotation_vel
        
    def draw_red(self, win):
        blit_rotate_center(win, self.img, (self.x, self.y), self.angle)

    def move_forward_red(self):
        self.vel = min(self.vel + self.acceleration, self.max_vel)
        self.move_red()

    def move_backward_red(self):
        self.vel = max(self.vel - self.acceleration, -self.max_vel/2)
        self.move_red()

    def move_red(self):
        radians = math.radians(self.angle)
        vertical = math.cos(radians) * self.vel
        horizontal = math.sin(radians) * self.vel

        self.y -= vertical 
        self.x -= horizontal 

    def collide_red(self, mask, x=0, y=0):
        car_mask = pygame.mask.from_surface(self.img)
        offset = (int(self.x - x), int(self.y - y))
        poi = mask.overlap(car_mask, offset)
        return poi
    
    

    def reset_red(self):
        self.x, self.y = self.START_POS
        self.angle = 0
        self.vel = 0

class PlayerCar(AbstractCar):
    IMG = RED_CAR
    START_POS = (156, 180)
    

    def reduce_speed_red(self):
        self.vel = max(self.vel - self.acceleration/2, 0)
        self.move_red()

    def bounce_red(self):
        self.vel = -self.vel/2
        self.move_red()

class Player2Car(AbstractCar):
    IMG = GREEN_CAR
    START_POS = (123, 180)
    
    def __init__(self, max_vel, rotation_vel):
        self.img = self.IMG
        self.max_vel = max_vel
        self.vel= 0
        self.rotation_vel = rotation_vel
        self.angle = 0
        self.x, self.y = self.START_POS
        self.acceleration = 0.1

    def draw_green(self, win):
        blit_rotate_center(win, self.img, (self.x, self.y), self.angle)

    def collide_green(self, mask, x=0, y=0):
        car_mask = pygame.mask.from_surface(self.img)
        offset = (int(self.x - x), int(self.y - y))
        poi = mask.overlap(car_mask, offset)
        return poi
    
    def rotate_green(self, left=False, right=False):
        if left:
            self.angle += self.rotation_vel
        elif right:
            self.angle -= self.rotation_vel

    def move_forward_green(self):
        self.vel = min(self.vel + self.acceleration, self.max_vel)
        self.move_green()

    def move_backward_green(self):
        self.vel = max(self.vel - self.acceleration, -self.max_vel/2)
        self.move_green()

    def move_green(self):
        radians = math.radians(self.angle)
        vertical = math.cos(radians) * self.vel
        horizontal = math.sin(radians) * self.vel

        self.y -= vertical 
        self.x -= horizontal 

    def reset_green(self):
        self.x, self.y = self.START_POS
        self.angle = 0
        self.vel = 0

    def bounce_green(self):
        self.vel = -self.vel/2
        self.move_green()

    def reduce_speed_green(self):
        self.vel = max(self.vel - self.acceleration/2, 0)
        self.move_green()

    def reset_green(self):
        self.x, self.y = self.START_POS
        self.angle = 0
        self.vel = 0

def draw(win, images, player_car, player_car1):
    for img, pos in images:
        win.blit(img, pos)

    player_car.draw_red(win)
    player_car1.draw_green(win)
    pygame.display.update()

def move_player_red(player_car):
    keys = pygame.key.get_pressed()
    moved = False
    if keys[pygame.K_a]:
        player_car.rotate_red(left=True)
    if keys[pygame.K_d]:
        player_car.rotate_red(right=True)
    if keys[pygame.K_w]:
        moved = True
        player_car.move_forward_red()
    if keys[pygame.K_s]:
        moved = True
        player_car.move_backward_red()

    if not moved:
        player_car.reduce_speed_red()

def move_player_green(player_car1):
    keys1 = pygame.key.get_pressed()
    moved1 = False
    if keys1[pygame.K_LEFT]:
        player_car1.rotate_green(left=True)
    if keys1[pygame.K_RIGHT]:
        player_car1.rotate_green(right=True)
    if keys1[pygame.K_UP]:
        moved1 = True
        player_car1.move_forward_green()
    if keys1[pygame.K_DOWN]:
        moved1 = True
        player_car1.move_backward_green()

    if not moved1:
        player_car1.reduce_speed_green()

run = True 
clock = pygame.time.Clock()
images = [(GRASS, (0, 0)), (TRACK, (0,0)), (FINISH, FINISH_POSITION), (TRACK_BORDER, (0,0))]
player_car = PlayerCar(2, 2)
player_car1 = Player2Car(2, 2)

while run:
    clock.tick(FPS)

    draw(WIN, images, player_car, player_car1)
  

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            break


    move_player_red(player_car)
    move_player_green(player_car1)


    if player_car.collide_red(TRACK_BORDER_MASK) != None:
        player_car.bounce_red()
    if player_car1.collide_green(TRACK_BORDER_MASK) != None:
        player_car1.bounce_green()

    finish_poi_collide = player_car.collide_red(FINISH_MASK, *FINISH_POSITION)
    if finish_poi_collide != None:
        if finish_poi_collide[1] == 0:
            player_car.bounce_red()
        else:
            player_car.reset_red()
            print("Red Wins!")

    finish_poi_collide1 = player_car1.collide_red(FINISH_MASK, *FINISH_POSITION)
    if finish_poi_collide1 != None:
        if finish_poi_collide1[1] == 0:
            player_car1.bounce_green()
        else:
            player_car1.reset_green()
            print("Green Wins!")

pygame.quit()
