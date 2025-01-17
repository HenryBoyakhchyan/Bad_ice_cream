from stable_baselines3 import DQN
from stable_baselines3.common.env_util import make_vec_env
import imageio
from stable_baselines3.common.callbacks import BaseCallback
import numpy as np
from env import Game
import gymnasium as gym 
import pygame

class RewardLoggerCallback(BaseCallback):
    def __init__(self):
        super(RewardLoggerCallback, self).__init__()
        self.rewards = []

    def _on_step(self) -> bool:
        # Record the reward of the current step
        self.rewards.append(self.locals["rewards"])
        return True
    
    # Register the environment
gym.envs.registration.register(
    id='Game',
    entry_point=Game
)

# Create the environment
env = gym.make("Game")
# Set up the DQN model
model = DQN("MlpPolicy", env, verbose=1, learning_rate=0.0001, buffer_size=100000, batch_size=32)

# Train the model
timesteps = 800000
reward_callback = RewardLoggerCallback()
model.learn(total_timesteps = timesteps, callback = reward_callback) # FILL IN

# Step 5: Save the model
model_path = "game"
model.save(model_path) # FILL IN

# Visualize the trained model
env = gym.make("Game")
obs, _ = env.reset()

frames = []

for _ in range(1000000):
    action, _ = model.predict(obs, deterministic=True)
    obs, reward, done, truncated, info = env.step(action)

    # Render the current state to a Pygame surface and capture it
    screen = env.render()
    frame = pygame.surfarray.array3d(screen)
    frame = frame.swapaxes(0, 1)
    frames.append(frame)

    if done:
        break

# Save the frames as a GIF
gif_path = "game.gif"
imageio.mimsave(gif_path, frames, fps=10)

# Output the GIF in Colab
from IPython.display import Image
Image(filename=gif_path)