from env import Game, UP, DOWN, LEFT, RIGHT, CREATE_BLOCK
import pygame

# Main game loop
if __name__ == "__main__":
    env = Game()  # Initialize the environment
    done = False
    observation, _ = env.reset()

    # Create a pygame event loop to handle keyboard input
    while not done:
        action = None  # Initialize action variable
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    action = UP
                elif event.key == pygame.K_DOWN:
                    action = DOWN
                elif event.key == pygame.K_LEFT:
                    action = LEFT
                elif event.key == pygame.K_RIGHT:
                    action = RIGHT
                elif event.key == pygame.K_SPACE:  # Space to create block
                    action = CREATE_BLOCK
                observation, reward, done, _ = env.step(action)

                env.render()  # Render the updated game state

    pygame.quit()  # Quit Pygame when the loop ends
