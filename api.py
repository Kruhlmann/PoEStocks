import json
from urllib.request import urlopen
from bs4 import BeautifulSoup
import numpy as NP
from matplotlib import pyplot as PLT

no_trades_found_text = "Oopsie! Nothing was found. If you want to buy currency why don't you"

def remove_localization(item):
    return item.replace("<<set:MS>>", "").replace("<<set:M>>", "").replace("<<set:S>>", "")

def get_public_stashes(id=""):
    request_url = "http://api.pathofexile.com/public-stash-tabs?id=" + id
    response = urlopen(request_url)
    response = response.read().decode(response.headers.get_content_charset() or 'ascii')
    return json.loads(response)

def write_public_stashes():
    id = ""
    unique_items = []
    while True:
        response = get_public_stashes(id)
        stashes = response["stashes"]
        id = response["next_change_id"]
        for stash in stashes:
            if not stash["public"]:
                continue
            for item in stash["items"]:
                delocalized_name = remove_localization(item["name"])
                if delocalized_name not in unique_items:
                    unique_items.append(delocalized_name)
        print("Item collection now contains " + str(len(unique_items)) + " items")
    with open("collection.txt", "w") as f:
        for item in unique_items:
            f.write(item + "\n")

def get_current_trades(league, want, have):
    request_url = "http://currency.poe.trade/search?league={0}&online=x&want={1}&have={2}".format(league, want, have)
    response = urlopen(request_url).read()
    if no_trades_found_text in str(response):
        return -1
    soup = BeautifulSoup(response)
    sellers = soup.findAll("div", { "class" : "displayoffer" })
    for seller in sellers:
        print(str(seller) + "\n" * 8)
    return 1

def get_average_exchange_rate(league, want, have):
    request_url = "http://currency.poe.trade/search?league={0}&online=x&want={1}&have={2}".format(league, want, have)
    try:
    	response = urlopen(request_url).read()
    except Exception:
    	return -1 
    if no_trades_found_text in str(response):
        return -1
    soup = BeautifulSoup(response)
    sellers = soup.findAll("div", { "class" : "displayoffer" })
    
    exchange_nums = 0
    chaos_accum = 0
    for seller in sellers:
        exchange = seller.find_all("small")
        for ex in exchange:
            exchange_extract = str(ex).replace(('<div class="currencyimg cur20-{0}"></div>').format(have), "").replace(('<div class="currencyimg cur20-{0}"></div>').format(want), "").replace("<small>", "").replace("</small>", "")
            if not "→" in exchange_extract:
                continue
            rates = exchange_extract.split("→")
            if len(rates) != 2:
                continue
            chaos_exchange = rates[1].replace("⨯", "").replace(" ", "")
            chaos_accum = chaos_accum + float(chaos_exchange)
            exchange_nums = exchange_nums + 1
    return chaos_accum / exchange_nums if exchange_nums > 0 else -1


# just create some random data
fnx = lambda : NP.random.randint(3, 10, 10)
y = NP.row_stack((fnx(), fnx(), fnx()))   
# this call to 'cumsum' (cumulative sum), passing in your y data, 
# is necessary to avoid having to manually order the datasets
x = NP.arange(10) 
y_stack = NP.cumsum(y, axis=0)   # a 3x10 array

fig = PLT.figure()
ax1 = fig.add_subplot(111)

ax1.fill_between(x, 0, y_stack[0,:], facecolor="#CC6666", alpha=.7)
ax1.fill_between(x, y_stack[0,:], y_stack[1,:], facecolor="#1DACD6", alpha=.7)
ax1.fill_between(x, y_stack[1,:], y_stack[2,:], facecolor="#6E5160")

PLT.savefig('ex.png', trasparent=True)