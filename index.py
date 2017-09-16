import api
import cherrypy
import os

class DashBoard(object):
    @cherrypy.expose
    def index(self):
        return  """
                    <img src="img/ex.png"></img>
                """
    @cherrypy.expose
    def api(self, league="Standard", want=1, have=1):
        return str(api.get_average_exchange_rate(league, want, have))
        

if __name__ == "__main__":
    file_path = os.getcwd().replace("\\", "/")
    config = {
        "/img": {
            "tools.staticdir.on": True,
            "tools.staticdir.dir": os.path.join(file_path, "img"),
        }
    }
    cherrypy.quickstart(DashBoard(), "/", config=config)
