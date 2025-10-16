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
VERT_EFREI = "#63f763"

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

        frame = FullScreenRectangle()
        self.play(Create(frame), run_time=1)
        self.wait()

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


        self.play(Write(circuit1), Write(res_names), run_time=2)
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

        passing_flash_bleu = AnimationGroup(
            ShowPassingFlash(fil_bleu[0].copy().set_stroke(width=5).set_color(WHITE), time_width=1),
            AnimationGroup(ShowPassingFlash(fil_bleu[1].copy().set_stroke(width=5).set_color(WHITE), time_width=1),
                            ShowPassingFlash(fil_bleu[2].copy().set_stroke(width=5).set_color(WHITE), time_width=2),
                           rate_func=linear
                           ),
            ShowPassingFlash(fil_bleu[3].copy().set_stroke(width=5).set_color(WHITE), time_width=1),
            lag_ratio=0.5,
            rate_func=linear
        )

        passing_flash_violet = AnimationGroup(
            ShowPassingFlash(fil_violet[0].copy().set_stroke(width=5).set_color(WHITE), time_width=1),
            ShowPassingFlash(fil_violet[1].copy().set_stroke(width=5).set_color(WHITE), time_width=1, reverse_rate_function=smooth),
            ShowPassingFlash(fil_violet[2].copy().set_stroke(width=5).set_color(WHITE), time_width=1, reverse_rate_function=smooth),
            lag_ratio=0.25,
            rate_func=linear
        )

        # self.play(ShowPassingFlash(fil_violet.copy().set_stroke(width=5).set_color(WHITE), time_width=1),
        #           ShowPassingFlash(fil_bleu.copy().set_stroke(width=5).set_color(WHITE), time_width=1))
        self.play(passing_flash_bleu, passing_flash_violet, rate_func=smooth, run_time=2)
        self.wait()

        encadre = SurroundingRectangle(VGroup(circuit1[2], circuit1[3], res_names[1], res_names[2]), color=ORANGE_EFREI, buff=0.2)
        eq23 = MathTex(r"\dfrac{R_2R_3}{R_2+R_3}").next_to(encadre, RIGHT, buff=0.2).set_color(ORANGE_EFREI)
        self.play(Create(encadre), run_time=1)
        self.wait()

        self.play(Write(eq23), run_time=1)
        self.wait()

        # eq23 = MathTex(r"= \dfrac{R_2R_3}{R_2+R_3}").next_to(r23, RIGHT, buff=0).set_color(ORANGE_EFREI).scale(0.7)
        # self.play(Write(eq23), run_time=1)
        # self.wait()

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

        r23 = MathTex(r"R_{23}").set_color(WHITE)
        r23.add_updater(lambda m: m.next_to(encadre, RIGHT, buff=0.2))
        eq23.generate_target()
        eq23.target = r23

        fil_violet.add(Line(start=circuit_23[2].get_left(), end=circuit_23[2].get_right(), color=VIOLET_EFREI))
        self.add(circuit_23, fil_violet[4])
        encadre.generate_target()
        encadre.target = Rectangle(width=circuit_23[1].width, height=circuit_23[1].height*0.56, color=WHITE).move_to(circuit_23[1].get_center())

        self.play(MoveToTarget(encadre), FadeOut(circuit1), FadeOut(fil_bleu[1], fil_bleu[3], fil_violet[0], fil_violet[2]), FadeOut(res_names[1:]), FadeOut(arrow), MoveToTarget(eq23), run_time=1)
        self.wait()

        # self.play(ShowPassingFlash(VGroup(fil_bleu[0],fil_bleu[2]).copy().set_stroke(width=5).set_color(WHITE),time_width=1))
        passing_flash_fil_bleu = AnimationGroup(
            ShowPassingFlash(fil_bleu[0].copy().set_stroke(width=5).set_color(WHITE),time_width=2),
            ShowPassingFlash(fil_bleu[2].copy().set_stroke(width=5).set_color(WHITE), time_width=2),
            lag_ratio=0.5,
            rate_func=linear
        )
        self.play(passing_flash_fil_bleu, rate_func=smooth)
        self.wait()

        encadre2 = SurroundingRectangle(VGroup(circuit_23[0], circuit_23[1], res_names[0], r23), color=ORANGE_EFREI, buff=0).shift(0.25*(UP+RIGHT)).scale(0.9)
        eq123 = MathTex(r"R_\textrm{eq}", r"= R_1 + R_{23}").next_to(encadre2, RIGHT, buff=0.2).set_color(ORANGE_EFREI)

        self.play(Create(encadre2), run_time=1)
        self.wait()

        self.play(Write(eq123), run_time=1)
        self.wait()

        circuit_123 = MathTex(
            r"\draw (0,0) to [short, *-] (2,0);",
            r"\draw (2,0) to [R] (2,-2);",
            r"\draw (2,-2) to [short, -*] (0,-2);",
            tex_environment="circuitikz",
            tex_template=tex_template,
            stroke_color=WHITE,
            stroke_width=3,
            fill_color=WHITE
        ).align_to(circuit_23,LEFT).align_to(circuit_23,DOWN).set_z_index(-1)

        encadre2.generate_target()
        encadre2.target = Rectangle(width=circuit_123[1].width, height=circuit_123[1].height*0.56, color=WHITE).move_to(circuit_123[1].get_center())
        eq123[0].generate_target()
        eq123[0].target = eq123[0].copy().set_color(WHITE).next_to(circuit_123, RIGHT, buff=0.2)

        # r23.remove_updater(r23.get_updaters())

        fil_rouge_2 = Line(start=circuit_123[0].get_left(), end=circuit_123[0].get_right(), color=ROUGE_EFREI)

        self.play(FadeOut(circuit_23, res_names[0], eq23, eq123[1:], encadre),
                  MoveToTarget(encadre2),
                  VGroup(fil_bleu[0],fil_bleu[2]).animate.set_color(ROUGE_EFREI),
                  FadeIn(circuit_123[1]),
                  MoveToTarget(eq123[0]),
                  Create(fil_rouge_2),
                  run_time=1)
        self.wait()

        eqf = MathTex(r"= R_1 + \dfrac{R_2R_3}{R_2+R_3}").set_color(WHITE).next_to(eq123[0], RIGHT, buff=0.2)

        self.play(Write(eqf), run_time=1)
        self.wait()

        eqf.add(eq123[0])
        eq_encadre = SurroundingRectangle(eqf, color=ORANGE_EFREI, buff=0.1)

        self.play(Create(eq_encadre), run_time=1)
        self.wait(2)
        self.play(VGroup(eqf,eq_encadre).animate.move_to(DOWN*2.5),
                  FadeOut(circuit_123[1], fil_rouge_2, fil_violet[1], fil_violet[3:], encadre2, fil_rouge, fil_bleu[0], fil_bleu[2]),
                  FadeIn(circuit1, res_names),
                    run_time=1
                  )
        self.wait()


