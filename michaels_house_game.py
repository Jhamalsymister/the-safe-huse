import pygame
import sys
from enum import Enum
from typing import List, Tuple
import random

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
FPS = 60
GRID_SIZE = 40

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
DARK_GRAY = (64, 64, 64)
LIGHT_GRAY = (200, 200, 200)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BROWN = (139, 69, 19)
BEIGE = (245, 245, 220)
DARK_BLUE = (0, 0, 139)

class RoomType(Enum):
    BEDROOM = 1
    KITCHEN = 2
    LIVING_ROOM = 3
    BATHROOM = 4
    HALLWAY = 5
    GARAGE = 6

class Room:
    def __init__(self, x: int, y: int, width: int, height: int, room_type: RoomType, color: Tuple):
        self.rect = pygame.Rect(x, y, width, height)
        self.room_type = room_type
        self.color = color
        self.name = room_type.name.replace('_', ' ').title()
        self.furniture = []
        self.items = []

    def draw(self, surface: pygame.Surface):
        pygame.draw.rect(surface, self.color, self.rect)
        pygame.draw.rect(surface, BLACK, self.rect, 3)

        # Draw room name
        font = pygame.font.Font(None, 36)
        text = font.render(self.name, True, BLACK)
        text_rect = text.get_rect(center=(self.rect.centerx, self.rect.y + 20))
        surface.blit(text, text_rect)

class Furniture:
    def __init__(self, x: int, y: int, width: int, height: int, name: str, color: Tuple):
        self.rect = pygame.Rect(x, y, width, height)
        self.name = name
        self.color = color

    def draw(self, surface: pygame.Surface):
        pygame.draw.rect(surface, self.color, self.rect)
        pygame.draw.rect(surface, BLACK, self.rect, 2)

class Item:
    def __init__(self, x: int, y: int, name: str, item_type: str):
        self.rect = pygame.Rect(x, y, 20, 20)
        self.name = name
        self.item_type = item_type
        self.color = GREEN if item_type == "money" else RED

    def draw(self, surface: pygame.Surface):
        pygame.draw.circle(surface, self.color, self.rect.center, 10)
        pygame.draw.circle(surface, BLACK, self.rect.center, 10, 2)

class NPC:
    def __init__(self, x: int, y: int, name: str):
        self.rect = pygame.Rect(x, y, 30, 30)
        self.name = name
        self.vx = random.uniform(-1, 1)
        self.vy = random.uniform(-1, 1)
        self.speed = 1

    def update(self, rooms: List[Room]):
        self.rect.x += self.vx * self.speed
        self.rect.y += self.vy * self.speed

        # Bounce off walls and stay within rooms
        for room in rooms:
            if room.rect.colliderect(self.rect):
                if self.rect.left < room.rect.left or self.rect.right > room.rect.right:
                    self.vx *= -1
                if self.rect.top < room.rect.top or self.rect.bottom > room.rect.bottom:
                    self.vy *= -1

    def draw(self, surface: pygame.Surface):
        pygame.draw.rect(surface, BLUE, self.rect)
        pygame.draw.rect(surface, BLACK, self.rect, 2)

        font = pygame.font.Font(None, 20)
        text = font.render(self.name, True, BLACK)
        surface.blit(text, (self.rect.x - 10, self.rect.y - 20))

