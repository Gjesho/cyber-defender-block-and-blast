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
| **Game Modes** | Story mode (21 levels across 3 acts, 5 boss encounters), Endless mode with escalating difficulty, Daily Challenge (seeded RNG) |
| **Save System** | JSON serialisation with versioned migration, settings normalization, and per-field validation via `save_system.py` |
| **Localization** | Full EN/MK bilingual support — all UI strings, scenario cards, quiz questions, and splash text driven by a single `localization.py` dictionary |
| **Progression** | XP ranking, coin economy, cosmetic unlocks (ship skins, trails, firewall palettes), 20+ achievements with claim rewards |
| **Gameplay Systems** | Tetris engine (rotation, wall-kick, hold, ghost piece), Invaders engine (wave spawning, AI movement, projectiles, collision), Dash mechanic with cooldown HUD |
| **Boss System** | 5 unique named bosses, each with its own sprite, health bar, and multi-phase behaviour |
| **UI/UX** | Custom panel renderer, smooth scroll with interpolation, animated achievement cards, settings page with audio/fullscreen controls |
| **Build & Distribution** | PyInstaller spec (`cyber_defender.spec`) for single-folder Windows executable |

---

## Project Structure

```
cyber-defender-block-and-blast/
├── main.py                    # Entry point (asyncio loop for pygbag web compat)
├── requirements.txt
├── cyber_defender.spec        # PyInstaller build config
├── assets/                    # Sprites, background, boss images
├── data/
│   └── save.json              # Auto-created on first run
└── src/
    ├── core.py                # App dataclass, scene lifecycle, display, settings
    ├── save_system.py         # SaveData, Settings, load/save, migration
    ├── assets.py              # Font loading, colour palette generation
    ├── constants.py           # Resolution, FPS, paths, balance constants
    ├── ui.py                  # Reusable Button, draw_panel, draw_text helpers
    ├── localization.py        # EN/MK string table
    ├── achievements.py        # Achievement definitions and unlock logic
    ├── scenes/
    │   ├── base.py            # BaseScene with shared draw_background helper
    │   ├── menu.py            # Main menu
    │   ├── hub.py             # Inter-level hub (story consequences, shop access)
    │   ├── build.py           # Tetris build phase
    │   ├── fight.py           # Space Invaders fight phase (largest scene, ~1600 LOC)
    │   ├── storymap.py        # Scrollable story level select
    │   ├── splash.py          # Narrative splash screens
    │   ├── quiz.py            # Educational quiz / scenario card system
    │   ├── shop.py            # Cosmetics shop
    │   ├── achievements.py    # Achievements UI with animated cards and claimable rewards
    │   ├── settings.py        # Settings page (audio, fullscreen, language, save reset)
    │   └── credits.py         # Credits screen
    └── gameplay/
        ├── level_config.py    # Per-level configuration (enemies, splashes, flags)
        ├── tetris.py          # Tetris engine (pieces, board, rotation, scoring)
        └── invaders.py        # Enemy types, spawning, projectiles, boss logic
```

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

Between waves, scenario cards present a real-world internet-safety situation (phishing email, DM from a stranger, suspicious download, etc.) with three labelled choices: **Safe to Share / Private / Never Share**. The correct answer is rewarded with better Tetris pieces, bonus coins, and XP. Wrong answers spawn junk blocks, trigger debuffs (lag lines, pop-up fog overlay, fake-reward trap), and deduct score — giving the choices immediate, tangible gameplay weight rather than treating the quiz as a separate activity.

---

## Build for Distribution

```bash
pyinstaller cyber_defender.spec
# Output: dist/CyberDefender/CyberDefender.exe (Windows, no Python required)
```
