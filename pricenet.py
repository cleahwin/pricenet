# TESTS
# show output price change for various ripeness levels (demo) before and after 5 days of simulated learning for multiple fuits ()

# libaries for reinforcement learning
from tensorforce.agents import PPOAgent
from random import randint

# libaries for HTTP servers
import BaseHTTPServer
import SocketServer
from socket import *

# server configuration
PORT = 8080

# various possible changes in price
PRICE_CHANGES = [
	-0.5, -0.45, -0.4, -0.35, -0.3, -0.25, -0.2, -0.15, -0.1, -0.05, 0,
	0.5, 0.45, 0.4, 0.35, 0.3, 0.25, 0.2, 0.15, 0.1, 0.05, 0,
]

# details for a product being sold
class Product:
	def __init__(self, name, light, price, quantity, avg_cost_estimate):
		# initalize product
		self.name = name

		# initialize state
		self.light = light
		self.quantity = quantity
		self.avg_cost_estimate = avg_cost_estimate # the approximated cost of each item sold

		self.price = price # what the price is being set at

		self.history_log = [] # history of product over time

		# initalize agent
		self.agent = PPOAgent(
			states=dict(type='float', shape=(4)),
			actions=dict(type='int', num_actions=len(PRICE_CHANGES)),
			network=[
				dict(type='dense', size=4),
				dict(type='dense', size=4)
			],
			step_optimizer=dict(type='adam', learning_rate=0.01)
		)
		self.agent.initialize_model()

	def get_history_log(self): return self.history_log

	def get_quantity(self): return self.quantity

	def get_avg_cost_estimate(self): return self.avg_cost_estimate

	def get_light(self): return self.light

	def get_price(self): return self.price

	def get_recommended_price(self): return max(0, self.price + PRICE_CHANGES[self.agent.act(states=(self.light, self.price, self.quantity, self.avg_cost_estimate), deterministic=True, independent=True)])

	def set_light(self, new_light):
		self.history_log.append("light=" + str(new_light))
		self.light = new_light

	def set_price(self, new_price):
		self.history_log.append("price=" + str(new_price))
		self.price = new_price

	def update_price(self):
		self.history_log.append("price=" + str(new_price))
		self.price = max(0, self.price + PRICE_CHANGES[self.agent.act(states=(self.light, self.price, self.quantity, self.avg_cost_estimate), deterministic=True, independent=True)])

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
		avg_profit_estimate = sale_quantity * (self.price - self.avg_cost_estimate)
		self.agent.act(states=(self.light, self.price, self.quantity, self.avg_cost_estimate), deterministic=False, independent=False)
		self.agent.observe(reward=avg_profit_estimate, terminal=False)

