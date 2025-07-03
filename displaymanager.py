import pygame


class DisplayManager:
    def __init__(self, resolutions, default_index=0, game_surface_size=(800, 600)):
        """
        resolutions: list of (width, height) tuples for window sizes
        default_index: which resolution to start with
        game_surface_size: fixed surface size for game rendering
        """
        self.resolutions = resolutions
        self.current_index = default_index
        self.game_surface_size = game_surface_size

        self.current_resolution = resolutions[default_index]
        self.screen = pygame.display.set_mode(self.current_resolution)
        self.game_surface = pygame.Surface(game_surface_size)

    def switch_resolution(self, index):
        if 0 <= index < len(self.resolutions):
            self.current_index = index
            self.current_resolution = self.resolutions[index]
            self.screen = pygame.display.set_mode(self.current_resolution)

    def get_game_surface(self):
        return self.game_surface

    def get_screen(self):
        return self.screen

    def blit_scaled(self):
        scaled = pygame.transform.smoothscale(
            self.game_surface, self.current_resolution
        )
        self.screen.blit(scaled, (0, 0))

    def get_current_resolution(self):
        return self.current_resolution
