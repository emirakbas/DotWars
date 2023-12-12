import pygame
import random
import math
import tkinter as tk
from tkinter import simpledialog

pygame.init()

# Oyun ekranını oluştur (800x600 piksel)
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("2D Battle Simulator")
clock = pygame.time.Clock()

RADIUS = 10
MAX_SPEED = 2
MAX_HEALTH = 100
BASE_ATTACK_DAMAGE = 0.5
FORMATION_SPACING = 30
ROWS = 2
GAME_OVER = False

# Renk sabitleri
RED_COLOR = pygame.Color("red")
BLUE_COLOR = pygame.Color("blue")
HEALTHY_COLOR = pygame.Color(0, 255, 0)
DAMAGED_COLOR = pygame.Color(255, 0, 0)

class Circle:
    def __init__(self, x, y, color, initial_health):
        self.x = x
        self.y = y
        self.color = color
        self.radius = RADIUS
        self.speed = random.uniform(1, MAX_SPEED)
        self.angle = random.uniform(0, 2 * math.pi)
        self.health = initial_health

    def move_towards_majority(self, other_team):
        average_x = sum(circle.x for circle in other_team) / len(other_team)
        average_y = sum(circle.y for circle in other_team) / len(other_team)
        self.angle = math.atan2(average_y - self.y, average_x - self.x)

    def move(self):
        self.move_towards_majority(RED_TEAM if self.color == BLUE_COLOR else BLUE_TEAM)
        self.x += math.cos(self.angle) * self.speed
        self.y += math.sin(self.angle) * self.speed

        # Ekran sınırlarını kontrol et ve düzelt
        self.x = max(self.radius, min(self.x, SCREEN_WIDTH - self.radius))
        self.y = max(self.radius, min(self.y, SCREEN_HEIGHT - self.radius))

    def check_collision(self, other_circle):
        distance_squared = (self.x - other_circle.x) ** 2 + (self.y - other_circle.y) ** 2
        return distance_squared < (self.radius + other_circle.radius) ** 2

    def resolve_collision(self, other_circle):
        angle = math.atan2(other_circle.y - self.y, other_circle.x - self.x)
        overlap = self.radius + other_circle.radius - math.sqrt((self.x - other_circle.x) ** 2 + (self.y - other_circle.y) ** 2)
        self.x -= math.cos(angle) * overlap / 2
        self.y -= math.sin(angle) * overlap / 2
        other_circle.x += math.cos(angle) * overlap / 2
        other_circle.y += math.sin(angle) * overlap / 2

    def take_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.health = 0

    def is_alive(self):
        return self.health > 0

    def draw(self):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)
        self.draw_health_bar()

    def draw_health_bar(self):
        bar_length = 2 * self.radius
        bar_height = 5
        bar_x = self.x - self.radius
        bar_y = self.y + self.radius + 2
        fill_length = int(bar_length * (self.health / MAX_HEALTH))
        health_color = HEALTHY_COLOR if self.health > 50 else DAMAGED_COLOR
        pygame.draw.rect(screen, health_color, (bar_x, bar_y, fill_length, bar_height))

def initialize_teams():
    global RED_TEAM, BLUE_TEAM
    RED_TEAM = []
    BLUE_TEAM = []

def position_soldiers(red_count, blue_count):
    for i in range(red_count):
        x = random.randint(50, SCREEN_WIDTH // 2 - 50)
        y = random.randint(50, SCREEN_HEIGHT - 50)
        initial_health = random.randint(50, 150)
        RED_TEAM.append(Circle(x, y, RED_COLOR, initial_health))

    for i in range(blue_count):
        x = random.randint(SCREEN_WIDTH // 2 + 50, SCREEN_WIDTH - 50)
        y = random.randint(50, SCREEN_HEIGHT - 50)
        initial_health = random.randint(50, 150)
        BLUE_TEAM.append(Circle(x, y, BLUE_COLOR, initial_health))

def draw_power_balance():
    red_team_power = sum(circle.health for circle in RED_TEAM)
    blue_team_power = sum(circle.health for circle in BLUE_TEAM)
    total_power = red_team_power + blue_team_power

    if total_power > 0:
        red_percentage = red_team_power / total_power
        blue_percentage = blue_team_power / total_power

        bar_length = 300
        bar_height = 20
        red_width = int(bar_length * red_percentage)
        blue_width = int(bar_length * blue_percentage)

        pygame.draw.rect(screen, RED_COLOR, (SCREEN_WIDTH // 2 - bar_length // 2, 10, red_width, bar_height))
        pygame.draw.rect(screen, BLUE_COLOR, (SCREEN_WIDTH // 2 - bar_length // 2 + red_width, 10, blue_width, bar_height))

def draw_team_counters():
    red_count_text = f"Red: {len(RED_TEAM)}"
    blue_count_text = f"Blue: {len(BLUE_TEAM)}"
    font = pygame.font.Font(None, 36)

    red_text_surface = font.render(red_count_text, True, RED_COLOR)
    blue_text_surface = font.render(blue_count_text, True, BLUE_COLOR)

    screen.blit(red_text_surface, (10, SCREEN_HEIGHT - 40))
    screen.blit(blue_text_surface, (SCREEN_WIDTH - 120, SCREEN_HEIGHT - 40))

def draw_fps(fps):
    font = pygame.font.Font(None, 24)
    fps_text = font.render(f"FPS: {fps}", True, (0, 0, 0))
    screen.blit(fps_text, (10, 10))

initialize_teams()

# Kullanıcıdan asker sayılarını ve konumlarını al
root = tk.Tk()
root.withdraw()  # Tkinter penceresini gizle

red_count = simpledialog.askinteger("Input", "Enter the number of red soldiers:", parent=root, minvalue=1)
blue_count = simpledialog.askinteger("Input", "Enter the number of blue soldiers:", parent=root, minvalue=1)

# Askere pozisyon ver
position_soldiers(red_count, blue_count)

while not GAME_OVER:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            GAME_OVER = True

    for circle in RED_TEAM + BLUE_TEAM:
        circle.move()

    for i, red_circle in enumerate(RED_TEAM):
        for j, blue_circle in enumerate(BLUE_TEAM):
            if red_circle.check_collision(blue_circle):
                red_circle.resolve_collision(blue_circle)
                red_circle.take_damage(BASE_ATTACK_DAMAGE)
                blue_circle.take_damage(BASE_ATTACK_DAMAGE)

    for i, red_circle in enumerate(RED_TEAM):
        for j, other_red_circle in enumerate(RED_TEAM[i+1:]):
            if red_circle.check_collision(other_red_circle):
                red_circle.resolve_collision(other_red_circle)

    for i, blue_circle in enumerate(BLUE_TEAM):
        for j, other_blue_circle in enumerate(BLUE_TEAM[i+1:]):
            if blue_circle.check_collision(other_blue_circle):
                blue_circle.resolve_collision(other_blue_circle)

    RED_TEAM = [circle for circle in RED_TEAM if circle.is_alive()]
    BLUE_TEAM = [circle for circle in BLUE_TEAM if circle.is_alive()]

    screen.fill((255, 255, 255))

    draw_power_balance()  # Güç dengesi çubuğunu çiz
    draw_team_counters()  # Takım sayılarını gösteren kutuları çiz
    draw_fps(int(clock.get_fps()))  # FPS göstergesini çiz

    for circle in RED_TEAM + BLUE_TEAM:
        circle.draw()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
