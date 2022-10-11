import pygame
from settings import Settings
from ship import Ship
import game_functions as gf
from game_stats import GameStats
from pygame.sprite import Group
from button import Button

def run_game():
    # Inicializa o pygame, as configurações e o objeto screen.
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption("Alien Invasion")

    # Cria o botão play.
    play_button = Button(ai_settings, screen, "Play")

    # Cria uma instância para armazenar dados estatísticos do jogo.
    stats = GameStats(ai_settings)

    # Cria uma espaçonave, um grupo de alienígenas e um grupo de balas.
    ship = Ship(ai_settings, screen)
    aliens = Group()
    bullets = Group()

    gf.create_fleet(ai_settings, screen, ship, aliens)
    # Inicia o laço principal do jogo.
    while True:
        gf.check_events(ai_settings, screen, ship, bullets)
        if stats.game_active:
            ship.update()
            gf.update_bullets(bullets, aliens, ai_settings, screen, ship)
            gf.update_aliens(ai_settings, stats, screen, ship, aliens, bullets)

        gf.update_screen(ai_settings, screen, stats, ship, aliens, bullets, play_button)


run_game()
