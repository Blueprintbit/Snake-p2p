from random import choice

import pygame

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (168, 236, 182)

# Скорость движения змейки:
SPEED = 20

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


# Тут опишите все классы игры.
class GameObject:
    """Базовый класс, от которого наследуются другие игровые объекты."""

    # Инициализация базовых атрибутов
    def __init__(self, position=None, body_color=None):
        self.position = (
            position if position else (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        )
        self.body_color = body_color

    def draw(self):
        """Абстрактный класс для переопределения в дочерних классах."""
        pass


class Snake(GameObject):
    """Дочерний класс GameObject, описывающий змейку и её поведение."""

    # Инициализация атрибутов класса Snake
    def __init__(self):
        super().__init__(body_color=SNAKE_COLOR)
        self.positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.length = 1
        self.direction = RIGHT
        self.next_direction = None
        self.last = None

    def update_direction(self):
        """Метод обновления направления после нажатия на кнопку."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Метод добавление в начало нового кортежа и удаление хвоста."""
        first_x, first_y = self.get_head_position()
        d_x, d_y = self.direction
        move_x = (first_x + d_x * GRID_SIZE) % SCREEN_WIDTH
        move_y = (first_y + d_y * GRID_SIZE) % SCREEN_HEIGHT
        tup_move = (move_x, move_y)
        # Если голова оказалась в теле, сброс
        if tup_move in self.positions[1:]:
            self.reset()
        # Иначе, вставляем вначале кортеж головы и удаляем хвостовой кортеж
        else:
            self.positions.insert(0, tup_move)
            if len(self.positions) > self.length:
                self.last = self.positions.pop()
            else:
                self.last = None

    def draw(self):
        """Метод отрисовки Snake."""
        for position in self.positions:
            rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        if self.last is not None:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def get_head_position(self):
        """Возвращает позицию головы."""
        head_position = self.positions[0]
        if head_position is None:
            return
        return head_position

    def reset(self):
        """Сбрасывает змейку в начальное состояние."""
        self.length = 1
        self.positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.direction = choice([UP, DOWN, LEFT, RIGHT])
        self.next_direction = None


class Apple(GameObject):
    """Дочерний класс GameObject, описывающий яблоко и действия с ним."""

    # Инициализация атрибутов класса Apple
    def __init__(self):
        super().__init__(body_color=APPLE_COLOR)
        self.randomize_position()

    def randomize_position(self):
        """Подготовка рандомной позиции для размещения яблока."""
        self.position = (
            choice(range(0, SCREEN_WIDTH, GRID_SIZE)),
            choice(range(0, SCREEN_HEIGHT, GRID_SIZE)),
        )

    def draw(self):
        """Метод отрисовки Apple."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


def handle_keys(game_object):
    """Функция обработки действий пользователя."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT:
                game_object.next_direction = RIGHT


def main():
    """Основная функция игры."""
    # Инициализация PyGame:
    pygame.init()
    # Тут создаются два игровых объекта
    snake = Snake()
    apple = Apple()

    # Бесконечный цикл игры, пока пользователь не закроет окно
    while True:

        # Вызов встроенной функции с установкой скорости движения
        clock.tick(SPEED)

        # Очистка экрана в начале каждой итерации
        screen.fill(BOARD_BACKGROUND_COLOR)

        # Вызов функции для отрисовки яблока и змеи
        apple.draw()
        snake.draw()

        # Нажатие на кнопку
        handle_keys(snake)
        # Обновление направления после нажатия на кнопку
        snake.update_direction()
        # Вызов движения
        snake.move()

        # Условие для начала нового подцикла игры если голова и яблоко совпали
        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position()

        pygame.display.update()


if __name__ == '__main__':
    main()
