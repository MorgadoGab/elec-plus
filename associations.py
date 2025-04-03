import numpy
import numpy as np
from manim import *
from manim_fonts import *

config.background_color = BLACK
config["background_color"] = BLACK

class Generique(Scene):

    def construct(self):
        text_logo = Text("Elec",font_size=80,font="Playwrite MX")

        image_logo = VGroup(Arc(angle=PI,color=YELLOW_B),
                           Cross(scale_factor=0.2).rotate(45*DEGREES).shift(UP/2.5).set_color(YELLOW)
                           ).rotate(-90*DEGREES).next_to(text_logo,RIGHT)

        logo = VGroup(text_logo,image_logo).move_to((0.,0.,0.))
        intro = AnimationGroup(Write(text_logo),
                               Create(image_logo)
        )
        # self.add(Circle(0.1,RED,fill_opacity=1))
        self.play(intro,run_time=1.5)
        self.wait()

class Serie(Scene):

    def construct(self):
        # self.add(Circle(0.1, RED, fill_opacity=1))

        titre = Tex("Association en série").to_edge(UP)
        serie = Text("Série :",color=YELLOW_E).to_corner(UL)

        anim1 = AnimationGroup(FadeTransform(titre[-5:],serie),
                               FadeOut(titre[:-5],shift=UP),
                               lag_ratio=0.1
                               )

        tex_template = TexTemplate()
        tex_template.add_to_preamble(r"\usepackage[siunitx, RPvoltages, european]{circuitikz}")

        text1=Tex("Deux résistances sont considérées en ","série"," lorsqu'elles sont parcourues par le"," même courant",".",font_size=32)
        text1.to_edge(UP)

        circuit = MathTex(
            r"\draw (0,0) to [R] (0,-2);",
            r"\draw (0,-2) to [R] (0,-4);",
            # r"\draw (0,0) to [open,i=$I$] (0,-2);",
            tex_environment="circuitikz",
            tex_template=tex_template,
            stroke_color=WHITE,
            stroke_width=2,
            fill_color=WHITE
        )

        current_arrow = Arrow(start=UP,end=DOWN,tip_shape=StealthTip,stroke_width=0,color=BLUE,buff=0).next_to(circuit,UP,buff=-1.5).set_length(0.001)

        courant = VGroup(current_arrow,
            MathTex("I",color=BLUE).next_to(current_arrow,LEFT)
        )

        r1 = MathTex("R_1")
        r2 = MathTex("R_2")

        r1.next_to(circuit[0])
        r2.next_to(circuit[1])

        circuit_group = VGroup(circuit,r1,r2,courant).to_edge(DOWN)

        cross_group = VGroup(Cross(color=RED,scale_factor=0.15),
                             Cross(color=RED,scale_factor=0.15).shift(LEFT*1.2)
                             ).next_to(circuit[0],DOWN,buff=-0.1)

        box_req = Rectangle(color=BLUE,width=circuit.width*1.3,height=circuit.height*0.9).move_to(circuit.get_center_of_mass())

        eq = MathTex(r"R_{\textrm{eq}}","=","R_1","+","R_2").next_to(box_req)

        eq.set_color_by_tex(r"R_{\textrm{eq}}",BLUE)

        # self.add(index_labels(eq[1]))
        # self.add(index_labels(r1[0]))

        self.play(Write(titre))
        self.wait(1)
        self.play(Create(circuit),Create(courant),FadeIn(r1,r2,shift=LEFT),lag_ratio=0.2)
        self.wait(1)
        self.play(Create(box_req),FadeIn(eq[0],shift=LEFT))
        self.wait(1)
        self.play(FadeOut(box_req),FadeOut(eq[0]))
        self.play(TransformMatchingShapes(titre,text1))
        self.wait(1)
        self.play(Indicate(text1[1].set_color(ORANGE)))
        self.wait(1)
        self.play(Circumscribe(text1[-2:-1].set_color(BLUE),color=BLUE),Indicate(courant))
        self.wait(1)
        self.play(Flash(circuit,color=YELLOW,line_length=1,time_width=0.3))
        self.wait(1)
        self.play(Create(cross_group))
        self.wait(1)
        self.play(FadeOut(cross_group),Create(box_req),FadeIn(eq[0],shift=LEFT))
        self.wait(1)
        self.play(TransformMatchingTex(Group(r1,r2).copy(),eq,path_arc=-PI/2))
        self.wait(1.5)

