import csv
import time

CURRENCY = "€"
STACK = int(500)
CSV_FILE = "data.csv"
START = time.time()


def csv_importer(csv_file):
    with open(csv_file, 'r') as file:
        reader = csv.reader(file)
        next(reader)
        items = list(line for line in reader)
        return convert_items(items)

def convert_items(items):
    for item in items:
        item[1], item[2] = float(item[1]), float(item[2])
        item[2] = item[1] * item[2]/100
    return items

def brute_force(stack, items, selection=[]):
    if items:
        next_profit, next_selection = brute_force(stack, items[1:], selection)
        current_item = items[0]
        if current_item[1] <= stack:
            current_profit, current_selection = brute_force(stack - current_item[1], items[1:], selection + [current_item])
            if next_profit < current_profit:
                return current_profit, current_selection
        return next_profit, next_selection
    else:
        return sum(i[2] for i in selection), selection


def display_results(results):
    global START
    total_profit = results[0]
    for action in results[-1]:
        print(f"Buy: {action[0]} | price: {action[1]} {CURRENCY} | profit: {action[2]} {CURRENCY}")
    print("")
    print(f"Total cost: {sum(action[1] for action in results[-1])} {CURRENCY}")
    print(f"Total profit: {total_profit} {CURRENCY}")
    end = time.time() - START
    print(f"Elapsed time: {round(end,2)} seconds")
    print("")

def main():
    items = csv_importer(CSV_FILE)
    results = brute_force(STACK, items)
    display_results(results)


if __name__ == "__main__":
    main()
