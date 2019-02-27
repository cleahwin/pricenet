import csv
import datetime

def delivery(product_id, quantity, cost):
    # update supply and avg. cost in products
    # [product_id, light, quantity, price, avg_cost, model]
    lines = list()
    with open('products.csv') as readProducts:
        reader = csv.reader(readProducts)
        i = -1
        index = 0
        updatedRow = ['', '', '', '', '', '']
        for row in reader:
            lines.append(row)
            i = i + 1
            if str(row[0]) == product_id:
                index = i
                updatedRow = row
                updatedRow[2] = quantity
                newCost = ((quanitity * cost) + (row[2] * row[4])) / (quantity + row[2])
                updatedRow[4] = newCost
        if index != 0:
            lines[index] = updatedRow

    with open('products.csv', 'w', newline='') as writeProducts:
        writer = csv.writer(writeProducts)
        writer.writerows(lines)

     # append delivery in delivery hisory
     # [product-id date-time quantity avg-cost]
    data_row = [product_id, str(datetime.datetime.now()), quantity, cost]
    with open('delivery_history.csv', 'a', newline='') as delivery_history:
        writer = csv.writer(delivery_history)
        writer.writerow(data_row)
    delivery_history.close()