import pygame

# single images
mars_img = pygame.image.load("images/mars.png")
sun_img = pygame.image.load("images/sun.png")
moon_img = pygame.image.load("images/moon.png")
# sprite sheets
shield_anim = pygame.image.load("images/animations/shield1big.png")


def center_finder_height(image):
    return pygame.Surface.get_rect(image).height / 2


def center_finder_width(image):
    return pygame.Surface.get_rect(image).width / 2


mars_half_y = center_finder_height(mars_img)
mars_half_x = center_finder_width(mars_img)

# animation logic


# sprite snipper
def strip_from_sheet(sheet, start, size, columns, rows=1):
    """Cut individual frames from a sprite sheet arranged in a grid."""
    frames = []
    for j in range(rows):
        for i in range(columns):
            location = (start[0] + size[0] * i, start[1] + size[1] * j)
            frame = sheet.subsurface(pygame.Rect(location, size))
            frames.append(frame)
    return frames


# all snipped sprite sheets
shield_anim_frames = strip_from_sheet(
    shield_anim, (0, 0), (480, 480), columns=5, rows=4
)


# animator
class SpriteAnimation:
    def __init__(self, frames, fps, loop=True):
        self.frames = frames
        self.fps = fps
        self.loop = loop
        self.current_frame = 0
        self.time_since_last = 0
        self.frame_duration = 1000 / fps
        self.finished = False

    def reset(self):
        self.current_frame = 0
        self.time_since_last = 0
        self.finished = False

    def update(self, dt):
        if self.finished:
            return  # Do nothing if done

        self.time_since_last += dt
        if self.time_since_last >= self.frame_duration:
            self.time_since_last -= self.frame_duration
            self.current_frame += 1

            if self.current_frame >= len(self.frames):
                if self.loop:
                    self.current_frame = 0
                else:
                    self.current_frame = len(self.frames) - 1  # stay on last frame
                    self.finished = True

    def get_current_frame(self):
        return self.frames[self.current_frame]
