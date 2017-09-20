import numpy as np
from matplotlib import pyplot as plt
import time
import connection
import datetime

def reverse_array(array):
    if len(array) < 2:
        return array
    res = []
    for i in range(len(array), 0, -1):
        res.append(array[i - 1])
    return res

def get_x_array(dates):
    res = []
    i = 0
    for date in dates:
        res.append(i)
        i = i + 1
    return res

def get_all_currencies(conn, limit=0):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM items")
    res = []
    items = cursor.fetchall()
    for cur in items:
        if limit > 0:
            cursor.execute("SELECT * FROM history WHERE currency_id=" + str(cur[0]) + " ORDER BY at DESC LIMIT " + str(limit))
        else:
            cursor.execute("SELECT * FROM history WHERE currency_id=" + str(cur[0]) + " ORDER BY at DESC")
        prices = cursor.fetchall()
        res.append({"id": cur[0], "name": cur[1], "display_name": cur[2], "prices": prices})
    return res

def export_minute_graphs(conn):
    print("Exporting minute graphs...")
    currencies = get_all_currencies(conn, limit=20)
    for i in range(len(currencies), 0, -1):
        currency = currencies[i - 1]
        values = []
        dates = []
        # Reversed since we're using DESC in the SQL query
        for price in reverse_array(currency["prices"]):
            # We only want data points from today
            if datetime.datetime.today().date() != datetime.datetime.strptime(price[2], "%Y-%m-%d %H:%M:%S.%f").date():
                continue
            values.append(price[1])
            dates.append(datetime.datetime.strptime(price[2], "%Y-%m-%d %H:%M:%S.%f").strftime("%H:%M"))
        plt.xticks(get_x_array(dates), dates, rotation=45)
        plt.plot(get_x_array(dates), values)
        plt.savefig("static/img/graphs/minute/{0}.png".format(currency["name"]), transparent=True)
        plt.clf()

def export_hour_graphs(conn):
    print("Exporting hour graphs...")
    currencies = get_all_currencies(conn, limit=80)

    for currency in currencies:
        values = []
        dates = []
        i = 0
        # Reversed since we're using DESC in the SQL query
        for price in reverse_array(currency["prices"]):
            # We only want data points from today
            if datetime.datetime.today().date() != datetime.datetime.strptime(price[2], "%Y-%m-%d %H:%M:%S.%f").date():
                continue
            if i % 4 == 0:
                values.append(price[1])
                dates.append(datetime.datetime.strptime(price[2], "%Y-%m-%d %H:%M:%S.%f").strftime("%H:%M"))
            i = i + 1
        plt.xticks(get_x_array(dates), dates, rotation=45)
        plt.plot(get_x_array(dates), values)
        plt.savefig("static/img/graphs/hour/{0}.png".format(currency["name"]), transparent=True)
        plt.clf()


def export_day_graphs(conn):
    print("Exporting day graphs...")
    currencies = get_all_currencies(conn)
    for currency in currencies:
        dates_added = []
        values = []
        dates = []
        # Reversed since we're using DESC in the SQL query
        for price in reverse_array(currency["prices"]):
            # We only want data points from today
            if datetime.datetime.strptime(price[2], "%Y-%m-%d %H:%M:%S.%f").date() not in dates_added:
                dates_added.append(datetime.datetime.strptime(price[2], "%Y-%m-%d %H:%M:%S.%f").date())
                values.append(price[1])
                dates.append(datetime.datetime.strptime(price[2], "%Y-%m-%d %H:%M:%S.%f").strftime("%d %b"))
        plt.xticks(get_x_array(dates), dates, rotation=45)
        plt.plot(get_x_array(dates), values)
        plt.savefig("static/img/graphs/day/{0}.png".format(currency["name"]), transparent=True)
        plt.clf()

def run():
    conn = connection.create_connection()
    export_minute_graphs(conn)
    export_hour_graphs(conn)
    export_day_graphs(conn)
    conn.close()

if __name__ == "__main__":
    run()