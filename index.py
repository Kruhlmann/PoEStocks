import api
import cherrypy
import os
import sqlite3
import connection

def get_dashboard_entries():
    entries = ""
    cur = connection.select_all_currencies()
    for c in cur:
        with open("templates/dash_entry.html") as f:
            if c[1] != "chaos":
                entries = entries + f.read().format(filename=c[1], display_name=c[2]) 
    return entries

def get_dashboard():
    with open("templates/dashboard.html") as f:
        return f.read().format(content=get_dashboard_entries())

def get_template(template):
    with open("templates/{0}.html".format(template)) as f:
        return f.read()

def currencies_to_js():
    res = "var currencies = ["
    cur = connection.select_all_currencies()
    for c in cur:
        res = res + "{\"id\": " + str(c[0]) + ", \"name\": \"" + str(c[1]) + "\", \"display_name\": \"" + str(c[2]) + "\"},"
    res = res + "];"
    return res

def get_main_js():
    with open("js/main.js") as f:
        return currencies_to_js() + "\n" + f.read()

class DashBoard(object):
    @cherrypy.expose
    def dashboard(self, page=""):
        if page == "":
            page = "dashboard"
        return get_template("main").format(content=get_dashboard(), js=get_main_js())
    @cherrypy.expose
    def api(self, league="Standard", want=1, have=1):
        return str(api.get_average_exchange_rate(league, want, have))
    @cherrypy.expose
    def index(self):
        return self.dashboard()
        

if __name__ == "__main__":
    file_path = os.getcwd().replace("\\", "/")
    config = {
        "/img": {
            "tools.staticdir.on": True,
            "tools.staticdir.dir": os.path.join(file_path, "img"),
        },
        "/css": {
            "tools.staticdir.on": True,
            "tools.staticdir.dir": os.path.join(file_path, "css")
        },
        "/js": {
            "tools.staticdir.on": True,
            "tools.staticdir.dir": os.path.join(file_path, "js")
        }
    }
    cherrypy.quickstart(DashBoard(), "/", config=config)
