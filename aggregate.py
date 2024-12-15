import json
from collections import defaultdict, Counter
import os


def formation_data(path,m,s,time):

    combined_data = []
    for file in os.listdir(path):
        file_path = os.path.join(path,file)
        ##print(file_path)
        map = file.split('_')[0]
        side = file.split('_')[1]
        print(file_path)
        print(map,side, time)

        if (map == map) & (side == side):
            with open(file_path,'r') as f:
                j = json.load(f)
                try:
                    obj = j[time]
                    combined_data.append(obj)
                except KeyError:
                    print("Key not found in JSON data.")
    return combined_data

                

##pull formation data

folder = ".venv/Scripts/Testing/formations"


data =  formation_data(folder,"Murovanka","2","75")

with open("out.json", 'w') as f:
        json.dump(data, f, indent=3)





