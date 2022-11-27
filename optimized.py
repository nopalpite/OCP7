import csv
import time

CURRENCY = "€"
STACK = int(500)
CSV_FILE = "dataset1_Python+P7.csv"
START = time.time()

def csv_importer(csv_file):
    with open(csv_file, 'r') as file:
        reader = csv.reader(file)
        next(reader)
        items = list(line for line in reader)
        return convert_items(items)

def convert_items(items):
    for item in items.copy():
        item[1], item[2] = float(item[1]), float(item[2])
        item[1], item[2] = int(100*item[1]), int(100*item[2])
        if item[1] <= 0 or item[2] <= 0:
            items.remove(item)
    return items


def optimized(stack, items):
    matrix = [[0 for x in range(stack + 1)] for x in range(len(items) + 1)]

    for i in range(1, len(items) + 1):
        current_item = items[i-1]
        current_item_price = current_item[1]
        current_item_profit = (current_item_price*current_item[2])
        for s in range(1, stack +1):
            if current_item_price <= s:
                matrix[i][s] = max(current_item_profit + matrix[i-1][s-current_item_price], matrix[i-1][s])
            else:
                matrix[i][s] = matrix[i-1][s]
        
    s = stack
    n = len(items)
    selection = []

    while s >= 0 and n >= 0:
        i = items[n-1]
        if matrix[n][s] == matrix[n-1][s-i[1]] + (i[2]*i[1]):
            selection.append(i)
            s -= i[1]
        n -= 1
    return matrix[-1][-1],selection

def display_results(results):
    total_profit = results[0]/1000000
    for action in results[-1]:
        print(f"Buy: {action[0]} | price: {action[1]/100} {CURRENCY} | profit: {action[1]*action[2]/1000000} {CURRENCY}")
    print("")
    print(f"Total cost: {sum(action[1] for action in results[-1])/100} {CURRENCY}")
    print(f"Total profit: {total_profit} {CURRENCY}")
    end = time.time() - START
    print(f"Elapsed time: {round(end,2)} seconds")
    print("")

def main():
    items = csv_importer(CSV_FILE)
    results = optimized(STACK*100, items)
    display_results(results)

if __name__ == "__main__":
    main()