#!/usr/bin/python3

import codecs
import numpy as np

from lasergen.primitive import ArcPath
from lasergen.planar import HexBoltCutout, CircleCutout, MountingScrewCutout, FanCutout, CutoutRoundedRect, AirVentsCutout, CutoutRect
from lasergen.planar import RectEdgeCutout, RoundedRectEdgeCutout
from lasergen.wall import ToplessWall, ExtendedWall, SubWall
from lasergen.edge import CutoutEdge, Edge, EDGE_STYLE, EDGE_ELEMENT_STYLE
from lasergen.config import Config
from lasergen.export import place_2d_objects, export_svg_with_paths, export_box_openscad
from lasergen.layer import Layer
from lasergen.util import DIR, DIR2
from lasergen.units import Rel, Frac
from lasergen.box import ClosedBox, ToplessBox

def main():
    c = Config(6., 10., 3., 3., 0)
    c.colors['cutout'] = 'grey'

    cb = ClosedBox(None, 180, 60, name='RootBox')
    left, middle, right = cb.subdivide(DIR.RIGHT, [
            (80, 'LeftBox'),
            (300, 'MiddleBox'),
            (80, 'RightBox'),
        ])

    left_cable, _ = right.subdivide(DIR.RIGHT, [Rel(1), Rel(1)])

    powersup, highv_half = left.subdivide(DIR.UP, [100, Rel(1)], ['Powersup', 'HighV'])
    highv, status = highv_half.subdivide(DIR.FRONT, [Rel(1), 23])
    #_, status = highv_half.subdivide(DIR.FRONT, [Rel(1), 12])

    _, ledh, _ = status.subdivide(DIR.UP, [Rel(1), 45, Rel(1)])
    _, led, _ = ledh.subdivide(DIR.RIGHT, [Rel(1), 45, Rel(1)])

    cb.configure(c)

    # configure the center backwall
    bw = middle.get_wall_by_direction(DIR.BACK)
    bw.add_child(MountingScrewCutout(6.5, 3, 20, DIR.DOWN), [20,Frac(1)-20,0])
    bw.add_child(MountingScrewCutout(6.5, 3, 20, DIR.DOWN), [20,40,0])
    bw.add_child(MountingScrewCutout(6.5, 3, 20, DIR.DOWN), [Frac(1)-20,Frac(1)-20,0])
    bw.add_child(MountingScrewCutout(6.5, 3, 20, DIR.DOWN), [Frac(1)-20,40,0])

    # add pcb outlines for reference
    bw.add_child(CutoutRect([80, 100], center=DIR.UP, layer=Layer('info')), [50, Frac(0.5), 0])
    bw.add_child(CutoutRect([100, 50], center=DIR.UP, layer=Layer('info')), [150, Frac(1) - (25+30), 0])
    bw.add_child(CutoutRect([100, 50], center=DIR.UP, layer=Layer('info')), [150, 25+30, 0])

    # no edge cutouts in the front wall
    middle.get_wall_by_direction(DIR.LEFT).get_edge_by_direction(DIR.FRONT).set_style(EDGE_ELEMENT_STYLE.FLAT)
    middle.get_wall_by_direction(DIR.RIGHT).get_edge_by_direction(DIR.FRONT).set_style(EDGE_ELEMENT_STYLE.FLAT)
    highv_half.get_wall_by_direction(DIR.DOWN).get_edge_by_direction(DIR.FRONT).set_style(EDGE_ELEMENT_STYLE.FLAT)
    ledh.get_wall_by_direction(DIR.UP).get_edge_by_direction(DIR.FRONT).set_style(EDGE_ELEMENT_STYLE.FLAT)
    ledh.get_wall_by_direction(DIR.DOWN).get_edge_by_direction(DIR.FRONT).set_style(EDGE_ELEMENT_STYLE.FLAT)
    led.get_wall_by_direction(DIR.LEFT).get_edge_by_direction(DIR.FRONT).set_style(EDGE_ELEMENT_STYLE.FLAT)
    led.get_wall_by_direction(DIR.RIGHT).get_edge_by_direction(DIR.FRONT).set_style(EDGE_ELEMENT_STYLE.FLAT)
    left_cable.get_wall_by_direction(DIR.RIGHT).get_edge_by_direction(DIR.FRONT).set_style(EDGE_ELEMENT_STYLE.FLAT)

    # add some air vents
    middle.get_wall_by_direction(DIR.DOWN).add_child(AirVentsCutout([Frac(1)-40, Frac(1)-10], center=True), [Frac(0.5),0,Frac(0.5)])
    middle.get_wall_by_direction(DIR.UP)  .add_child(AirVentsCutout([Frac(1)-40, Frac(1)-10], center=True), [Frac(0.5),0,Frac(0.5)])
    left.get_wall_by_direction(DIR.DOWN)  .add_child(AirVentsCutout([Frac(1)-20, Frac(1)-10], center=True), [Frac(0.5),0,Frac(0.5)])

    powersup.get_wall_by_direction(DIR.RIGHT).add_child(FanCutout(40), [0, Frac(0.5), Frac(0.5)])

    # cable holes
    powersup.get_wall_by_direction(DIR.RIGHT).add_child(CircleCutout(5), [0, Frac(0.5) + 10 + Frac(0.25), Frac(0.5)])
    powersup.get_wall_by_direction(DIR.RIGHT).add_child(CircleCutout(5), [0, Frac(0.5) - 10 - Frac(0.25), Frac(0.5)])
    highv.get_wall_by_direction(DIR.DOWN).add_child(CircleCutout(5), [Frac(1) - 15, 0, Frac(0.5)])
    ledh.get_wall_by_direction(DIR.RIGHT).add_child(CircleCutout(3), [0, Frac(0.5), Frac(0.5) - c.subwall_thickness/2])
    led.get_wall_by_direction(DIR.RIGHT).add_child(CircleCutout(3), [0, Frac(0.5), Frac(0.5) - c.subwall_thickness/2])

    # cutout one edge for the power supply
    pw = powersup.get_wall_by_direction(DIR.UP)
    pw.get_edge_by_direction(DIR.LEFT).add_element(0, 30, EDGE_ELEMENT_STYLE.REMOVE, EDGE_STYLE.FLAT, None, next_style=EDGE_STYLE.FLAT)
    pw.get_edge_by_direction(DIR.BACK).add_element(0, 50, EDGE_ELEMENT_STYLE.REMOVE, EDGE_STYLE.FLAT, None, next_style=EDGE_STYLE.FLAT)
    pw.add_child(Edge(50, DIR.BACK, EDGE_STYLE.FLAT, EDGE_STYLE.INTERNAL_FLAT, style=EDGE_ELEMENT_STYLE.FLAT), [0,30])
    pw.add_child(Edge(30, DIR.LEFT, EDGE_STYLE.FLAT, EDGE_STYLE.INTERNAL_FLAT, style=EDGE_ELEMENT_STYLE.FLAT), [50,0])

    # ok, the following will get messy
    # add a cutout for the status light
    cw = SubWall([45, 45])
    cw.add_child(CutoutRoundedRect([30,30], 5, center=True), [Frac(0.5), Frac(0.5)])
    cw.add_child(CutoutRoundedRect([35,35], 7.5, center=True, layer=Layer('info')), [Frac(0.5), Frac(0.5)])
    led.get_wall_by_direction(DIR.FRONT).add_child(CutoutRoundedRect([35,35], 7.5, center=True), [Frac(0.5), Frac(0.5)])
    for d in [DIR2.UP, DIR2.DOWN, DIR2.LEFT, DIR2.RIGHT]:
        cw.get_edge_by_direction(d).set_begin_style(EDGE_STYLE.TOOTHED, False)
        cw.get_edge_by_direction(d).set_end_style(EDGE_STYLE.TOOTHED, False)
    for d in [DIR.UP, DIR.DOWN]:
        led.get_wall_by_direction(d).get_edge_by_direction(DIR.FRONT).add_element(0, Frac(1), EDGE_ELEMENT_STYLE.REMOVE, prev_style=EDGE_STYLE.FLAT, next_style=EDGE_STYLE.FLAT)
        # these edges are probably overkill, but they handle displacement
        led.get_wall_by_direction(d).add_child(Edge(c.wall_thickness, DIR.RIGHT, EDGE_STYLE.INTERNAL_FLAT, EDGE_STYLE.FLAT, EDGE_ELEMENT_STYLE.FLAT), [0,  Frac(1) - c.wall_thickness])
        led.get_wall_by_direction(d).add_child(Edge(c.wall_thickness, DIR.LEFT,  EDGE_STYLE.INTERNAL_FLAT, EDGE_STYLE.FLAT, EDGE_ELEMENT_STYLE.FLAT), [45, Frac(1) - c.wall_thickness])
        new_edge = Edge(45, DIR.FRONT, EDGE_STYLE.INTERNAL_FLAT, EDGE_STYLE.INTERNAL_FLAT, EDGE_ELEMENT_STYLE.TOOTHED)
        new_edge.set_counterpart(cw.get_edge_by_direction(d[:2]))
        led.get_wall_by_direction(d).add_child(new_edge, [0, Frac(1) - c.wall_thickness])
    for d in [DIR.LEFT, DIR.RIGHT]:
        led.get_wall_by_direction(d).get_edge_by_direction(DIR.FRONT).set_style(EDGE_ELEMENT_STYLE.REMOVE)
        led.get_wall_by_direction(d).get_edge_by_direction(DIR.DOWN).add_element(Frac(1) - c.wall_thickness, c.wall_thickness, EDGE_ELEMENT_STYLE.REMOVE, prev_style=EDGE_STYLE.FLAT)
        led.get_wall_by_direction(d).get_edge_by_direction(DIR.UP).add_element(Frac(1) - c.wall_thickness, c.wall_thickness, EDGE_ELEMENT_STYLE.REMOVE, prev_style=EDGE_STYLE.FLAT)
        new_edge = Edge(45, DIR.FRONT, EDGE_STYLE.FLAT, EDGE_STYLE.FLAT)
        new_edge.set_counterpart(cw.get_edge_by_direction(d[:2]))
        led.get_wall_by_direction(d).add_child(new_edge, [0, Frac(1) - c.wall_thickness])

    # setup the cable wall
    cable_wall = left_cable.get_wall_by_direction(DIR.RIGHT)
    right.get_wall_by_direction(DIR.LEFT).add_child(RoundedRectEdgeCutout([0, 50, Frac(0.5)], 10, DIR.FRONT, center=True), [0, Frac(0.5), Frac(1)])
    cable_wall.add_child(RoundedRectEdgeCutout([0, Frac(0.2), Frac(0.7)], 10, DIR.FRONT, center=True), [0, Frac(0.2), Frac(1)])
    cable_wall.add_child(RoundedRectEdgeCutout([0, Frac(0.2), Frac(0.7)], 10, DIR.FRONT, center=True), [0, Frac(0.7), Frac(1)])

    # outer wall cable holes
    right.get_wall_by_direction(DIR.UP).add_child(RoundedRectEdgeCutout([40, 0, 30], 10, DIR.BACK, center=True), [Frac(0.5), 0, 0])
    cable_wall.get_edge_by_direction(DIR.UP).add_element(0, 30, EDGE_ELEMENT_STYLE.REMOVE)
    cable_wall.get_edge_by_direction(DIR.BACK).add_element(Frac(1) - 30, 30, EDGE_ELEMENT_STYLE.REMOVE)
    displace = c.cutting_width / 2
    cable_wall.add_child(ArcPath([150+displace, -displace], [180+displace, 30-displace], 30-displace, large_arc=False, layer=Layer('outline')), [0,0])

    highv_half.get_wall_by_direction(DIR.UP).add_child(RoundedRectEdgeCutout([20, 0, 10], 10, DIR.BACK, center=True), [Frac(0.5), 0, 0])

    # svg export
    objects = cb.render(c) + [cw.render(c)]
    objects = place_2d_objects(objects, c)

    with codecs.open('autoc4.svg', 'wb', 'utf-8') as f:
        f.write(export_svg_with_paths(objects, c))

    # openscad export
    cn = c.copy()
    cn.colors['cutout'] = 'grey'
    cn.colors['outline'] = 'grey'
    cn.cutting_width = 0
    cn.print_wall_names = False
    export_box_openscad(cb, cn, 'autoc4', join_all_svg=False, single_wall_rules=True)

if __name__ == "__main__":
    main()
