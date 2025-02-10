import random
import pygame
import sys

pygame.font.init()

# Определяем параметры игры
WIDTH = 400
HEIGHT = 400
GRID_SIZE = 4 # razmer 4/4
CELL_SIZE = WIDTH // GRID_SIZE
MARGIN = 5

# Цвета
BACKGROUND_COLOR = (187, 173, 160)
GRID_COLOR = (205, 193, 180)
CELL_COLORS =  {   #rgb цвета р-ред джи-зеленый б-синиий Чем выше значение, тем ярче  цвет. Например: (255, 0, 0) — чистый красный (0, 255, 0) — чистый зеленый.(0, 0, 255) — чистый синий.

    2: (238, 228, 218),
    4: (237, 224, 200),
    8: (242, 177, 121),
    16: (245, 149, 99),
    32: (246, 124, 95),
    64: (246, 94, 59),
    128: (237, 207, 114),
    256: (237, 204, 97),
    512: (237, 200, 80),
    1024: (237, 197, 63),
    2048: (237, 194, 46),
}
TEXT_COLOR = (119, 110, 101)

def initialize_grid():
    #для создания пустой клетки перед началом игры
    grid = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]
    spawn(grid)
    return grid

# Расположает число случайной пустой клетке
def spawn(grid):
    empty_cells = [(r, c) for r in range(GRID_SIZE) for c in range(GRID_SIZE) if grid[r][c] == 0]
    if empty_cells:
        r, c = random.choice(empty_cells)
        grid[r][c] = random.choice([2])  #начинаем с 2

def compress(grid):
    #для перемещения клеток
    new_grid = []
    for row in grid:
        new_row = [i for i in row if i != 0]
        new_row += [0] * (GRID_SIZE - len(new_row))
        new_grid.append(new_row)
    return new_grid

def merge(grid):
    #умножает одинаковые клетки
    for r in range(GRID_SIZE):
        for c in range(GRID_SIZE - 1):
            if grid[r][c] != 0 and grid[r][c] == grid[r][c + 1]:  # Если элементы одинаковы и не равны 0
                grid[r][c] *= 2            # Удваиваем значение
                grid[r][c + 1] = 0         # Обнуляем второе значение
    return grid



def reverse(grid):
    #двжиения во все стороны
    return [row[::-1] for row in grid]

# Функция для транспонирования поля на 90 градусов
def transpose(grid):
    return [list(row) for row in zip(*grid)]

def move_left(grid):
    #поворот плиток на лево
    grid = compress(grid)
    grid = merge(grid)
    grid = compress(grid)
    return grid

def move_right(grid):
    #Двигает плитки вправо
    grid = reverse(grid)
    grid = move_left(grid)
    grid = reverse(grid)
    return grid

def move_up(grid):
    #Вверх
    grid = transpose(grid)
    grid = move_left(grid)
    grid = transpose(grid)
    return grid


def move_down(grid):
    # вниз# Т
    grid = transpose(grid)
    grid = move_right(grid)
    grid = transpose(grid)
    return grid


def is_game_over(grid):
    #Проверяет, закончена ли игра
    # Проверка на наличие пустых клеток
    if any(0 in row for row in grid):
        return False
    # Проверка на возможность слияния
    for r in range(GRID_SIZE):
        for c in range(GRID_SIZE - 1):
            if grid[r][c] == grid[r][c + 1]:
                return False
    for c in range(GRID_SIZE):
        for r in range(GRID_SIZE - 1):
            if grid[r][c] == grid[r + 1][c]:
                return False
    return True

def draw_grid(grid, screen, font, game_over=False):
    #Отображает игровое поле с помощью цветов
    screen.fill(BACKGROUND_COLOR)
    for r in range(GRID_SIZE):
        for c in range(GRID_SIZE):
            value = grid[r][c]
            x = c * CELL_SIZE + MARGIN
            y = r * CELL_SIZE + MARGIN
            pygame.draw.rect(screen, CELL_COLORS.get(value, (205, 193, 180)), (x, y, CELL_SIZE - MARGIN, CELL_SIZE - MARGIN))
            if value != 0:
                text = font.render(str(value), True, TEXT_COLOR)
                text_rect = text.get_rect(center=(x + CELL_SIZE // 2, y + CELL_SIZE // 2))
                screen.blit(text, text_rect)

    # Отображение сообщения, если игра окончена
    if game_over:
        game_over_text = font.render("Game Over", True, (255, 0, 0))
        text_rect = game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(game_over_text, text_rect)

    pygame.display.update()

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("2048")
    font = pygame.font.Font(pygame.font.get_default_font(), 40)

    grid = initialize_grid()

    while True:
        game_over = is_game_over(grid)
        draw_grid(grid, screen, font, game_over)

        if game_over:
            pygame.time.wait(3000)  # Задержка 3 секунды перед завершением игры
            pygame.quit()
            sys.exit()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    new_grid = move_left(grid)
                    if new_grid != grid:
                        grid = new_grid
                        spawn(grid)
                elif event.key == pygame.K_RIGHT:
                    new_grid = move_right(grid)
                    if new_grid != grid:
                        grid = new_grid
                        spawn(grid)
                elif event.key == pygame.K_UP:
                    new_grid = move_up(grid)
                    if new_grid != grid:
                        grid = new_grid
                        spawn(grid)
                elif event.key == pygame.K_DOWN:
                    new_grid = move_down(grid)
                    if new_grid != grid:
                        grid = new_grid
                        spawn(grid)

if __name__ == "__main__":
    main()
