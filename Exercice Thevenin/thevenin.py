import numpy
import numpy as np
from manim import *
from manim_fonts import *

config.background_color = BLACK
config["background_color"] = BLACK


class Generique_Ex(Scene):

    def construct(self):
        text_logo = Text("Elec", font_size=80, font="Playwrite MX")

        image_logo = VGroup(Arc(angle=PI, color=YELLOW_B),
                            Cross(scale_factor=0.2).rotate(45 * DEGREES).shift(UP / 2.5).set_color(YELLOW)
                            ).rotate(-90 * DEGREES).next_to(text_logo, RIGHT)

        logo = VGroup(text_logo, image_logo).move_to((0., 0., 0.))
        intro = AnimationGroup(Write(text_logo),
                               Create(image_logo)
                               )
        texte = Text("Résolution d'exercice", font_size=48, font="Playwrite MX", color=TEAL).shift(DOWN * 2)
        # self.add(Circle(0.1,RED,fill_opacity=1))
        self.play(AnimationGroup(intro, Write(texte), lag_ratio=0.25), run_time=1.5)
        self.wait(2)


class Exercice(Scene):

    def construct(self):
        # self.add(Circle(0.1, RED, fill_opacity=1))

        frame = FullScreenRectangle()
        self.add(frame)

        titre = Text("Transformation Thévenin - Norton", font="Playwrite MX", color=TEAL_A, font_size=36)
        exercice = Text("Exercice", font="Playwrite MX", color=TEAL, font_size=20).to_corner(UL)
        self.play(Write(titre))
        self.play(Write(exercice), Create(Underline(exercice, color=TEAL, stroke_width=2)),
                  titre.animate.scale_to_fit_height(exercice.height).next_to(exercice, DOWN, aligned_edge=LEFT))
        self.wait(2)

        split_line = Line(start=UP, end=DOWN, stroke_width=5, color=TEAL_A).stretch_to_fit_height(
            config["frame_height"] * 0.9).shift(LEFT)
        self.play(GrowFromEdge(split_line, DOWN))

        page1 = Rectangle(color=BLUE).stretch_to_fit_height(frame.height).stretch_to_fit_width(
            Line(start=frame.get_left(), end=split_line.get_center(), buff=0).width).to_edge(LEFT, buff=0)
        page2 = Rectangle(color=RED).stretch_to_fit_height(frame.height).stretch_to_fit_width(
            frame.width - page1.width).to_edge(RIGHT, buff=0)
        # self.add(page1,page2)
        self.wait(2)

        tex_template = TexTemplate()
        tex_template.add_to_preamble(r"\usepackage[siunitx, RPvoltages, european]{circuitikz}")

        circuit_full = VGroup()
        circuit = MathTex(
            r"\draw (0,0) to [american voltage source] (0,2);",  # E1      0
            r"\draw (0,2) to [R] (0,4);",  # R1    1
            r"\draw (0,4) to [short] (2,4);",
            r"\draw (2,4) to [R] (2,0);",  # R2    3
            r"\draw (2,0) to [short] (0,0);",
            r"\draw (2,4) to [short] (4,4);",
            r"\draw (4,4) to [current source] (4,0);",  # I2    6
            r"\draw (4,0) to [short] (2,0);",
            r"\draw (4,0) to [short] (6,0);",
            r"\draw (6,0) to [american voltage source] (6,2);",  # E3    9
            r"\draw (6,2) to [R] (6,4);",  # R3    10
            r"\draw (6,4) to [short] (4,4);",
            r"\draw (6,0) to [short] (8,0);",
            r"\draw (8,0) to [R] (8,4);",  # R4    13
            r"\draw (8,4) to [short] (6,4);",
            tex_environment="circuitikz",
            tex_template=tex_template,
            stroke_color=WHITE,
            stroke_width=2,
            fill_color=WHITE
        )

        R1 = MathTex("R_1").next_to(circuit[1], LEFT)
        E1 = MathTex("E_1").next_to(circuit[0], LEFT)
        R2 = MathTex("R_2").next_to(circuit[3], RIGHT)
        I2 = VGroup()
        I2.arrow = Arrow(start=DOWN, end=UP, tip_shape=StealthTip, stroke_width=0, color=TEAL_A, buff=0).move_to(
            circuit[6].get_center() + UP * 1.5).set_length(0.001)
        I2.text = MathTex("I_2").next_to(I2.arrow, LEFT)
        I2.add(I2.arrow, I2.text)
        E3 = MathTex("E_3").next_to(circuit[9], LEFT)
        R3 = MathTex("R_3").next_to(circuit[10], LEFT)
        R4 = MathTex("R_4").next_to(circuit[13], RIGHT)
        I4 = VGroup()
        I4.arrow = Arrow(start=UP, end=DOWN, tip_shape=StealthTip, stroke_width=0, color=TEAL_A, buff=0).move_to(
            circuit[13].get_center() + UP * 1.5).set_length(0.001)
        I4.text = MathTex("I_4").next_to(I4.arrow, LEFT)
        I4.add(I4.arrow, I4.text)

        circuit_text = VGroup()
        circuit_text.add(R1, E1, R2, I2, E3, R3, R4, I4)
        circuit_full.add(circuit, circuit_text).scale_to_fit_width(page1.width * 0.9).next_to(titre, DOWN,
                                                                                              aligned_edge=LEFT)

        consigne = Tex(r"{30em}\par En utilisant la technique de la transformation de Thévenin-Norton,"
                       r" déterminer le courant $I_4$ dans la résistance $R_4$ du circuit ci-dessus."
                       r"\\"
                       r" \newline On donne : \\ \par - $R_1=\SI{60}{\ohm}$ \par - $R_2=\SI{100}{\ohm}$ \par - $R_3=\SI{30}{\ohm}$ \par - $R_4=\SI{40}{\ohm}$ \par - $E_1=\SI{10}{V}$ \par - $I_2=\SI{100}{mA}$ \par - $E_3=\SI{7}{V}$",
                       tex_environment="minipage",
                       font_size=12,
                       tex_template=tex_template).scale_to_fit_width(circuit_full.width).next_to(circuit_full, DOWN,
                                                                                                 aligned_edge=LEFT)
        # appnum = Tex(r"\item[-] $R_1=\SI{60}{\ohm}$",
        #              r"\item $R_2=\SI{100}{\ohm}$",
        #              tex_environment="itemize",
        #              tex_template=tex_template).scale_to_fit_width(circuit_full.width * 0.5).next_to(consigne, DOWN,
        #                                                                                               aligned_edge=LEFT).shift(
        #     RIGHT)

        self.play(Create(circuit), Write(circuit_text), Write(consigne))
        self.wait(2)

        correction = VGroup()

        rappel = Text("Rappels", font="Playwrite MX", color=TEAL, font_size=20).next_to(split_line.get_top(),
                                                                                        direction=RIGHT,
                                                                                        aligned_edge=UP)
        underline_rappel = Underline(rappel, color=TEAL, stroke_width=2, buff=-0.05)
        th_de_thevenin = Text("Théorème de Thévenin", font="Playwrite MX", color=TEAL_A, font_size=14).next_to(rappel,
                                                                                                               direction=DOWN,
                                                                                                               aligned_edge=LEFT,
                                                                                                               buff=0.05)
        correction.add(rappel, th_de_thevenin, underline_rappel)
        self.play(Write(rappel), Create(underline_rappel), Write(th_de_thevenin))
        self.wait(2)

        enonce_thevenin = Tex(
            r"{37em}Tout circuit linéaire est équivalent à un générateur de tension dit « de Thévenin » de tension $E_{\textrm{th}}$ et de résistance interne $R_{\textrm{th}}$.",
            font_size=20,
            tex_environment="minipage"
        ).next_to(th_de_thevenin, DOWN, aligned_edge=LEFT)
        correction.add(enonce_thevenin)
        circuit_th = MathTex(
            r"\draw (0,0) to [american voltage source] (0,2);",  # E1      0
            r"\draw (0,2) to [R] (2,2);",  # R1    1
            r"\draw (0,0) to [short] (2,0);",  # R1    1
            tex_environment="circuitikz",
            tex_template=tex_template,
            stroke_color=WHITE,
            stroke_width=2,
            fill_color=WHITE
        )
        circuit_th.add(Dot(circuit_th[1].get_right(), 0.15, color=TEAL_A),
                       Tex("A").next_to(circuit_th[1].get_right(), RIGHT),
                       Dot(circuit_th[2].get_right(), 0.15, color=TEAL_A),
                       Tex("B").next_to(circuit_th[2].get_right(), RIGHT),
                       MathTex(r"R_{\textrm{th}}").next_to(circuit_th[1], UP),
                       MathTex(r"E_{\textrm{th}}").next_to(circuit_th[0], LEFT)
                       )

        circuit_th.scale_to_fit_height(circuit_full.height * 0.75).next_to(enonce_thevenin, DOWN)
        correction.add(circuit_th)

        self.play(Write(enonce_thevenin), Create(circuit_th))
        self.wait(2)

        texte_rth = Tex(
            r"{37em}Pour calculer $R_{\textrm{th}}$, il suffit « d'éteindre les générateurs » et de calculer la résistance équivalente du circuit",
            font_size=20,
            tex_environment="minipage",
        ).next_to(circuit_th, DOWN)
        correction.add(texte_rth)
        self.play(Write(texte_rth))
        self.wait(2)

        Vsource = MathTex(
            r"\draw (0,0) to [american voltage source] (0,2);",  # E1      0
            tex_environment="circuitikz",
            tex_template=tex_template,
            stroke_color=WHITE,
            stroke_width=2,
            fill_color=WHITE
        )

        closed_switch = MathTex(
            r"\draw (0,0) to [ccsw] (0,2);",  # E1      0
            tex_environment="circuitikz",
            tex_template=tex_template,
            stroke_color=WHITE,
            stroke_width=2,
            fill_color=WHITE
        )

        Isource = MathTex(
            r"\draw (0,0) to [current source] (0,2);",  # E1      0
            tex_environment="circuitikz",
            tex_template=tex_template,
            stroke_color=WHITE,
            stroke_width=2,
            fill_color=WHITE
        )

        open_switch = MathTex(
            r"\draw (0,0) to [cosw] (0,2);",  # E1      0
            tex_environment="circuitikz",
            tex_template=tex_template,
            stroke_color=WHITE,
            stroke_width=2,
            fill_color=WHITE
        )

        eq_group = VGroup(Vsource, closed_switch, Isource, open_switch).arrange(RIGHT, buff=2).scale_to_fit_height(
            page2.height * 0.2).next_to(texte_rth, DOWN)

        arrow_1 = Arrow(start=Vsource.get_right(), end=closed_switch.get_center(), color=TEAL_A)
        arrow_2 = Arrow(start=Isource.get_right(), end=open_switch.get_center(), color=TEAL_A)

        eq_group.add(arrow_1, arrow_2)
        correction.add(eq_group)
        self.play(Create(eq_group))
        self.wait(2)

        self.play(correction.animate.shift(UP * 4))
        self.wait(2)

        texte_eth = Tex(
            r"{37em}Pour calculer $E_{\textrm{th}}$, il faut « débrancher » les bornes du circuit que l'on cherche à transformer et calculer la tension aux bornes du circuit ouvert. ",
            font_size=20,
            tex_environment="minipage",
        ).next_to(eq_group, DOWN)

        circuit_ouvert = circuit.copy()
        circuit_ouvert.remove(circuit_ouvert[13])
        circuit_ouvert_texte = circuit_text.copy()[:-2]
        eth_arrow = Arrow(circuit_ouvert[-2].get_right(), circuit_ouvert[-1].get_right(), color=TEAL_A, stroke_width=2,
                          tip_length=I2.arrow.tip_length * 0.4, tip_shape=StealthTip)
        circuit_ouvert.add(Dot(circuit_ouvert[-1].get_right(), 0.05 * circuit_ouvert[-1].width, color=TEAL_A),
                           Tex("A", font_size=R3.font_size).next_to(circuit_ouvert[-1].get_right(), RIGHT),
                           Dot(circuit_ouvert[-2].get_right(), 0.05 * circuit_ouvert[-1].width, color=TEAL_A),
                           Tex("B", font_size=R3.font_size).next_to(circuit_ouvert[-2].get_right(), RIGHT),
                           eth_arrow,
                           MathTex(r"E_{\textrm{th}}", color=TEAL_A, font_size=R3.font_size).next_to(eth_arrow, RIGHT)
                           )

        circuit_ouvert_full = VGroup(circuit_ouvert_texte, circuit_ouvert).scale_to_fit_height(
            circuit_full.height).next_to(texte_eth, DOWN)

        correction.add(circuit_ouvert_full, texte_eth)
        self.play(Write(texte_eth), Create(circuit_ouvert_full))
        self.wait(2)

        self.play(correction.animate.shift(UP * 3))
        self.wait(2)

        th_de_norton = Text("Théorème de Norton", font="Playwrite MX", color=TEAL_A, font_size=14).next_to(
            circuit_ouvert_full, direction=DOWN, buff=0.05).align_to(th_de_thevenin, LEFT)
        correction.add(th_de_norton)
        self.play(Write(th_de_norton))
        self.wait(2)

        enonce_norton = Tex(
            r"{37em}Tout réseau linéaire dipolaire est équivalent à un générateur de courant dit « de Norton », de courant $I_{\textrm{no}}$ et de résistance interne $R_{\textrm{no}}$ égale à la résistance interne $R_{\textrm{th}}$ du générateur de Thévenin.",
            font_size=20,
            tex_environment="minipage"
        ).next_to(th_de_norton, DOWN, aligned_edge=LEFT)
        correction.add(enonce_norton)
        circuit_no = MathTex(
            r"\draw (0,0) to [current source] (0,2);",
            r"\draw (2,0) to [R] (2,2);",
            r"\draw (0,2) to [short] (4,2);",
            r"\draw (0,0) to [short] (4,0);",
            tex_environment="circuitikz",
            tex_template=tex_template,
            stroke_color=WHITE,
            stroke_width=2,
            fill_color=WHITE
        )
        I = VGroup()
        I.arrow = Arrow(start=DOWN, end=UP, tip_shape=StealthTip, stroke_width=0, color=TEAL_A, buff=0,
                        max_tip_length_to_length_ratio=0.1).move_to(
            circuit_no[0].get_center() + UP * 1.25).set_length(0.001)
        I.text = MathTex(r'I_{\textrm{no}}').next_to(I.arrow, LEFT)
        I.add(I.arrow, I.text)
        circuit_no.add(Dot(circuit_no[2].get_right(), 0.015 * circuit_no[2].width, color=TEAL_A),
                       Tex("A").next_to(circuit_no[2].get_right(), RIGHT),
                       Dot(circuit_no[3].get_right(), 0.015 * circuit_no[2].width, color=TEAL_A),
                       Tex("B").next_to(circuit_no[3].get_right(), RIGHT),
                       MathTex(r"R_{\textrm{no}}").next_to(circuit_no[1], LEFT),
                       I
                       )

        circuit_no.scale_to_fit_height(circuit_full.height * 0.75).next_to(enonce_norton, DOWN)
        correction.add(circuit_no)

        self.play(Write(enonce_norton), Create(circuit_no))
        self.wait(2)

        self.play(correction.animate.shift(UP * 2.25))
        self.wait(2)

        texte_ino = Tex(
            r"{37em}Pour calculer $I_{\textrm{no}}$, il faut \textit{court-circuiter} les bornes du circuit que l'on cherche à transformer et calculer l'intensité du courant qui traverse le court-circuit. ",
            font_size=20,
            tex_environment="minipage",
        ).next_to(circuit_no, DOWN)

        circuit_ferme = circuit.copy()
        circuit_ferme.remove(circuit_ferme[-2])
        circuit_ferme_texte = circuit_text.copy()[:-2]
        ino_arrow = Arrow(start=UP, end=DOWN, tip_shape=StealthTip, stroke_width=0, color=TEAL_A, buff=0,
                          max_tip_length_to_length_ratio=0.08)
        circuit_ferme.add(Dot(circuit_ferme[-1].get_right(), 0.05 * circuit_ferme[-1].width, color=TEAL_A),
                          Tex("A", font_size=R3.font_size).next_to(circuit_ferme[-1].get_right(), RIGHT),
                          Dot(circuit_ferme[-2].get_right(), 0.05 * circuit_ferme[-1].width, color=TEAL_A),
                          Tex("B", font_size=R3.font_size).next_to(circuit_ferme[-2].get_right(), RIGHT),
                          ino_arrow,
                          Line(start=circuit_ferme[-1].get_right(), end=circuit_ferme[-2].get_right(), color=TEAL_A,
                               stroke_width=3)
                          )

        ino_arrow.move_to(circuit_ferme[-1].get_center()).set_length(0.001).scale(0.25)
        circuit_ferme.add(MathTex(r"I_{\textrm{no}}", color=TEAL_A, font_size=R3.font_size).next_to(ino_arrow, RIGHT))
        circuit_ferme_full = VGroup(circuit_ferme, circuit_ferme_texte).scale_to_fit_height(
            circuit_full.height).next_to(texte_ino, DOWN)

        correction.add(circuit_ferme_full, texte_ino)
        self.play(Write(texte_ino), Create(circuit_ferme_full))
        self.wait(2)


