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


class PontDivTension(Scene):

    def construct(self):
        # self.add(Circle(0.1, RED, fill_opacity=1))

        titre = Tex("Pont diviseur de tension").to_edge(UP)

        tex_template = TexTemplate()
        tex_template.add_to_preamble(r"\usepackage[siunitx, RPvoltages, european]{circuitikz}")

        text1 = Tex("Pour réaliser un ", "pont diviseur de tension", ", il nous faut au moins deux résistances en ",
                    "série", ".", font_size=32)
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

        r1 = MathTex("R_1")
        r2 = MathTex("R_2")

        E = VoltArrow(start=circuit[0].get_bottom() + UP,
                      end=circuit[0].get_top() - UP,
                      dipole=circuit[0],
                      name="E")

        U1 = VoltArrow(start=circuit[2].get_bottom(),
                       end=circuit[2].get_top(),
                       dipole=circuit[2],
                       name="U_1",
                       side=RIGHT,
                       buff_side=4,
                       color=BLUE)

        U2 = VoltArrow(start=circuit[3].get_bottom(),
                       end=circuit[3].get_top(),
                       dipole=circuit[3],
                       name="U_2",
                       side=RIGHT,
                       buff_side=4,
                       color=BLUE)

        r1.next_to(circuit[2])
        r2.next_to(circuit[3])

        # circuit_group = VGroup(circuit, r1, r2, E).scale(0.8)

        # box_req = Rectangle(color=BLUE, width=circuit.width * 1.3, height=circuit.height * 0.9).move_to(
        #           circuit.get_center_of_mass())

        eq1 = MathTex(r"=", r"{ {{R_1}} \over {{R_1}} + {{R_2}} }", r"E")
        eq1.next_to(U1).set_color(BLUE)

        eq2 = MathTex(r"=", r"{ {{R_2}} \over {{R_1}} + {{R_2}} }", r"E")
        eq2.next_to(U2).set_color(BLUE)

        r1.generate_target()
        r2.generate_target()
        E.label.generate_target()

        # self.add(index_labels(eq2))
        # print(eq1.submobjects)

        self.play(Write(titre))
        self.wait(2)
        self.play(TransformMatchingShapes(titre, text1[1]), FadeIn(text1[0], text1[2:]))
        self.wait(2)
        self.play(Create(circuit))
        self.play(FadeIn(r1, r2, shift=LEFT), GrowArrow(E, run_time=1.5))
        self.wait(2)
        # self.play(FadeIn(U1, U2, shift=LEFT))
        self.play(GrowArrow(U1), GrowArrow(U2), run_time=1.5)
        self.wait(2)
        self.play(Transform(E.copy(), VGroup(U1, U2)))
        self.wait(2)
        self.play(Circumscribe(r1, Circle), Circumscribe(r2, Circle))
        self.wait(2)

        self.play(FadeIn(eq1[0:2]))
        r1.target = eq1[2]
        self.play(MoveToTarget(r1.copy()))
        # self.wait(2)
        self.play(FadeIn(eq1[3]))
        # self.wait(2)
        r1.target = eq1[4]
        self.play(MoveToTarget(r1.copy()))
        self.play(FadeIn(eq1[5]))
        # self.wait(2)
        r2.target = eq1[6]
        self.play(MoveToTarget(r2.copy()))
        # self.wait(2)
        E.label.target = eq1[8]
        self.play(MoveToTarget(E.label.copy()))
        self.wait(2)

        self.play(FadeIn(eq2[0:2]))
        # self.wait(2)
        r2.target = eq2[2]
        self.play(MoveToTarget(r2.copy()))
        # self.wait(2)
        self.play(FadeIn(eq2[3]))
        # self.wait(2)
        r1.target = eq2[4]
        self.play(MoveToTarget(r1.copy()))
        self.play(FadeIn(eq2[5]))
        # self.wait(2)
        r2.target = eq2[6]
        self.play(MoveToTarget(r2.copy()))
        # self.wait(2)
        E.label.target = eq2[8]
        self.play(MoveToTarget(E.label.copy()))
        self.wait(2)

        # self.play(TransformMatchingShapes(VGroup(r2.copy(),E.label.copy(), r1.copy()), eq2), run_time = 2)
        self.wait(2)


