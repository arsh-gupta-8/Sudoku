import pygame

pygame.init()

# Frames management
clock = pygame.time.Clock()
FPS = 30

# Colour constant variables
WHITE = (255, 255, 255)
SUPER_LIGHT_GREY = (211, 211, 211)
LIGHT_GREY = (118, 118, 118)
DARK_GREY = (64, 64, 64)
BLACK = (0, 0, 0)
BACKGROUND_SHADE = (232, 234, 236)
BOX_SHADE_LIGHT = (212, 212, 212)
BOX_SHADE_MEDIUM = (191, 191, 191)
BOX_SHADE_DARK = (170, 170, 170)
SELECT_BOX = (140, 180, 207)

# Screen management
screen = pygame.display.set_mode((902, 582))
pygame.display.set_caption('Sudoku Game')
screen.fill(BACKGROUND_SHADE)

# Font management
number_font = pygame.font.SysFont("Ariel", 40)

# Making grid/2D array for storing game numbers
grid = []
for row in range(9):
    grid.append([])
    for column in range(9):
        grid[row].append(0)

# Game settings
place_holder_rect = None
hovering_box = None
x_line = None
y_line = None


# Update screen
def window_update(grid_rect, grid_hover, lines):
    screen.fill(BACKGROUND_SHADE)
    if lines[0] is not None:
        for line in lines:
            pygame.draw.rect(screen, BOX_SHADE_MEDIUM, line)
    set_dimensions()
    if grid_hover is not None:
        pygame.draw.rect(screen, BOX_SHADE_LIGHT, grid_hover)
    if grid_rect is not None:
        pygame.draw.rect(screen, SELECT_BOX, grid_rect)
    pygame.display.update()


def set_dimensions():
    # Draws smaller lines between every line
    for line_x in range(3):
        pygame.draw.rect(screen, LIGHT_GREY, pygame.Rect(50 + line_x * 159 + 55, 50, 54, 482), 2)
    for line_y in range(3):
        pygame.draw.rect(screen, LIGHT_GREY, pygame.Rect(50, line_y * 159 + 105, 482, 54), 2)

    # Draws bold lines between each set of 9 squares
    pygame.draw.rect(screen, DARK_GREY, pygame.Rect(50, 50, 482, 482), 5)
    pygame.draw.rect(screen, DARK_GREY, pygame.Rect(209, 50, 164, 482), 5)
    pygame.draw.rect(screen, DARK_GREY, pygame.Rect(50, 209, 482, 164), 5)


def find_box_dim(x_val, y_val):
    x_box = -1
    y_box = -1
    addition = 0
    for box in range(9):
        if x_val >= 55 + 50 * box + addition:
            x_box += 1
        if y_val >= 55 + 50 * box + addition:
            y_box += 1
        addition += 2
        if box % 3 == 2:
            addition += 3

    x_box_cord = x_box * 50 + (x_box // 3) * 3 + x_box * 2 + 55
    y_box_cord = y_box * 50 + (y_box // 3) * 3 + y_box * 2 + 55

    return x_box_cord, y_box_cord


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
                if 55 <= x <= 527 and 55 <= y <= 527:
                    if colour_clicked == SELECT_BOX:
                        place_holder_rect = None
                        x_line = None
                        y_line = None
                    elif colour_clicked not in [DARK_GREY, LIGHT_GREY, SUPER_LIGHT_GREY]:
                        x_place, y_place = find_box_dim(x, y)
                        place_holder_rect = pygame.Rect(x_place, y_place, 50, 50)
                        x_line = pygame.Rect(x_place, 50, 50, 482)
                        y_line = pygame.Rect(50, y_place, 482, 50)

    if 55 <= x <= 527 and 55 <= y <= 527:
        colour_clicked = screen.get_at((x, y))[:3]
        if colour_clicked not in [DARK_GREY, LIGHT_GREY, SUPER_LIGHT_GREY]:
            x_place, y_place = find_box_dim(x, y)
            hovering_box = pygame.Rect(x_place, y_place, 50, 50)
            if hovering_box == place_holder_rect:
                hovering_box = None
    else:
        hovering_box = None

    window_update(place_holder_rect, hovering_box, [x_line, y_line])
    clock.tick(FPS)
