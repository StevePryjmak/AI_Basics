import matplotlib.pyplot as plt
import os
import json
import datetime


def plot_results(averaged_rewards, labels, title, colors):
    """Plot the results for baseline and modified rewards."""
    fig = plt.figure(figsize=(10, 6))
    ax = fig.add_subplot(1, 1, 1)

    for avg_reward, label, color in zip(averaged_rewards, labels, colors):
        ax.plot(avg_reward, label=label, color=color)

    ax.spines['left'].set_position('center')
    ax.spines['bottom'].set_position('zero')
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')
    ax.set_xlabel("Episodes")
    ax.legend()
    plt.savefig("plot.png")
    plt.show()


def save_plot_data(averaged_rewards, labels, constants, base_dir="results"):
    if not os.path.exists(base_dir):
        os.makedirs(base_dir)
    # Define the filename with the current timestamp
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = os.path.join(base_dir, f"plot_data_{timestamp}.json")

    # Prepare data to be saved
    data = {
        "constants": constants,
        "rewards": [
            {"label": label, "reward": avg_reward.tolist()} 
            for label, avg_reward in zip(labels, averaged_rewards)
        ]
    }
    # Save the data to a JSON file
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)
    print(f"Plot data saved to {filename}")