class Parallele(Scene):

    def construct(self):
        # self.add(Circle(0.1, RED, fill_opacity=1))

        titre = Tex("Association en parallèle").to_edge(UP)
        serie = Text("Parallèle :",color=YELLOW_E).to_corner(UL)

        anim1 = AnimationGroup(FadeTransform(titre[-5:],serie),
                               FadeOut(titre[:-5],shift=UP),
                               lag_ratio=0.1
                               )

        tex_template = TexTemplate()
        tex_template.add_to_preamble(r"\usepackage[siunitx, RPvoltages, european]{circuitikz}")

        circuit = MathTex(
            r"\draw (0,0) to [short] (0,-1);",
            r"\draw (0,-1) to [short] (-0.5,-1);",
            r"\draw (0,-1) to [short] (0.5,-1);",
            r"\draw (-0.5,-1) to [R] (-0.5,-3);",
            r"\draw (0.5,-1) to [R] (0.5,-3);",
            r"\draw (-0.5,-3) to [short] (0,-3);",
            r"\draw (0.5,-3) to [short] (0,-3);",
            r"\draw (0,-3) to [short] (0,-4);",
            tex_environment="circuitikz",
            tex_template=tex_template,
            stroke_color=WHITE,
            stroke_width=2,
            fill_color=WHITE
        )

        r1 = MathTex("R_1").next_to(circuit[3],LEFT)
        r2 = MathTex("R_2").next_to(circuit[4])

        # current_arrow = Arrow(start=UP,end=DOWN,tip_shape=StealthTip,stroke_width=0,color=BLUE,buff=0).next_to(circuit,UP,buff=-2.5).set_length(0.001)
        #
        # courant = VGroup(current_arrow,
        #     MathTex("I",color=BLUE).next_to(current_arrow,LEFT)
        # )

        circuit_group = VGroup(circuit,r1,r2).to_edge(DOWN,buff=0.5)

        volt_arrow = Arrow(start=circuit.get_bottom()+UP,end=circuit.get_top()-UP,tip_shape=StealthTip,stroke_width=2,color=YELLOW_E).next_to(circuit,LEFT,buff=1)

        voltage = VGroup(volt_arrow,
            MathTex("U",color=YELLOW_E).next_to(volt_arrow,LEFT)
        )

        box_req = Rectangle(color=BLUE, width=circuit.width * 1.2, height=circuit.height * 0.7).move_to(
            circuit.get_center_of_mass())

        text1 = Tex("Deux résistances sont considérées en ", "parallèle", r" lorsqu'elles présentent \\la ",
                    "même tension", " à leurs bornes.", font_size=32)
        text1.to_edge(UP)

        req = MathTex(r"R_{\textrm{eq}}").next_to(box_req).set_color(BLUE).shift(DOWN)
        eq = MathTex(r"\dfrac{1}{R_{\textrm{eq}}}","=","\dfrac{1}{R_1}","+","\dfrac{1}{R_2}").next_to(box_req).shift(DOWN)

        eq.set_color_by_tex(r"R_{\textrm{eq}}",BLUE)

        self.play(Write(titre))
        self.wait(1)
        self.play(Create(circuit),FadeIn(r1,shift=RIGHT),FadeIn(r2,shift=LEFT))
        self.wait(1)
        self.play(Create(box_req),FadeIn(req,shift=LEFT))
        self.wait(1)
        self.play(FadeOut(box_req),FadeOut(req))
        self.play(TransformMatchingShapes(titre,text1))
        self.wait(1)
        self.play(Indicate(text1[1].set_color(ORANGE)))
        self.wait(1)
        self.play(Circumscribe(text1[-2].set_color(YELLOW_E)),Indicate(voltage))
        self.wait(1)
        self.play(ShowPassingFlashWithThinningStrokeWidth(circuit[0:3].copy().set(color=YELLOW_E,stroke_width=15),time_width=2.5),ShowPassingFlashWithThinningStrokeWidth(circuit[-3:].reverse_points().copy().set(color=YELLOW_E,stroke_width=15),time_width=2.5),run_time=2)
        self.wait(1)
        self.play(Create(box_req),FadeIn(req,shift=LEFT))
        self.wait(1)
        self.play(TransformMatchingShapes(Group(req,r1.copy(),r2.copy()),eq,path_arc=-PI/2))
        self.wait(1.5)