class Exercice2(Scene):
    def construct(self):
        frame = FullScreenRectangle()
        self.add(frame)

        titre = Text("Transformation Thévenin - Norton", font="Playwrite MX", color=TEAL_A, font_size=36)
        exercice = Text("Exercice", font="Playwrite MX", color=TEAL, font_size=20).to_corner(UL)
        self.play(Write(titre))
        self.play(Write(exercice), Create(Underline(exercice, color=TEAL, stroke_width=2)),
                  titre.animate.scale_to_fit_height(exercice.height).next_to(exercice, DOWN, aligned_edge=LEFT))
        self.wait(2)

        split_line = Line(start=UP, end=DOWN, stroke_width=5, color=TEAL_A).stretch_to_fit_height(
            config["frame_height"] * 0.9).shift(LEFT)
        self.play(GrowFromEdge(split_line, DOWN))

        page1 = Rectangle(color=BLUE).stretch_to_fit_height(frame.height).stretch_to_fit_width(
            Line(start=frame.get_left(), end=split_line.get_center(), buff=0).width).to_edge(LEFT, buff=0)
        page2 = Rectangle(color=RED).stretch_to_fit_height(frame.height).stretch_to_fit_width(
            frame.width - page1.width).to_edge(RIGHT, buff=0)
        # self.add(page1,page2)
        self.wait(2)

        tex_template = TexTemplate()
        tex_template.add_to_preamble(r"\usepackage[siunitx, RPvoltages, european]{circuitikz}")

        circuit_full = VGroup()
        circuit = MathTex(
            r"\draw (0,0) to [american voltage source] (0,2);",  # E1      0
            r"\draw (0,2) to [R] (0,4);",  # R1    1
            r"\draw (0,4) to [short] (2,4);",
            r"\draw (2,4) to [R] (2,0);",  # R2    3
            r"\draw (2,0) to [short] (0,0);",
            r"\draw (2,4) to [short] (4,4);",
            r"\draw (4,4) to [current source] (4,0);",  # I2    6
            r"\draw (4,0) to [short] (2,0);",
            r"\draw (4,0) to [short] (6,0);",
            r"\draw (6,0) to [american voltage source] (6,2);",  # E3    9
            r"\draw (6,2) to [R] (6,4);",  # R3    10
            r"\draw (6,4) to [short] (4,4);",
            r"\draw (6,0) to [short] (8,0);",
            r"\draw (8,0) to [R] (8,4);",  # R4    13
            r"\draw (8,4) to [short] (6,4);",
            tex_environment="circuitikz",
            tex_template=tex_template,
            stroke_color=WHITE,
            stroke_width=2,
            fill_color=WHITE
        )

        R1 = MathTex("R_1").next_to(circuit[1], LEFT)
        E1 = MathTex("E_1").next_to(circuit[0], LEFT)
        R2 = MathTex("R_2").next_to(circuit[3], RIGHT)
        I2 = VGroup()
        I2.arrow = Arrow(start=DOWN, end=UP, tip_shape=StealthTip, stroke_width=0, color=TEAL_A, buff=0).move_to(
            circuit[6].get_center() + UP * 1.5).set_length(0.001)
        I2.text = MathTex("I_2").next_to(I2.arrow, LEFT)
        I2.add(I2.arrow, I2.text)
        E3 = MathTex("E_3").next_to(circuit[9], LEFT)
        R3 = MathTex("R_3").next_to(circuit[10], LEFT)
        R4 = MathTex("R_4").next_to(circuit[13], RIGHT)
        I4 = VGroup()
        I4.arrow = Arrow(start=UP, end=DOWN, tip_shape=StealthTip, stroke_width=0, color=TEAL_A, buff=0).move_to(
            circuit[13].get_center() + UP * 1.5).set_length(0.001)
        I4.text = MathTex("I_4").next_to(I4.arrow, LEFT)
        I4.add(I4.arrow, I4.text)

        circuit_text = VGroup()
        circuit_text.add(R1, E1, R2, I2, E3, R3, R4, I4)
        circuit_full.add(circuit, circuit_text).scale_to_fit_width(page1.width * 0.9).next_to(titre, DOWN,
                                                                                              aligned_edge=LEFT)

        consigne = Tex(r"{30em}\par En utilisant la technique de la transformation de Thévenin-Norton,"
                       r" déterminer le courant $I_4$ dans la résistance $R_4$ du circuit ci-dessus."
                       r"\\"
                       r" \newline On donne : \\ \par - $R_1=\SI{60}{\ohm}$ \par - $R_2=\SI{100}{\ohm}$ \par - $R_3=\SI{30}{\ohm}$ \par - $R_4=\SI{40}{\ohm}$ \par - $E_1=\SI{10}{V}$ \par - $I_2=\SI{100}{mA}$ \par - $E_3=\SI{7}{V}$",
                       tex_environment="minipage",
                       font_size=12,
                       tex_template=tex_template).scale_to_fit_width(circuit_full.width).next_to(circuit_full, DOWN,
                                                                                                 aligned_edge=LEFT)
        # appnum = Tex(r"\item[-] $R_1=\SI{60}{\ohm}$",
        #              r"\item $R_2=\SI{100}{\ohm}$",
        #              tex_environment="itemize",
        #              tex_template=tex_template).scale_to_fit_width(circuit_full.width * 0.5).next_to(consigne, DOWN,
        #                                                                                               aligned_edge=LEFT).shift(
        #     RIGHT)

        self.play(Create(circuit), Write(circuit_text), Write(consigne))
        self.wait(2)

        correction = VGroup()
        register_font("..\PlaywriteMX-VariableFont_wght.ttf")
        resolution = Text("Résolution de l'exercice", font='Playwrite MX', color=MAROON, font_size=20).next_to(
                split_line.get_top(),
                direction=RIGHT,
                aligned_edge=UP)
        underline_resolution = Underline(resolution, color=MAROON, stroke_width=2)
        # th_de_thevenin = Text("Théorème de Thévenin", font="Playwrite MX", color=TEAL_A, font_size=14).next_to(rappel,
        #                                                                                                        direction=DOWN,
        #                                                                                                        aligned_edge=LEFT,
        #                                                                                                        buff=0.05)
        correction.add(resolution, underline_resolution)
        self.play(Write(resolution), Create(underline_resolution))
        self.wait(2)


class CArrayElement(VMobject):
    def __init__(self, value, index, **kwargs: any):
        super().__init__(**kwargs)
        self.value = MathTex(str(value))
        self.index = Tex(str(index))
        self.square = Square(side_length=1)
        self.value.move_to(self.square.get_center())
        self.index.next_to(self.square, UP)
        self.add(self.square, self.value, self.index)


class Tableau(Scene):
    def construct(self):
        element = CArrayElement(value="0", index="tab")
        self.play(Write(element))
        self.wait(2)
