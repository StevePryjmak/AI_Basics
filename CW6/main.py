import gymnasium as gym
import numpy as np
import math
from ploter import plot_results, save_plot_data
import random
import pickle


# Constants
NUM_RUNS = 25
NUM_EPISODES_NO_SLIP = 1000
NUM_EPISODES_SLIP = 10000
DISCOUNT_FACTOR = 0.9
LEARNING_RATE = 0.8
EPSILON_START = 1
SCALING_CONSTANT = 0.1
MAX_MOVES_PER_EPISODE = 100
rng = np.random.default_rng()


def reward_baseline(state, next_state, base_reward, terminated, info):
    return base_reward


def reward_avoiding_wals(state, next_state, base_reward, terminated, info):
    if state == next_state:
        return -0.5
    return base_reward


def reward_avoiding_holes(state, next_state, base_reward, terminated, info):
    if terminated and base_reward == 0:
        return base_reward - 1
    return base_reward

def reward_avoiding_wals_and_holes(state, next_state, base_reward, terminated, info):
    if state == next_state:
        return -0.5
    if terminated and base_reward == 0:
        return base_reward - 1
    return base_reward


def print_q_table(qtable):
    print("Q-table after training:")
    for state in range(qtable.shape[0]):
        print(f"State {state}: {qtable[state]}")

def train_q_learning(env, num_episodes, reward_system):
    """Q-learning algorithm."""
    state_size = env.observation_space.n
    action_size = env.action_space.n
    averaged_reward = np.zeros(num_episodes)
    qtable = 0
    for run in range(NUM_RUNS):
        qtable = np.zeros((state_size, action_size))

        for episode in range(num_episodes):
            if (episode + 1) % 100 == 0:
                print(f"Run: {run + 1:>3} - Episode: {episode + 1:>6}")
            state, _ = env.reset()
            terminated, truncated = False, False
            total_reward = 0
            num_moves = 0
            while not terminated and not truncated:
                epsilon = EPSILON_START / math.sqrt(1 + SCALING_CONSTANT * episode)
                if rng.random() < epsilon:
                    action = env.action_space.sample()
                else:
                    max_value = np.max(qtable[state, :])
                    best_actions = [a for a in range(action_size) if qtable[state, a] == max_value]
                    action = random.choice(best_actions)

                next_state, base_reward, terminated, truncated, info = env.step(action)
                reward = reward_system(state, next_state, base_reward, terminated, info)

                qtable[state, action] += LEARNING_RATE * (
                    reward + DISCOUNT_FACTOR * np.max(qtable[next_state, :]) - qtable[state, action]
                )

                total_reward += base_reward
                state = next_state

                num_moves += 1
                if num_moves >= MAX_MOVES_PER_EPISODE:
                    truncated = True
            averaged_reward[episode] += total_reward
    averaged_reward /= NUM_RUNS
    print_q_table(qtable)
    return averaged_reward




def save_rewards(filename, data):
    with open(filename, 'wb') as file:
        pickle.dump(data, file)


def load_rewards(filename):
    with open(filename, 'rb') as file:
        data = pickle.load(file)
    return data


def main():
    env = gym.make('FrozenLake-v1', desc=None, map_name="8x8", is_slippery=False)
    averaged_reward_base = train_q_learning(env, NUM_EPISODES_NO_SLIP, reward_baseline)
    # averaged_reward_out_of_field = train_q_learning(env, NUM_EPISODES_NO_SLIP, reward_avoiding_holes)
    # # averaged_reward_custom2 = train_q_learning(env, NUM_EPISODES_NO_SLIP, reward_custom2)
    averaged_reward_av_w_h = train_q_learning(env, NUM_EPISODES_NO_SLIP, reward_avoiding_wals_and_holes)
    plot_results(
        [averaged_reward_base, averaged_reward_av_w_h],# , averaged_reward_custom1, averaged_reward_custom2
        ["Basic", "Avoid holes wall moves"], # , "Custom Reward 1", "Custom Reward 2"
        "FrozenLake (No Slippery Surface)",
        ['r', 'b']# , 'g', 'b'
    )

    # Experiment 2: Slippery environment
    # env = gym.make('FrozenLake-v1', desc=None, map_name="8x8", is_slippery=True)
    # averaged_reward_base_slip = train_q_learning(env, NUM_EPISODES_SLIP, reward_baseline)
    # averaged_reward_av_w = train_q_learning(env, NUM_EPISODES_SLIP, reward_avoiding_wals)
    # averaged_reward_av_h = train_q_learning(env, NUM_EPISODES_SLIP, reward_avoiding_holes)
    # averaged_reward_av_w_h = train_q_learning(env, NUM_EPISODES_SLIP, reward_avoiding_wals_and_holes)
    # save_rewards("rewards.pkl", [averaged_reward_base_slip, averaged_reward_av_w, averaged_reward_av_h])
    # averaged_reward_base_slip, averaged_reward_av_w, averaged_reward_av_h = load_rewards("rewards.pkl")
    # plot_results(
    #     [averaged_reward_base_slip[::15]],
    #     ["Basic"],
    #     "FrozenLake (Slippery Surface)",
    #     ['r']
    # )
    # plot_results(
    #     [averaged_reward_base_slip[::15], averaged_reward_av_w_h[::15]],
    #     ["Basic", "Avoid wals and holes"],
    #     "FrozenLake (Slippery Surface)",
    #     ['r', 'b']
    # )
    # plot_results(
    #     [averaged_reward_base_slip[::15], averaged_reward_av_h[::15]],
    #     ["Basic", "Avoid Holes"],
    #     "FrozenLake (Slippery Surface)",
    #     ['r', 'b']
    # )
if __name__ == "__main__":
    main()