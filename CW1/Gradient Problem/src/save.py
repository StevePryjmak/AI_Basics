import os
import matplotlib.pyplot as plt


def save_plot(func_name, beta, base_dir='resources/plots'):
    folder_path = os.path.join(base_dir, func_name)
    os.makedirs(folder_path, exist_ok=True)

    existing_images = [f for f in os.listdir(folder_path) if f.endswith('.png')]
    next_index = len(existing_images) + 1

    plot_filename = os.path.join(folder_path, f'{next_index}_{beta}.png')
    plt.savefig(plot_filename, dpi=800)
    print(f'Saved plot to {plot_filename}')