import pygame
import random
import os

pygame.mixer.init()
pygame.init()

# Colors
white = (255, 255, 255)
red = (255, 0, 0)
black = (0, 0, 0)
green = (124,252,0)
lightseagreen = (32,178,170)
aqua = (0,255,255)
gold = (255,215,0)
azure = (240,255,255)

# Creating window
screen_width = 900
screen_height = 600
gameWindow = pygame.display.set_mode((screen_width, screen_height))

#Background Image
bgimg = pygame.image.load("snake_bg.jpeg")
bgimg = pygame.transform.scale(bgimg, (screen_width, screen_height)).convert_alpha()

#Welcome Image
wlcome =pygame.image.load("snake_bg.png")
wlcome = pygame.transform.scale(wlcome, (screen_width, screen_height)).convert_alpha()

# Game Title
pygame.display.set_caption("Snake GAME")
pygame.display.update()

clock = pygame.time.Clock()
font = pygame.font.SysFont(None,30)

def text_screen(text,color,x,y):
    screen_text = font.render(text, True, color)
    gameWindow.blit(screen_text, [x,y])

def plot_snake(gameWindow, color, snk_list, snake_size):
    for x,y in snk_list:
        pygame.draw.rect(gameWindow, color, [x, y, snake_size, snake_size])


def welcome():
    exit_game = False
    while not exit_game:
        gameWindow.fill((233,210,229))
        gameWindow.blit(wlcome, (0, 0))
        text_screen("Welcome to Snakes", azure, 340, 115)
        text_screen("Press Space Bar To Play", azure, 320, 135)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    pygame.mixer.music.load('Loop_Music.mp3')
                    pygame.mixer.music.play()
                    gameloop()

        pygame.display.update()
        clock.tick(30)

        
        # Game Loop
def gameloop():

    snk_list = []
    snk_length = 1
    # Game specific variables
    exit_game = False
    game_over = False
    snake_x = 45
    snake_y = 55
    velocity_x = 0
    velocity_y = 0
    food_x = random.randint(10,screen_width/2)
    food_y = random.randint(10,screen_height/2)
    score = 0
    init_velocity = 5

    snake_size = 10
    fps = 30

    #CHECK IF HIGH_SCORE FILE EXISTS OR NOT
    if(not os.path.exists("high_score.txt")):
        with open("high_score.txt","w") as f:
            hiscore="0"
            f.write(hiscore)
            

    with open("high_score.txt","r") as f:
        hiscore = f.read()


    while not exit_game:
        if game_over:
            with open("high_score.txt", "w") as f:
                f.write(str(hiscore))
            gameWindow.fill(gold)
            text_screen("Game Over!!! Press Enter to Continue",red,250,250)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        welcome()

        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        velocity_x = init_velocity
                        velocity_y = 0
                        
                    if event.key == pygame.K_LEFT:
                        velocity_x = -init_velocity
                        velocity_y = 0

                    if event.key == pygame.K_UP:
                        velocity_y = -init_velocity
                        velocity_x = 0
                        
                    if event.key == pygame.K_DOWN:
                        velocity_y = init_velocity
                        velocity_x = 0

                    if event.key == pygame.K_q:
                        score += 10

            snake_x = snake_x + velocity_x
            snake_y = snake_y + velocity_y

            if abs(snake_x - food_x)<7 and abs(snake_y - food_y)<7:
                score+=10
                #print("SCORE : ",score*10)
                food_x = random.randint(10,screen_width/2)
                food_y = random.randint(10,screen_height/2)
                snk_length += 5
                if score>int(hiscore):
                    hiscore=score
            gameWindow.fill(white)
            gameWindow.blit(bgimg, (0, 0))
            text_screen("Score: " + str(score) + "  HighScore: "+str(hiscore), lightseagreen, 5, 5)
            pygame.draw.rect(gameWindow, red, [food_x, food_y, snake_size, snake_size])
            
            head = []
            head.append(snake_x)
            head.append(snake_y)
            snk_list.append(head)

            if len(snk_list)>snk_length:
                del snk_list[0]

            if head in snk_list[:-1]:
                game_over = True
                pygame.mixer.music.load('End_Music.mp3')
                pygame.mixer.music.play()

            if snake_x<0 or snake_x>screen_width or snake_y<0 or snake_y>screen_height:
                game_over= True
                pygame.mixer.music.load('End_Music.mp3')
                pygame.mixer.music.play()
                #print("Game Over")
            #pygame.draw.rect(gameWindow, black, [snake_x, snake_y, snake_size, snake_size])
            plot_snake(gameWindow, green,snk_list, snake_size)
        pygame.display.update()
        clock.tick(fps)


    pygame.quit()
    quit()
welcome()