# products being sold
# index of each product corresponds to ID of product
products = {
	"banana" : Product(
		name              = "banana",
		light             = 10,
		price             = 0.2,
		quantity          = 0,
		avg_cost_estimate = 0.1
	),
	"pear" : Product(
		name              = "pear",
		light             = 10,
		price             = 0.5,
		quantity          = 0,
		avg_cost_estimate = 0.2
	),
	"orange" : Product(
		name              = "orange",
		light             = 10,
		price             = 0.6,
		quantity          = 0,
		avg_cost_estimate = 0.2
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
			s.wfile.write(str(products[prod_name].get_light()))
		elif path_parts[1] == "get-quantity":
			s.wfile.write(str(products[prod_name].get_quantity()))
		elif path_parts[1] == "get-avg-cost-estimate":
			s.wfile.write(str(products[prod_name].get_avg_cost_estimate()))
		elif path_parts[1] == "get-price":
			s.wfile.write(str(products[prod_name].get_price()))
		elif path_parts[1] == "get-recommended-price":
			s.wfile.write(str(products[prod_name].get_recommended_price()))

		if path_parts[1] == "set-light":
			products[prod_name].set_light(float(path_parts[2]))
		elif path_parts[1] == "set-rice":
			products[prod_name].set_price(float(path_parts[2]))
		elif path_parts[1] == "update-price":
			products[prod_name].update_price()

		if path_parts[1] == "record-sale":
			products[prod_name].record_sale(int(float(path_parts[2]))) # records batch sale at given point in time 
		elif path_parts[1] == "record-delivery":
			products[prod_name].record_delivery(int(float(path_parts[2])), float(path_parts[3]))

		if path_parts[1] == "simulate-learning":
			product_to_simulate = products[prod_name]

			if product_to_simulate.name == "banana":
				# demo before
				# - show banana that isn't yet ripe
				# - show that algorithm can't make very good predictions yet

				# day 1
				# - record light of 10
				# - delivery of 100 bananas
				# - decent sales
				product_to_simulate.record_delivery(100, 0.05)
				product_to_simulate.set_light(10)
				product_to_simulate.record_sale(50)
				# print("average profit per item" + str(abs(product_to_simulate.get_recommended_price() - product_to_simulate.get_avg_cost_estimate())))
				print("light: " + str(product_to_simulate.get_light()))
				print("recommended price: " + str(product_to_simulate.get_recommended_price()))

				# day 2
				# - light reduces to 8
				# - sales become worse
				product_to_simulate.set_light(5)
				product_to_simulate.record_sale(10)
				# print("average profit per item" + str(abs(product_to_simulate.get_recommended_price() - product_to_simulate.get_avg_cost_estimate())))
				print("light: " + str(product_to_simulate.get_light()))
				print("recommended price: " + str(product_to_simulate.get_recommended_price()))

				# day 3
				# - price is decreased
				# - sales improve
				# - supply is depleted
				product_to_simulate.set_price(0.1)
				product_to_simulate.record_sale(40)
				# print("average profit per item" + str(abs(product_to_simulate.get_recommended_price() - product_to_simulate.get_avg_cost_estimate())))
				print("light: " + str(product_to_simulate.get_light()))
				print("recommended price: " + str(product_to_simulate.get_recommended_price()))

				# day 4
				# - delivery of 100 bananas
				# - light returns to 10
				# - decrease price
				product_to_simulate.record_delivery(100, 0.05)
				product_to_simulate.set_light(10)
				product_to_simulate.set_price(0.1)
				product_to_simulate.record_sale(50)
				# print("average profit per item" + str(abs(product_to_simulate.get_recommended_price() - product_to_simulate.get_avg_cost_estimate())))
				print("light: " + str(product_to_simulate.get_light()))
				print("recommended price: " + str(product_to_simulate.get_recommended_price()))

				# day 5
				product_to_simulate.set_light(5)
				product_to_simulate.record_sale(20)
				# print("average profit per item" + str(abs(product_to_simulate.get_recommended_price() - product_to_simulate.get_avg_cost_estimate())))
				print("light: " + str(product_to_simulate.get_light()))
				print("recommended price: " + str(product_to_simulate.get_recommended_price()))

				product_to_simulate.record_delivery(80, 0.05)
				product_to_simulate.set_price(0.2)
				product_to_simulate.set_light(10)

				# final
				# - quantity: 100
				# - price: 0.2
				# - light: 10

				# expected
				# - lower price is recommended when light is less (fruit is more ripe and demand is less)

			elif product_to_simulate.name == "pear":
				# demo before
				# - show pear that isn't yet ripe
				# - show that algorithm can't make very good predictions yet

				# day 1
				# - record light of 10
				# - delivery of 100 pears
				# - decent sales
				product_to_simulate.record_delivery(100, 0.05)
				product_to_simulate.set_light(8)
				product_to_simulate.record_sale(60)
				# print("average profit per item" + str(abs(product_to_simulate.get_recommended_price() - product_to_simulate.get_avg_cost_estimate())))
				print("light: " + str(product_to_simulate.get_light()))
				print("recommended price: " + str(product_to_simulate.get_recommended_price()))

				# day 2
				# - light reduces to 8
				# - sales become worse
				product_to_simulate.set_light(6)
				product_to_simulate.record_sale(10)
				# print("average profit per item" + str(abs(product_to_simulate.get_recommended_price() - product_to_simulate.get_avg_cost_estimate())))
				print("light: " + str(product_to_simulate.get_light()))
				print("recommended price: " + str(product_to_simulate.get_recommended_price()))

				# day 3
				# - price is decreased
				# - sales improve
				# - supply is depleted
				product_to_simulate.set_price(0.3)
				product_to_simulate.record_sale(30)
				# print("average profit per item" + str(abs(product_to_simulate.get_recommended_price() - product_to_simulate.get_avg_cost_estimate())))
				print("light: " + str(product_to_simulate.get_light()))
				print("recommended price: " + str(product_to_simulate.get_recommended_price()))

				# day 4
				# - delivery of 100 pears
				# - light returns to 10
				# - decrease price
				product_to_simulate.record_delivery(100, 0.05)
				product_to_simulate.set_light(8)
				product_to_simulate.set_price(0.3)
				product_to_simulate.record_sale(30)
				# print("average profit per item" + str(abs(product_to_simulate.get_recommended_price() - product_to_simulate.get_avg_cost_estimate())))
				print("light: " + str(product_to_simulate.get_light()))
				print("recommended price: " + str(product_to_simulate.get_recommended_price()))

				# day 5
				product_to_simulate.set_light(6)
				product_to_simulate.record_sale(10)
				# print("average profit per item" + str(abs(product_to_simulate.get_recommended_price() - product_to_simulate.get_avg_cost_estimate())))
				print("light: " + str(product_to_simulate.get_light()))
				print("recommended price: " + str(product_to_simulate.get_recommended_price()))

				product_to_simulate.record_delivery(40, 0.05)
				product_to_simulate.set_price(0.5)
				product_to_simulate.set_light(8)

				# final
				# - quantity: 100
				# - price: 0.5
				# - light: 8

				# expected
				# - lower price is recommended when light is less (fruit is more ripe and demand is less)
			elif product_to_simulate.name == "orange":
				# demo before
				# - show orange that isn't yet ripe
				# - show that algorithm can't make very good predictions yet

				# day 1
				# - record light of 10
				# - delivery of 100 oranges
				# - decent sales
				product_to_simulate.record_delivery(100, 0.05)
				product_to_simulate.set_light(9)
				product_to_simulate.record_sale(60)
				# print("average profit per item" + str(abs(product_to_simulate.get_recommended_price() - product_to_simulate.get_avg_cost_estimate())))
				print("light: " + str(product_to_simulate.get_light()))
				print("recommended price: " + str(product_to_simulate.get_recommended_price()))

				# day 2
				# - light reduces to 8
				# - sales become worse
				product_to_simulate.set_light(7)
				product_to_simulate.record_sale(10)
				# print("average profit per item" + str(abs(product_to_simulate.get_recommended_price() - product_to_simulate.get_avg_cost_estimate())))
				print("light: " + str(product_to_simulate.get_light()))
				print("recommended price: " + str(product_to_simulate.get_recommended_price()))

				# day 3
				# - price is decreased
				# - sales improve
				# - supply is depleted
				product_to_simulate.set_price(0.4)
				product_to_simulate.record_sale(30)
				# print("average profit per item" + str(abs(product_to_simulate.get_recommended_price() - product_to_simulate.get_avg_cost_estimate())))
				print("light: " + str(product_to_simulate.get_light()))
				print("recommended price: " + str(product_to_simulate.get_recommended_price()))

				# day 4
				# - delivery of 100 oranges
				# - light returns to 10
				# - decrease price
				product_to_simulate.record_delivery(100, 0.05)
				product_to_simulate.set_light(9)
				product_to_simulate.set_price(0.1)
				product_to_simulate.record_sale(30)
				# print("average profit per item" + str(abs(product_to_simulate.get_recommended_price() - product_to_simulate.get_avg_cost_estimate())))
				print("light: " + str(product_to_simulate.get_light()))
				print("recommended price: " + str(product_to_simulate.get_recommended_price()))

				# day 5
				product_to_simulate.set_light(8)
				product_to_simulate.record_sale(10)
				# print("average profit per item" + str(abs(product_to_simulate.get_recommended_price() - product_to_simulate.get_avg_cost_estimate())))
				print("light: " + str(product_to_simulate.get_light()))
				print("recommended price: " + str(product_to_simulate.get_recommended_price()))

				product_to_simulate.record_delivery(40, 0.05)
				product_to_simulate.set_price(0.4)
				product_to_simulate.set_light(9)

				# final
				# - quantity: 100
				# - price: 0.2
				# - light: 10

				# expected
				# - lower price is recommended when light is less (fruit is more ripe and demand is less)
			else:
				# no simulation available for given product
				return

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