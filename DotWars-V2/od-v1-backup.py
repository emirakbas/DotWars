import pygame
import random
import math

pygame.init()

# Oyun ekranını oluştur (800x600 piksel)
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("2D Battle Simulator")
clock = pygame.time.Clock()

radius = 10
max_speed = 2
max_health = 100
base_attack_damage = 0.5
formation_spacing = 30
rows = 2
red_count = 50
blue_count = 50
red_team = []
blue_team = []
game_over = False

class Circle:
    def __init__(self, x, y, color, initial_health):
        self.x = x
        self.y = y
        self.color = color
        self.radius = radius
        self.speed = random.uniform(1, max_speed)
        self.angle = random.uniform(0, 2 * math.pi)
        self.health = initial_health

    def move_towards_majority(self, other_team):
        average_x = sum(circle.x for circle in other_team) / len(other_team)
        average_y = sum(circle.y for circle in other_team) / len(other_team)
        self.angle = math.atan2(average_y - self.y, average_x - self.x)

    def move(self):
        self.move_towards_majority(red_team if self.color == "blue" else blue_team)
        self.x += math.cos(self.angle) * self.speed
        self.y += math.sin(self.angle) * self.speed

        # Ekran sınırlarını kontrol et ve düzelt
        self.x = max(self.radius, min(self.x, screen_width - self.radius))
        self.y = max(self.radius, min(self.y, screen_height - self.radius))

    def check_collision(self, other_circle):
        distance = math.sqrt((self.x - other_circle.x) ** 2 + (self.y - other_circle.y) ** 2)
        return distance < self.radius + other_circle.radius

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
        pygame.draw.circle(screen, pygame.Color(self.color), (int(self.x), int(self.y)), self.radius)
        self.draw_health_bar()

    def draw_health_bar(self):
        bar_length = 2 * self.radius
        bar_height = 5
        bar_x = self.x - self.radius
        bar_y = self.y + self.radius + 2
        fill_length = int(bar_length * (self.health / max_health))
        health_color = pygame.Color(0, 255, 0) if self.health > 50 else pygame.Color(255, 0, 0)
        pygame.draw.rect(screen, health_color, (bar_x, bar_y, fill_length, bar_height))

# Kırmızı takımı oluştur
for i in range(red_count):
    x = screen_width // 4
    y = (i % (red_count // rows)) * formation_spacing + formation_spacing
    initial_health = random.randint(50, 150)
    red_team.append(Circle(x, y, "red", initial_health))

# Mavi takımı oluştur
for i in range(blue_count):
    x = screen_width * 3 // 4
    y = (i % (blue_count // rows)) * formation_spacing + formation_spacing
    initial_health = random.randint(50, 150)
    blue_team.append(Circle(x, y, "blue", initial_health))

def draw_power_balance():
    red_team_power = sum(circle.health for circle in red_team)
    blue_team_power = sum(circle.health for circle in blue_team)
    total_power = red_team_power + blue_team_power

    if total_power > 0:
        red_percentage = red_team_power / total_power
        blue_percentage = blue_team_power / total_power

        bar_length = 300
        bar_height = 20
        red_width = int(bar_length * red_percentage)
        blue_width = int(bar_length * blue_percentage)

        pygame.draw.rect(screen, pygame.Color(255, 0, 0), (screen_width // 2 - bar_length // 2, 10, red_width, bar_height))
        pygame.draw.rect(screen, pygame.Color(0, 0, 255), (screen_width // 2 - bar_length // 2 + red_width, 10, blue_width, bar_height))

def draw_team_counters():
    red_count_text = f"Red: {len(red_team)}"
    blue_count_text = f"Blue: {len(blue_team)}"
    font = pygame.font.Font(None, 36)

    red_text_surface = font.render(red_count_text, True, (255, 0, 0))
    blue_text_surface = font.render(blue_count_text, True, (0, 0, 255))

    screen.blit(red_text_surface, (10, screen_height - 40))
    screen.blit(blue_text_surface, (screen_width - 120, screen_height - 40))

while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True

    for circle in red_team + blue_team:
        circle.move()

    for i, red_circle in enumerate(red_team):
        for j, blue_circle in enumerate(blue_team):
            if red_circle.check_collision(blue_circle):
                red_circle.resolve_collision(blue_circle)
                red_circle.take_damage(base_attack_damage)
                blue_circle.take_damage(base_attack_damage)

    for i, red_circle in enumerate(red_team):
        for j, other_red_circle in enumerate(red_team):
            if i != j and red_circle.check_collision(other_red_circle):
                red_circle.resolve_collision(other_red_circle)

    for i, blue_circle in enumerate(blue_team):
        for j, other_blue_circle in enumerate(blue_team):
            if i != j and blue_circle.check_collision(other_blue_circle):
                blue_circle.resolve_collision(other_blue_circle)

    red_team = [circle for circle in red_team if circle.is_alive()]
    blue_team = [circle for circle in blue_team if circle.is_alive()]

    screen.fill((255, 255, 255))

    draw_power_balance()  # Güç dengesi çubuğunu çiz
    draw_team_counters()  # Takım sayılarını gösteren kutuları çiz

    for circle in red_team + blue_team:
        circle.draw()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
