import broadlink
import base64

d=broadlink.discover(local_ip_address="192.168.199.97")
d.auth()
d.enter_learning()
ir = d.check_data()
while ir == None:
  ir = d.check_data()
print base64.b64encode(ir)
