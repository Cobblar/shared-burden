import pygame

# single images
mars_img = pygame.image.load("images/mars.png").convert_alpha()
sun_img = pygame.image.load("images/sun.png").convert_alpha()
moon_img = pygame.image.load("images/moon.png").convert_alpha()
asteroid_img = pygame.image.load("images/asteroid.png").convert_alpha()
asteroid_gray_img = pygame.image.load("images/asteroidgray.png").convert_alpha()
terraformer_img = pygame.image.load("images/terraformer.png").convert_alpha()
terraformer_death_img = pygame.image.load("images/terraformer_dead.png").convert_alpha()
# sprite sheets
shield_anim = pygame.image.load("images/animations/shield1big2.png").convert_alpha()
asteroid_poof_anim = pygame.image.load("images/animations/poof1.png").convert_alpha()


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


def mask_from_sheet(sheet, start, size, columns, rows=1):
    """Cut individual frames from a sprite sheet arranged in a grid."""
    masks = []
    for j in range(rows):
        for i in range(columns):
            location = (start[0] + size[0] * i, start[1] + size[1] * j)
            mask = sheet.subsurface(pygame.Rect(location, size))
            mask = pygame.mask.from_surface(mask)
            masks.append(mask)
    return masks


# all snipped sprite sheets
shield_anim_frames = strip_from_sheet(
    shield_anim, (0, 0), (480, 480), columns=5, rows=4
)
asteroid_poof_frames = strip_from_sheet(
    asteroid_poof_anim, (0, 0), (64, 28), columns=9, rows=1
)
shield_anim_mask = mask_from_sheet(shield_anim, (0, 0), (480, 480), columns=5, rows=4)


# animator
class SpriteAnimation(pygame.sprite.Sprite):
    def __init__(self, pos, frames, fps, masks=None, loop=True):
        pygame.sprite.Sprite.__init__(self)
        self.frames = frames
        self.all_mask_frames = masks if masks else []
        self.fps = fps
        self.loop = loop
        self.current_index = 0
        self.mask = masks[self.current_index] if masks else None
        self.time_since_last = 0
        self.frame_duration = 1000 / fps
        self.finished = False
        self.rect = self.frames[0].get_rect()
        self.pos = pos
        self.rect.center = pos
        self.image = self.frames[self.current_index]

    def reset(self):
        self.current_index = 0
        self.time_since_last = 0
        self.finished = False

    def update(self, dt):
        self.rect.center = self.pos

        if self.finished:
            return  # Do nothing if done

        self.time_since_last += dt
        if self.time_since_last >= self.frame_duration:
            self.time_since_last -= self.frame_duration
            self.current_index += 1

            if self.current_index >= len(self.frames):
                if self.loop:
                    self.current_index = 0
                else:
                    self.current_index = len(self.frames) - 1
                    self.finished = True

        # Update image and mask only after fixing current_frame/current_mask
        self.image = self.frames[self.current_index]
        self.mask = self.all_mask_frames[self.current_index]

    def get_current_frame(self):
        return self.frames[self.current_index]

    def get_current_mask(self):
        return self.all_mask_frames[self.current_index]

    def is_done(self):
        return self.finished
