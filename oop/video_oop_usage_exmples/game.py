import pygame
import random

# Инициализация Pygame
pygame.init()

# Константы
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
FPS = 60

# Настройка дисплея
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Simple Game with Two Players")

# Цвета
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)


# Классы
class Player(pygame.sprite.Sprite):
    def __init__(self, color, start_pos, control_scheme):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.center = start_pos
        self.speed = 5
        self.control_scheme = control_scheme  # Словарь для управления

    def update(self, active_keys):
        for key, direction in self.control_scheme.items():
            if active_keys[key]:
                if direction == 'left':
                    self.rect.x -= self.speed
                elif direction == 'right':
                    self.rect.x += self.speed
                elif direction == 'up':
                    self.rect.y -= self.speed
                elif direction == 'down':
                    self.rect.y += self.speed


class Item(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((20, 20))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, SCREEN_WIDTH - 20)
        self.rect.y = random.randint(0, SCREEN_HEIGHT - 20)


class Game:
    def __init__(self):
        controls = {pygame.K_LEFT: 'left', pygame.K_RIGHT: 'right', pygame.K_UP: 'up', pygame.K_DOWN: 'down'}
        self.player1 = Player(GREEN, (SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2), controls)
        self.player2 = Player(BLUE, (3 * SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2), controls)
        self.active_player = self.player1  # Активный игрок по умолчанию
        self.items = pygame.sprite.Group()
        for _ in range(20):
            self.items.add(Item())
        self.all_sprites = pygame.sprite.Group(self.player1, self.player2, *self.items)

    def check_active_player(self, event):
        if event.key == pygame.K_1:
            self.active_player = self.player1
        elif event.key == pygame.K_2:
            self.active_player = self.player2

    def refresh_world(self, active_keys):
        self.active_player.update(active_keys)
        self.items.update()

    def check_hits(self):
        hits = pygame.sprite.spritecollide(self.active_player, self.items, True)
        if hits:
            print("Collected an item!")

    def run(self):
        clock = pygame.time.Clock()
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    self.check_active_player(event)

            # Обновление
            active_keys = pygame.key.get_pressed()
            self.refresh_world(active_keys)

            # Проверка столкновений
            self.check_hits()

            # Отрисовка
            screen.fill((0, 0, 0))
            self.all_sprites.draw(screen)

            pygame.display.flip()
            clock.tick(FPS)

        pygame.quit()


# Создание и запуск игры
if __name__ == "__main__":
    game = Game()
    game.run()
