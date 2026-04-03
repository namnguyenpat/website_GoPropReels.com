---
title: "Trailing vs Static Drawdown Explained — What Every Prop Trader Must Know"
description: "Understand the critical difference between trailing and static drawdown in prop firms. Learn how each type works, which is harder, and how to trade around them."
pubDate: "2026-04-02"
category: "Knowledge"
tags: ["trailing drawdown", "static drawdown", "prop firm drawdown", "max drawdown", "funded account rules"]
---

## The Rule That Ends More Challenges Than Any Bad Trade

Ask any experienced prop trader what trips up new challenge participants the most, and you will hear the same answer: **drawdown misunderstanding**.

Specifically, the confusion between **trailing drawdown** and **static drawdown**. These two rule types behave in fundamentally different ways — and failing to understand the difference can cause you to violate a rule you thought you were obeying.

This is the scene that defines your career. Pay close attention.

---

## Static Drawdown: The Simpler Model

Static drawdown (also called **fixed drawdown**) is calculated from a fixed baseline — your starting account balance. It does not move as your equity grows.

**How it works:**

- Account starts at $100,000
- Maximum drawdown is 10% = $10,000 buffer
- Your **hard floor** is $90,000 — forever
- Even if you grow your account to $130,000, your floor remains $90,000

**Formula:** `Hard Floor = Starting Balance − Maximum Drawdown Amount`

### Example

| Day | Equity | Hard Floor | Buffer Remaining |
|-----|--------|------------|------------------|
| Start | $100,000 | $90,000 | $10,000 |
| After gain | $108,000 | $90,000 | $18,000 |
| After loss | $94,000 | $90,000 | $4,000 |

The key insight: **profits create more room in a static model**. As your equity grows, your drawdown buffer relative to current equity expands.

---

## Trailing Drawdown: The Tighter, Moving Floor

Trailing drawdown (also called **dynamic drawdown**) moves upward with your peak equity. It is the harder of the two models and the one that catches traders off-guard most frequently.

**How it works:**

- Account starts at $100,000
- Maximum drawdown is 10% = trailing by $10,000
- Your floor starts at $90,000
- If your equity hits $105,000, your floor moves up to $95,000
- If your equity hits $112,000, your floor moves up to $102,000

**Formula:** `Current Floor = Peak Equity − Maximum Drawdown Amount`

### Example

| Day | Equity | Peak Equity | Floor | Buffer |
|-----|--------|-------------|-------|--------|
| Start | $100,000 | $100,000 | $90,000 | $10,000 |
| Gain day | $107,000 | $107,000 | $97,000 | $10,000 |
| Loss day | $101,000 | $107,000 | $97,000 | $4,000 |
| Gain day | $109,000 | $109,000 | $99,000 | $10,000 |

The critical reality: **you can never increase your drawdown buffer in a trailing model**. It always stays at the maximum allowed drawdown from your highest point.

---

## The Dangerous Variant: End-of-Day vs Real-Time Trailing

Some firms use **end-of-day trailing** (the floor moves based on your closing equity each day), while others use **real-time trailing** (the floor tracks your intraday peak).

**Real-time trailing is the most unforgiving.** Your intraday floating equity — even unrealized profits you never locked in — can push your floor higher. Then if the trade reverses, you are suddenly closer to your floor than you realized.

### Real-Time Trailing Trap Example

- Account balance: $100,000
- Floor at start: $90,000
- Trade goes up, floating equity reaches $106,000 → floor moves to $96,000
- Trade reverses to $94,000 → you are only $4,000 from the floor
- You thought you had $10,000 buffer. You only have $4,000.

This scenario ends challenges every single day.

---

## Which Is Harder: Trailing or Static?

**Trailing drawdown is significantly harder**, particularly at the start of an evaluation.

With static drawdown, a few early wins give you breathing room. With trailing drawdown, early wins raise the floor and leave you with the same buffer — but now trading closer to breakeven with less psychological margin.

### Head-to-Head Comparison

| Feature | Static Drawdown | Trailing Drawdown |
|---------|----------------|-------------------|
| Floor position | Fixed forever | Moves up with peak equity |
| Does winning help? | Yes — increases buffer | No — buffer stays the same |
| Intraday risk | Predictable | Can change with open positions |
| Preferred by traders? | Yes | Less preferred |
| Common in: | FTMO, The5ers | Apex, older Topstep models |

---

## How to Trade Safely With Trailing Drawdown

**1. Protect your unrealized gains.**
Never let a winning trade turn into a loss that impacts your floor. Move stop-losses to breakeven as soon as a trade moves 1:1 in your favor.

**2. Do not scalp aggressively in real-time trailing models.**
Multiple small floating gains that reverse quickly are a recipe for floor creep without the corresponding retained profits.

**3. Know your current floor at all times.**
Use a spreadsheet or your firm's dashboard to track your peak equity and current floor daily.

**4. Be conservative in the first two weeks.**
The floor cannot go down — only up. Build your equity slowly and consistently. The worst thing you can do is sprint to a big gain early and then give it back.

**5. Treat every day like your floor just moved.**
Assume the floor is higher than yesterday. This conservative mindset prevents complacency.

---

## Quick Reference Card

| Question | Static Answer | Trailing Answer |
|----------|--------------|----------------|
| "Does my floor move if I profit?" | No | Yes — upward |
| "Does my buffer shrink if I profit?" | No — it grows | No — stays fixed |
| "Can floating equity move the floor?" | No | Yes (in real-time models) |
| "What is my floor on Day 1?" | Starting balance minus max DD | Same as static on Day 1 |

---

## Final Cut

Understanding drawdown is not optional — it is foundational. Before you fund any challenge, confirm whether the firm uses static or trailing drawdown, and whether trailing is end-of-day or real-time.

The firm that seems cheaper might use trailing drawdown. The target that looks easy might be sitting on a real-time trailing floor. Know the terrain before you enter the scene.
