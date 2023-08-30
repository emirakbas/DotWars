# start_game.py

import pygame
# Oyun ekranının boyutları
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080

# Renkler
BLACK = (20, 0, 0)

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("DOT WARS - Oyun")

    # Oyunun devamını işleyen kodu buraya yerleştirin
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        # Ekranı siyah renkle doldur
        screen.fill(BLACK)

        # Diğer oyun işlemleri buraya gelecek

        pygame.display.flip()

if __name__ == "__main__":
    main()
