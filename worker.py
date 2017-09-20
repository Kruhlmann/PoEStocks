import numpy as np
from matplotlib import pyplot as plt
import time
import api
import connection
import export
import datetime

league = "Harbinger"
currencies = [
    {"display_name": "Orb of Alteration", "price": [], "name": "alteration", "id": 1},
    {"display_name": "Orb of Fusing", "price": [], "name": "fusing", "id": 2},
    {"display_name": "Orb of Alchemy", "price": [], "name": "alchemy", "id": 3},
    {"display_name": "Chaos Orb", "price": [], "name": "chaos", "id": 4},
    {"display_name": "Gemcutter\'s Prism", "price": [], "name": "gemcutter", "id": 5},
    {"display_name": "Exalted Orb", "price": [], "name": "exalted", "id": 6},
    {"display_name": "Chromatic Orb", "price": [], "name": "chromatic", "id": 7},
    {"display_name": "Jeweller\'s Orb", "price": [], "name": "jeweller", "id": 8},
    {"display_name": "Orb of Chance", "price": [], "name": "chance", "id": 9},
    {"display_name": "Cartographer\'s Chisel", "price": [], "name": "chisel", "id": 10},
    {"display_name": "Orb of Scouring", "price": [], "name": "scouring", "id": 11},
    {"display_name": "Blessed Orb", "price": [], "name": "blessed", "id": 12},
    {"display_name": "Orb of Regret", "price": [], "name": "regret", "id": 13},
    {"display_name": "Regal Orb", "price": [], "name": "regal", "id": 14},
    {"display_name": "Divine Orb", "price": [], "name": "divine", "id": 15},
    {"display_name": "Vaal Orb", "price": [], "name": "vaal", "id": 16},
    {"display_name": "Scroll of Wisdom", "price": [], "name": "wisdom", "id": 17},
    {"display_name": "Portal Scroll", "price": [], "name": "portal", "id": 18},
    {"display_name": "Armourer\'s Scrap", "price": [], "name": "scrap", "id": 19},
    {"display_name": "Blacksmith\'s Whetstone", "price": [], "name": "whetstone", "id": 20},
    {"display_name": "Glassblower\'s Bauble", "price": [], "name": "glassblower", "id": 21},
    {"display_name": "Orb of Transmutation", "price": [], "name": "transmutation", "id": 22},
    {"display_name": "Orb of Augmentation", "price": [], "name": "augmentation", "id": 23},
    {"display_name": "Mirror of Kalandra", "price": [], "name": "mirror", "id": 24},
    {"display_name": "Eternal Orb", "price": [], "name": "eternal", "id": 25},
    {"display_name": "Perandus Coin", "price": [], "name": "perandus", "id": 26},
    {"display_name": "Silver Coin", "price": [], "name": "coin", "id": 27},
    {"display_name": "Sacrifice at Dusk", "price": [], "name": "dusk-sacrifice", "id": 28},
    {"display_name": "Sacrifice at Midnight", "price": [], "name": "midnight-sacrifice", "id": 29},
    {"display_name": "Sacrifice at Dawn", "price": [], "name": "dawn-sacrifice", "id": 30},
    {"display_name": "Sacrifice at Noon", "price": [], "name": "noon-sacrifice", "id": 31},
    {"display_name": "Mortal Grief", "price": [], "name": "mortal-grief", "id": 32},
    {"display_name": "Mortal Rage", "price": [], "name": "mortal-rage", "id": 33},
    {"display_name": "Mortal Hope", "price": [], "name": "mortal-hope", "id": 34},
    {"display_name": "Mortal Ignorance", "price": [], "name": "mortal-ignorance", "id": 35},
    {"display_name": "Eber\'s Key", "price": [], "name": "key-eber", "id": 36},
    {"display_name": "Yriel\'s Key", "price": [], "name": "key-yriel", "id": 37},
    {"display_name": "Inya\'s Key", "price": [], "name": "key-inya", "id": 38},
    {"display_name": "Volkuur\'s Key", "price": [], "name": "key-volkuur", "id": 39},
    {"display_name": "Offering to the Goddess", "price": [], "name": "offering", "id": 40},
    {"display_name": "Fragment of the Hydra", "price": [], "name": "hydra-fragment", "id": 41},
    {"display_name": "Fragment of the Phoenix", "price": [], "name": "phoenix-fragment", "id": 42},
    {"display_name": "Fragment of the Minotaur", "price": [], "name": "minotaur-fragment", "id": 43},
    {"display_name": "Fragment of the Chimera", "price": [], "name": "chimera-fragment", "id": 44},
]

def insert_currencies(cursor, currencies):
    for currency in currencies:
        cursor.execute("INSERT INTO history VALUES ({0}, {1}, '{2}')".format(currency["id"], currency["price"][0], datetime.datetime.now()))

def routine(cursor):
    for currency in currencies:
        currency["price"].append(api.get_average_exchange_rate(league=league, want=4, have=currency["id"]))
    insert_currencies(cursor, currencies)
    export.run()

def init_db(cursor):
    print("Initializing")
    cursor.execute("""CREATE TABLE IF NOT EXISTS items (id INTEGER, name TEXT, display_name TEXT)""")
    cursor.execute("""CREATE TABLE IF NOT EXISTS history (currency_id INTEGER, price DECIMAL, at DATETIME)""")
    for currency in currencies:
        cursor.execute("""INSERT INTO items VALUES({0}, "{1}", "{2}")""".format(currency["id"], currency["name"], currency["display_name"]))
    conn.commit()

if __name__ == "__main__":
    conn = connection.create_connection()
    cursor = conn.cursor()
    #init_db(cursor)

    while True:
        try:
            time_before = time.time()
            routine(cursor)
            delta_time = time.time() - time_before
            print("Routine took {0} seconds".format(delta_time))
            conn.commit()
            time.sleep(15 * 60 - delta_time) #15 minutes
        except KeyboardInterrupt:
            print("Exiting...")
            exit(0)
            conn.close()
