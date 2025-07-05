import pygame
import asyncio  # Added for async game loop


# Base class for all game scenes
class Scene:
    """
    Base class for all game scenes.
    Subclasses should override on_draw, on_event, and on_update methods.
    """

    def __init__(self, engine):
        """
        Initializes the Scene with a reference to the DisplayEngine.

        Args:
            engine: The DisplayEngine instance managing the game.
        """
        self.engine = engine

    def on_draw(self, surface):
        """
        Handles drawing operations for the scene.
        This method should be overridden by subclasses.

        Args:
            surface: The Pygame display surface to draw on.
        """
        pass

    def on_event(self, event):
        """
        Handles user input events for the scene.
        This method should be overridden by subclasses.

        Args:
            event: A Pygame event object.
        """
        pass

    def on_update(self, delta):
        """
        Handles game logic updates for the scene.
        This method should be overridden by subclasses.

        Args:
            delta: Time elapsed since the last frame in milliseconds.
        """
        pass


# Manages transitions between different scenes
class Machine:
    """
    Manages the current and next game scenes, facilitating transitions.
    """

    def __init__(self):
        """
        Initializes the Machine with no current or pending next scene.
        """
        self.current_scene = None
        self.next_scene = None

    def update(self):
        """
        Checks if a scene transition is pending and updates the current scene.
        This method is called once per game loop iteration.
        """
        if self.next_scene:
            self.current_scene = self.next_scene
            self.next_scene = None


# The main game engine, handling the game loop and display
class DisplayEngine:
    """
    The main game engine, responsible for the game loop, display management,
    and integrating with the Scene Machine.
    """

    def __init__(
        self, caption, fps, resolutions, default_index, game_surface_size, flags=0
    ):
        """
        Initializes the DisplayEngine.

        Args:
            caption (str): The title of the game window.
            fps (int): The target frames per second.
            resolutions (list): A list of (width, height) tuples for screen resolutions.
            default_index (int): The index of the default resolution in the resolutions list.
            game_surface_size (tuple): The fixed internal game surface size (e.g., (SCREEN_WIDTH, SCREEN_HEIGHT)).
            flags (int, optional): Pygame display flags. Defaults to 0.
        """
        pygame.display.set_caption(caption)
        self.flags = flags
        self.resolutions = resolutions
        self.current_resolution_index = default_index
        self.game_surface_size = game_surface_size

        # The internal surface where all game elements are drawn at a fixed size
        self._game_surface = pygame.Surface(self.game_surface_size)

        # The actual display screen, which will be scaled
        self._screen = pygame.display.set_mode(
            self.resolutions[self.current_resolution_index], self.flags
        )
        self.rect = self._screen.get_rect()  # Rect of the actual screen

        self.clock = pygame.time.Clock()
        self.running = True
        self.delta = 0  # Time elapsed since last frame
        self.fps = fps

        self.machine = Machine()  # Instance of the scene manager

    def get_game_surface(self):
        """Returns the internal game surface where game elements are drawn."""
        return self._game_surface

    def get_screen(self):
        """Returns the actual Pygame display screen surface."""
        return self._screen

    def set_resolution(self, index):
        """
        Changes the display resolution of the actual screen.

        Args:
            index (int): The index of the desired resolution in the resolutions list.

        Returns:
            bool: True if resolution was successfully set, False otherwise.
        """
        if 0 <= index < len(self.resolutions):
            self.current_resolution_index = index
            self._screen = pygame.display.set_mode(
                self.resolutions[self.current_resolution_index], self.flags
            )
            self.rect = self._screen.get_rect()  # Update screen rect
            return True
        return False

    def blit_scaled(self):
        # Scales the internal game_surface to fit the current screen resolution and blits it onto the actual screen.
        screen_width, screen_height = self._screen.get_size()
        scaled_game_surface = pygame.transform.scale(
            self._game_surface, (screen_width, screen_height)
        )
        self._screen.blit(
            scaled_game_surface, (0, 0)
        )  # Blit directly to fill the screen

    async def loop(self):
        """
        The main game loop. Handles event processing, scene drawing,
        scene updates, and display refreshing.
        """
        while self.running:
            # Update the scene machine to handle any pending scene transitions
            self.machine.update()

            # Process Pygame events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False  # Exit the loop if the user closes the window
                else:
                    # Pass the event to the current scene for handling
                    self.machine.current_scene.on_event(event)

            # Draw the current scene onto the internal game_surface
            self.machine.current_scene.on_draw(self._game_surface)

            # Update the current scene's game logic
            self.machine.current_scene.on_update(self.delta)

            # Scale and blit the internal game surface to the actual screen
            self.blit_scaled()

            # Update the full display Surface to the screen
            pygame.display.flip()

            # Control the frame rate and get the delta time
            self.delta = self.clock.tick(self.fps)
            # Yield control to asyncio for Pygbag compatibility
            await asyncio.sleep(0)

    async def run(self, initial_scene):  # The run method is now async
        """
        Starts the game loop with a specified initial scene.

        Args:
            initial_scene (Scene): The first scene to load and run.
        """
        self.machine.current_scene = initial_scene
        await self.loop()  # Await the async loop
