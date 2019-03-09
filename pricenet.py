from tensorforce.agents import PPOAgent

import gym
from gym import spaces

# various possible changes in price
PRICE_CHANGES = [
	-10,
	-5,
	0,
	5,
	10
]

class Product:
	def __init__(self, prod_id, init_light, init_price, init_quantity, avg_cost_estimate):
		# initalize product
		self.id = prod_id

		# initialize state
		self.light = init_light
		self.quantity = init_quantity
		self.cost = avg_cost_estimate # the approximated cost of each item sold

		self.price = init_price # what the price is being set at
		self.recommended_price = init_price # what the mode recommends

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

	def get_quantity(self): return self.quantity

	def get_light(self): return self.light

	def get_price(self): return self.price

	def get_recommended_price(self): return self.recommended_price

	def update_light(self, new_light): self.light = new_light

	def update_price(self):
		# updates price to recommended price
		self.recommended_price += PRICE_CHANGES[self.agent.act(states=(self.light, self.price, self.quantity, self.cost))]

	def set_price(self, new_price): self.price = new_price

	def record_delivery(self, delivery_quantity, delivery_cost_per_item):
		# increase quantity as per size of delivery
		self.quantity += delivery_quantity

		# update cost
		# TODO improve algorithm
		self.cost = delivery_cost_per_item

	def record_sale(self, sale_quantity, sale_price_per_item):
		# decrease quantity as per size of sale
		self.quantity -= sale_quantity

		# calculate approximate profit per item of sale
		avg_profit_estimate = sale_price_per_item - self.cost
		self.agent.observe(reward=avg_profit_estimate, terminal=False)

banana = Product(0, 100, 2, 50, 1.75)
banana.record_sale(5, )
print(banana.get_price())

# TODO
# add functions to log records
# add HTTP API to call correct functions
# save Product objects to file