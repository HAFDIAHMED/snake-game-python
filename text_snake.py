import random
import os
import time
from threading import Timer
import sys
import termios
import tty

def getch():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch

class SnakeGame:
    def __init__(self, width=20, height=10):
        self.width = width
        self.height = height
        self.snake = [(width//2, height//2)]
        self.direction = 'RIGHT'
        self.food = self._generate_food()
        self.score = 0
        self.game_over = False

    def _generate_food(self):
        while True:
            food = (random.randint(0, self.width-1), random.randint(0, self.height-1))
            if food not in self.snake:
                return food

    def move(self):
        head = self.snake[0]
        if self.direction == 'UP':
            new_head = (head[0], head[1]-1)
        elif self.direction == 'DOWN':
            new_head = (head[0], head[1]+1)
        elif self.direction == 'LEFT':
            new_head = (head[0]-1, head[1])
        else:  # RIGHT
            new_head = (head[0]+1, head[1])

        # Check for collisions
        if (new_head[0] < 0 or new_head[0] >= self.width or
            new_head[1] < 0 or new_head[1] >= self.height or
            new_head in self.snake):
            self.game_over = True
            return

        self.snake.insert(0, new_head)
        
        # Check if food is eaten
        if new_head == self.food:
            self.score += 1
            self.food = self._generate_food()
        else:
            self.snake.pop()

    def draw(self):
        os.system('clear' if os.name == 'posix' else 'cls')
        print(f'Score: {self.score}')
        print('=' * (self.width + 2))
        
        for y in range(self.height):
            print('|', end='')
            for x in range(self.width):
                if (x, y) == self.food:
                    print('*', end='')
                elif (x, y) in self.snake:
                    print('O' if (x, y) == self.snake[0] else 'o', end='')
                else:
                    print(' ', end='')
            print('|')
            
        print('=' * (self.width + 2))
        print('Use WASD to move, Q to quit')

def main():
    game = SnakeGame()
    last_update = time.time()
    update_interval = 0.2  # seconds

    while not game.game_over:
        if time.time() - last_update >= update_interval:
            game.move()
            game.draw()
            last_update = time.time()

        if sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
            key = getch().lower()
            if key == 'w' and game.direction != 'DOWN':
                game.direction = 'UP'
            elif key == 's' and game.direction != 'UP':
                game.direction = 'DOWN'
            elif key == 'a' and game.direction != 'RIGHT':
                game.direction = 'LEFT'
            elif key == 'd' and game.direction != 'LEFT':
                game.direction = 'RIGHT'
            elif key == 'q':
                game.game_over = True

    print(f'\nGame Over! Final score: {game.score}')

if __name__ == '__main__':
    import select
    try:
        main()
    except KeyboardInterrupt:
        print('\nGame terminated by user')