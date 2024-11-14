import os
import matplotlib.pyplot as plt

def save(path, name="plot"):
    if not os.path.exists(path):
        os.makedirs(path)

    index = 1
    while os.path.exists(f"{path}/{name}_{index}.png"):
        index += 1
    
    file_path = f"{path}/{name}_{index}.png"
    plt.savefig(file_path, dpi=600)
    print(f"Plot saved as {file_path}")
    return file_path
