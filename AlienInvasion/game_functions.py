import pygame
import sys
from bullet import Bullet
from alien import Alien
from time import sleep


def check_events(ai_settings, screen, ship, bullets):
    # Observa eventos de teclado e de mouse.
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, ship, bullets)

        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)


def check_keydown_events(event, ai_settings, screen, ship, bullets):
    """Responde a eventos de pressionamento de teclas e de mouse."""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True

    elif event.key == pygame.K_LEFT:
        ship.moving_left = True

    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, ship, bullets)

    elif event.key == pygame.K_ESCAPE:
        sys.exit()


def check_keyup_events(event, ship):
    """Responde a solturas de tecla."""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False


def update_screen(ai_settings, screen, stats, ship, aliens, bullets, play_button):
    """"Atualiza as imagens na tela e alterna para a nova tela."""
    # Redesenha a tela a cada passagem pelo laço.
    screen.fill(ai_settings.bg_color)

    # Redesenha todos os projéteis atrás da espaçonave e dos alienígenas.
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()
    aliens.draw(screen)

    if not stats.game_active:
        play_button.draw_button()
    # Deixa a tela mais recente visível.
    pygame.display.flip()


def update_bullets(bullets, aliens, ai_settings, screen, ship):
    # Livra-se dos projéteis que desapareceram.
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    bullets.update()

    # Verifica se algum projétil atingiu os alienígenas.
    # Em caso afirmativo, livra-se do projétil e do alienígena.
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)

    # Destrói os projéteis existentes e cria uma nova frota.
    if len(aliens) == 0:
        bullets.empty()
        create_fleet(ai_settings, screen, ship, aliens)


def fire_bullet(ai_settings, screen, ship, bullets):
    # Cria um novo projétil e o adiciona ao grupo de projéteis.
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)


def get_number_rows(ai_settings, ship_height, alien_height):
    """Determina o número de linhas com o número de alienígenas que cabem na tela."""
    available_space_y = (ai_settings.screen_height - (3 * alien_height) - ship_height)
    number_row = int(available_space_y / (2 * alien_height))
    return number_row


def get_number_alien_x(ai_settings, alien_width):
    """Determina o número de alienígenas em uma linha."""
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x


def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    """Cria um alienígena e o posiciona na linha."""
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)


def create_fleet(ai_settings, screen, ship, aliens):
    """Cria uma frota completa de alienígenas."""
    # Cria um alienígena e calcula o número de alienígenas em uma linha.
    # O espaçamento entre os alienígenas é igual à largura de um alienígena.
    alien = Alien(ai_settings, screen)
    number_aliens_x = get_number_alien_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height, alien.rect.height)

    # Cria a primeira linha de alienígenas.
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings, screen, aliens, alien_number, row_number)


def check_fleet_edges(ai_settings, aliens):
    """Responde apropriadamente se algum alienígena alcançou uma borda."""
    for alien in aliens:
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break


def change_fleet_direction(ai_settings, aliens):
    """Faz toda a frota descer e muda a sua direção."""
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1


def ship_hit(ai_settings, stats, screen, ship, aliens, bullets):
    """Responde ao fato da espaçonave ter sido atingida por um alienígena."""
    if stats.ships_left > 0:
        # Decrementa ships_left.
        stats.ships_left -= 1

        # Esvazia a lista de alienígenas e projéteis.
        aliens.empty()
        bullets.empty()

        # Cria uma nova frota e centraliza a espaçonave
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()

        # Faz uma pausa.
        sleep(0.5)

    else:
        stats.game_active = False


def check_aliens_bottom(ai_settings, stats, screen, ship, aliens, bullets):
    """Verifica se algum alienígena alcançou a parte inferior da tela."""
    screen_rect = screen.get_rect()

    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            # Traz esse caso do mesmo modo quando a espaçonave é atingida.
            # Decrementa ships_left.
            stats.ships_left -= 1

            # Esvazia a lista de alienígenas e projéteis.
            aliens.empty()
            bullets.empty()

            # Cria uma nova frota e centraliza a espaçonave
            create_fleet(ai_settings, screen, ship, aliens)
            ship.center_ship()

            # Faz uma pausa.
            sleep(0.5)


def update_aliens(ai_settings, stats, screen, ship, aliens, bullets):
    """Verifica se a frota está em uma das bordas e então
    atualiza as posições de todos os alienígenas da frota."""
    check_fleet_edges(ai_settings, aliens)
    aliens.update()

    # Verifica se houve colisões entre alienígenas e a espaçonave.
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, stats, screen, ship, aliens, bullets)

    # Verifica se há alguma alienígena que atingiu a parte inferior da tela.
    check_aliens_bottom(ai_settings, stats, screen, ship, aliens, bullets)
