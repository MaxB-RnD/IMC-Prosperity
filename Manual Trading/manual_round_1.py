# Define the products and their indices
products = ['seashells', 'pizza', 'silicon', 'snowballs']
product_index = {name: idx for idx, name in enumerate(products)}

# Example exchange rates: rates[i][j] = amount of product j you get for 1 of product i
# Fill this with your actual exchange rates
rates = [
    [1.0, 1.98, 0.64, 1.34],  # seashells to [seashells, pizza, silicon, snowballs]
    [0.48, 1, 0.31, 0.7],  # pizza to ...
    [1.49, 3.1, 1.0, 1.95],  # silicon to ...
    [0.72, 1.45, 0.52, 1.0],  # snowballs to ...
]

# DFS function with memoization
from functools import lru_cache

@lru_cache(maxsize=None)
def dfs(current_product, amount, trades_left):
    if trades_left == 0:
        if current_product == product_index['seashells']:
            return amount, [products[current_product]]
        else:
            return 0, []

    max_amount = 0
    best_path = []
    for next_product in range(4):
        exchanged_amount = amount * rates[current_product][next_product]
        result_amount, result_path = dfs(next_product, exchanged_amount, trades_left - 1)

        if result_amount > max_amount:
            max_amount = result_amount
            best_path = [products[current_product]] + result_path

    return max_amount, best_path

# Run the search
start_product = 'seashells'
start_amount = 500
max_seashells, trade_path = dfs(product_index[start_product], start_amount, 5)

# Print result
print(f"Maximum seashells after 5 trades: {max_seashells:.4f}")
print("Trade path:")
for i in range(len(trade_path)-1):
    print(f"  {i+1}. {trade_path[i]} → {trade_path[i+1]}")
