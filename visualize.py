import json
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from matplotlib.colors import Normalize
import matplotlib.image as mpimg
import os
import keyboard

def load_data(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)

def prepare_heatmap_data(grid_data, time_bin, grid_size=50, map_size=1000):
    # Initialize a 2D array for the heatmap (100x100 grid for a 1000x1000 map, each cell is 10x10)
    num_cells = map_size // grid_size
    heatmap = np.zeros((num_cells, num_cells))

    # Fill the heatmap with counts from the data
    for box, data in grid_data.get(str(time_bin), {}).items():
        x_bin, y_bin = eval(box)  # Convert string tuple "(x, y)" to tuple (x, y)
        heatmap[y_bin, x_bin] = data["count"]

    return heatmap

def filter_bottom_20_percent(heatmap):
    # Flatten the heatmap to compute the threshold
    flattened = heatmap.flatten()
    threshold = np.percentile(flattened, 20)  # Find the 20th percentile value

    # Set all values below the threshold to 0 (removing bottom 20%)
    filtered_heatmap = np.where(heatmap >= threshold, heatmap, 0)

    return filtered_heatmap

def plot_heatmap_with_background(heatmap, time_bin, background_path, grid_size=50, map_size=1000):
    # Load the background image
    img = mpimg.imread(background_path)

    
    # Set up the figure
    plt.figure(figsize=(12, 10))

    # Display the background image for grid size 10 use [-0, 100, -0, 100]
    extent = [-0, map_size/grid_size, -0, map_size/grid_size]
    plt.imshow(img,extent=extent, aspect='auto', zorder=1)
    ##plt.show()
    # Create a mask for transparency (values of 0 will be transparent)
    mask = heatmap == 0

    # Create the heatmap
    sns.heatmap(
        heatmap,
        cmap="YlGnBu",
        linewidths=0.5,
        linecolor='gray',
        cbar_kws={'label': 'Count'},
        square= True,
        alpha=0.7,
        mask=mask,
        zorder=2,  # Ensure heatmap is plotted above the image
    )

    # Add labels and title
    plt.title(f"Filtered Heatmap of Positions at Time Bin {time_bin} (Top 80%)", fontsize=16)
    plt.xlabel("X-coordinate (grid)", fontsize=14)
    plt.ylabel("Y-coordinate (grid)", fontsize=14)
    ##plt.tight_layout()
    plt.show()

# Example usage
data_file = ".venv/Scripts/Testing/formations/Murovanka_1_formation.json"
background_image_path = ".venv/Scripts/Testing/11_murovanka.png"  # Replace with your background image file path

print(os.getcwd())
# Load the data
grid_data = load_data(data_file)

# Visualize all time bins with background image
for time_bin in sorted(map(int, grid_data.keys())):  # Iterate through all time bins
    heatmap = prepare_heatmap_data(grid_data, time_bin)
    filtered_heatmap = filter_bottom_20_percent(heatmap)  # Remove bottom 20% of values
    plot_heatmap_with_background(filtered_heatmap, time_bin, background_image_path)

    if(keyboard.is_pressed('q')): continue