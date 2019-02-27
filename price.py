import csv
import datetime

def price(product_id, price):
    # returns price from products??????

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
                updatedRow[3] = price
        if index != 0:
            lines[index] = updatedRow

    with open('products.csv', 'w', newline='') as writeProducts:
        writer = csv.writer(writeProducts)
        writer.writerows(lines)

