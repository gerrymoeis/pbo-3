import pygame, sys, random, time

pygame.init()

class GameObject:
    def __init__(self, color, position, size):
        self.color = color
        self.position = position
        self.size = size
    
    def draw(self, game_window):
        pygame.draw.rect(game_window, self.color, pygame.Rect(self.position[0], self.position[1], self.size, self.size))

class Snake(GameObject):
    def __init__(self, color, position, size, speed=10):
        super().__init__(color, position, size)
        self.body = [list(position), [position[0] - size, position[1]], [position[0] - size, position[1]]]
        self.speed = speed
        self.direction = 'RIGHT'
        self.change_to = self.direction
    
    def change_direction(self, direction):
        if direction == 'UP' and self.direction != 'DOWN':
            self.change_to = 'UP'
        if direction == 'DOWN' and self.direction != 'UP':
            self.change_to = 'DOWN'
        if direction == 'LEFT' and self.direction != 'RIGHT':
            self.change_to = 'LEFT'
        if direction == 'RIGHT' and self.direction != 'LEFT':
            self.change_to = 'RIGHT'
    
    def move(self):
        self.direction = self.change_to
        if self.direction == 'UP':
            self.position[1] -= self.speed
        if self.direction == 'DOWN':
            self.position[1] += self.speed
        if self.direction == 'LEFT':
            self.position[0] -= self.speed
        if self.direction == 'RIGHT':
            self.position[0] += self.speed
        self.body.insert(0, list(self.position))
    
    def shrink(self):
        self.body.pop()
    
    def draw(self, game_window):
        for pos in self.body:
            pygame.draw.rect(game_window, self.color, pygame.Rect(pos[0], pos[1], self.size, self.size))
    
    def check_collision(self, frame_size_x, frame_size_y):
        if self.position[0] < 50 or self.position[0] > frame_size_x - 50 - self.size or self.position[1] < 50 or self.position[1] > frame_size_y - self.size:
            return True
        
        for block in self.body[1:]:
            if self.position[0] == block[0] and self.position[1] == block[1]:
                return True
        
        return False

class Apple(GameObject):
    def __init__(self, frame_size_x, frame_size_y, color):
        self.position = self.spawn(frame_size_x, frame_size_y)
        super().__init__(color, self.position, 10)
    
    def spawn(self, frame_size_x, frame_size_y):
        return [random.randrange(6, (frame_size_x // 10 - 6)) * 10, random.randrange(6, (frame_size_y // 10 - 6)) * 10]
    
    def respawn(self, frame_size_x, frame_size_y):
        self.position = self.spawn(frame_size_x, frame_size_y)

class Arena(GameObject):
    def __init__(self, color, position, size):
        super().__init__(color, position, size)

class Game:
    def __init__(self, apple_amount):
        self.frame_size_x = 720
        self.frame_size_y = 480
        self.game_window = pygame.display.set_mode((self.frame_size_x, self.frame_size_y))
        pygame.display.set_caption('Aowkwk')

        self.fps_controller = pygame.time.Clock()
        self.snake = Snake(pygame.Color(0, 255, 0), [100, 50], 10)
        self.score = 0

        self.apples = []
        for _ in range(apple_amount):
            self.apples.append(Apple(self.frame_size_x, self.frame_size_y, pygame.Color(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))))

        self.arena_position = (50, 50)
        self.arena_size = (self.frame_size_x - 100, self.frame_size_y - 100)

    def draw_arena(self):
        pygame.draw.rect(self.game_window, pygame.Color(0, 0, 0), pygame.Rect(self.arena_position[0], self.arena_position[1], self.arena_size[0], self.arena_size[1]), 2)

    def game_over(self):
        my_font = pygame.font.SysFont('Times New Roman', 90)
        game_over_surface = my_font.render('YOU DIED', True, pygame.Color(255, 0, 0))
        game_over_rect = game_over_surface.get_rect()
        game_over_rect.midtop = (self.frame_size_x / 2, self.frame_size_y / 4)
        self.game_window.fill(pygame.Color(0, 0, 0))
        self.game_window.blit(game_over_surface, game_over_rect)

        pygame.display.flip()
        time.sleep(3)
        pygame.quit()
        sys.exit()
    
    def show_score(self):
        score_font = pygame.font.SysFont('Times New Roman', 20)
        score_surface = score_font.render('Score : ' + str(self.score), True, pygame.Color(0, 0, 0))
        score_rect = score_surface.get_rect()
        score_rect.midtop = (72, 15)
        self.game_window.blit(score_surface, score_rect)
    
    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.snake.change_direction('UP')
                    if event.key == pygame.K_DOWN:
                        self.snake.change_direction('DOWN')
                    if event.key == pygame.K_LEFT:
                        self.snake.change_direction('LEFT')
                    if event.key == pygame.K_RIGHT:
                        self.snake.change_direction('RIGHT')

                    if event.key == pygame.K_ESCAPE:
                        pygame.event.post(pygame.event.Event(pygame.QUIT))
            
            self.snake.move()

            if self.snake.position in map(lambda apple: apple.position, self.apples):
                eated_apple = [apple for apple in self.apples if apple.position == self.snake.position][0]
                eated_apple.respawn(self.arena_size[0], self.arena_size[1])

                self.score += 1
            else:
                self.snake.shrink()
            
            self.game_window.fill(pygame.Color(255, 255, 255))

            self.draw_arena()
            self.snake.draw(self.game_window)
            self.show_score()

            for apple in self.apples:
                apple.draw(self.game_window)

            if self.snake.check_collision(self.frame_size_x, self.arena_size[1] + self.arena_position[1]):
                self.game_over()
            
            pygame.display.update()
            self.fps_controller.tick(10)

if __name__ == '__main__':
    game = Game(20)
    game.run()