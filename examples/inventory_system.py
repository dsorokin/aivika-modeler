#!/usr/local/bin/python3

# Example: Inventory System with Lost Sales and Backorders
#
# It is described in different sources [1, 2]. So, this is chapter 11 of [2]
# and section 6.7 of [1].
#
# [1] A. Alan B. Pritsker, Simulation with Visual SLAM and AweSim, 2nd ed.
#
# [2] Труб И.И., Объектно-ориентированное моделирование на C++: Учебный курс. - СПб.: Питер, 2006
#
# A large discount house is planning to install a system to control
# the inventory of a particular radio. The time between demands for a radio is
# exponentially distributed with a mean time of 0.2 weeks. In the case where
# customers demand the radio when it is not in stock, 80 percent will go to
# another nearby discount house to find it, thereby representing lost sales,
# while the other 20 percent will backorder the radio and wait for the next
# shipment arrival. The store employs a periodic review-reorder point inventory
# system where the inventory status is reviewed every four weeks to decide if
# an order should be placed. The company policy is to order up to the stock
# control level of 72 radios whenever the inventory position, consisting of
# the radios in stock plus the radios on order minus the radios on backorder,
# is found to be less than or equal to the reorder point of 18 radios.
# The procurement lead time (the time from the placement of an order to
# its receipt) is constant and requires three weeks. The objective of
# this example is to simulate the inventory system for a period of six years
# (312 weeks) to obtain statistics on the following quantities:
#
#   1) number of radios in stock;
#   2) inventory position;
#   3) safety stock (radios in stock at order receipt times); and
#   4) time between lost sales.
#
# The initial conditions for the simulation are an inventory position of 72 and
# no initial backorders. In order to reduce the bias in the statistics due to
# the initial starting conditions, all the statistics are to be cleared at
# the end of the first year of the six year simulation period.

from simulation.aivika.modeler import *

# the initial count of radio
INIT_RADIO = 72

# reorder position threshold
REORDER_PT = 18

# stock control level
SCL = 72

# lead time
LEAD_TIME = 3

# review period
REVIEW_PERIOD = 4

model = MainModel()

# the transacts can have assignable and updatable fields, but it is not used here
data_type = TransactType(model, 'Transact')

# the available resource of radio, where the upper bound is not specified
radio = create_resource_with_max_count(model, INIT_RADIO, None,
    name = 'radio', descr = 'the radio resource')
radio_source = radio.add_result_source()

# the inventory position
inv_pos = create_ref(model, INIT_RADIO, INT_TYPE,
    name = 'inv_pos', descr = 'the inventory position')
inv_pos_source = inv_pos.add_result_source()

safety_stock = create_ref(model, EMPTY_SAMPLING_STATS, INT_SAMPLING_STATS,
    name = 'safety_stock', descr = 'the safety stock')
safety_stock_source = safety_stock.add_result_source()

# the last arriving time for the lost sale; otherwise, -1
lost_sale_arrive = create_ref(model, -1, DOUBLE_TYPE, name = 'lost_sale_arrive')

# time between lost sales
tb_lost_sales = create_ref(model, EMPTY_SAMPLING_STATS, DOUBLE_SAMPLING_STATS,
    name = 'tb_lost_sales', descr = 'time between lost sales')
tb_lost_sales_source = tb_lost_sales.add_result_source()

# a stream of customers
customers = exponential_random_stream(data_type, 0.2)

# an expression that checks whether the customer stays with us
customer_test1 = resource_count(radio) > 0
customer_test2 = uniform_random_expr(model, 0, 1) <= 0.2
customer_test  = customer_test1 | customer_test2

# divide the incoming customers to those that stay with us and those that go to another discount house
(customers, lost_customers) = test_stream(customer_test, customers)

# serve our customers
customers = within_stream(dec_ref(inv_pos), customers)
customers = request_resource_in_parallel(radio, customers)
terminate_stream(customers)

# server the customers that go to another discount house
update_tb_lost_sales = if_expr(read_ref(lost_sale_arrive) < 0,
    # then
    write_ref(lost_sale_arrive, time_expr(model)),
    # else
    expr_sequence([write_ref(tb_lost_sales,
                    add_sampling_stats(time_expr(model) - read_ref(lost_sale_arrive),
                        read_ref(tb_lost_sales))),
                   write_ref(lost_sale_arrive, time_expr(model))]))

lost_customers = within_stream(update_tb_lost_sales, lost_customers)
terminate_stream(lost_customers)

# the order quantity
order_qty = create_ref(model, 0, INT_TYPE, name = 'order_qty')

# the review process queue
review_queue = create_unbounded_queue(model, data_type, name = 'review_queue')

# initiate the inventory review process
review_stream = uniform_random_stream(data_type, REVIEW_PERIOD, REVIEW_PERIOD)
unbounded_enqueue_stream(review_queue, review_stream)

review_stream = unbounded_dequeue_stream(review_queue)
review_stream = filter_stream(read_ref(inv_pos) <= REORDER_PT, review_stream)
review_stream = within_stream(write_ref(order_qty,
    return_expr(model, SCL) - read_ref(inv_pos)), review_stream)
review_stream = within_stream(write_ref(inv_pos, return_expr(model, SCL)), review_stream)
review_stream = hold_stream(return_expr(model, LEAD_TIME), review_stream)
review_stream = within_stream(write_ref(safety_stock,
    add_sampling_stats(resource_count(radio),
        read_ref(safety_stock))), review_stream)
review_stream = inc_resource(radio, read_ref(order_qty), review_stream)
terminate_stream(review_stream)

# it defines the simulation specs
specs = Specs(0, 312, 0.1)

# it compiles the model and runs the simulation experiment
model.run(specs)
