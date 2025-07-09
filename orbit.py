import math


class OrbitingBehavior:
    def __init__(self, central_pos, orbit_radius, orbit_speed, initial_angle=0.0):
        self.central_pos = central_pos
        self.orbit_radius = orbit_radius
        self.orbit_speed = orbit_speed
        self.current_angle = initial_angle

    def get_position(self):
        angle_rad = math.radians(self.current_angle)
        orbit_x = self.central_pos[0] + self.orbit_radius * math.cos(angle_rad)
        orbit_y = self.central_pos[1] + self.orbit_radius * math.sin(angle_rad)
        return int(orbit_x), int(orbit_y)

    def update(self):
        self.current_angle = (self.current_angle + self.orbit_speed) % 360
