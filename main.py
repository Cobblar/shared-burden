import pygame
import asyncio  # Needed for asyncio.run to start the async game loop

from scenemanager import DisplayEngine  # Import the adapted DisplayEngine

# Import your game scenes
from menuscenes import MainMenuScene  # Keep if you plan to use it later
from gamemainscene import GameMainScene  # This will be your initial game scene

# Import constants needed for DisplayEngine initialization
from constants import SCREEN_WIDTH, SCREEN_HEIGHT


async def main():
    pygame.init()  # Initialize all Pygame modules

    # Define resolutions for the DisplayEngine (from your original main.py)
    resolutions = [(540, 720), (810, 1080), (1080, 1440)]

    # Create the DisplayEngine instance
    # It now handles the screen setup, scaling, and the main game loop.
    engine = DisplayEngine(
        caption="Terraforming Simulator",  # Set your game's window title
        fps=60,  # Target frames per second
        resolutions=resolutions,  # List of supported screen resolutions
        # Default resolution (index 2 corresponds to 1080x1440)
        default_index=2,
        game_surface_size=(
            SCREEN_WIDTH,
            SCREEN_HEIGHT,
        ),  # The fixed internal resolution for drawing
    )

    await engine.run(GameMainScene(engine))

    pygame.quit()


if __name__ == "__main__":
    # Run the asynchronous main function
    asyncio.run(main())
