import pgzrun
import random

WIDTH = 600
HEIGHT = 800
BULLETS = 3
PINK = ('250, 75, 212')
RED = ('184, 33, 22')
level = 1
lives = 5
score = 0

background = Actor("bg")
player = Actor("actor", (200, 580))
enemies = []
bullets = []
bombs = []
game_over = False


def draw():
    screen.blit('bg', (0, 0))
    background.draw()
    player.draw()
    for enemy in enemies:
        enemy.draw()
    for bullet in bullets:
        bullet.draw()
    for bomb in bombs:
        bomb.draw()
    if game_over:
        screen.draw.text("GAME OVER!!", (200, 300), fontsize=45, color="RED")
    draw_text()


def update():
    if not game_over:
      move_player()
      move_bullets()
      move_enemies()
      create_bombs()
      move_bombs()
      check_for_end_of_level()


def move_player():
       if keyboard.right:
          player.x += 5
       if keyboard.left:
          player.x -= 5
       if player.x > WIDTH:
          player.x = WIDTH
       if player.x < 0:
          player.x = 0




def create_enemies():
    for x in range(0, 600, 60):
        for y in range(0, 200, 60):
            enemy = Actor("enemy", (x, y))
            enemy.vx = level * 1
            enemies.append(enemy)


def move_enemies():
    global score
    for enemy in enemies:
        enemy.x = enemy.x + enemy.vx
        if enemy.x > WIDTH or enemy.x < 0:
            enemy.vx = -enemy.vx
            animate(enemy, duration=0.1, y=enemy.y + 60)
        for bullet in bullets:
            if bullet.colliderect(enemy):
                sounds.shoot.play()
                enemies.remove(enemy)
                bullets.remove(bullet)
                score += 1
        if enemy.colliderect(player):
            enemies.remove(enemy)

def move_bullets():
    for bullet in bullets:
        bullet.y = bullet.y - 6
        if bullet.y < 0:
            bullets.remove(bullet)

def create_bombs():
    if random.randint(0, 100 - level * 6) == 0:
        enemy = random.choice(enemies)
        bomb = Actor("bomb", enemy.pos)
        bombs.append(bomb)

def move_bombs():
    global game_over
    global lives
    for bomb in bombs:
        bomb.y += 10
        if bomb.colliderect(player):
            sounds.warn_sound.play()
            bombs.remove(bomb)
            lives -= 1
        if lives == 0:
            player.image = "damage"
            sounds.blast.play()
            game_over = True

def check_for_end_of_level():
    global level
    if len(enemies) == 0:
        level += 1
        create_enemies()


def draw_text():
        screen.draw.text("Level " + str(level), (0, 0),  color="PINK")
        screen.draw.text("Score " + str(score), (100, 0), color="PINK")
        screen.draw.text("Lives " + str(lives), (200, 0), color="PINK")



def on_key_down(key):
    if not game_over:
       if key == keys.SPACE and len(bullets) < BULLETS:
          bullet = Actor("bullet", pos=(player.x, player.y))
          bullets.append(bullet)


create_enemies()
pgzrun.go()