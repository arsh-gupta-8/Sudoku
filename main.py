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
BOX_SHADE_MEDIUM = (200, 200, 200)
BOX_SHADE_DARK = (170, 170, 170)
SELECT_BOX = (140, 180, 207)
SOL_RED = (197, 30, 58)

# Screen management
screen = pygame.display.set_mode((902, 582))
pygame.display.set_caption('Sudoku Game')
screen.fill(BACKGROUND_SHADE)

# Font management
number_font = pygame.font.SysFont("Ariel", 60)

# Making grid/2D array for storing game numbers
grid = []
for row in range(9):
    grid.append([])
    for column in range(9):
        grid[row].append(0)

grid_copy = []
for row in range(9):
    grid_copy.append([])
    for column in range(9):
        grid_copy[row].append(0)


def check_square(x_cord, y_cord, search_number, search_grid):

    if search_number in search_grid[y_cord]:
        return False

    for y_adjacent in range(y_cord):
        if search_number == search_grid[y_adjacent][x_cord]:
            return False

    for y_adjacent in range(y_cord + 1, 9):
        if search_number == search_grid[y_adjacent][x_cord]:
            return False

    x_cord = (x_cord//3) * 3
    y_cord = (y_cord//3) * 3

    for down in range(y_cord, y_cord+3):
        for across in range(x_cord, x_cord+3):
            if search_grid[down][across] == search_number:
                return False

    return True


def solve_game(given_grid, temp_grid):
    error_iter = 0
    y_val = 0
    x_val = 0
    forward = True

    while y_val < 9:

        error_iter += 1
        if error_iter >= 100000:
            print("no answer found")
            return grid, grid

        if given_grid[y_val][x_val] == 0 and forward:
            start = temp_grid[y_val][x_val] + 1
            move_on = False

            for possible_num in range(start, 10):
                passed = check_square(x_val, y_val, possible_num, temp_grid)

                if passed:
                    move_on = True
                    temp_grid[y_val][x_val] = possible_num
                    break

            if not move_on:
                temp_grid[y_val][x_val] = 0
                forward = False
                if x_val == 0 and y_val == 0:
                    print("not possible")
                    return grid

            else:
                x_val += 1
                if x_val == 9:
                    y_val += 1
                    x_val = 0

        elif forward:
            x_val += 1
            if x_val == 9:
                y_val += 1
                x_val = 0
        else:
            x_val -= 1

            if x_val == -1:
                y_val -= 1
                x_val = 8

            if given_grid[y_val][x_val] == 0:
                forward = True

    return temp_grid, temp_grid


# Game settings
GAME_NUMS = [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5, pygame.K_6, pygame.K_7, pygame.K_8, pygame.K_9]
place_holder_rect = None
hovering_box = None
x_place = None
y_place = None
x_line = None
y_line = None
selected = False
numbers_stated = [100]


# Update screen
def window_update(grid_rect, grid_hover, lines, game_grid, num_positions):
    screen.fill(BACKGROUND_SHADE)
    if lines[0] is not None:
        for line in lines:
            pygame.draw.rect(screen, BOX_SHADE_MEDIUM, line)
    set_dimensions()
    if grid_hover is not None:
        pygame.draw.rect(screen, BOX_SHADE_LIGHT, grid_hover)
    if grid_rect is not None:
        pygame.draw.rect(screen, SELECT_BOX, grid_rect)
    for grid_y in range(9):
        for grid_x in range(9):
            current_num = game_grid[grid_y][grid_x]
            if current_num != 0:
                num_display = number_font.render(str(current_num), False, BLACK)
                if len(num_positions) == 0 or num_positions[0] != 100:
                    if [grid_y, grid_x] not in num_positions:
                        num_display = number_font.render(str(current_num), False, SOL_RED)
                x_pos = 80 + 50 * grid_x + grid_x * 2 + (grid_x // 3) * 3 - num_display.get_width()//2
                y_pos = 80 + 50 * grid_y + grid_y * 2 + (grid_y // 3) * 3 - num_display.get_height()//2
                screen.blit(num_display, (x_pos, y_pos))
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


def find_box_dim(data, x_val, y_val):
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

    if data == 1:
        x_box_cord = x_box * 50 + (x_box // 3) * 3 + x_box * 2 + 55
        y_box_cord = y_box * 50 + (y_box // 3) * 3 + y_box * 2 + 55

        return x_box_cord, y_box_cord
    elif data == 2:
        return x_box, y_box


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
                        selected = False
                        place_holder_rect = None
                        x_line = None
                        y_line = None
                    elif colour_clicked not in [DARK_GREY, LIGHT_GREY, SUPER_LIGHT_GREY]:
                        selected = True
                        x_place, y_place = find_box_dim(1, x, y)
                        place_holder_rect = pygame.Rect(x_place, y_place, 50, 50)
                        x_line = pygame.Rect(x_place, 50, 50, 482)
                        y_line = pygame.Rect(50, y_place, 482, 50)

        elif event.type == pygame.KEYDOWN:
            for pygame_number in GAME_NUMS:
                if event.key == pygame_number:
                    x_place_index, y_place_index = find_box_dim(2, x_place, y_place)
                    grid[y_place_index][x_place_index] = GAME_NUMS.index(pygame_number) + 1
                    grid_copy[y_place_index][x_place_index] = GAME_NUMS.index(pygame_number) + 1

            if event.key == pygame.K_SPACE:
                numbers_stated.pop()
                for col in range(9):
                    for row in range(9):
                        if grid[col][row] != 0:
                            numbers_stated.append([col, row])
                grid, grid_copy = solve_game(grid, grid_copy)

    if 55 <= x <= 527 and 55 <= y <= 527:
        colour_clicked = screen.get_at((x, y))[:3]
        if colour_clicked not in [DARK_GREY, LIGHT_GREY, SUPER_LIGHT_GREY]:
            x_cursor_box, y_cursor_box = find_box_dim(1, x, y)
            hovering_box = pygame.Rect(x_cursor_box, y_cursor_box, 50, 50)
            if hovering_box == place_holder_rect:
                hovering_box = None
    else:
        hovering_box = None

    window_update(place_holder_rect, hovering_box, [x_line, y_line], grid, numbers_stated)
    clock.tick(FPS)
