import pygame
import numpy as np
import gymnasium as gym
from gymnasium import spaces
import random
import time


# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
GRID_SIZE = 50
GRID_ROWS = SCREEN_HEIGHT // GRID_SIZE  # Make sure this reflects the screen height
GRID_COLS = SCREEN_WIDTH // GRID_SIZE  # Make sure this reflects the screen width
FPS = 10

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Action constants (Up, Down, Left, Right, Create Block)
UP = 0
DOWN = 1
LEFT = 2
RIGHT = 3
CREATE_BLOCK = 4

# Entity constants (Ice Cream, Enemy, Fruit, Block)
ICE_CREAM = 1
ENEMY = 2
FRUIT = 3
BLOCK = 4

# Directions for the enemy's movement (up, right, down, left)
DIRECTIONS = [(-1, 0), (0, 1), (1, 0), (0, -1)]  # Up, Right, Down, Left

MAX_STEPS = 40

class Game(gym.Env):
    def __init__(self):
        super(Game, self).__init__()

        self.state = None
        self.reward = 0
        self.done = False
        self.ice_cream_pos = None
        self.enemy_positions = []
        self.fruit_positions = []
        self.block_positions = []
        self.start_time = None  # Timer variable

        # Action space (5 actions)
        self.action_space = spaces.Discrete(5)

        # Observation space (grid)
        self.observation_space = spaces.Box(low=0, high=5, shape=(GRID_ROWS, GRID_COLS), dtype=np.int32)

        self.steps = 0 # number of steps taken

        # Pygame setup
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Bad Ice Cream")
        self.font = pygame.font.SysFont(None, 36)

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        self.state = np.zeros((GRID_ROWS, GRID_COLS), dtype=np.int32)
        self.reward = 0
        self.done = False
        
        # Ice Cream Position
        self.ice_cream_pos = (random.randint(0, GRID_ROWS - 1), random.randint(0, GRID_COLS - 1))
        
        # Randomly generate number of enemies (between 3 and 5, for example)
        num_enemies = random.randint(3, 5)
        self.enemy_positions = []
        for _ in range(num_enemies):
            enemy_pos = (random.randint(0, GRID_ROWS - 1), random.randint(0, GRID_COLS - 1))
            self.enemy_positions.append(enemy_pos)

        # Randomly generate number of fruits (between 3 and 7, for example)
        num_fruits = random.randint(3, 7)
        self.fruit_positions = []
        for _ in range(num_fruits):
            self.fruit_positions.append((random.randint(0, GRID_ROWS - 1), random.randint(0, GRID_COLS - 1)))

        self.block_positions = []

        self._update_grid()

        # Start the timer when the game resets
        self.start_time = time.time()

        return np.array(self.state, dtype=np.int32), {}

    def _update_grid(self):
        self.state.fill(0)
        self.state[self.ice_cream_pos[0], self.ice_cream_pos[1]] = ICE_CREAM
        for pos in self.enemy_positions:
            self.state[pos[0], pos[1]] = ENEMY
        for pos in self.fruit_positions:
            self.state[pos[0], pos[1]] = FRUIT
        for pos in self.block_positions:
            self.state[pos[0], pos[1]] = BLOCK

    def step(self, action):
        self.steps += 1

        # Calculate the new position based on the action
        if action == UP:
            new_pos = (self.ice_cream_pos[0] - 1, self.ice_cream_pos[1])
        elif action == DOWN:
            new_pos = (self.ice_cream_pos[0] + 1, self.ice_cream_pos[1])
        elif action == LEFT:
            new_pos = (self.ice_cream_pos[0], self.ice_cream_pos[1] - 1)
        elif action == RIGHT:
            new_pos = (self.ice_cream_pos[0], self.ice_cream_pos[1] + 1)
        elif action == CREATE_BLOCK:
            self.block_positions.append(self.ice_cream_pos)
            self._update_grid()
            return np.array(self.state, dtype=np.int32), 0, self.done, False, {}

        # Bound the new position within grid limits
        new_pos = (max(0, min(GRID_ROWS - 1, new_pos[0])), max(0, min(GRID_COLS - 1, new_pos[1])))

        # Check if the ice cream bumps into an enemy
        if new_pos in self.enemy_positions: # OLD ENEMY POS
            self.done = True
            return np.array(self.state, dtype=np.int32), -10, self.done, False, {}  # Immediate death penalty

        # Check if the ice cream collides with a block
        if self.state[new_pos[0], new_pos[1]] == BLOCK:
            return np.array(self.state, dtype=np.int32), -1, True, False, {}

        # If no collision, move the ice cream
        self.ice_cream_pos = new_pos
        self._update_grid()

        # Check if ice cream eats a fruit
        if self.state[self.ice_cream_pos[0], self.ice_cream_pos[1]] == FRUIT:
            self.reward += 1
            self.fruit_positions.remove(self.ice_cream_pos)
            self._update_grid()
        
        # self.enemy_pos = old enemy positions

        # Move enemies randomly
        self._move_enemies()

        # self.enemy_pos = new enemy pos
        
        # Check if the ice cream bumps into an enemy
        if new_pos in self.enemy_positions: #NEW ENEMY POS
            self.done = True
            return np.array(self.state, dtype=np.int32), -10, self.done, False, {}  # Immediate death penalty

        # Check the timer
        # elapsed_time = time.time() - self.start_time
        # if elapsed_time > 10:
        #     self.done = True
        #     return np.array(self.state, dtype=np.int32), -10, self.done, {}  # Loss due to timeout

        if self.steps > MAX_STEPS:
            self.done = True
            return np.array(self.state, dtype=np.int32), -10, True, False, {}  

        if len(self.fruit_positions) == 0:
            self.done = True
            return np.array(self.state, dtype=np.int32), 10, True, False, {}  
             ## self.done = True when new player position is in enemy position

        return np.array(self.state, dtype=np.int32), self.reward, self.done, False, {}

    def _move_enemies(self):
        # Randomly move each enemy, but don't allow them to go into a block containing fruit
        new_enemy_positions = []
        for pos in self.enemy_positions:
            # Randomly choose a direction
            direction = random.choice(DIRECTIONS)  # Randomly select a direction
            new_pos = (pos[0] + direction[0], pos[1] + direction[1])

            # Keep enemy inside grid bounds
            new_pos = (max(0, min(GRID_ROWS - 1, new_pos[0])), max(0, min(GRID_COLS - 1, new_pos[1])))

            # Ensure the new position is not a block that contains fruit
            if self.state[new_pos[0], new_pos[1]] == BLOCK or self.state[new_pos[0], new_pos[1]] == FRUIT:
                # If the enemy is about to go to a blocked or fruit-filled position, keep the old position
                new_pos = pos

            new_enemy_positions.append(new_pos)

        self.enemy_positions = new_enemy_positions
        self._update_grid()

    def render(self):
        self.screen.fill(WHITE)
        for x in range(0, SCREEN_WIDTH, GRID_SIZE):
            for y in range(0, SCREEN_HEIGHT, GRID_SIZE):
                pygame.draw.rect(self.screen, BLACK, pygame.Rect(x, y, GRID_SIZE, GRID_SIZE), 1)

        for x in range(self.state.shape[0]):
            for y in range(self.state.shape[1]):
                if self.state[x, y] == ICE_CREAM:
                    pygame.draw.circle(self.screen, BLUE, (y * GRID_SIZE + GRID_SIZE // 2, x * GRID_SIZE + GRID_SIZE // 2), GRID_SIZE // 3)
                elif self.state[x, y] == ENEMY:
                    pygame.draw.rect(self.screen, RED, pygame.Rect(y * GRID_SIZE, x * GRID_SIZE, GRID_SIZE, GRID_SIZE))
                elif self.state[x, y] == FRUIT:
                    pygame.draw.circle(self.screen, GREEN, (y * GRID_SIZE + GRID_SIZE // 2, x * GRID_SIZE + GRID_SIZE // 2), GRID_SIZE // 4)
                elif self.state[x, y] == BLOCK:
                    pygame.draw.rect(self.screen, (200, 200, 255), pygame.Rect(y * GRID_SIZE, x * GRID_SIZE, GRID_SIZE, GRID_SIZE))

        # Display the remaining time
        # elapsed_time = time.time() - self.start_time
        # remaining_time = max(0, 10 - int(elapsed_time))
        # timer_text = self.font.render(f"Time: {remaining_time}s", True, BLACK)
        # self.screen.blit(timer_text, (SCREEN_WIDTH - 150, 20))


        # Display the remaining number of steps
        steps_left = MAX_STEPS - self.steps
        steps_text = self.font.render(f"Steps Left: {steps_left}s", True, BLACK)
        self.screen.blit(steps_text, (SCREEN_WIDTH - 300, 20))
        pygame.display.update()

        return self.screen