class PontDivCourant(Scene):

    def construct(self):
        # self.add(Circle(0.1, RED, fill_opacity=1))

        titre = Tex("Pont diviseur de courant").to_edge(UP)

        tex_template = TexTemplate()
        tex_template.add_to_preamble(r"\usepackage[siunitx, RPvoltages, european]{circuitikz}")

        text1 = Tex("Pour réaliser un ", "pont diviseur de courant", ", il nous faut au moins deux résistances en ",
                    "parallèle", ".", font_size=32)
        text1.to_edge(UP)

        circuit = MathTex(
            r"\draw (0,0) to [I] (0,2);",
            r"\draw (0,2) to [short] (4,2);",
            r"\draw (2,2) to [R] (2,0);",
            r"\draw (4,2) to [R] (4,0);",
            r"\draw (4,0) to [short] (0,0);",
            tex_environment="circuitikz",
            tex_template=tex_template,
            stroke_color=WHITE,
            stroke_width=2,
            fill_color=WHITE
        )

        r1 = MathTex("R_1", color=YELLOW_E).next_to(circuit[2])
        r2 = MathTex("R_2", color=YELLOW_E).next_to(circuit[3])

        I0 = CurrentArrow(wire=circuit[0],
                          name="I",
                          direction=UP,
                          location=UP,
                          side=LEFT,
                          color=PURPLE,
                          path=Path([circuit[0].get_center(), circuit[0].get_top(), circuit[1].get_center()])
                          )

        I1 = CurrentArrow(wire=circuit[2],
                          name="I_1",
                          direction=DOWN,
                          location=UP * 1.1,
                          side=LEFT,
                          color=RED,
                          path=Path([circuit[2].get_top(), circuit[2].get_bottom()])
                          )

        I2 = CurrentArrow(wire=circuit[3],
                          name="I_2",
                          direction=DOWN,
                          location=UP * 1.1,
                          side=LEFT,
                          color=BLUE,
                          path=Path([circuit[2].get_top(), circuit[1].get_right(), circuit[3].get_bottom(),
                                     circuit[4].get_center()])
                          )

        If = CurrentArrow(wire=circuit[4],
                          name="I",
                          direction=UP,
                          location=UP,
                          side=LEFT,
                          color=PURPLE,
                          path=Path([circuit[4].get_center(), circuit[4].get_left(), circuit[0].get_center()])
                          )

        def updater_current(c, dt):
            rate = 0.003
            pre_alpha = c.t_offset % 1
            alpha = (c.t_offset + rate) % 1
            opacity = min(alpha * (1 - alpha) * 10, c.opac)
            c.opac += 0.02
            c.set_opacity(opacity)
            #     Direction de la fleche
            c.put_start_and_end_on(start=c.path.point_from_proportion(pre_alpha),
                                   end=c.path.point_from_proportion(alpha))
            c.move_to(c.path.point_from_proportion(alpha))
            c.t_offset += rate

        eq1 = MathTex(r"I_1", r"=", r"{ {{R_2}} \over {{R_1}} + {{R_2}} }", r"I").scale(0.75)
        eq1.next_to(circuit[4], direction=DOWN).set_color(RED)

        eq2 = MathTex(r"I_2", r"=", r"{ {{R_1}} \over {{R_1}} + {{R_2}} }", r"I").scale(0.75)
        eq2.next_to(circuit[3], direction=DOWN).set_color(BLUE)

        moving_currents = []
        nb_currents = 10
        for i in range(nb_currents):
            moving_currents.append([I0.copy(),I1.copy(),I2.copy(),If.copy()])
            for j in range(4):
                moving_currents[i][j].add_updater(updater_current)
                moving_currents[i][j].t_offset = i / nb_currents
                moving_currents[i][j].opac = 0

        Arrow1 = Arrow(start=I1.label.get_center(), end=r2.get_center(), color=YELLOW_E, fill_opacity=0.5,
                       stroke_opacity=0.5)
        Arrow2 = Arrow(start=I2.label.get_center(), end=r1.get_center(), color=YELLOW_E, fill_opacity=0.5,
                       stroke_opacity=0.5)

        I1.label.generate_target()
        I2.label.generate_target()

        self.play(Create(circuit), run_time=1.5)
        self.play(Write(titre))
        self.wait(2)
        self.play(TransformMatchingShapes(titre, text1[1]), FadeIn(text1[0], text1[2:]))
        self.wait(2)
        for mob in moving_currents:
            self.add(*mob)
        self.play(Write(r1), Write(r2))

        I1.label.target = eq1[0]
        I2.label.target = eq2[0]
        self.play(Write(I0.label),Write(I1.label),Write(I2.label))
        self.wait(2)
        self.play(GrowArrow(Arrow1),GrowArrow(Arrow2))
        self.wait(2)
        self.play(MoveToTarget(I1.label.copy()),MoveToTarget(I2.label.copy()))
        self.wait(2)

        r1.target = eq2[3]
        r2.target = eq1[3]
        self.play(FadeIn(eq1[1],eq2[1]),MoveToTarget(r1.copy()),MoveToTarget(r2.copy()))
        self.wait(2)

        r1.target = eq1[5]
        r2.target = eq1[7]
        self.play(FadeIn(eq1[4],eq2[4]),MoveToTarget(r1.copy()),MoveToTarget(r2.copy()))
        r1.target = eq2[5]
        r2.target = eq2[7]
        self.play(FadeIn(eq1[6],eq2[6]),MoveToTarget(r1.copy()),MoveToTarget(r2.copy()))
        self.wait(2)
        Ip=I0.copy()
        I0.label.target = eq1[9]
        Ip.label.target = eq2[9]
        self.play(MoveToTarget(I0.label.copy()), MoveToTarget(Ip.label))
        self.wait(5)

