import os
import time

import requests
import json

def save_info_to_json():
    dict = {}
    for i in range (1000_000):
        dict[i] = i**2
    print(dict)
    with open("wzz/test.json", 'w') as f:
        json.dump(dict, f, indent=4)

    
if __name__ == "__main__":
    save_info_to_json()
