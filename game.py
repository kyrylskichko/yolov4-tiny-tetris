import pygame
from yolo_object_detection import detect_and_show, net
from objects import Tetris, colors


# Initialize the game engine
pygame.init()

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)

size = (800, 1000)
screen = pygame.display.set_mode(size)

pygame.display.set_caption("Tetris")

# Loop until the user clicks the close button.
done = False
game = Tetris(20, 10)
counter = 0

count = {"rotate": 1,
         "drop": 1,
         "right": 1,
         "left": 1}


def restart_counter(dict):
    for i in dict:
        dict[i] = 1


while not done:
    counter += 1
    if game.figure is None:
        game.new_figure()

    if counter > 100000:
        counter = 0

    if counter % 10 == 0:
        if game.state == "start":
            game.go_down()

    pred = detect_and_show(net)

    if pred in count:
        count[pred] += 1
        if count["rotate"] % 10 == 0:
            game.rotate()
            restart_counter(count)
        if count["drop"] % 14 == 0:
            game.go_space()
            restart_counter(count)
        if count["right"] % 5 == 0:
            game.go_side(1)
            restart_counter(count)
        if count["left"] % 5 == 0:
            game.go_side(-1)
            restart_counter(count)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                game.__init__(20, 10)

    screen.fill(BLACK)

    for i in range(game.height):
        for j in range(game.width):
            pygame.draw.rect(screen, GRAY, [game.x + game.zoom * j, game.y + game.zoom * i, game.zoom, game.zoom], 1)
            if game.field[i][j] > 0:
                pygame.draw.rect(screen, colors[game.field[i][j]],
                                 [game.x + game.zoom * j + 1, game.y + game.zoom * i + 1, game.zoom - 2, game.zoom - 1])

    if game.figure is not None:
        for i in range(4):
            for j in range(4):
                p = i * 4 + j
                if p in game.figure.image():
                    pygame.draw.rect(screen, colors[game.figure.color],
                                     [game.x + game.zoom * (j + game.figure.x) + 1,
                                      game.y + game.zoom * (i + game.figure.y) + 1,
                                      game.zoom - 2, game.zoom - 2])

    font = pygame.font.SysFont('Calibri', 25, True, False)
    font1 = pygame.font.SysFont('Calibri', 65, True, False)
    text = font.render("Score: " + str(game.score), True, BLACK)

    screen.blit(text, [0, 0])
    if game.state == "gameover":
        done = True

    pygame.display.flip()

pygame.quit()
