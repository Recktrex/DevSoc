import pygame
import sys

pygame.init()
pygame.mixer.init()

# Constants
WIDTH, HEIGHT = 800, 600
LIGHT_GR = (200, 200, 200)
LIGHT_COLOR = (255, 255, 255)
FPS = 60
PADDLE_SPEED = 5
BALL_SPEED_X = 4
BALL_SPEED_Y = 4
BALL_SIZE = 20
WINNING_SCORE = 11

HITBOX_X = 4
HITBOX_Y = 6

# Initialize screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong with Skins")
clock = pygame.time.Clock()

background_img_raw = pygame.image.load("bog.png").convert()
background_img = pygame.transform.scale(background_img_raw, (WIDTH, HEIGHT))

pygame.mixer.music.load("bgm.mp3") # i made with suno.ai
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)

left_paddle_img_raw = pygame.image.load("frr.png").convert_alpha()  #desgned in piskel both
right_paddle_img_raw = pygame.image.load("enm.png").convert_alpha()

left_paddle_img = pygame.transform.rotate(left_paddle_img_raw, -90)
right_paddle_img = pygame.transform.rotate(right_paddle_img_raw, -90)

left_paddle_img = pygame.transform.scale(left_paddle_img, (40, 100))
right_paddle_img = pygame.transform.scale(right_paddle_img, (40, 100))

left_paddle_rect = left_paddle_img.get_rect(topleft=(10, HEIGHT//2 - 50))
right_paddle_rect = right_paddle_img.get_rect(topleft=(WIDTH - 50, HEIGHT//2 - 50))

left_paddle_hitbox = left_paddle_rect.inflate(-HITBOX_X * 2, -HITBOX_Y * 2)
right_paddle_hitbox = right_paddle_rect.inflate(-HITBOX_X * 2, -HITBOX_Y * 2)

ball = pygame.Rect(WIDTH//2 - BALL_SIZE//2, HEIGHT//2 - BALL_SIZE//2, BALL_SIZE, BALL_SIZE)
ball_speed_x = BALL_SPEED_X
ball_speed_y = BALL_SPEED_Y

p1_score = 0
p2_score = 0
game_state = "playing"
winner_text = ""

score_font = pygame.font.Font(None, 74) #fonts and styling enhanced using Gemini
prompt_font = pygame.font.Font(None, 36)

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.mixer.music.stop()
            pygame.quit()
            sys.exit()

        if game_state == "game_over":
            if event.type == pygame.MOUSEBUTTONDOWN:
                game_state = "playing"
                p1_score = 0
                p2_score = 0
                winner_text = ""
                ball.x = WIDTH//2 - BALL_SIZE//2
                ball.y = HEIGHT//2 - BALL_SIZE//2
                ball_speed_x = BALL_SPEED_X
                ball_speed_y = BALL_SPEED_Y
                left_paddle_rect.y = HEIGHT//2 - left_paddle_rect.height//2
                right_paddle_rect.y = HEIGHT//2 - right_paddle_rect.height//2
                left_paddle_hitbox.y = left_paddle_rect.y + HITBOX_Y
                right_paddle_hitbox.y = right_paddle_rect.y + HITBOX_Y

    if game_state == "playing":
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] and left_paddle_rect.top > 0:
            left_paddle_rect.y -= PADDLE_SPEED
        if keys[pygame.K_s] and left_paddle_rect.bottom < HEIGHT:
            left_paddle_rect.y += PADDLE_SPEED
        if keys[pygame.K_UP] and right_paddle_rect.top > 0:
            right_paddle_rect.y -= PADDLE_SPEED
        if keys[pygame.K_DOWN] and right_paddle_rect.bottom < HEIGHT:
            right_paddle_rect.y += PADDLE_SPEED
        
        left_paddle_hitbox.y = left_paddle_rect.y + HITBOX_Y
        right_paddle_hitbox.y = right_paddle_rect.y + HITBOX_Y
        
        ball.x += ball_speed_x
        ball.y += ball_speed_y

        if ball.top <= 0 or ball.bottom >= HEIGHT:
            ball_speed_y *= -1

        if ball.colliderect(left_paddle_hitbox) and ball_speed_x < 0:
            ball_speed_x *= -1
        if ball.colliderect(right_paddle_hitbox) and ball_speed_x > 0:
            ball_speed_x *= -1

        if ball.left <= 0:
            p2_score += 1
            if p2_score >= WINNING_SCORE:
                winner_text = "P2 Wins!"
                game_state = "game_over"
            else:
                ball.x = WIDTH//2 - BALL_SIZE//2
                ball.y = HEIGHT//2 - BALL_SIZE//2
                ball_speed_x *= -1
                left_paddle_rect.y = HEIGHT//2 - left_paddle_rect.height//2
                right_paddle_rect.y = HEIGHT//2 - right_paddle_rect.height//2
                left_paddle_hitbox.y = left_paddle_rect.y + HITBOX_Y
                right_paddle_hitbox.y = right_paddle_rect.y + HITBOX_Y

        elif ball.right >= WIDTH:
            p1_score += 1
            if p1_score >= WINNING_SCORE:
                winner_text = "P1 Wins!"
                game_state = "game_over"
            else:
                ball.x = WIDTH//2 - BALL_SIZE//2
                ball.y = HEIGHT//2 - BALL_SIZE//2
                ball_speed_x *= -1
                left_paddle_rect.y = HEIGHT//2 - left_paddle_rect.height//2
                right_paddle_rect.y = HEIGHT//2 - right_paddle_rect.height//2
                left_paddle_hitbox.y = left_paddle_rect.y + HITBOX_Y
                right_paddle_hitbox.y = right_paddle_rect.y + HITBOX_Y
    
    # Drawing
    screen.blit(background_img, (0, 0))

    screen.blit(left_paddle_img, left_paddle_rect)
    screen.blit(right_paddle_img, right_paddle_rect)

    pygame.draw.ellipse(screen, LIGHT_COLOR, ball)
    
    p1_text = score_font.render(str(p1_score), True, LIGHT_COLOR)
    screen.blit(p1_text, (WIDTH//4 - p1_text.get_width()//2, 20))
    
    p2_text = score_font.render(str(p2_score), True, LIGHT_COLOR)
    screen.blit(p2_text, (WIDTH * 3//4 - p2_text.get_width()//2, 20))

    # # === DEBUG: ===
    # if game_state == "playing":
    #     pygame.draw.rect(screen, (255, 0, 0), left_paddle_hitbox, 2)
    #     pygame.draw.rect(screen, (0, 255, 0), right_paddle_hitbox, 2)
    
    if game_state == "game_over":
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180)) 
        screen.blit(overlay, (0, 0))

        win_text_render = score_font.render(winner_text, True, LIGHT_COLOR)
        screen.blit(win_text_render, (WIDTH//2 - win_text_render.get_width()//2, HEIGHT//2 - 50))
        
        prompt_text_render = prompt_font.render("Click anywhere to restart", True, LIGHT_COLOR)
        screen.blit(prompt_text_render, (WIDTH//2 - prompt_text_render.get_width()//2, HEIGHT//2 + 30))

    pygame.display.flip()
    clock.tick(FPS)

