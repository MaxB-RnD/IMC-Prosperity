# 🏝️ **IMC Prosperity 3 — Round 5 Submission**

Ahoy, Prosperous Pirates! 🏴‍☠️  
The final wave is here — Round 5 has arrived to test your mettle one last time.

No new products? Don’t be fooled — this round sharpens the edge with **social dynamics** and **strategic escalation**. 🧠📈  
It’s not just about market mechanics anymore — it’s about **who** you’re trading with… and **how** you outplay them.

---

## 📊 **Algorithmic Challenge: Know Thy Counterparty**

The twist? The exchange has started revealing the **identity of your trading counterparty**.
Meet the new attribute in the `OwnTrade` object:
```python
class OwnTrade:
    def __init__(self, symbol: Symbol, price: int, quantity: int, counter_party: UserId = None) -> None:
        self.symbol = symbol
        self.price: int = price
        self.quantity: int = quantity
        self.counter_party = counter_party
```

**This change unlocks powerful possibilities:**
- Track **opponents’ behavior**.
- Identify **market manipulators**.
- Avoid **bad fills** or exploit **predictable actors**.
- Build **player models** and craft strategies to outsmart them.

> _Every trade tells a story. It’s time to read between the lines… and rewrite your ending._ ✍️

---

## 🌐 **Manual Challenge: The West Archipelago Exchange**

Welcome to a **one-day special event** in the **West Archipelago** — hosted by none other than **Benny the Bull**. 🐂💼  
It’s a **high-stakes playground** where fortunes are made — and lost — at lightning speed.

### 📰 Goldberg’s Insider Tips

Benny shares his most **trusted news source** with you: **Goldberg**.  
Use it wisely — insights from Goldberg can give you a **critical edge**.

### ⚠️ Escalating Trade Costs

The more you trade a **single product**, the **more expensive** it gets.  
Overtrading will eat your profits — so trade **strategically**, not just frequently.

> _This is the endgame. Everyone’s swinging for the fences. Stay sharp, trade smart, and remember: sometimes the boldest move is the one not made._ ⚔️

---

## 🐜🕷️🪳 **Know Your Enemies (and Friends)**

With counterparty visibility, you’ll see names like:

- **Amir Ant** — master of coordination  
- **Bashir Beetle** — smooth talker, risk taker  
- **Sami Spider** — hammocked code wizard  
- **Cristiano Cockroach** — the comeback king

...and many more. Each trader brings quirks, strategies, and reputations. Use this intel.  
Track trends. Find patterns. Learn their tells. And beat them at their own game.

---

## 🏁 **Final Words**

This is it. The last stretch. No do-overs. No retries.  
You’ve come this far — now show the island what you’re made of.

Outwit the spiders, outmaneuver the beetles, outlast the cockroaches.  
Make every trade count — and bring it home. 💰🏆

Let’s finish strong, pirates.  
**For glory. For profit. For Prosperity.** 🏝️🔥