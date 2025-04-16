# 🏝️ **IMC Prosperity 3 — Round 4 Submission**

Ahoy again, Prosperous Pirates! 🏴‍☠️  
Round 4 has docked — and it brings **culinary delights and suitcase strategy** to test your trading wits and psychological instincts.

The market grows stranger still, but our resolve? Never stronger. Let’s sink our teeth into this one. 🧁💼

---

## 🍰 **Algorithmic Challenge: Magnificent Macarons**

The latest luxury commodity on the island is the delectable `MAGNIFICENT_MACARONS`. Prized for their complexity, these sweet treats fluctuate in value based on a recipe of real-world-like factors: ☀️ **sunlight hours**, 💰 **sugar prices**, 🚢 **shipping costs**, 📦 **storage limitations**, and 🎯 **tariffs**.

But the macarons come with a twist — you can only get them from **Pristine Cuisine**, and each transaction comes at a **cost**:

### ⚙️ Mechanics

- **Buy** from Pristine Cuisine:  
  - Pay `askPrice` + `TRANSPORT_FEES` + `IMPORT_TARIFF`

- **Sell** to Pristine Cuisine:  
  - Receive `bidPrice` - `TRANSPORT_FEES` - `EXPORT_TARIFF`

- **Position Limits**:  
  - `MAGNIFICENT_MACARONS`: **75**
  - Conversion Limit: **10 per request**

- **Storage Fees**:  
  - **0.1 Seashells** per timestamp **for every net long unit**  
  - No storage fee for short positions

> _The key: determine true fair value — account for all frictions and forecast supply-demand._  
> _Buy low, sell high — but storage and conversion costs could eat your profits like ants at a picnic._

---

## 💼 **Manual Challenge: Suitcase Showdown**

Welcome to the island’s hottest new game show. 🎉  
Every inhabitant is offered a shot at treasure by opening up to **three** mysterious **suitcases**. The catch? You split the loot — and your curiosity costs coins.

### 🧳 Game Rules:

- **Open up to 3 suitcases**
  - First suitcase: **free**
  - Second/third suitcases: **cost seashells**

- Each suitcase has:
  - **Treasure Multiplier** (max 100)
  - **Inhabitants** (up to 15 choosing the same)
  - **Global Pick %** (how often this suitcase is chosen)

- **Profit Formula:**

```text
PRIZE = (10,000 × multiplier) / (inhabitants + pickPercentageOfAllSuitcaseOpens)
```

Your Profit = PRIZE - Opening Costs

>_Pick a popular suitcase and your share shrinks. Pick an unpopular one and... maybe it’s empty._🧠
>_Smart pirates strategize — they don’t just follow the crowd._

---

## 🌊 **In Summary**

Round 4 sharpens the edge between **fundamental forecasting** and strategic **resource allocation**. Whether you’re mastering macarons or cracking the suitcase code, only the cleverest will thrive.

Let’s cook up profits — and uncover hidden treasures. 🍬💸
