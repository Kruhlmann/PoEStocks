import api
import cherrypy
import os

def get_template(template):
    with open("templates/{0}.html".format(template)) as f:
        return f.read()

class DashBoard(object):
    @cherrypy.expose
    def dashboard(self, page=""):
        if page == "":
            page = "dashboard"
        return get_template("main").format(get_template(page))
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
        }
    }
    cherrypy.quickstart(DashBoard(), "/", config=config)