class Conclusion(Scene):
    def construct(self):

        tex_template = TexTemplate()
        tex_template.add_to_preamble(r"\usepackage[siunitx, RPvoltages, european]{circuitikz}")

        titre = Tex(r"Cas général")
        text1 = Tex(r"$N$ résistances en série")
        text2 = Tex(r"$N$ résistances en parallèle")

        text=VGroup(text1,text2).arrange(buff=3).to_edge(UP)

        circuit_serie = MathTex(
            r"\draw (0,0) to [R] (2,0);",
            r"\draw (2,0) to [R] (4,0);",
            r"\draw (4,0) to [short] (5,0);",
            r"\draw (5,0) to [R] (7,0);",
            tex_environment="circuitikz",
            tex_template=tex_template,
            stroke_color=WHITE,
            stroke_width=2,
            fill_color=WHITE
        ).next_to(text1,DOWN,buff=1)

        circuit_parallel = MathTex(
            r"\draw (0,0) to [short] (1,0);",
            r"\draw (1,0) to [short] (1,2);",
            r"\draw (1,1) to [R] (3,1);",
            r"\draw (1,2) to [R] (3,2);",
            r"\draw (3,0) to [short] (3,2);",
            r"\draw (1,0) to [short] (1,-1);",
            r"\draw (3,0) to [short] (3,-1);",
            r"\draw (3,0) to [short] (4,0);",
            r"\draw (1,-1) to [R] (3,-1);",
            tex_environment="circuitikz",
            tex_template=tex_template,
            stroke_color=WHITE,
            stroke_width=2,
            fill_color=WHITE
        ).next_to(text2,DOWN)

        r1 = MathTex("R_1").next_to(circuit_serie[0],UP)
        r2 = MathTex("R_2").next_to(circuit_serie[1],UP)
        rN = MathTex("R_N").next_to(circuit_serie[-1],UP)

        r1p = MathTex("R_1").next_to(circuit_parallel[3],UP)
        r2p = MathTex("R_2").next_to(circuit_parallel[2], UP)
        rNp = MathTex("R_N").next_to(circuit_parallel[-1], UP)

        circuit_serie_2 = VGroup(circuit_serie[:2],
                                 DashedLine(start=circuit_serie[:2].get_right(),end=circuit_serie[-1:].get_left(),stroke_width=2),
                                 circuit_serie[-1:],
                                 r1,
                                 r2,
                                 rN
                                 ).scale(scale_factor=0.5)

        circuit_parallel_2 = VGroup(circuit_parallel[:5],
                                 DashedLine(start=circuit_parallel[1].get_bottom(),end=circuit_parallel[-1].get_left(),stroke_width=2),
                                DashedLine(start=circuit_parallel[4].get_bottom(),end=circuit_parallel[-1].get_right(), stroke_width=2),
                                 circuit_parallel[-2:],
                                 r1p,
                                 r2p,
                                 rNp
                                 ).scale(scale_factor=0.7)

        box_req_serie = Rectangle(color=BLUE, width=circuit_serie_2.width * 0.95, height=circuit_serie_2.height * 1.2).move_to(
            circuit_serie_2.get_center())
        req_serie = MathTex(r"R_{\textrm{eq}}").next_to(box_req_serie, DOWN).set_color(BLUE)

        box_req_parallel = Rectangle(color=BLUE, width=circuit_parallel_2.width * 0.8, height=circuit_parallel_2.height * 1.1).move_to(
            circuit_parallel_2.get_center())
        req_parallel = MathTex(r"R_{\textrm{eq}}").next_to(box_req_parallel, DOWN).set_color(BLUE)

        eq_serie1 = MathTex(r"R_{\textrm{eq}}=R_1+R_2+...+R_N").next_to(circuit_serie_2, DOWN, buff=2)
        eq_serie2 = MathTex(r"R_{\textrm{eq}}=\sum_{i=0}^{N} R_i").next_to(circuit_serie_2,DOWN,buff=2)

        eq_parallel1 = MathTex(r"\dfrac{1}{R_{\textrm{eq}}}=\dfrac{1}{R_1}+\dfrac{1}{R_2}+...+\dfrac{1}{R_N}").next_to(box_req_parallel, DOWN, buff=1)
        eq_parallel2 = MathTex(r"\dfrac{1}{R_{\textrm{eq}}}=\sum_{i=0}^{N} \dfrac{1}{R_i}").next_to(box_req_parallel, DOWN, buff=0.9)

        self.play(Write(titre))
        self.wait(1)
        self.play(TransformMatchingShapes(titre,text),Create(Line(start=config.bottom,end=config.top,color=BLUE)))
        self.wait(1)
        self.play(FadeIn(circuit_serie_2,shift=UP))
        self.wait(1)
        self.play(Create(box_req_serie),Write(req_serie))
        self.wait(1)
        self.play(TransformMatchingShapes(VGroup(req_serie,r1.copy(),r2.copy(),rN.copy()),eq_serie1))
        self.wait(1)
        self.play(TransformMatchingShapes(eq_serie1,eq_serie2))
        self.wait(1)
        self.play(FadeOut(box_req_serie),TransformMatchingShapes(circuit_serie_2.copy(),circuit_parallel_2))
        self.wait(1)
        self.play(Create(box_req_parallel),Write(req_parallel))
        self.wait(1)
        self.play(TransformMatchingShapes(VGroup(req_parallel,r1p,r2p,rNp),eq_parallel1))
        self.wait(1)
        self.play(TransformMatchingShapes(eq_parallel1,eq_parallel2))
        self.wait(1.5)




