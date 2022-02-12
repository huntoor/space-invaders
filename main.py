from distutils.spawn import spawn
import math
import pygame
import random
from pygame import mixer


#sounds/ufo_highpitch.wav
#initilalize game
pygame.init()

#creating screen
screen = pygame.display.set_mode((800,600))
backgorund = pygame.image.load("background.jpeg")
backgorund = pygame.transform.scale(backgorund, (800, 600))



#caption and ion
pygame.display.set_caption("my first pygame")
icon = pygame.image.load("space-invaders.png")
pygame.display.set_icon(icon)


#players
playericon = pygame.image.load("player.png")
playericon = pygame.transform.scale(playericon, (80,80))
playerXChange = 0
playerX = 340
playerY = 465

def player(x, y):
  screen.blit(playericon, (x, y))

#Enemies
enemyicon = []
enemyX = []
enemyY = []
enemyXchange = []
NoOfEnemies = 10

for i in range(NoOfEnemies):
  enemyicon.append(pygame.image.load("enemy1.png"))
  enemyicon[i] = pygame.transform.scale(enemyicon[i], (60, 50))
  enemyX.append(10)
  enemyY.append(random.randint(30, 70))
  if i > 0:
    enemyX[i] = enemyX[i - 1] + 70
    enemyY[i] = enemyY[0]
  enemyXchange.append(2)

def enemy(x, y, i):
  screen.blit(enemyicon[i], (x, y))


#bullet
bulleticon = pygame.image.load("bullet.png")
bulletX = playerX
bulletY = playerY - 100
bulletYchange = 0
bulletState = "Ready"


#Score
scoreValue = 0
font = pygame.font.Font('ttf/PlayfairDisplay-Bold.ttf', 32)

def viewScore():
  score = font.render("Score: " + str(scoreValue), True, (98, 222, 109))
  screen.blit(score, (10,10))


#GameOver
isWinner = True
gameOver = pygame.font.Font('ttf/PlayfairDisplay-Bold.ttf', 64)
playAgain = pygame.font.Font('ttf/PlayfairDisplay-Regular.ttf', 32)

def viewGameOver():
  if not isWinner:
    over = gameOver.render("Game Over", True, (248, 59, 58))
    play = playAgain.render("press enter to play again", True, (248, 59, 58))
    screen.blit(over, (240,200))
    screen.blit(play, (230, 300))
    for i in range(NoOfEnemies):
      enemyY[i] = 900


def bullet(x,y):
  global bulletState
  bulletState = "Fire"
  screen.blit(bulleticon, (x + 8,y))


def isCollision(x1,x2,y1,y2):
  D = math.sqrt(pow(x1-x2, 2) + pow(y1-y2, 2))
  if D <= 35:
    return True
  return False

#Game Loop
running = True
while running:
  #Background 
  screen.blit(backgorund, (0,0))
  
  for event in pygame.event.get():
    #Quit the Gmae
    if event.type == pygame.QUIT:
      running = False
    #Game Movment
    if event.type == pygame.KEYDOWN:
      if event.key == pygame.K_LEFT:
        playerXChange = -2
      if event.key == pygame.K_RIGHT:
        playerXChange = 2

      if event.key == pygame.K_SPACE:
        if bulletState is "Ready":
          bulletX = playerX
          mixer.music.load("sounds/shoot.wav")
          mixer.music.play()
          bullet(bulletX, bulletY)

      if event.key == pygame.K_RETURN:
        if not isWinner:
          isWinner = True
          scoreValue = 0
          for i in range(NoOfEnemies):
            enemyX[i] = 10
            enemyY[i] = random.randint(30, 70)
            if i > 0:
              enemyX[i] = enemyX[i - 1] + 70
              enemyY[i] = enemyY[0]



    if event.type == pygame.KEYUP:
      if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
        playerXChange = 0


    
#Bullet
  if bulletState is "Fire":
    bullet(bulletX, bulletY)
    bulletY += -3
    if bulletY <= 0:
      bulletY = playerY
      bulletState = "Ready"
    

#player
  playerX += playerXChange
  if playerX <= 0:
    playerX = 0
  elif playerX >= 720:
    playerX = 720
  player(playerX, playerY)

#Enemy
  for i in range(NoOfEnemies):
    
    #Game Over  
    if isCollision(enemyX[i], playerX, enemyY[i], playerY):
      mixer.music.load("sounds/explosion.wav")
      mixer.music.play()
      isWinner = False
      print("loster")
      break  
    viewGameOver()

    enemyX[i] += enemyXchange[i]
    if enemyX[i] <= 0:
      enemyXchange[i] = 1.7
      enemyY[i] += 50
    elif enemyX[i] >= 720:
      enemyXchange[i] = -1.7
      enemyY[i] += 50
    enemy(enemyX[i], enemyY[i], i)


  #collision occured
    if isCollision(enemyX[i], bulletX, enemyY[i], bulletY):
      mixer.music.load("sounds/invaderkilled.wav")
      mixer.music.play()
      bulletState = "Ready"
      scoreValue += 1
      bulletX = -30
      bulletY = playerY
      enemyX[i] = random.randint(0, 750)
      enemyY[i] = random.randint(30, 100)
  
  viewScore()
  pygame.display.update()
    