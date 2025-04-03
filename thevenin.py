from abc import ABC

import numpy
import numpy as np
from manim import *
from manim_fonts import *
from scene import Path

config.background_color = BLACK
config["background_color"] = BLACK


class Generique(Scene):

    def construct(self):
        text_logo = Text("Elec", font_size=80, font="Playwrite MX")

        image_logo = VGroup(Arc(angle=PI, color=YELLOW_B),
                            Cross(scale_factor=0.2).rotate(45 * DEGREES).shift(UP / 2.5).set_color(YELLOW)
                            ).rotate(-90 * DEGREES).next_to(text_logo, RIGHT)

        logo = VGroup(text_logo, image_logo).move_to((0., 0., 0.))
        intro = AnimationGroup(Write(text_logo),
                               Create(image_logo)
                               )
        # self.add(Circle(0.1,RED,fill_opacity=1))
        self.play(intro, run_time=1.5)
        self.wait()


class VoltArrow(Arrow, ABC):

    def __init__(self, dipole: MathTex, name, side=LEFT, buff_side=1, buff_name=0, color=YELLOW_E, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tip_shape = StealthTip
        self.stroke_width = 2
        self.dipole = dipole
        self.color = color
        self.name = str(name)
        self.side = side
        self.next_to(dipole, side * buff_side)
        self.label = MathTex(self.name, color=self.color)
        self.add(self.label.next_to(self, direction=self.side, buff=buff_name))

    def add_label(self):
        return VGroup(self, self.label.next_to(self, direction=self.side))


class CurrentArrow(Arrow, ABC):

    def __init__(self, wire: MathTex, name, direction, location, path=None, side=None, buff_side=1, color=YELLOW_E,
                 tip_shape=StealthTip, *args, **kwargs):
        super().__init__(start=wire.get_center(), end=wire.get_center() + direction, tip_shape=tip_shape, tip_length=2,
                         *args, **kwargs)
        self.scale(factor=0.1, scale_tips=False)
        # self.stroke_width = 0.5
        self.wire = wire
        self.direction = direction
        # self.start = self.wire.get_center()
        # self.end = self.wire.get_center() + self.direction
        self.color = color
        self.name = str(name)
        self.set_side()
        self.buff_side = buff_side
        self.move_to(wire.get_center() + location)
        self.label = MathTex(self.name, color=self.color)
        self.label.next_to(self, direction=self.side * buff_side)
        # self.arrow = self.submobjects[0]
        self.path = path
        self.location = self.get_center()
        # self.prev_point=self.path.get_important_points()[0]
        # self.wires = []
        #
        # for point in self.path.get_important_points() :
        #     self.wires.append(Line(start=self.prev_point,end=point))

    def add_label(self):
        return self.add(self.label.next_to(self, direction=self.side * self.buff_side))

    def remove_label(self):
        return self.remove(self.label)

    def set_side(self, side=None):
        if side is None:
            if self.direction is UP:
                self.side = LEFT
            elif self.direction is DOWN:
                self.side = RIGHT
            elif self.direciton is RIGHT:
                self.side = UP
            elif self.direction is LEFT:
                self.side = DOWN
            else:
                self.side = side

    def set_direction(self, dir):
        self.direction = dir
        self.put_start_and_end_on(self.wire.get_center(), self.wire.get_center() + dir)
        self.scale(factor=0.01, scale_tips=False)
        return self

    def reset_direction(self):
        pass


class Thevenin(Scene):

    def construct(self):
        # self.add(Circle(0.1, RED, fill_opacity=1))

        titre = Tex("Théorème de Thévenin")

        tex_template = TexTemplate()
        tex_template.add_to_preamble(r"\usepackage[siunitx, RPvoltages, european]{circuitikz}")

        text1 = Tex("Prenons un exemple d'application du ", "théorème de Thévenin",".", font_size=32)
        text1.to_edge(UP)

        circuit = MathTex(
            r"\draw (0,0) to [american, V] (0,4);",
            r"\draw (0,4) to [short] (1,4);",
            r"\draw (1,4) to [R] (1,2);",
            r"\draw (1,2) to [R] (1,0);",
            r"\draw (1,0) to [short] (0,0);",
            tex_environment="circuitikz",
            tex_template=tex_template,
            stroke_color=WHITE,
            stroke_width=2,
            fill_color=WHITE
        ).to_edge(DOWN)

        self.play(Write(titre))
        self.wait(1)
        titre.generate_target()
        titre.target = text1[1]
        self.play(MoveToTarget(titre, path_arc=-PI/2), FadeIn(text1[0], text1[2:]))
        self.wait(4)