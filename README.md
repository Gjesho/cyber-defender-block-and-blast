# Cyber Defender: Block & Blast

> A full-featured, original 2D game built from scratch in Python + Pygame — combining Tetris-style tower building with Space Invaders defense, wrapped in an internet-safety narrative with a polished progression system.

---

## Overview

**Cyber Defender: Block & Blast** is a team-developed game that blends two classic arcade genres into a cohesive gameplay loop. Players defend against cyber-threat enemies by first constructing a firewall using falling Tetris pieces, then fighting off waves of invaders with a ship in real time. Between waves, educational scenario cards present internet-safety dilemmas whose outcomes feed back into the game as buffs or debuffs.

The project demonstrates end-to-end game development in Python — custom engine, scene management, save/load system, localization, progression, UI, and a modular content pipeline — without relying on any game-development framework beyond raw Pygame.

---

## Key Technical Highlights

| Area | Detail |
|------|--------|
| **Architecture** | Custom scene-graph engine (`core.py`) with a clean `Scene` base class, scene transitions, and a centralised app state object |
| **Game Modes** | Story mode (21 levels across 3 acts, 5 boss encounters)|
| **Save System** | JSON serialisation with versioned migration, settings normalization, and per-field validation via `save_system.py` |
| **Localization** | Full EN/MK bilingual support — all UI strings, scenario cards, quiz questions, and splash text driven by a single `localization.py` dictionary |
| **Progression** | XP ranking, coin economy, 20+ achievements with claim rewards |
| **Gameplay Systems** | Tetris engine (rotation, wall-kick, hold, ghost piece), Invaders engine (wave spawning, AI movement, projectiles, collision), Dash mechanic with cooldown HUD |
| **Boss System** | 5 unique named bosses, each with its own sprite, health bar, and multi-phase behaviour |
| **UI/UX** | Custom panel renderer, smooth scroll with interpolation, animated achievement cards, settings page with audio/fullscreen controls |
| **Build & Distribution** | Place holder untill wasm is integrated |

---

## Running Locally

```bash
python -m venv .venv
.venv\Scripts\activate        # Windows
# source .venv/bin/activate   # macOS / Linux

pip install -r requirements.txt
python main.py
```

**Requirements:** Python 3.10+, Pygame 2.x

---

## Controls

| Context | Key | Action |
|---------|-----|--------|
| Build phase | `←` `→` | Move piece |
| | `↓` | Soft drop |
| | `↑` / `X` | Rotate clockwise |
| | `Z` | Rotate counter-clockwise |
| | `C` | Hold piece |
| Fight phase | `←` `→` | Move ship |
| | `Space` | Shoot |
| | `Shift` | Dash |
| | `Esc` | Pause |
| Menus | Mouse | All navigation |

---

## Gameplay Loop

```
Story Map → [Splash / Narrative] → Build Phase (Tetris firewall)
         → Fight Phase (wave 1 … n) → [Quiz Card between waves]
         → Hub (XP/coins, shop, next level or boss)
```

Boss encounters replace the standard fight phase with a multi-wave scripted sequence. Completing Act I (levels 1–8) or Act II (9–14) triggers an act-transition splash that advances the story.

---

## Educational Mechanic

The Library is the core progression and educational system of the game, where players answer questions selected from a structured database. Correct answers reward the player with in-game currency, which is necessary to maintain financial stability and unlock further progress. This creates a gameplay loop where knowledge directly impacts the player’s economic survival and advancement.

---
