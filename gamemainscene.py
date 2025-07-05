import pygame
from scenemanager import Scene  # Import the base Scene class
import asyncio  # Needed for handle_input if it uses async operations

# Import other scenes that this scene might transition to directly
# from menuscenes import MainMenuScene

# Import classes and constants from your original main.py
from classes import Box
from constants import (
    BG_COLOR,
    CONTROL_SURFACE_BG_COLOR,
    CONTROL_SURFACE_HEIGHT,
    CONTROL_SURFACE_WIDTH,
    CONTROL_SURFACE_Y_HEIGHT,
    GREEN_COLOR,
    NODE_SIZE,
    ORANGE_COLOR,
    PURPLE_COLOR,
    RED_COLOR,
    SCREEN_HEIGHT,  # This refers to the fixed internal game surface height
    SCREEN_WIDTH,  # This refers to the fixed internal game surface width
    YELLOW_COLOR,
)

# Assuming handle_input is adapted for DisplayEngine
from controls import handle_input
from selector import selector_func
from sound import load_sound_effects


class GameMainScene(Scene):
    """
    Represents the main gameplay scene, containing all the game logic
    and drawing operations previously in main.py.
    """

    def __init__(self, engine):
        """
        Initializes the GameMainScene, setting up game objects and variables.

        Args:
            engine: The DisplayEngine instance managing the game.
        """
        super().__init__(engine)

        # Clear existing boxes BEFORE creating new ones
        Box.clear_boxes()  # Call this here!

        # Game-specific initializations moved from original main.py
        self.debug_font = pygame.font.Font(None, 30)
        self.sfx = load_sound_effects()

        self.selected_index = 0
        self.selected_box = None  # Will be set to an actual Box object later

        # Initialize Box objects. Box.all_boxes is a class variable.
        # For simplicity, assuming these are created once per game session.
        self.yellow_box = Box(
            "yellow_box",
            YELLOW_COLOR,
            ((CONTROL_SURFACE_WIDTH // 6) * 1),
            CONTROL_SURFACE_HEIGHT / 2,
            NODE_SIZE,
        )
        self.green_box = Box(
            "green_box",
            GREEN_COLOR,
            ((CONTROL_SURFACE_WIDTH // 6) * 2),
            CONTROL_SURFACE_HEIGHT / 2,
            NODE_SIZE,
        )
        self.orange_box = Box(
            "orange_box",
            ORANGE_COLOR,
            ((CONTROL_SURFACE_WIDTH // 6) * 3),
            CONTROL_SURFACE_HEIGHT / 2,
            NODE_SIZE,
        )
        self.purple_box = Box(
            "purple_box",
            PURPLE_COLOR,
            ((CONTROL_SURFACE_WIDTH // 6) * 4),
            CONTROL_SURFACE_HEIGHT / 2,
            NODE_SIZE,
        )
        self.red_box = Box(
            "red_box",
            RED_COLOR,
            ((CONTROL_SURFACE_WIDTH // 6) * 5),
            CONTROL_SURFACE_HEIGHT / 2,
            NODE_SIZE,
        )

        # Control surface for UI elements, drawn at the fixed game_surface_size
        self.control_surface = pygame.Surface(
            (CONTROL_SURFACE_WIDTH, CONTROL_SURFACE_HEIGHT), pygame.SRCALPHA
        )
        print(
            f"GameMainScene initialized. control_surface set: {
                hasattr(self, 'control_surface')
            }"
        )

        # Set initial selected box after all boxes are created
        if Box.all_boxes:
            self.selected_box = Box.all_boxes[self.selected_index]

    def on_event(self, event):
        """
        Handles user input events for the game scene.
        Delegates input handling to the `handle_input` function.
        """
        # handle_input returns (should_continue_running, new_selected_index, new_selected_box)
        # We pass the engine instance so handle_input can manage resolution changes
        # and potentially signal the engine to quit.
        # Removed 'self.engine.resolutions' as it's no longer a direct parameter for handle_input
        should_continue_running, new_selected_index, new_selected_box = handle_input(
            event,
            self.engine,  # Pass the DisplayEngine instance
            self.selected_index,
            self.selected_box,
            self.sfx,
            Box,
        )

        self.selected_index = new_selected_index
        self.selected_box = new_selected_box

        # If handle_input signals to stop, set the engine's running flag to False
        if not should_continue_running:
            self.engine.running = False
            # If you want to transition to another scene on quit (e.g., MainMenuScene)
            # self.engine.machine.next_scene = MainMenuScene(self.engine)

    def on_update(self, delta):
        """
        Handles game logic updates for the scene.
        `delta` is the time elapsed since the last frame in milliseconds.
        """
        # Update selected_box based on selected_index, ensuring it's valid
        if Box.all_boxes and 0 <= self.selected_index < len(Box.all_boxes):
            self.selected_box = Box.all_boxes[self.selected_index]
        else:
            self.selected_box = None  # Or handle error/default

    def on_draw(self, game_surface):
        """
        Handles drawing operations for the game scene onto the game_surface.
        """
        # Fill the background of the internal game_surface
        game_surface.fill(BG_COLOR)
        self.control_surface.fill(CONTROL_SURFACE_BG_COLOR)

        # Draw all boxes onto the control_surface
        for box in Box.all_boxes:
            pygame.draw.rect(
                self.control_surface,
                box.color,
                box.rect,
            )

        # Draw the selector around the selected box
        if self.selected_box:  # Ensure selected_box is valid before drawing selector
            selector_func(
                self.control_surface, self.selected_box.x, self.selected_box.y
            )

        # Display debug information on game_surface
        debug_display_string = (
            f"selected_box: {self.selected_box.name if self.selected_box else 'None'}"
        )
        text_surface = self.debug_font.render(debug_display_string, True, (0, 200, 0))
        game_surface.blit(text_surface, (10, 10))

        # BLIT control_surface ONTO game_surface (at the specified Y height)
        game_surface.blit(self.control_surface, (0, CONTROL_SURFACE_Y_HEIGHT))

        # The engine's blit_scaled() and pygame.display.flip() are handled by DisplayEngine.loop()
