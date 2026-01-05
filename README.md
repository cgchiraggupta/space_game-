# Space Shooter Game

A 2D aerospace shooter game built with Python and Pygame.

## Features

- **Player spaceship** with smooth controls
- **Enemies** that fly from the right side of the screen
- **Asteroids** to dodge and destroy
- **Power-ups** that restore health
- **Shooting mechanics** with bullet projectiles
- **Explosion effects** when objects are destroyed
- **Score tracking** system
- **Health bar** display
- **Scrolling star background** for atmosphere
- **Game over and restart** functionality

## Installation

1. Make sure you have Python 3.7+ installed
2. Install the required dependency:

```bash
pip install -r requirements.txt
```

Or install pygame directly:

```bash
pip install pygame
```

## How to Play

Run the game:

```bash
python space_shooter.py
```

### Controls

- **WASD** or **Arrow Keys**: Move your spaceship
- **SPACE**: Shoot bullets
- **R**: Restart game (when game over)

### Gameplay

- Destroy enemies and asteroids to earn points
- Avoid collisions with enemies and asteroids (they damage your ship)
- Collect green power-ups to restore health
- Survive as long as possible and achieve a high score!

### Scoring

- Enemy destroyed: **10 points**
- Asteroid destroyed: **5 points**
- Power-up collected: **15 points**

## Project Structure

```
space_game/
├── space_shooter.py    # Main game file
├── requirements.txt    # Python dependencies
└── README.md          # This file
```

## Customization

You can easily modify the game by editing `space_shooter.py`:

- Change colors in the color constants at the top
- Adjust player speed, health, and shooting rate in the Player class
- Modify enemy/asteroid spawn rates in the game loop
- Change screen dimensions with WIDTH and HEIGHT variables
- Adjust difficulty by modifying enemy speeds and spawn frequencies

Enjoy playing!
# space_game-
