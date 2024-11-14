import numpy as np
import matplotlib.pyplot as plt
from constants import * 
from save import save 
from population import Population
from draw import setup_grid 
from PIL import Image
import os

def create_gif_from_images(path, gif_name="evolution.gif", duration=200):
    images = sorted([img for img in os.listdir(path) if img.endswith(".png")], key=lambda x: int(x.split('.')[0]))
    
    frames = [Image.open(os.path.join(path, img)) for img in images]

    if frames:
        frames[0].save(
            os.path.join(path, gif_name),
            save_all=True,
            append_images=frames[1:],
            duration=duration,
            loop=0
        )
    else:
        print("No images found to create GIF.")




def plot_points_in_projection(population, generation, path, dimension_1=DEM_1, dimension_2=DEM_2):
    plt.figure(figsize=(8, 6))
    setup_grid(FUNKTION)
    points = [rep.get_position() for rep in population.representants]
    x_coords = [point[dimension_1] for point in points]
    y_coords = [point[dimension_2] for point in points]
    
    plt.scatter(x_coords, y_coords, c='blue', label=f'Generation {generation}')
    plt.xlabel(f"Dimension {dimension_1 + 1}")
    plt.ylabel(f"Dimension {dimension_2 + 1}")
    plt.title(f"Projection of Points - Generation {generation}")
    plt.grid(True)
    save(path, name=f'{generation}')


def main():
    path = '../resources/temp_grids'
    population = Population(POPULATION_SIZE, FUNKTION)
    for gen in range(int(MAX_EVALUATIONS / POPULATION_SIZE)):
        population.evolve()
        plot_points_in_projection(population, gen + 1, path)
    
    create_gif_from_images('../resources/temp_grids', gif_name="evolution.gif", duration=200)
    
    # plt.show()



if __name__ == "__main__":
    main()
