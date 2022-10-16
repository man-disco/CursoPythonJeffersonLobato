import pygame.font


class Scoreboard:
    """Uma classe para mostrar informações sobre a pontuação do jogo."""
    def __init__(self, ai_settings, screen, stats):
        """Inicializa os atributos da pontuação."""
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.ai_settings = ai_settings
        self.stats = stats

        # Configurações de fonte para as informações de pontuação.
        self.text_color = (30, 30, 30)
        self.font = pygame.font.SysFont("None", 48)

        # Prepara as imagens das pontuações na tela.
        self.prep_score()
        self.prep_high_score()

    def prep_score(self):
        """Transforma a pontuação em uma imagem renderizada."""
        rounded_score = int(round(self.stats.score, -1))
        score_str = "{:,}".format(rounded_score)
        self.score_image = self.font.render("Pontuação:  " + score_str, True, self.text_color, self.ai_settings.bg_color)

        # Exibe a pontuação na parte superior direita da tela.
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def prep_high_score(self):
        """Transforma a pontuação máxima em uma imagem renderizada."""
        high_score = int(round(self.stats.high_score, -1))
        high_score_str = "{:,}".format(high_score)
        self.high_score_image = self.font.render("Recorde:  " + high_score_str, True, self.text_color, self.ai_settings.bg_color)

        # Centraliza a pontuação máxima na parte superior da tela.
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.left = self.screen_rect.left + 20
        self.high_score_rect.top = self.score_rect.top

    def show_score(self):
        """Desenha a pontuação na tela."""
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)

