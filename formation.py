import json
from collections import defaultdict, Counter
import os

def process_positions_with_tanks(file_path, grid_size=50, map_size=1000, time_interval=1):
    # To store counts of tanks in each grid box per time interval
    grid_data = defaultdict(lambda: defaultdict(lambda: {"count": 0, "tanks": Counter()}))

    with open(file_path, 'r') as file:
        for line in file:
            data = json.loads(line)
            map = data["map"]
            side = data["side"]
            time = data["time"]
            pos = data["pos"]
            tank = data["tank"]
            x, y = pos["x"], pos["y"]
            win = data["win"]
            

            # grid box for the position
            x_bin = int((x + map_size // 2) // grid_size)
            y_bin = int((y + map_size // 2) // grid_size)

            time_bin = time // time_interval

            # Update the count for this box and time interval
            grid_data[time_bin][(x_bin, y_bin)]["count"] += 1
            grid_data[time_bin][(x_bin, y_bin)]["tanks"][tank] += 1

    return grid_data, map, side, win

def save_results_with_tanks(win,grid_data, output_file):
    # Convert Counter objects to dictionaries for JSON serialization
    serializable_data = {
        time_bin: {
            str(box): {
                "win": win,
                "count": data["count"],
                "tanks": dict(data["tanks"])
            }
            for box, data in boxes.items()
        }
        for time_bin, boxes in grid_data.items()
    }

    with open(output_file, 'w') as f:
        json.dump(serializable_data, f, indent=4)

def process(file_path):
    x=0
    for file in os.listdir(file_path):
        x+=1
        print( os.path.join(file_path,file))
        file = os.path.join(file_path,file)
        print(os.getcwd()) ## for when file DNE err
        grid_data, map, side,win = process_positions_with_tanks(file)
        output_file = f'.venv/Scripts/Testing/formations/{map}_{side}_formations_{x}.json'
        save_results_with_tanks(win,grid_data, output_file)

## Start of usage
file_path = "/Users/simon/Desktop/Wot_Analyzer/Movement/Movement/src/Out"

process(file_path)
