import numpy as np
import math

from util import orthon
from primitive import Object2D, PlanarObject, Line, Circle, ArcPath


class CutoutRect(PlanarObject):

    data_to_local_coords = ['size']

    def __init__(self, size, layer='cut'):
        super(CutoutRect, self).__init__(layer)

        self.size = np.array(size)

    def render(self, config):

        displace = config.cutting_width / 2
        width, height = self.size

        l = []

        l.append(Line(np.array([displace,         displace]),          np.array([width - displace, displace])))
        l.append(Line(np.array([width - displace, displace]),          np.array([width - displace, height - displace])))
        l.append(Line(np.array([width - displace, height - displace]), np.array([displace,         height - displace])))
        l.append(Line(np.array([displace,         height - displace]), np.array([displace,         displace])))

        return Object2D(l, self.layer)

class CutoutRoundedRect(PlanarObject):

    data_to_local_coords = ['size']

    def __init__(self, size, radius, layer='cut'):
        super(CutoutRoundedRect, self).__init__(layer)

        self.size = np.array(size)
        self.radius = radius

    def render(self, config):

        displace = config.cutting_width / 2
        width, height = self.size
        radius = self.radius

        assert(width >= 2*radius)
        assert(height >= 2*radius)

        l = []

        l.append(Line(np.array([displace + radius, displace]), np.array([width - radius - displace, displace])))
        l.append(ArcPath(np.array([width - radius - displace, displace]), np.array([width - - displace, radius + displace]), radius, False, False))
        l.append(Line(np.array([width - displace, radius + displace]), np.array([width - displace, height - radius - displace])))
        l.append(ArcPath(np.array([width - displace, height - radius - displace]), np.array([width - radius - displace, height - displace]), radius, False, False))
        l.append(Line(np.array([width - radius - displace, height - displace]), np.array([radius + displace, height - displace])))
        l.append(ArcPath(np.array([radius + displace, height - displace]), np.array([displace, height - radius - displace]), radius, False, False))
        l.append(Line(np.array([displace, height - radius - displace]), np.array([displace, radius + displace])))
        l.append(ArcPath(np.array([displace, radius + displace]), np.array([displace + radius, displace]), radius, False, False))

        return Object2D(l, self.layer)

class HexBoltCutout(PlanarObject):
    def __init__(self, width, layer='cut'):
        super(HexBoltCutout, self).__init__(layer)

        self.width = width

    def render(self, config):
        displace = config.cutting_width / 2
        radius = 2 * self.width / math.sqrt(3)

        y_pos = self.width - displace
        x_pos = radius/2 - (displace / math.sqrt(3))

        hor_x_pos = radius - (2 * displace / math.sqrt(3))

        corners = [
                np.array([-x_pos,  y_pos]),
                np.array([ x_pos,  y_pos]),
                np.array([ hor_x_pos, 0]),
                np.array([ x_pos, -y_pos]),
                np.array([-x_pos, -y_pos]),
                np.array([-hor_x_pos, 0]),

                np.array([-x_pos,  y_pos]),
            ]
        return Object2D([Line(a,b) for a,b in zip(corners, corners[1:])], self.layer)

class CircleCutout(PlanarObject):
    def __init__(self, radius, layer='cut'):
        super(CircleCutout, self).__init__(layer)

        self.radius = radius

    def render(self, config):
        displace = config.cutting_width / 2

        return Object2D([Circle(0, self.radius - displace)], self.layer)

class MountingScrewCutout(PlanarObject):

    data_to_local_coords = ['shaft_dir']

    def __init__(self, radius_head, radius_shaft, shaft_length, shaft_dir, layer='cut'):
        super(MountingScrewCutout, self).__init__(layer)

        assert(radius_head >= radius_shaft)

        self.radius_head = radius_head
        self.radius_shaft = radius_shaft
        self.shaft_length = shaft_length
        self.shaft_dir = np.array(shaft_dir)

    def render(self, config):
        displace = config.cutting_width / 2

        on = orthon(self.shaft_dir)
        rh = self.radius_head - displace
        rs = (self.radius_shaft - displace)

        shaft_straight_endpoint = (self.shaft_length - math.sqrt(rh*rh - rs*rs)) * self.shaft_dir

        l = []
        l.append(ArcPath(rs * (-on), rs * on, rs))
        l.append(Line(rs * on, rs * on + shaft_straight_endpoint))
        l.append(ArcPath(rs * on + shaft_straight_endpoint, rs * (-on) + shaft_straight_endpoint, rh))
        l.append(Line(rs * (-on) + shaft_straight_endpoint, rs * (-on)))

        return Object2D(l, self.layer)

class FanCutout(PlanarObject):

    # TODO only 40mm size verified
    dimensions = {
            # (main diameter, mounting hole diameter, mounting hole displace)
            40:  ( 38, 4, 3.5),
            60:  ( 58, 4, 4.0),
            70:  ( 68, 4, 4.0),
            80:  ( 76, 4, 4.5),
            92:  ( 89, 4, 5.0),
            120: (117, 4, 7.0),
        }

    def __init__(self, size, layer='cut'):
        super(FanCutout, self).__init__(layer)

        assert(size in self.dimensions)
        self.size = size

    def render(self, config):
        displace = config.cutting_width / 2

        main_dia, mounting_hole_dia, mounting_hole_displace = self.dimensions[self.size]

        main_radius = main_dia / 2
        mounting_hole_radius = mounting_hole_dia / 2
        mounting_position = self.size / 2 - mounting_hole_displace

        l = []
        l.append(Circle(0, main_radius - displace))
        l.append(Circle(np.array([ mounting_position,  mounting_position]), mounting_hole_radius - displace))
        l.append(Circle(np.array([-mounting_position,  mounting_position]), mounting_hole_radius - displace))
        l.append(Circle(np.array([ mounting_position, -mounting_position]), mounting_hole_radius - displace))
        l.append(Circle(np.array([-mounting_position, -mounting_position]), mounting_hole_radius - displace))

        return Object2D(l, self.layer)

class AirVentsCutout(PlanarObject):

    data_to_local_coords = ['size']

    # TODO make more configurable
    def __init__(self, size, layer='cut'):
        super(AirVentsCutout, self).__init__(layer)

        self.size = np.array(size)

    def render(self, config):

        displace = config.cutting_width / 2
        width, height = self.size

        short_count = int(math.ceil((width + 5) / (5+5)))
        short_length = (width + 5) / short_count

        long_count = int(math.ceil((height + 5) / (30+5)))
        long_length = (height + 5) / long_count

        short_positions = [(i*short_length, (i+1)*short_length-5) for i in range(short_count)]
        long_positions = [(i*long_length, (i+1)*long_length-5) for i in range(long_count)]

        l = []

        for x1, x2 in short_positions:
            for y1, y2 in long_positions:

                l.append(Line(np.array([x1 + displace, y1 + displace]), np.array([x2 - displace, y1 + displace])))
                l.append(Line(np.array([x2 - displace, y1 + displace]), np.array([x2 - displace, y2 - displace])))
                l.append(Line(np.array([x2 - displace, y2 - displace]), np.array([x1 + displace, y2 - displace])))
                l.append(Line(np.array([x1 + displace, y2 - displace]), np.array([x1 + displace, y1 + displace])))

        return Object2D(l, self.layer)

    @staticmethod
    def _render_rectangle(pos, size):
        pass
