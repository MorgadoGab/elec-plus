from abc import ABC

import numpy
import numpy as np
from manim import *
from manim_fonts import *

config.background_color = BLACK
config["background_color"] = BLACK

BLEU_FONCE_EFREI = "#163767"
BLEU_CLAIR_EFREI = "#008aff"
VIOLET_EFREI = "#e945ff"
BLEU_MOYEN_EFREI = "#3653a0"
ORANGE_EFREI = "#e7873b"
ROUGE_EFREI = "#dd5555"

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

class Intro(Scene):
    def construct(self):

        titre = Tex("Calculer une résistance équivalente")

        self.play(Write(titre))
        self.wait(1)
        self.play(titre.animate.to_edge(UP))
        self.wait(1)

        thumbnail_asso = ImageMobject("thumbnail_asso.png").scale(2)
        thumbnail_asso.add(SurroundingRectangle(thumbnail_asso, color=BLEU_CLAIR_EFREI, buff=0.1))

        self.play(FadeIn(thumbnail_asso, shift=DOWN))
        self.wait()
        self.play(FadeOut(thumbnail_asso, shift=UP), FadeOut(titre, shift=UP))
        self.wait()


class ResEq(Scene):

    def construct(self):

        def get_leftres(circuit):
            return circuit.get_left() + circuit.width / 4.55 * RIGHT

        def get_rightres(circuit):
            return circuit.get_right() + circuit.width / 4.75 * LEFT

        def get_topres(circuit):
            return circuit.get_top() + circuit.height / 4.6 * DOWN

        def get_bottomres(circuit):
            return circuit.get_bottom() + circuit.height / 4.6 * UP

        # self.add(Circle(0.1, RED, fill_opacity=1))

        titre2 = Tex("Exemple 1 :").to_corner(UL)
        self.play(Write(titre2))

        tex_template = TexTemplate()
        tex_template.add_to_preamble(r"\usepackage[siunitx, RPvoltages, european]{circuitikz}")
        circuit1 = MathTex(
            r"\draw (0,0) to [R, *-] (2,0);",
            r"\draw (2,0) to [short] (4,0);",
            r"\draw (2,0) to [R] (2,-2);",
            r"\draw (4,0) to [R] (4,-2);",
            r"\draw (4,-2) to [short, -*] (0,-2);",
            tex_environment="circuitikz",
            tex_template=tex_template,
            stroke_color=WHITE,
            stroke_width=3,
            fill_color=WHITE
        )

        res_names = VGroup(
            MathTex(r"R_1").next_to(circuit1[0], UP, buff=0.2),
            MathTex(r"R_2").next_to(circuit1[2], RIGHT, buff=0.2),
            MathTex(r"R_3").next_to(circuit1[3], RIGHT, buff=0.2)
        )


        self.play(Write(circuit1), run_time=2)
        self.play(Write(res_names), run_time=1)
        self.wait()

        fil_rouge = Line(start=circuit1[0].get_left(), end=get_leftres(circuit1[0])+0.05*RIGHT, color=ROUGE_EFREI)
        borne_rouge = Dot(fil_rouge.get_start()+0.075*RIGHT, radius=0.1, color=ROUGE_EFREI)
        fil_rouge.add(borne_rouge)

        fil_bleu = VGroup(Line(start=get_rightres(circuit1[0]), end=circuit1[0].get_right(), color=BLEU_CLAIR_EFREI)
        ,Line(start=circuit1[1].get_left(), end=circuit1[1].get_right(), color=BLEU_CLAIR_EFREI)
        ,Line(start=circuit1[2].get_top(), end=get_topres(circuit1[2]), color=BLEU_CLAIR_EFREI)
        ,Line(start=circuit1[3].get_top(), end=get_topres(circuit1[3]), color=BLEU_CLAIR_EFREI))

        fil_violet = VGroup(Line(start=circuit1[4].get_left(), end=circuit1[4].get_right(), color=VIOLET_EFREI)
        ,Line(start=get_bottomres(circuit1[2]), end=circuit1[2].get_bottom(), color=VIOLET_EFREI)
        ,Line(start=get_bottomres(circuit1[3]), end=circuit1[3].get_bottom(), color=VIOLET_EFREI)
        ,Dot(circuit1[4].get_left()+0.075*RIGHT, radius=0.1, color=VIOLET_EFREI))

        self.play(FadeIn(fil_rouge, fil_bleu, fil_violet), run_time=1)
        self.wait()

        arrow = DashedLine(start=circuit1.get_corner(UR)+UP, end=circuit1.get_corner(UL)+UP, color=YELLOW, stroke_width=6, tip_length=0.3, dash_length=0.1).add_tip(tip_shape=StealthTip, tip_length=0.3)
        self.play(GrowFromEdge(arrow,RIGHT), run_time=1)
        self.wait()

        encadre = SurroundingRectangle(VGroup(circuit1[2], circuit1[3], res_names[1], res_names[2]), color=ORANGE_EFREI, buff=0.2)
        r23 = MathTex(r"R_{23}").next_to(encadre, RIGHT, buff=0.2).set_color(ORANGE_EFREI)
        self.play(Create(encadre), Write(r23), run_time=1)
        self.wait()

        circuit_23 = MathTex(
            r"\draw (0,0) to [R, *-] (2,0);",
            r"\draw (2,0) to [R] (2,-2);",
            r"\draw (2,-2) to [short, -*] (0,-2);",
            tex_environment="circuitikz",
            tex_template=tex_template,
            stroke_color=WHITE,
            stroke_width=3,
            fill_color=WHITE
        ).align_to(circuit1,LEFT).set_z_index(-1)

        fil_violet.add(Line(start=circuit_23[2].get_left(), end=circuit_23[2].get_right(), color=VIOLET_EFREI))
        self.add(circuit_23, fil_violet[4])
        encadre.generate_target()
        encadre.target = Rectangle(width=circuit_23[1].width, height=circuit_23[1].height*0.56, color=ORANGE_EFREI).move_to(circuit_23[1].get_center())
        self.play(MoveToTarget(encadre), run_time = 1)
        self.play(FadeOut(circuit1), FadeOut(fil_bleu[1], fil_bleu[3], fil_violet[0], fil_violet[2]), FadeOut(encadre), FadeOut(res_names[1:]), r23.animate.next_to(circuit_23,RIGHT,buff=0.2).set_color(WHITE), run_time=1)
        self.wait()