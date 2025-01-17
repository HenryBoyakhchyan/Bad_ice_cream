Here's an explanation of the project and how to run and train the RL (DQN) agent:

---

### **Game Explanation:**

The game you're working on is a simplified version of the **Bad Ice Cream** game, where the player controls an ice cream character that needs to avoid enemies, collect fruits, and can create blocks to prevent enemies from reaching them. Here's a breakdown of the **state**, **action**, and **reward**:

#### **State:**
- The game state is represented as a grid (2D numpy array) where each position can contain:
  - **0**: Empty space
  - **1**: Ice cream (player)
  - **2**: Enemy
  - **3**: Fruit
  - **4**: Block (created by the player)

#### **Action:**
The agent can perform one of the following actions:
1. **UP**: Move the ice cream up.
2. **DOWN**: Move the ice cream down.
3. **LEFT**: Move the ice cream left.
4. **RIGHT**: Move the ice cream right.
5. **CREATE_BLOCK**: Place a block in the current position.

#### **Reward:**
- **+1**: Reward for collecting a fruit.
- **-10**: Penalty for colliding with an enemy.
- **-1**: Penalty for colliding with a block.
- **0**: No reward for an empty action or creating a block.
- **+10**: Reward for completing the game (e.g., all fruits collected).
- **-10**: Penalty for exceeding the maximum steps or losing the game due to collision.

---

### **Instructions to Run the Game:**

1. **Clone this Repository**:  
   Make a copy of this repository to your local machine.

2. **Run the Game**:  
   Navigate to the directory where `game.py` is located and run the script:
   ```bash
   python game.py
   ```
   This will start the game, and you'll control the ice cream using the arrow keys (up, down, left, right) and the space bar to create blocks.

---

### **Instructions to Train RL (DQN) Agent:**

1. **Clone this Repository**:  
   Make a copy of this repository to your local machine.

2. **Train the RL Agent**:  
   Navigate to the directory where `train_agent.py` is located and run the script:
   ```bash
   python train_agent.py
   ```
   This script will use the **DQN (Deep Q-Network)** algorithm from the **stable-baselines3** library to train an agent to play the game.

3. **Monitor Training**:  
   You can track the agent's progress using the `RewardLoggerCallback`, which logs rewards for each training step.

4. **Save the Model**:  
   After training, the model will be saved at the path `game`, which can later be loaded to test the agent.

---

### **Contributions:**

This project was created as part of a TUMO (Training, Understanding, and Mastering Outcomes) initiative and uses the **Gymnasium** library (for creating environments) and **stable-baselines3** (for training the DQN agent).

---









