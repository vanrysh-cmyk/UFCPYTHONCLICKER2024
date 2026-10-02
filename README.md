# 🥊 UFC Python Clicker 2024 (v2)

A clean, standalone 3D MMA Manager and Clicker game built with **Python** and the **Ursina Engine**. Experience the ultimate cyber-grind from the streets to the UFC top tiers!

> **"the my 6 project"** — Designed to run flawlessly out of the box with zero complex configurations.

---

## ✨ Core Features

- 🎮 **Hybrid Gameplay:** 
  - **Manual Mode:** Get close to your opponent and smash your Left Mouse Button (LMB) to strike.
  - **AUTO Mode:** Sit back, turn on the AI manager, and watch your fighter dominate while managing stamina and attack cooldowns automatically.
- 📈 **Career Progression & RPG Upgrades:** Earn **\$200** per victory to level up your **HP** and **Damage** stats.
- 🏆 **Locked Leagues & Roster:** Face dynamic opponents across multiple tiers:
  - **STREET:** Drunk Joe, Slim Shady
  - **REGIONAL:** Gym Owner, Pro Prospect (Unlocks at 5+ wins)
  - **UFC TOP:** Makhachev, Jon Jones (Unlocks at 15+ wins)
- 💥 **Juicy Combat Effects:** Model blinking on hits, dynamic blood particle spawning, stamina drain mechanics, and a dramatic knockout (KO) fall animation.
- 💾 **Auto-Save System:** Fully integrated local JSON storage ensures your career wins and cash are never lost.

---

## 🚀 Quick Start (Out of the Box)

1. **Install dependencies:**
   ```bash
   pip install ursina
   ```

2. **Run the game:**
   ```bash
   python ufc2024v2.py
   ```

---

## 🛠️ Tech Stack & Architecture

- **Language:** Python 100%
- **Engine:** Ursina Engine (3D Graphics & UI)
- **Data-Driven Design:** Easily extendable opponent dictionaries and dynamic menu rendering.
- **Storage:** Built-in `json` serialization for state management.
