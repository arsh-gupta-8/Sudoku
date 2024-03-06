import pygame

pygame.init()

# Frames management
clock = pygame.time.Clock()
FPS = 30

# Colour constant variables
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHT_GREY = (118, 118, 118)
DARK_GREY = (64, 64, 64)

# Screen management
screen = pygame.display.set_mode((482, 557))
pygame.display.set_caption('Sudoku Game')
screen.fill(WHITE)

# Font management
number_font = pygame.font.SysFont("Ariel", 40)

# Making grid/2D array for storing game numbers
grid = []
for row in range(9):
    grid.append([])
    for column in range(9):
        grid[row].append(0)


def set_dimensions():
    # Draws smaller lines between every line
    for line_x in range(3):
        pygame.draw.rect(screen, LIGHT_GREY, pygame.Rect(line_x * 159 + 55, 75, 54, 482), 2)
    for line_y in range(3):
        pygame.draw.rect(screen, LIGHT_GREY, pygame.Rect(0, line_y * 159 + 130, 482, 54), 2)

    # Draws bold lines between each set of 9 squares
    pygame.draw.rect(screen, DARK_GREY, pygame.Rect(0, 75, 482, 482), 5)
    pygame.draw.rect(screen, DARK_GREY, pygame.Rect(159, 75, 164, 482), 5)
    pygame.draw.rect(screen, DARK_GREY, pygame.Rect(0, 234, 482, 164), 5)


def find_box_dim(x_val, y_val):
    x_box = -1
    y_box = -1
    addition = 0
    for box in range(9):
        if x_val >= 5 + 50 * box + addition:
            x_box += 1
        if y_val >= 80 + 50 * box + addition:
            y_box += 1
        addition += 2
        if box % 3 == 2:
            addition += 3

    a = x_box * 50 + (x_box // 3) * 3 + x_box * 2 + 5
    b = y_box * 50 + (y_box // 3) * 3 + y_box * 2 + 80

    return a, b


# Main game loop
running = True
while running:

    x, y = pygame.mouse.get_pos()

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                colour_clicked = screen.get_at((x, y))[:3]
                if 5 <= x <= 477 and 80 <= y <= 552 and colour_clicked != DARK_GREY and colour_clicked != LIGHT_GREY:
                    print("inside")
                    x_place, y_place = find_box_dim(x, y)
                    pygame.draw.rect(screen, LIGHT_GREY, pygame.Rect(x_place, y_place, 50, 50))

    set_dimensions()
    pygame.display.update()
    clock.tick(FPS)
