import csv
import datetime

def light(product_id, light):
    # update light in products
    # [product_id, light, quantity, price, avg_cost, model]
    lines = list()
    with open('products.csv') as readProducts:
        #listReader = csv.reader(readProducts)
        #lines = list(listReader)
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
                updatedRow[1] = light
        if index != 0:
            lines[index] = updatedRow

    with open('products.csv', 'w', newline='') as writeProducts:
        writer = csv.writer(writeProducts)
        writer.writerows(lines)

    # append light in light hisory
    data_row = [product_id, str(datetime.datetime.now()), light]
    with open('light_history.csv', 'a', newline='') as light_history:
        writer = csv.writer(light_history)
        writer.writerow(data_row)
    light_history.close()