class Player:
    def __init__(self, x: int, y: int):
        self.rect = pygame.Rect(x, y, 25, 25)
        self.speed = 3
        self.health = 100
        self.money = 0
        self.inventory = []
        self.message = ""
        self.message_timer = 0

    def handle_input(self, keys):
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.rect.x += self.speed
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.rect.y += self.speed

    def clamp_to_screen(self):
        self.rect.x = max(0, min(self.rect.x, SCREEN_WIDTH - self.rect.width))
        self.rect.y = max(0, min(self.rect.y, SCREEN_HEIGHT - self.rect.height))

    def update(self, rooms: List[Room]):
        # Keep player in valid room
        in_valid_room = False
        for room in rooms:
            if room.rect.colliderect(self.rect):
                in_valid_room = True
                break

        if not in_valid_room:
            self.rect.x = max(room.rect.left, min(self.rect.x, room.rect.right - self.rect.width))
            self.rect.y = max(room.rect.top, min(self.rect.y, room.rect.bottom - self.rect.height))

        if self.message_timer > 0:
            self.message_timer -= 1

    def draw(self, surface: pygame.Surface):
        pygame.draw.rect(surface, RED, self.rect)
        pygame.draw.rect(surface, BLACK, self.rect, 2)

        # Draw health bar
        bar_width = 50
        bar_height = 5
        bar_x = self.rect.x - 12.5
        bar_y = self.rect.y - 10
        pygame.draw.rect(surface, RED, (bar_x, bar_y, bar_width, bar_height))
        pygame.draw.rect(surface, GREEN, (bar_x, bar_y, bar_width * (self.health / 100), bar_height))
        pygame.draw.rect(surface, BLACK, (bar_x, bar_y, bar_width, bar_height), 1)

        # Draw message
        if self.message_timer > 0:
            font = pygame.font.Font(None, 24)
            text = font.render(self.message, True, BLACK)
            surface.blit(text, (self.rect.x - 40, self.rect.y - 30))

    def interact(self, npcs: List[NPC], items: List[Item]):
        # Check interaction with NPCs
        for npc in npcs:
            if self.rect.colliderect(npc.rect):
                self.message = f"Met {npc.name}!"
                self.message_timer = 60

        # Check interaction with items
        for item in items[:]:
            if self.rect.colliderect(item.rect):
                if item.item_type == "money":
                    self.money += 50
                    self.message = "+$50"
                    self.message_timer = 60
                else:
                    self.inventory.append(item.name)
                    self.message = f"Picked up {item.name}"
                    self.message_timer = 120
                items.remove(item)

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Michael's House - GTA Style Game")
        self.clock = pygame.time.Clock()
        self.running = True
        self.rooms: List[Room] = []
        self.furniture: List[Furniture] = []
        self.npcs: List[NPC] = []
        self.items: List[Item] = []
        self.player = Player(300, 300)

        self.setup_house()

    def setup_house(self):
        """Setup Michael's house layout"""

        # Living room
        living_room = Room(50, 50, 400, 300, RoomType.LIVING_ROOM, BEIGE)
        self.rooms.append(living_room)
        # Furniture
        self.furniture.append(Furniture(100, 100, 100, 80, "Couch", BROWN))
        self.furniture.append(Furniture(250, 120, 80, 60, "TV", DARK_GRAY))
        self.items.append(Item(350, 200, "Money", "money"))

        # Kitchen
        kitchen = Room(500, 50, 300, 300, RoomType.KITCHEN, LIGHT_GRAY)
        self.rooms.append(kitchen)
        self.furniture.append(Furniture(550, 100, 120, 60, "Counter", GRAY))
        self.furniture.append(Furniture(550, 200, 80, 80, "Fridge", WHITE))
        self.items.append(Item(650, 250, "Food", "item"))

        # Bedroom
        bedroom = Room(850, 50, 300, 300, RoomType.BEDROOM, LIGHT_GRAY)
        self.rooms.append(bedroom)
        self.furniture.append(Furniture(900, 120, 120, 100, "Bed", BROWN))
        self.furniture.append(Furniture(980, 250, 80, 60, "Dresser", BROWN))
        self.items.append(Item(950, 180, "Money", "money"))

        # Bathroom
        bathroom = Room(50, 400, 250, 300, RoomType.BATHROOM, LIGHT_GRAY)
        self.rooms.append(bathroom)
        self.furniture.append(Furniture(100, 450, 80, 60, "Toilet", WHITE))
        self.furniture.append(Furniture(200, 450, 60, 60, "Sink", WHITE))
        self.items.append(Item(150, 550, "Money", "money"))

        # Hallway
        hallway = Room(350, 400, 400, 300, RoomType.HALLWAY, BEIGE)
        self.rooms.append(hallway)
        self.items.append(Item(500, 500, "Key", "item"))

        # Garage
        garage = Room(800, 400, 350, 300, RoomType.GARAGE, DARK_GRAY)
        self.rooms.append(garage)
        self.furniture.append(Furniture(850, 450, 150, 120, "Car", DARK_BLUE))
        self.items.append(Item(1000, 550, "Money", "money"))

        # NPCs
        self.npcs.append(NPC(150, 150, "Tracey"))
        self.npcs.append(NPC(600, 150, "Chef"))
        self.npcs.append(NPC(950, 150, "Maid"))

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_SPACE:
                    self.player.interact(self.npcs, self.items)

    def update(self):
        keys = pygame.key.get_pressed()
        self.player.handle_input(keys)
        self.player.clamp_to_screen()
        self.player.update(self.rooms)

        for npc in self.npcs:
            npc.update(self.rooms)

    def draw(self):
        self.screen.fill(WHITE)

        # Draw rooms
        for room in self.rooms:
            room.draw(self.screen)

        # Draw furniture
        for furn in self.furniture:
            furn.draw(self.screen)

        # Draw items
        for item in self.items:
            item.draw(self.screen)

        # Draw NPCs
        for npc in self.npcs:
            npc.draw(self.screen)

        # Draw player
        self.player.draw(self.screen)

        # Draw HUD
        self.draw_hud()

        pygame.display.flip()

    def draw_hud(self):
        font = pygame.font.Font(None, 28)

        # Money display
        money_text = font.render(f"Money: ${self.player.money}", True, GREEN)
        self.screen.blit(money_text, (10, 10))

        # Health display
        health_text = font.render(f"Health: {int(self.player.health)}", True, RED)
        self.screen.blit(health_text, (10, 40))

        # Inventory display
        inventory_text = font.render(f"Items: {len(self.player.inventory)}", True, BLUE)
        self.screen.blit(inventory_text, (10, 70))

        # Instructions
        font_small = pygame.font.Font(None, 20)
        instructions = [
            "ARROW KEYS/WASD - Move",
            "SPACE - Interact",
            "ESC - Quit"
        ]
        for i, instruction in enumerate(instructions):
            instr_text = font_small.render(instruction, True, BLACK)
            self.screen.blit(instr_text, (SCREEN_WIDTH - 250, 10 + i * 25))

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)

        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run()
