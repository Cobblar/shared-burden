import math


class OrbitingBehavior:
    def __init__(
        self,
        central_pos,
        orbit_radius,
        orbit_speed,
        initial_angle=0.0,
        tidal_lock=False,
        tidal_lock_offset=0.0,
    ):
        self.central_pos = central_pos
        self.orbit_radius = orbit_radius
        self.orbit_speed = orbit_speed
        self.current_angle = initial_angle
        self.tidal_lock = tidal_lock
        self.tidal_lock_offset = tidal_lock_offset

    def update(self):
        self.current_angle = (self.current_angle + self.orbit_speed) % 360

    def get_tidal_lock_angle(self):
        return -self.current_angle + self.tidal_lock_offset

    def get_position(self):
        angle_rad = math.radians(self.current_angle)
        orbit_x = self.central_pos[0] + self.orbit_radius * math.cos(angle_rad)
        orbit_y = self.central_pos[1] + self.orbit_radius * math.sin(angle_rad)
        return int(orbit_x), int(orbit_y)

    def get_facing_angle(self, orbit_pos):
        dx = self.central_pos[0] - orbit_pos[0]
        dy = self.central_pos[1] - orbit_pos[1]
        angle_rad = math.atan2(-dy, dx)
        return math.degrees(angle_rad)