class ResEq2(Scene):

    def construct(self):

        def get_leftres(circuit):
            return circuit.get_left() + circuit.width / 4.55 * RIGHT

        def get_rightres(circuit):
            return circuit.get_right() + circuit.width / 4.75 * LEFT

        def get_topres(circuit):
            return circuit.get_top() + circuit.height / 4.6 * DOWN

        def get_bottomres(circuit):
            return circuit.get_bottom() + circuit.height / 4.6 * UP


        titre2 = Tex("Exemple 2 :").to_corner(UL)
        self.play(Write(titre2))

        frame = FullScreenRectangle()
        self.play(Create(frame), run_time=1)
        self.wait()

        tex_template = TexTemplate()
        tex_template.add_to_preamble(r"\usepackage[siunitx, RPvoltages, european]{circuitikz}")
        circuit1 = MathTex(
            r"\draw (0,0) to [short, *-] (1,0);",
            r"\draw (1,0) to [R] (1,-2);",  #R1
            r"\draw (1,-2) to [R] (1,-4);",  #R2
            r"\draw (1,0) to [R] (3,0);", #R3
            r"\draw (3,0) to [R] (3,-4);", #R4
            r"\draw (3,0) to [short] (4,0);",
            r"\draw (4,0) to [R] (4,-4);", #R5
            r"\draw (4,-4) to [short, -*] (0,-4);",
            tex_environment="circuitikz",
            tex_template=tex_template,
            stroke_color=WHITE,
            stroke_width=3,
            fill_color=WHITE
        ).scale(0.7)

        res_names = VGroup(
            MathTex(r"R_1").next_to(circuit1[1], LEFT, buff=0.2),
            MathTex(r"R_2").next_to(circuit1[2], LEFT, buff=0.2),
            MathTex(r"R_3").next_to(circuit1[3], UP, buff=0.2),
            MathTex(r"R_4").next_to(circuit1[4], LEFT, buff=0.2),
            MathTex(r"R_5").next_to(circuit1[6], RIGHT, buff=0.2)
        )

        self.play(Write(circuit1), Write(res_names), run_time=2)
        self.wait()

        fil_rouge = VGroup(
            Line(start=circuit1[0].get_left(), end=get_leftres(circuit1[3]), color=ROUGE_EFREI),
            Line(start=circuit1[1].get_top(), end=get_topres(circuit1[1]), color=ROUGE_EFREI),
            Dot(circuit1[0].get_left()+0.075*RIGHT, radius=0.1, color=ROUGE_EFREI)
        )

        fil_bleu = VGroup(
            Line(start=get_rightres(circuit1[3]), end=circuit1[5].get_right(), color=BLEU_CLAIR_EFREI),
            Line(start=circuit1[4].get_top(), end=get_topres(circuit1[4])+0.55*DOWN, color=BLEU_CLAIR_EFREI),
            Line(start=circuit1[6].get_top(), end=get_topres(circuit1[6])+0.55*DOWN, color=BLEU_CLAIR_EFREI)
        )

        fil_mauve = VGroup(
            Line(start=circuit1[7].get_left(), end=circuit1[7].get_right(), color=VIOLET_EFREI),
            Line(start=get_bottomres(circuit1[2]), end=circuit1[2].get_bottom(), color=VIOLET_EFREI),
            Line(start=get_bottomres(circuit1[4])+0.55*UP, end=circuit1[4].get_bottom(), color=VIOLET_EFREI),
            Line(start=get_bottomres(circuit1[6])+0.55*UP, end=circuit1[6].get_bottom(), color=VIOLET_EFREI),
            Dot(circuit1[7].get_left()+0.075*RIGHT, radius=0.1, color=VIOLET_EFREI)
        )

        fil_vert = Line(start=get_bottomres(circuit1[1]), end=get_topres(circuit1[2]), color=VERT_EFREI)

        self.play(FadeIn(fil_rouge, fil_bleu, fil_mauve, fil_vert), run_time=1)
        self.wait()

        arrow = DashedLine(start=circuit1.get_corner(UR)+UP, end=circuit1.get_corner(UL)+UP, color=YELLOW, stroke_width=6, tip_length=0.3, dash_length=0.1).add_tip(tip_shape=StealthTip, tip_length=0.3)
        self.play(GrowFromEdge(arrow,RIGHT), run_time=1)
        self.wait()

        passing_flash_bleu = AnimationGroup(
            ShowPassingFlash(fil_bleu[0].copy().set_stroke(width=5).set_color(WHITE), time_width=1),
            ShowPassingFlash(fil_bleu[1].copy().set_stroke(width=5).set_color(WHITE), time_width=1),
            ShowPassingFlash(fil_bleu[2].copy().set_stroke(width=5).set_color(WHITE), time_width=1),
            lag_ratio=0.25,
            rate_func=linear
        )

        passing_flash_mauve = AnimationGroup(
            ShowPassingFlash(fil_mauve[0].copy().set_stroke(width=5).set_color(WHITE), time_width=1),
            # ShowPassingFlash(fil_mauve[1].copy().set_stroke(width=5).set_color(WHITE), time_width=1, reverse_rate_function=linear),
            ShowPassingFlash(fil_mauve[2].copy().set_stroke(width=5).set_color(WHITE), time_width=1, reverse_rate_function=linear),
            ShowPassingFlash(fil_mauve[3].copy().set_stroke(width=5).set_color(WHITE), time_width=1, reverse_rate_function=linear),
            lag_ratio=0.2,
            rate_func=linear
        )

        self.play(passing_flash_bleu, passing_flash_mauve, rate_func=smooth, run_time=2)
        self.wait()

        encadre45 = SurroundingRectangle(VGroup(circuit1[4], circuit1[6], res_names[3], res_names[4]), color=ORANGE_EFREI, buff=0.2).stretch_to_fit_height(circuit1[4].height*0.8)
        eq45 = MathTex(r"\dfrac{R_4R_5}{R_4+R_5}").next_to(encadre45, RIGHT, buff=0.2).set_color(ORANGE_EFREI).scale(0.8)

        self.play(Create(encadre45), run_time=1)
        self.wait()

        self.play(Write(eq45), run_time=1)
        self.wait()

        encadre45.generate_target()
        encadre45.target = Rectangle(width=circuit1[4].width, height=circuit1[4].height*0.56, color=WHITE).move_to(circuit1[4].get_center())
        eq45.generate_target()
        eq45.target = MathTex(r"R_{45}").set_color(WHITE).next_to(encadre45.target, RIGHT, buff=0.2).scale(0.8)

        self.play(MoveToTarget(encadre45), MoveToTarget(eq45), FadeOut(circuit1[6]), FadeOut(res_names[3], res_names[4]), run_time=1)
        self.wait()


