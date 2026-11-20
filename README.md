# Michael's House - GTA Style Video Game

A Python-based top-down video game set inside Michael's house from GTA V. Move around the house, interact with characters and items, and collect money!

## Features

- **6 Interactive Rooms**: Living Room, Kitchen, Bedroom, Bathroom, Hallway, and Garage
- **Player Movement**: Move around Michael's house with smooth controls
- **NPCs**: Meet characters like Tracey, the Chef, and the Maid
- **Item Collection**: Pick up money and items to increase your score
- **Health System**: Monitor your health with a visual health bar
- **Money System**: Collect money scattered throughout the house
- **Inventory System**: Keep track of collected items

## Setup Instructions

### Requirements
- Python 3.7+
- Pygame

### Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the game:
```bash
python michaels_house_game.py
```

## Controls

| Key | Action |
|-----|--------|
| **Arrow Keys** | Move up, down, left, right |
| **WASD** | Alternative movement controls |
| **SPACE** | Interact with NPCs and items |
| **ESC** | Quit game |

## Game Mechanics

### Rooms
- **Living Room**: Start here, collect money and meet Tracey
- **Kitchen**: Find the Chef and grab some food
- **Bedroom**: Meet the Maid and collect items
- **Bathroom**: Quick room to explore
- **Hallway**: Central connecting area
- **Garage**: Michael's car and money items

### Items & Collectibles
- **Money** (Green circles): Collect for cash
- **Items** (Red circles): Pick up for inventory

### NPCs
- Tracey, Chef, and Maid wander around the house
- Press SPACE near them to interact

### HUD Display
- **Money Counter**: Shows total cash collected
- **Health Bar**: Visual representation of your health
- **Inventory Count**: Number of items you're carrying
- **Instructions**: Control reminders on screen

## Game Systems

### Player Stats
- Health: 100 (decreases if you interact with certain NPCs)
- Money: Earned by collecting money items
- Inventory: Tracks collected items

### NPC Behavior
- NPCs move around their respective rooms
- They bounce off walls staying within their room boundaries

### Item Mechanics
- Money items give +$50 when collected
- Other items are added to your inventory
- Items only appear once and disappear when collected

## Tips

1. Explore all rooms to find all items
2. Interact with NPCs to earn messages/achievements
3. Collect as much money as possible
4. The garage has valuable items to collect

## Customization

You can easily customize:
- Room colors and sizes (in `setup_house()`)
- NPC names and spawn locations
- Item locations and values
- Player speed and health
- Screen size (modify constants at the top)

## Architecture

- **Room**: Represents individual rooms with properties
- **Furniture**: Static decorative objects in rooms
- **Item**: Collectible items (money/objects)
- **NPC**: Non-player characters with AI movement
- **Player**: Main character controlled by player
- **Game**: Main game loop and state management

Enjoy exploring Michael's house!
