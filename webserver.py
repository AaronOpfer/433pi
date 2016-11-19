from tornado.web import Application, RequestHandler, StaticFileHandler
from tornado.ioloop import IOLoop
from send_rf import Lights, GPIOSetup

from tornado.options import define, options, parse_command_line

define("port", default=8888, help="run on the given port", type=int)

lights = None

class LightHandler(RequestHandler):
    def get(self, cmd):
        lights.do_cmd(cmd)

if __name__ == "__main__":
    parse_command_line()
    lights = Lights()
    with GPIOSetup():
        app = Application(
            [
                (r'/()', StaticFileHandler, {"path": "static", "default_filename": "index.html"}),
                (r'/lights/(._o[fn]+)', LightHandler),
            ],
            static_path='static'
        )
        app.listen(8080)
        IOLoop.current().start()
