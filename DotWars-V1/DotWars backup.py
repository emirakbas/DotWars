import pygame
import json
import os
import start_game

# Oyun ekranının boyutları
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080

# Renkler
WHITE = (255, 255, 255)
BLUE = (0, 102, 204)
RED = (204, 0, 0)
GREEN = (0, 204, 102)
BLACK = (0, 0, 0)

def ask_confirmation(screen, message):
    font = pygame.font.Font(None, 36)
    text = font.render(message, True, WHITE)
    text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))

    confirmation_box_width = 590
    confirmation_box_height = 250
    confirmation_box_rect = pygame.Rect(
        (SCREEN_WIDTH - confirmation_box_width) // 2,
        (SCREEN_HEIGHT - confirmation_box_height) // 2,
        confirmation_box_width,
        confirmation_box_height
    )

    # Yarı saydam siyah bir kutu çiz
    confirmation_surface = pygame.Surface((confirmation_box_width, confirmation_box_height), pygame.SRCALPHA)
    pygame.draw.rect(confirmation_surface, (128, 1, 1, 255), confirmation_surface.get_rect(), border_radius=10)
    screen.blit(confirmation_surface, confirmation_box_rect.topleft)

    yes_button_rect = pygame.Rect(
        confirmation_box_rect.centerx - 80,
        confirmation_box_rect.centery + 50,
        100,
        50
    )
    no_button_rect = pygame.Rect(
        confirmation_box_rect.centerx + 30,
        confirmation_box_rect.centery + 50,
        100,
        50
    )

    while True:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if yes_button_rect.collidepoint(event.pos):
                    return True
                elif no_button_rect.collidepoint(event.pos):
                    return False
                
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        screen.blit(confirmation_surface, confirmation_box_rect.topleft)
        screen.blit(text, text_rect)

        pygame.draw.rect(screen, GREEN, yes_button_rect, border_radius=10)
        yes_text = font.render("Evet", True, WHITE)
        yes_text_rect = yes_text.get_rect(center=yes_button_rect.center)
        screen.blit(yes_text, yes_text_rect)

        pygame.draw.rect(screen, RED, no_button_rect, border_radius=10)
        no_text = font.render("Hayır", True, WHITE)
        no_text_rect = no_text.get_rect(center=no_button_rect.center)
        screen.blit(no_text, no_text_rect)

        pygame.display.flip()
# Ana menüyü gösteren fonksiyon
def show_main_menu(screen):
    background = pygame.image.load("background.jpg")
    background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))

    font = pygame.font.Font(None, 48)
    title_text = font.render("DOT WARS", True, BLUE)

    title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3))

    start_button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 25, 200, 50)
    settings_button_rect = start_button_rect.move(0, 75)
    exit_button_rect = settings_button_rect.move(0, 75)  # Çıkış butonu

    buttons = [
        {"rect": start_button_rect, "text": "Başlat", "action": "start_game"},
        {"rect": settings_button_rect, "text": "Ayarlar", "action": "ayarlar"},
        {"rect": exit_button_rect, "text": "Çıkış", "action": "exit_confirmation"}
    ]

    is_hovered = [False, False, False]
    is_clicked = [False, False, False]

    while True:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                for button in buttons:
                    if button["rect"].collidepoint(event.pos):
                        if button["action"] == "start_game":
                            import start_game
                            start_game.start_game()
                            return  # Oyun ekranından çıkarak ana menüye geri dön

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        screen.blit(background, (0, 0))
        screen.blit(title_text, title_rect)

        for button in buttons:
            rect = button["rect"]
            text = font.render(button["text"], True, WHITE)
            text_rect = text.get_rect(center=rect.center)

            if rect.collidepoint(pygame.mouse.get_pos()):
                is_hovered[buttons.index(button)] = True
                pygame.draw.rect(screen, RED, rect, border_radius=10)
            else:
                is_hovered[buttons.index(button)] = False
                pygame.draw.rect(screen, GREEN, rect, border_radius=10)

            if is_clicked[buttons.index(button)]:
                if button["action"] == "exit_confirmation":
                    return handle_exit_confirmation(screen)  # Özel fonksiyonu çağır
                else:
                    return button["action"]

            screen.blit(text, text_rect)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                for button in buttons:
                    if button["rect"].collidepoint(event.pos):
                        is_clicked[buttons.index(button)] = True
            if event.type == pygame.MOUSEBUTTONUP:
                for i in range(len(is_clicked)):
                    is_clicked[i] = False  # Tüm tıklamaları sıfırla

