import mathsscripts.projectile.moving_2d as moving2d

g = 9.8


class Projectile(moving2d.MovingObject):
    @property
    def force_y(self) -> float:
        force = (super().force_y - (self.mass * g))
        return force