class FinalScene(Scene):
    def construct(self):
        titre = Tex("Cas général d'un pont diviseur de tension")
        tex_template = TexTemplate()
        tex_template.add_to_preamble(r"\usepackage[siunitx, RPvoltages, european]{circuitikz}")
        circuit = MathTex(
            r"\draw (10,0) to [american voltage source] (0,0);",
            r"\draw (0,0) to [short] (0,2);",
            r"\draw (0,2) to [R] (2,2);",
            r"\draw (2,2) to [R] (4,2);",
            r"\draw (5,2) to [R] (7,2);",
            r"\draw (8,2) to [R] (10,2);",
            r"\draw (10,2) to [short] (10,0);",
            tex_environment="circuitikz",
            tex_template=tex_template,
            stroke_color=WHITE,
            stroke_width=2,
            fill_color=WHITE
        )

        E = MathTex("E").next_to(circuit[0],UP)
        r1 = MathTex("R_1").next_to(circuit[2],UP)
        r2 = MathTex("R_2").next_to(circuit[3],UP)
        rj = MathTex("R_i").next_to(circuit[4],UP)
        rN = MathTex("R_N").next_to(circuit[-2],UP)

        circuit_f = VGroup(circuit[:4],
                            DashedLine(start=circuit[3].get_right(),end=circuit[4].get_left(),stroke_width=2),
                            circuit[4],
                            DashedLine(start=circuit[4].get_right(), end=circuit[5].get_left(), stroke_width=2),
                            circuit[-2:],
                            r1,
                            r2,
                            rj,
                            rN,
                            E
                            ).scale(scale_factor=0.5).shift(UP)

        U = []
        U.append(VoltArrow(start=circuit[2].get_right(),end=circuit[2].get_left(),dipole=circuit[2],name="U_1",side=DOWN,buff_name=0.,buff_side=0.5))
        U.append(VoltArrow(start=circuit[3].get_right(),end=circuit[3].get_left(),dipole=circuit[3],name="U_2",side=DOWN,buff_name=0,buff_side=0.5))
        U.append(VoltArrow(start=circuit[4].get_right(),end=circuit[4].get_left(),dipole=circuit[4],name="U_i",side=DOWN,buff_name=0,buff_side=0.5))
        U.append(VoltArrow(start=circuit[5].get_right(),end=circuit[5].get_left(),dipole=circuit[5],name="U_n",side=DOWN,buff_name=0,buff_side=0.5))

        for ar in U :
            ar.label.scale(0.7)

        eq = MathTex(r"U_i", r"=", r"{ {{R_i}} \over \sum\limits_{j=1}^{n} R_j }", r"E").scale(0.75).shift(DOWN)

        self.play(Write(titre))
        self.wait(2)
        self.play(titre.animate.to_edge(UP))
        self.play(FadeIn(circuit_f, shift=DOWN))
        self.wait(2)
        self.play(*[GrowArrow(i) for i in U])
        self.wait(2)
        self.play(Write(eq),run_time=2)
        self.wait(4)

class TestCourant(Scene):
    def construct(self):
        square = Square()

        #I = Arrow(start=DOWN,end=UP).move_to(square.get_left()).scale(factor=0.1, scale_tips=False)
        ball = Circle(radius=0.1, fill_color=RED, fill_opacity=1).move_to(LEFT)
        ball.vx, ball.vy = 0.05, 0.05

        def ball_updater(c):
            sens = "CCW" # Décision du sens du courant

            point_x = c.get_x() - square.get_x()
            point_y = c.get_y() - square.get_y()

            if point_x >= 0 :
                # Cadran RIGHT
                dir_x = RIGHT
            else:
                # Cadran LEFT
                dir_x = LEFT

            if point_y >= 0:
                dir_y = UP
            else:
                dir_y = DOWN


            # if sens is "CCW":
            start_point = c.get_center()

            try:
                end_point = square.point_from_proportion(square.proportion_from_point(start_point)+0.02)
                print("ok ", square.proportion_from_point(start_point))
            except ValueError:
                end_point = square.point_from_proportion(0.25)
                # print("err ", square.proportion_from_point(start_point))

            c.move_to(end_point)

        self.add(square, ball)
        ball.add_updater(ball_updater)
        #self.play(ball.animate.move_to(square.get_corner(UP+LEFT)))
        self.wait(5,frozen_frame=False)
        # self.play(MoveAlongPath(ball,square),run_time=2,rate_func=linear)
        # self.wait(2,frozen_frame=False)