# Ayarların tutulacağı dosya
SETTINGS_FILE = "settings.json"

# Ayarları yükle
def load_settings():
    try:
        with open(SETTINGS_FILE, "r") as file:
            settings = json.load(file)
            return settings
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

# Ayarları kaydet
def save_settings(settings):
    with open(SETTINGS_FILE, "w") as file:
        json.dump(settings, file)

#Ayarlar yazısını gösterme fonksiyonu
        
def draw_settings_text(screen, font, settings, panel_rect):
    checkbox_x = panel_rect.left + 50
    checkbox_y = panel_rect.centery - 20
    text_x = checkbox_x + 30
    text_y = checkbox_y - 5

    checkbox_rect = pygame.Rect(checkbox_x, checkbox_y, 20, 20)

    fullscreen_text = font.render("Tam Ekran", True, WHITE)
    screen.blit(fullscreen_text, (text_x, text_y))

    music_text = font.render("Menü Müziği", True, WHITE)  # Yeni seçeneğin yazısı
    screen.blit(music_text, (text_x, text_y + 40))  # Yeni seçeneği biraz aşağı kaydırın

    # "Tam Ekran" yazısı çizdir
    fullscreen_text = font.render("Tam Ekran", True, WHITE)
    fullscreen_text_rect = fullscreen_text.get_rect(topleft=(text_x, text_y))  # Yazının sol üst köşesini belirle
    screen.blit(fullscreen_text, fullscreen_text_rect)

