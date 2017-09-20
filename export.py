import numpy as np
from matplotlib import pyplot as plt
import time
import connection
import datetime

def get_x_array(dates):
    res = []
    i = 0
    for date in dates:
        res.append(i)
        i = i + 1
    return res

def get_all_currencies(limit=0):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM items")
    res = []
    items = cursor.fetchall()
    for cur in items:
        if limit > 0:
            cursor.execute("SELECT * FROM history WHERE currency_id=" + str(cur[0]) + " LIMIT " + str(limit))
        else:
            cursor.execute("SELECT * FROM history WHERE currency_id=" + str(cur[0]))
        prices = cursor.fetchall()
        res.append({"id": cur[0], "name": cur[1], "display_name": cur[2], "prices": prices})
    return res

def export_minute_graphs():
    print("Exporting minute graphs...")
    currencies = get_all_currencies(limit=20)
    for currency in currencies:
        values = []
        dates = []
        for price in currency["prices"]:
            values.append(price[1])
            dates.append(datetime.datetime.strptime(price[2], "%Y-%m-%d %H:%M:%S.%f").strftime("%H:%M"))
        plt.xticks(get_x_array(dates), dates, rotation=45)
        plt.plot(get_x_array(dates), values)
        plt.savefig("static/img/graphs/minute/{0}.png".format(currency["name"]), transparent=True)
        plt.clf()

def export_hour_graphs():
    print("Exporting hour graphs...")
    unfiltered_currencies = get_all_currencies(limit=1)
    currencies = []
    for i in range(0, len(unfiltered_currencies)):
        if i % 4 == 0:
            currencies.append(unfiltered_currencies[i])
    print(len(currencies))
    print(len(unfiltered_currencies))

    for currency in currencies:
        values = []
        dates = []
        for price in currency["prices"]:
            values.append(price[1])
            dates.append(datetime.datetime.strptime(price[2], "%Y-%m-%d %H:%M:%S.%f").strftime("%H:%M"))
        plt.xticks(get_x_array(dates), dates, rotation=45)
        plt.plot(get_x_array(dates), values)
        plt.savefig("static/img/graphs/hour/{0}.png".format(currency["name"]), transparent=True)
        plt.clf()

if __name__ == "__main__":
    conn = connection.create_connection()
    export_minute_graphs()
    export_hour_graphs()
    conn.close()