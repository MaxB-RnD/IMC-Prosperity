# 🌋 **IMC Prosperity 3 — Round 3 Submission**

Ahoy once more, trader! 🏴‍☠️  
Welcome to **Round 3** of the **IMC Prosperity 3 Trading Competition**.

With Round 2 behind us, we’ve weathered storms and plundered plenty — but the tides are shifting again. This time, volcanic rumblings bring **fiery new financial instruments**, and a curious visit from some slippery traders of the sea. Let’s hoist the sails and dive in! 🌋📈

---

## 🧭 **Overview**

Round 3 erupts with **derivative-style trading**, testing our strategic depth and pricing intuition. Meanwhile, new guests arrive with a peculiar marketplace of their own.

> _“Where there’s smoke, there’s opportunity — if you know how to trade it.”_

---

## ⚙️ **Algorithmic Challenge**

The islanders have gone wild for **Volcanic Rock** — so much so, they've created **Volcanic Rock Vouchers**: tradable contracts that give you the right to purchase `VOLCANIC_ROCK` at a fixed strike price.

Your goal? Evaluate and trade these vouchers smartly before they expire, balancing **premium cost**, **strike price**, and **time left**. 🧠💰

### 🌋 New Products:

Each **Voucher** comes with:
- A **strike price** (fixed cost to redeem)
- A **premium** (traded market value)
- A fixed **expiration** (7 trading days from Round 1 start)

| Product | Strike Price | Position Limit |
|--------|--------------|----------------|
| `VOLCANIC_ROCK_VOUCHER_9500` | 9,500 | 200 |
| `VOLCANIC_ROCK_VOUCHER_9750` | 9,750 | 200 |
| `VOLCANIC_ROCK_VOUCHER_10000` | 10,000 | 200 |
| `VOLCANIC_ROCK_VOUCHER_10250` | 10,250 | 200 |
| `VOLCANIC_ROCK_VOUCHER_10500` | 10,500 | 200 |
| `VOLCANIC_ROCK` | — | 400 |

By Round 3, **only 5 days remain** until expiry.

This challenge is about **option-like valuation** and timing:  
> _Is the premium worth paying for a chance to redeem at a favorable price?_  
> _Should we hold or trade the vouchers themselves?_  

Your strategy must be as solid as the rocks you’re trading.

---

## 🐢 **Manual Challenge**

A curious convoy of **Sea Turtles** has washed ashore, bearing precious `FLIPPERS` — and they’re open to bids.

But beware: they’re picky, and a little... superstitious.

### 🐚 The Rules:
- You get **two chances** to submit a bid.
  - First bid: evaluated independently  
  - Second bid: compared **globally** across all traders

- Turtles accept the **lowest bid** above their **secret reserve price**.

- **Reserve Prices**:
  - Uniformly distributed:
    - 160–200
    - 250–320  
  - Absolutely **no trades** between 200–250. Ancient superstition. Don’t even try.

- **Second Bids**:
  - If your second bid is **above the global average**, great!
  - If **below**, you might still get a trade — but your PNL gets scaled:
    
    ```p = ((320 – average bid) / (320 – your bid))^3```

> Lower your bid too far, and your profits could vanish like a turtle into the sea...

### 💸 The Reward:
All acquired `FLIPPERS` can be sold back to the market for **320 SeaShells each** at the end of the round.

---

## 🌊 **In Summary**

Round 3 is where **risk meets reward** — introducing time-decaying opportunities and dynamic, player-influenced outcomes.  
Success now depends not just on tactical brilliance, but also on understanding **market psychology** and timing your plays.

We’re not just navigating the tides.  
We’re shaping them. 🌅

Let’s make Round 3 our most **prosperous** yet. 🏝️📉📈