# Ayarlar ekranını gösterme fonksiyonu
def show_settings(screen):
    background = pygame.image.load("background.jpg")
    background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))

    font = pygame.font.Font(None, 48)
    settings_title = font.render("Ayarlar", True, RED)

    title_rect = settings_title.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 6))

    panel_width = 1100
    panel_height = 730
    panel_rect = pygame.Rect(
        (SCREEN_WIDTH - panel_width) // 2,
        (SCREEN_HEIGHT - panel_height) // 1.5,
        panel_width,
        panel_height
    )

    settings_panel_surface = pygame.Surface((panel_width, panel_height), pygame.SRCALPHA)
    pygame.draw.rect(settings_panel_surface, (190, 1, 1, 240), settings_panel_surface.get_rect(), border_radius=30)
    screen.blit(settings_panel_surface, panel_rect.topleft)

    back_button_rect = pygame.Rect(20, SCREEN_HEIGHT - 70, 100, 50)
    fullscreen_checkbox_rect = pygame.Rect(panel_rect.left + 50, panel_rect.centery - 20, 20, 20)

    button_color = RED
    button_original_size = back_button_rect.size

    is_hovered = False
    is_clicked = False

    settings = load_settings()
    fullscreen = settings.get("fullscreen", False)
    music = settings.get("music", False)

    screen.blit(background, (0, 0))

    pygame.display.flip()

    music_checkbox_rect = pygame.Rect(panel_rect.left + 50, panel_rect.centery + 20, 20, 20)
    music_text_rect = music_checkbox_rect.move(30, -5)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_button_rect.collidepoint(event.pos):
                    is_clicked = True
                elif fullscreen_checkbox_rect.collidepoint(event.pos):
                    fullscreen = not fullscreen
                    settings["fullscreen"] = fullscreen
                    save_settings(settings)
                    if fullscreen:
                        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
                    else:
                        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

 
                elif music_checkbox_rect.collidepoint(event.pos):
                    music = not music
                    settings["music"] = music
                    save_settings(settings)
                    if music:
                        pygame.mixer.music.load("C:/Users/lastg/Masaüstü/DotWars/music/1-603711__retykristof__respect-orchestral-music_1.mp3")
                        pygame.mixer.music.set_volume(0.5)
                        pygame.mixer.music.play(-1)
                    else:
                        pygame.mixer.music.stop()

            if event.type == pygame.MOUSEMOTION:
                if back_button_rect.collidepoint(event.pos):
                    is_hovered = True
                else:
                    is_hovered = False
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        screen.blit(background, (0, 0))
        screen.blit(settings_title, title_rect)
        screen.blit(settings_panel_surface, panel_rect.topleft)

        if is_clicked:
            return "ana_menu"

        if is_hovered:
            button_color = (255, 0, 0)
            back_button_rect.width = button_original_size[0] + 5
            back_button_rect.height = button_original_size[1] + 5
        else:
            button_color = RED
            back_button_rect.size = button_original_size
        pygame.draw.rect(screen, button_color, back_button_rect, border_radius=10)
        button_text = font.render("Geri", True, WHITE)
        button_text_rect = button_text.get_rect(center=back_button_rect.center)
        screen.blit(button_text, button_text_rect)

        draw_settings_text(screen, font, settings, panel_rect)

        pygame.draw.rect(screen, WHITE, music_checkbox_rect, border_radius=5)
        if music:
            pygame.draw.line(screen, BLUE, (music_checkbox_rect.left + 2, music_checkbox_rect.centery), (music_checkbox_rect.right - 2, music_checkbox_rect.centery), 4)
            pygame.draw.line(screen, BLUE, (music_checkbox_rect.centerx, music_checkbox_rect.top + 2), (music_checkbox_rect.centerx, music_checkbox_rect.bottom - 2), 4)

        pygame.draw.rect(screen, WHITE, fullscreen_checkbox_rect, border_radius=5)
        if fullscreen:
            pygame.draw.line(screen, BLUE, (fullscreen_checkbox_rect.left + 2, fullscreen_checkbox_rect.centery), (fullscreen_checkbox_rect.right - 2, fullscreen_checkbox_rect.centery), 4)
            pygame.draw.line(screen, BLUE, (fullscreen_checkbox_rect.centerx, fullscreen_checkbox_rect.top + 2), (fullscreen_checkbox_rect.centerx, fullscreen_checkbox_rect.bottom - 2), 4)

        pygame.display.flip()
        
# "Çıkış Onayı" ekranını yöneten özel fonksiyon
def handle_exit_confirmation(screen):
    confirmation_message = "Oyundan çıkmak istediğinize emin misiniz?"
    confirm_exit = ask_confirmation(screen, confirmation_message)
    if confirm_exit:
        pygame.quit()
        exit()
    else:
        return "ana_menu"  # Hayır'a tıklanınca ana menüye dön

# Oyun başlatma
if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("DOT WARS")

    # Ayarları yükle
    settings = load_settings()

    # Müziği yükleyin ve başlatın (sadece ayarlarda müzik seçiliyse)
    pygame.mixer.init()
    if settings.get("music", False):
        pygame.mixer.music.load("C:/Users/lastg/Masaüstü/DotWars/music/1-603711__retykristof__respect-orchestral-music_1.mp3")  # Menü müziği dosyasının adını değiştirin
        pygame.mixer.music.set_volume(0.5)  # Müzik ses seviyesi
        pygame.mixer.music.play(-1)  # Başlangıçta müziği çal

    current_screen = "ana_menu"

    while True:
        if current_screen == "ana_menu":
            current_screen = show_main_menu(screen)
        elif current_screen == "ayarlar":
            current_screen = show_settings(screen)
            
# ARAYÜZ SONU #