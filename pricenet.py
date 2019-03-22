# libaries for reinforcement learning
from tensorforce.agents import PPOAgent

# libaries for HTTP servers
import BaseHTTPServer
import SocketServer
from socket import *

# server configuration
PORT = 8080

# various possible changes in price
PRICE_CHANGES = [
	price for price in range(-10, 10)
]

# details for a product being sold
class Product:
	def __init__(self, name, light, price, quantity, avg_cost_estimate):
		# initalize product
		self.name = name

		# initialize state
		self.light = light
		self.quantity = quantity
		self.cost = avg_cost_estimate # the approximated cost of each item sold

		self.price = price # what the price is being set at
		self.recommended_price = price # what the mode recommends

		self.history_log = [] # history of product over time

		# initalize agent
		self.agent = PPOAgent(
		    states=dict(type='float', shape=(4)),
		    actions=dict(type='int', num_actions=len(PRICE_CHANGES)),
		    network=[
		        dict(type='dense', size=64),
		        dict(type='dense', size=64)
		    ],
		    step_optimizer=dict(type='adam', learning_rate=1e-4)
		)
		self.agent.initialize_model()

	def get_history_log(self): return self.history_log

	def get_quantity(self): return self.quantity

	def get_avg_cost_estimate(self): return self.avg_cost_estimate

	def get_light(self): return self.light

	def get_price(self): return self.price

	def get_recommended_price(self): return self.recommended_price + PRICE_CHANGES[self.agent.act(states=(self.light, self.price, self.quantity, self.cost), independent=true)]

	def set_light(self, new_light):
		self.history_log.append("light=" + str(new_light))
		self.light = new_light

	def set_price(self, new_price):
		self.history_log.append("price=" + str(new_price))
		self.price = new_price

	def update_price(self):
		self.history_log.append("price=" + str(new_price))
		recommended_price_update = PRICE_CHANGES[self.agent.act(states=(self.light, self.price, self.quantity, self.cost), independent=true)]
		self.recommended_price += recommended_price_update

	def record_delivery(self, delivery_quantity, delivery_cost_per_item):
		self.history_log.append("delivery," + str(delivery_quantity) + str(delivery_cost_per_item))

		# increase quantity as per size of delivery
		self.quantity += delivery_quantity

		# update cost
		# TODO improve algorithm
		self.cost = delivery_cost_per_item

	def record_sale(self, sale_quantity):
		self.history_log.append("sale," + str(sale_quantity))

		# decrease quantity as per size of sale
		self.quantity -= sale_quantity

		# calculate approximate profit per item of sale
		avg_profit_estimate = self.price - self.cost
		self.agent.act(states=(self.light, self.price, self.quantity, self.cost))
		self.agent.observe(reward=avg_profit_estimate, terminal=False)

# products being sold
# index of each product corresponds to ID of product
products = {
	"banana" : Product(
		name              = "banana",
		light             = 100,
		price             = 2,
		quantity          = 50, 
		avg_cost_estimate = 1.75
	),
	"apple" : Product(
		name              = "apple",
		light             = 100,
		price             = 2,
		quantity          = 50,
		avg_cost_estimate = 1.75
	)
}

class PriceNetHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    def do_HEAD(s):
    	s.send_response(200)
        s.send_header("Content-type", "text/plain")
        s.end_headers()

    def do_GET(s):
        s.send_response(200)
        s.send_header("Content-type", "text/plain")
        s.end_headers()

        path_parts = filter(None, s.path.split("/"))

        prod_name = path_parts[0]

        if path_parts[1] == "get-light":
        	s.wfile.write(products[prod_name].get_light())
        elif path_parts[1] == "get-quantity":
        	s.wfile.write(products[prod_name].get_quantity())
        elif path_parts[1] == "get-avg-cost":
        	s.wfile.write(products[prod_name].get_avg_cost_estimate())
        elif path_parts[1] == "get-price":
        	s.wfile.write(products[prod_name].get_price())
        elif path_parts[1] == "get-recommended-price":
        	s.wfile.write(products[prod_name].get_recommended_price())

        if path_parts[1] == "set-light":
        	products[prod_name].set_light(float(path_parts[2]))
        elif path_parts[1] == "set_price":
        	products[prod_name].set_price(float(path_parts[2]))
        elif path_parts[1] == "update_price":
        	products[prod_name].update_price()

        if path_parts[1] == "record-sale":
        	products[prod_name].record_sale(int(float(path_parts[2])))
        elif path_parts[1] == "record-delivery":
        	products[prod_name].record_delivery(int(float(path_parts[2])), float(path_parts[3]))

        if path_parts[1] == "history":
        	for log in products[prod_name].get_history_log():
        		s.wfile.write(log + "\n")

if __name__ == '__main__':
	SocketServer.TCPServer.allow_reuse_address=True
	httpd = SocketServer.TCPServer(('', PORT), PriceNetHandler)
	try:
		httpd.serve_forever()
	except KeyboardInterrupt:
		pass
	httpd.server_close()
	httpd.shutdown()

# TODO
# add functions to log records
# add HTTP API to call correct functions
# save Product objects to file