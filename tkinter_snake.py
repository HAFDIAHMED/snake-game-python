import tkinter as tk
from tkinter import messagebox
import random

class SnakeGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Snake Game")
        
        # Game constants
        self.GAME_WIDTH = 700
        self.GAME_HEIGHT = 500
        self.SPEED = 100
        self.SPACE_SIZE = 20
        self.BODY_SIZE = 2
        self.SNAKE_COLOR = "#00FF00"
        self.FOOD_COLOR = "#FF0000"
        self.BACKGROUND_COLOR = "#000000"

        # Game variables
        self.direction = 'right'
        self.score = 0
        
        # Create score label
        self.label = tk.Label(self.root, text=f"Score: {self.score}", font=('consolas', 20))
        self.label.pack()

        # Create game canvas
        self.canvas = tk.Canvas(self.root, 
                              bg=self.BACKGROUND_COLOR,
                              height=self.GAME_HEIGHT,
                              width=self.GAME_WIDTH)
        self.canvas.pack()

        # Initialize game
        self.root.update()

        # Center the window
        window_width = self.root.winfo_width()
        window_height = self.root.winfo_height()
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        x = int((screen_width/2) - (window_width/2))
        y = int((screen_height/2) - (window_height/2))
        
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")

        # Bind keys
        self.root.bind('<Left>', lambda event: self.change_direction('left'))
        self.root.bind('<Right>', lambda event: self.change_direction('right'))
        self.root.bind('<Up>', lambda event: self.change_direction('up'))
        self.root.bind('<Down>', lambda event: self.change_direction('down'))

        # Initialize snake and food
        self.snake_positions = []
        self.food_position = []
        self.snake_body = []
        
        self.start_game()

    def start_game(self):
        # Create snake
        for i in range(self.BODY_SIZE):
            x = self.SPACE_SIZE * (self.BODY_SIZE - i)
            y = self.SPACE_SIZE
            self.snake_positions.append([x, y])
            square = self.canvas.create_rectangle(
                x, y,
                x + self.SPACE_SIZE, y + self.SPACE_SIZE,
                fill=self.SNAKE_COLOR, tag="snake"
            )
            self.snake_body.append(square)

        # Create food
        self.spawn_food()

        # Start game
        self.next_turn()

    def spawn_food(self):
        if self.food_position:  # If food exists, delete it
            self.canvas.delete("food")
            self.food_position = []

        # Generate random coordinates for new food
        while True:
            x = random.randint(0, (self.GAME_WIDTH - self.SPACE_SIZE) // self.SPACE_SIZE) * self.SPACE_SIZE
            y = random.randint(0, (self.GAME_HEIGHT - self.SPACE_SIZE) // self.SPACE_SIZE) * self.SPACE_SIZE
            
            # Make sure food doesn't spawn on snake
            if [x, y] not in self.snake_positions:
                self.food_position = [x, y]
                break

        self.canvas.create_oval(
            x, y,
            x + self.SPACE_SIZE, y + self.SPACE_SIZE,
            fill=self.FOOD_COLOR, tag="food"
        )

    def next_turn(self):
        # Get current head position
        head = self.snake_positions[0].copy()

        # Move head according to direction
        if self.direction == 'left':
            head[0] -= self.SPACE_SIZE
        elif self.direction == 'right':
            head[0] += self.SPACE_SIZE
        elif self.direction == 'up':
            head[1] -= self.SPACE_SIZE
        elif self.direction == 'down':
            head[1] += self.SPACE_SIZE

        # Insert new head
        self.snake_positions.insert(0, head)

        # Create new square for head
        square = self.canvas.create_rectangle(
            head[0], head[1],
            head[0] + self.SPACE_SIZE, head[1] + self.SPACE_SIZE,
            fill=self.SNAKE_COLOR
        )
        self.snake_body.insert(0, square)

        # Check if food is eaten
        if head == self.food_position:
            self.score += 1
            self.label.config(text=f"Score: {self.score}")
            self.spawn_food()
        else:
            # Remove tail
            del self.snake_positions[-1]
            self.canvas.delete(self.snake_body[-1])
            del self.snake_body[-1]

        # Check for collision
        if self.check_collision():
            self.game_over()
        else:
            self.root.after(self.SPEED, self.next_turn)

    def check_collision(self):
        head = self.snake_positions[0]
        
        # Check wall collision
        if (head[0] < 0 or 
            head[0] >= self.GAME_WIDTH or 
            head[1] < 0 or 
            head[1] >= self.GAME_HEIGHT):
            return True
        
        # Check self collision
        if head in self.snake_positions[1:]:
            return True
        
        return False

    def change_direction(self, new_direction):
        if new_direction == 'left' and self.direction != 'right':
            self.direction = new_direction
        elif new_direction == 'right' and self.direction != 'left':
            self.direction = new_direction
        elif new_direction == 'up' and self.direction != 'down':
            self.direction = new_direction
        elif new_direction == 'down' and self.direction != 'up':
            self.direction = new_direction

    def game_over(self):
        self.canvas.delete("all")
        self.canvas.create_text(
            self.GAME_WIDTH/2,
            self.GAME_HEIGHT/2,
            font=('consolas', 70),
            text="GAME OVER",
            fill="red",
            tag="gameover"
        )
        
        # Add restart button
        restart_button = tk.Button(
            self.root,
            text="Restart Game",
            command=self.restart_game,
            font=('consolas', 20)
        )
        restart_button.pack()

    def restart_game(self):
        # Clear everything
        self.canvas.delete("all")
        for widget in self.root.winfo_children():
            if isinstance(widget, tk.Button):
                widget.destroy()
        
        # Reset variables
        self.direction = 'right'
        self.score = 0
        self.label.config(text=f"Score: {self.score}")
        self.snake_positions = []
        self.food_position = []
        self.snake_body = []
        
        # Start new game
        self.start_game()

def main():
    root = tk.Tk()
    game = SnakeGame(root)
    root.mainloop()

if __name__ == "__main__":
    main()