import numpy as np
from matplotlib import pyplot as plt
import time
import api
import sqlite3

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
    {"price": [], "name": "key-inya", "id": 38},
    {"price": [], "name": "key-volkuur", "id": 39},
    {"price": [], "name": "offering", "id": 40},
    {"price": [], "name": "hydra-fragment", "id": 41},
    {"price": [], "name": "phoenix-fragment", "id": 42},
    {"price": [], "name": "minotaur-fragment", "id": 43},
    {"price": [], "name": "chimera-fragment", "id": 44},
]

def routine():
    for currency in currencies:
        currency["price"].append(api.get_average_exchange_rate(league=league, want=4, have=currency["id"]))

def init_db(cursor):
    cursor.execute("""CREATE TABLE IF NOT EXISTS items (id INTEGER, name TEXT)""")
    for currency in currencies:
        cursor.execute("""INSERT INTO items VALUES({0}, "{1}")""".format(currency["id"], currency["name"]))

if __name__ == "__main__":
    conn = sqlite3.connect("db/currencies.db")
    cursor = conn.cursor()
    init_db(cursor)
    conn.commit()
    conn.close()

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