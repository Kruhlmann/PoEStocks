import api
import cherrypy
import os
import sqlite3
import connection

sub_header = open("static/templates/sub_header.html").read()

def get_dashboard_entries():
    entries = ""
    cur = connection.select_all_currencies()
    for c in cur:
        with open("static/templates/dash_entry.html") as f:
            if c[1] != "chaos":
                entries = entries + f.read().format(filename=c[1], display_name=c[2]) 
    return entries

def get_template(template):
    with open("static/templates/{0}.html".format(template)) as f:
        return f.read()

def currencies_to_js():
    res = "var currencies = ["
    cur = connection.select_all_currencies()
    for c in cur:
        res = res + "{\"id\": " + str(c[0]) + ", \"name\": \"" + str(c[1]) + "\", \"display_name\": \"" + str(c[2]) + "\"},"
    res = res + "];"
    return res

def get_main_js():
    with open("static/js/main.js") as f:
        return currencies_to_js() + "\n" + f.read()

class DashBoard(object):
    @cherrypy.expose
    def index(self):
        return get_template("main").format(sub_header=sub_header, content=open("static/templates/dashboard.html").read().format(content=get_dashboard_entries()), js=get_main_js())

class Rates(object):
    @cherrypy.expose
    def index(self):
        return get_template("main").format(sub_header="", content=open("static/templates/rates.html").read(), js=get_main_js())
        
class About(object):
    @cherrypy.expose
    def index(self):
        return get_template("main").format(sub_header="", content="About page", js=get_main_js())
    

if __name__ == "__main__":
    config_file = os.path.join(os.path.dirname(__file__), "server.conf")
    cherrypy.tree.mount(DashBoard(), '/', config=config_file)
    cherrypy.tree.mount(Rates(), '/rates', config=config_file)
    cherrypy.tree.mount(About(), '/about', config=config_file)
    cherrypy.engine.start()
    cherrypy.engine.block()