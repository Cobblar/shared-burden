import pygame
from scenemanager import Scene  # Import the base Scene class

# Import other scenes that this scene might transition to directly
from gamemainscene import GameMainScene


class MainMenuScene(Scene):
    """
    Represents the main menu scene of the game.
    """

    def __init__(self, engine):
        """
        Initializes the MainMenuScene.

        Args:
            engine: The DisplayEngine instance.
        """
        super().__init__(engine)
        self.background = "dodgerblue"  # A nice blue color

    def on_draw(self, surface):
        """
        Draws the main menu background.
        """
        surface.fill(self.background)
        # You could add text, buttons, etc. here for the main menu

    def on_event(self, event):
        """
        Handles events specific to the main menu (e.g., starting the game).
        """
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                # Transition to the GameMainScene when SPACE is pressed
                # Note: We instantiate the scene here, passing the engine.
                self.engine.machine.next_scene = GameMainScene(self.engine)
