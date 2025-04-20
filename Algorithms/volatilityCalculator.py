# CODE TO CALCULATE THE HISTROCIAL VOLATILITY OF ROCK VOUCHERS
import pandas as pd
import numpy as np
import glob
import matplotlib.pyplot as plt

# Load all CSVs from current directory matching the round 5 day files
file_paths = glob.glob("Algorithms/Performance Data/Historic Data/prices_round_5_day_*.csv")

# Read and concatenate all days into a single DataFrame
dfs = [pd.read_csv(f, sep=";") for f in file_paths]
df = pd.concat(dfs, ignore_index=True)

# Filter for ROCK_VOUCHER
rock_df = df[df['product'] == 'VOLCANIC_ROCK_VOUCHER_9500'].copy()

# Compute the midprice: (bid_price_1 + ask_price_1) / 2
rock_df['midprice'] = (rock_df['bid_price_1'] + rock_df['ask_price_1']) / 2

# Calculate log returns
rock_df['log_return'] = np.log(rock_df['midprice'] / rock_df['midprice'].shift(1))

# Drop NaNs from the log return column
rock_df = rock_df.dropna(subset=['log_return'])

# Calculate historical volatility (standard deviation of log returns)
volatility = rock_df['log_return'].std()

# Optional: Annualize the volatility (e.g., assuming 1,000 ticks ~ 1 trading day, 252 days)
annualized_vol = volatility * np.sqrt(252 * (1000 / len(rock_df)))

print(f"Historical volatility of ROCK_VOUCHER: {volatility:.6f}")
print(f"Historical volatility of ROCK_VOUCHER: {annualized_vol:.6f}")

# Optional: Plot log returns
plt.figure(figsize=(10, 4))
plt.plot(rock_df['log_return'].values, label='Log Returns')
plt.title("ROCK_VOUCHER Log Returns")
plt.xlabel("Time")
plt.ylabel("Log Return")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
