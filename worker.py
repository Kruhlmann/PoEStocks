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