import time
import BaseHTTPServer
import broadlink
import base64
import yaml

HOST_NAME = '0.0.0.0' # !!!REMEMBER TO CHANGE THIS!!!
PORT_NUMBER = 8124 # Maybe set this to 9000.
BROADLINK = ""
global y

def br_init():
  global BROADLINK
  BROADLINK=broadlink.discover(local_ip_address="192.168.199.97")
  BROADLINK.auth()
  return
  
def br_send(data):
  global BROADLINK
#  print base64.b64decode(data)
  BROADLINK.send_data(base64.b64decode(data))
  return

def br_learn():
  global BROADLINK
  BROADLINK.enter_learning()
  ir = BROADLINK.check_data()
  while ir == None:
    ir = BROADLINK.check_data()
  return base64.b64encode(ir)

class MyHandler(BaseHTTPServer.BaseHTTPRequestHandler):
  def do_HEAD(s):
    s.send_response(200)
    s.send_header("Content-type", "text/html")
    s.end_headers()
  def do_GET(s):
    global y
    """Respond to a GET request."""
    path = ""
    path = s.path
    if s.path == "/learn":
      s.send_response(200)
      s.send_header("Content-type", "text/html")
      s.end_headers()
      s.wfile.write(br_learn())
      return
    if path.split("/")[1] == "send":
      br_send(y["commands"][path.split("/")[2]])
      s.send_response(302)
      s.send_header('Location', "/")
      s.end_headers()
      return
    s.send_response(200)
    s.send_header("Content-type", "text/html")
    s.end_headers()
    s.wfile.write("<html><body><h1>Available commands</h1><br>")
    for i in y["commands"]:
      s.wfile.write("<a href='/send/"+i+"'>"+i+"</a></br>")
    s.wfile.write("</body></html>")
    return

if __name__ == '__main__':
  with open("config.yaml", 'r') as stream:
    try:
      y = yaml.load(stream)
    except yaml.YAMLError as exc:
      print(exc)
      exit

  y["server"]["port"]
  print "Init Broadlink"
  br_init()
  server_class = BaseHTTPServer.HTTPServer
  httpd = server_class((y["server"]["host"], y["server"]["port"]), MyHandler)
  print time.asctime(), "Server Starts - %s:%s" % (y["server"]["host"], y["server"]["port"])
  try:
    httpd.serve_forever()
  except KeyboardInterrupt:
    pass
    httpd.server_close()
  print time.asctime(), "Server Stops - %s:%s" % (y["server"]["host"], y["server"]["port"])
