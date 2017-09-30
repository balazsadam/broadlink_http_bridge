import broadlink
import base64
import sys

d=broadlink.discover(local_ip_address="192.168.199.97")
d.auth()
ir = d.send_data(base64.b64decode(sys.argv[1]))
