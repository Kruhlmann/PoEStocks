import numpy as np
from matplotlib import pyplot as plt
import time
import api

league = "Harbinger"
currencies = [
    {"price": [], "name": "alteration", "id": 1},
    {"price": [], "name": "fusing", "id": 2},
    {"price": [], "name": "alchemy", "id": 3},
    {"price": [], "name": "chaos", "id": 4},
    {"price": [], "name": "gemcutter", "id": 5},
    {"price": [], "name": "exalted", "id": 6},
    {"price": [], "name": "chromatic", "id": 7},
    {"price": [], "name": "jeweler", "id": 8},
    {"price": [], "name": "chance", "id": 9},
    {"price": [], "name": "chisel", "id": 10},
    {"price": [], "name": "scouring", "id": 11},
    {"price": [], "name": "blessed", "id": 12},
    {"price": [], "name": "regret", "id": 13},
    {"price": [], "name": "regal", "id": 14},
    {"price": [], "name": "divine", "id": 15},
    {"price": [], "name": "vaal", "id": 16},
    {"price": [], "name": "wisdom", "id": 17},
    {"price": [], "name": "portal", "id": 18},
    {"price": [], "name": "scrap", "id": 19},
    {"price": [], "name": "whetstone", "id": 20},
    {"price": [], "name": "glassblower", "id": 21},
    {"price": [], "name": "transmutation", "id": 22},
    {"price": [], "name": "augmentation", "id": 23},
    {"price": [], "name": "mirror", "id": 24},
    {"price": [], "name": "eternal", "id": 25},
    {"price": [], "name": "perandus", "id": 26},
    {"price": [], "name": "coin", "id": 27},
    {"price": [], "name": "dusk-sacrifice", "id": 28},
    {"price": [], "name": "midnight-sacrifice", "id": 29},
    {"price": [], "name": "dawn-sacrifice", "id": 30},
    {"price": [], "name": "noon-sacrifice", "id": 31},
    {"price": [], "name": "mortal-grief", "id": 32},
    {"price": [], "name": "mortal-rage", "id": 33},
    {"price": [], "name": "mortal-hope", "id": 34},
    {"price": [], "name": "mortal-ignorance", "id": 35},
    {"price": [], "name": "key-eber", "id": 36},
    {"price": [], "name": "key-yriel", "id": 37},
    {"price": [], "name": "key-inya", "id": 37},
    {"price": [], "name": "key-volkuur", "id": 37},
    {"price": [], "name": "noon-sacrifice", "id": 37},
    {"price": [], "name": "noon-sacrifice", "id": 37},
    {"price": [], "name": "noon-sacrifice", "id": 37},
    {"price": [], "name": "noon-sacrifice", "id": 37},
    {"price": [], "name": "noon-sacrifice", "id": 37},
    {"price": [], "name": "noon-sacrifice", "id": 37},
    {"price": [], "name": "noon-sacrifice", "id": 37},
]

def routine():
    for currency in currencies:
        currency["price"].append(api.get_average_exchange_rate(league=league, want=4, have=currency["id"]))

for i in range(0, 5):
    try:
        routine()
    except KeyboardInterrupt:
        print("Exiting...")
        exit(0)

for currency in currencies:
    y = np.array(currency["price"])
    plt.plot(y)
    plt.savefig("img/graphs/{0}.png".format(currency["name"]), transparent=True)
    plt.clf()