import numpy
import numpy as np
from manim import *
from manim_fonts import *

config.background_color = BLACK
config["background_color"] = BLACK

fancy_font = "Playwrite CL"
std_font_size = 20

class I_Arrow(VGroup):
    def __init__(self,start,end, text, place, tip_shape=StealthTip, direction_text=RIGHT, color=WHITE, color_text=WHITE, **kwargs: any):
        super().__init__(**kwargs)
        self.place = place
        self.arrow = Arrow(start=start, end=end, tip_shape=tip_shape, stroke_width=0, buff=0, color=color).move_to(self.place).set_length(0.001)
        self.text = MathTex(text,color=color_text).next_to(self.arrow, direction=direction_text)
        self.add(self.arrow, self.text)

class Generique_Ex(Scene):

    def construct(self):
        text_logo = Text("Elec", font_size=80, font=fancy_font)

        image_logo = VGroup(Arc(angle=PI, color=YELLOW_B),
                            Cross(scale_factor=0.2).rotate(45 * DEGREES).shift(UP / 2.5).set_color(YELLOW)
                            ).rotate(-90 * DEGREES).next_to(text_logo, RIGHT)

        logo = VGroup(text_logo, image_logo).move_to((0., 0., 0.))
        intro = AnimationGroup(Write(text_logo),
                               Create(image_logo)
                               )
        texte = Text("Résolution d'exercice", font_size=48, font=fancy_font, color=TEAL).shift(DOWN * 2)
        # self.add(Circle(0.1,RED,fill_opacity=1))
        self.play(AnimationGroup(intro, Write(texte), lag_ratio=0.25), run_time=1.5)
        self.wait(2)


class Exercice(Scene):

    def construct(self):
        # self.add(Circle(0.1, RED, fill_opacity=1))

        frame = FullScreenRectangle()
        self.add(frame)

        titre = Text("Transformation Thévenin - Norton", font=fancy_font, color=TEAL_A, font_size=std_font_size*1.5)
        exercice = Text("Exercice", font=fancy_font, color=TEAL, font_size=std_font_size).to_corner(UL)
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

        rappel = Text("Rappels", font=fancy_font, color=TEAL, font_size=std_font_size).next_to(split_line.get_top(),
                                                                                        direction=RIGHT,
                                                                                        aligned_edge=UP)
        underline_rappel = Underline(rappel, color=TEAL, stroke_width=2, buff=-0.05)
        th_de_thevenin = Text("Théorème de Thévenin", font=fancy_font, color=TEAL_A, font_size=std_font_size*0.7).next_to(rappel,
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

        th_de_norton = Text("Théorème de Norton", font=fancy_font, color=TEAL_A, font_size=std_font_size*0.7).next_to(
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

        exercice = Text("Exercice", font=fancy_font, color=TEAL, font_size=std_font_size).to_corner(UL)
        titre = Text("Transformation Thévenin - Norton", font=fancy_font, color=TEAL_A, font_size=std_font_size*1.5).scale_to_fit_height(exercice.height).next_to(exercice, DOWN, aligned_edge=LEFT)
        self.add(exercice, Underline(exercice, color=TEAL, stroke_width=2), titre)

        split_line = Line(start=UP, end=DOWN, stroke_width=5, color=TEAL_A).stretch_to_fit_height(
            config["frame_height"] * 0.9).shift(LEFT)
        self.add(split_line)

        page1 = Rectangle(color=BLUE).stretch_to_fit_height(frame.height).stretch_to_fit_width(
            Line(start=frame.get_left(), end=split_line.get_center(), buff=0).width).to_edge(LEFT, buff=0)
        page2 = Rectangle(color=RED).stretch_to_fit_height(frame.height).stretch_to_fit_width(
            frame.width - page1.width).to_edge(RIGHT, buff=0)
        # self.add(page1,page2)

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

        # self.play(Create(circuit), Write(circuit_text), Write(consigne))
        self.add(circuit,circuit_text,consigne)

        self.wait()
        correction = VGroup()
        resolution = Text("Résolution de l'exercice", font=fancy_font, color=MAROON_B, font_size=std_font_size).next_to(
                split_line.get_top(),
                direction=RIGHT,
                aligned_edge=UP)
        underline_resolution = Underline(resolution, color=MAROON_B, stroke_width=2)

        res_text = Text("Equivalence Thévenin-Norton", font=fancy_font, color=MAROON_A, font_size=std_font_size*0.7).next_to(
            resolution,
            direction=DOWN,
            aligned_edge = LEFT
        )

        texte_rth = Tex(
            r"{37em}On remplace les générateurs de tension par des générateurs de courant équivalents. ",
            font_size=20,
            tex_environment="minipage",
        ).next_to(res_text, DOWN, aligned_edge=LEFT)

        correction.add(resolution, underline_resolution, res_text)
        self.play(Write(resolution), Create(underline_resolution), Write(res_text))
        self.wait(2)

        circuit_res = circuit.copy()
        circuit_res.remove(circuit_res[-2]).next_to(texte_rth,DOWN,aligned_edge=LEFT)
        circuit_res_texte = circuit_text.copy()
        circuit_res_texte.remove(*circuit_res_texte[-2:])
        circuit_res_texte.next_to(circuit_res[6].get_center(),submobject_to_align=circuit_res_texte[3][0].set_color(MAROON_A),direction=UP,buff=0.5)
        circuit_res_full = VGroup()
        circuit_res_full.add(circuit_res,circuit_res_texte).next_to(texte_rth.get_center(),DOWN)

        A = VGroup(Dot(circuit_res[-1].get_right(), 0.05 * circuit_res[-1].width, color=MAROON_A),
        Tex("A", font_size=R3.font_size).next_to(circuit_res[-1].get_right(), RIGHT))
        B = VGroup( Dot(circuit_res[-2].get_right(), 0.05 * circuit_res[-1].width, color=MAROON_A),
        Tex("B", font_size=R3.font_size).next_to(circuit_res[-2].get_right(), RIGHT))
        circuit_res.add(A,B)

        self.play(Write(texte_rth),Create(circuit_res),Write(circuit_res_texte))
        self.wait()

        arrow = Arrow(start=UP,end=DOWN,color=MAROON_B,max_tip_length_to_length_ratio=0.15).next_to(circuit_res,DOWN,buff=-0.2).scale(0.5)
        ino = MathTex(r"I_{\textrm{no}}=\dfrac{E_{\textrm{th}}}{R_{\textrm{th}}}",color=MAROON_A).scale_to_fit_height(arrow.height).next_to(arrow,RIGHT)

        self.play(GrowArrow(arrow),Write(ino))
        self.wait()

        circuit_eq = MathTex(
            r"\draw (0,0) to [current source] (0,4);",  # E1      0
            r"\draw (1,0) to [R] (1,4);",  # R1    1
            r"\draw (0,4) to [short] (2,4);",
            r"\draw (2,4) to [R] (2,0);",  # R2    3
            r"\draw (2,0) to [short] (0,0);",
            r"\draw (2,4) to [short] (4,4);",
            r"\draw (3.5,4) to [current source] (3.5,0);",  # I2    6
            r"\draw (4,0) to [short] (2,0);",
            r"\draw (4,0) to [short] (6,0);",
            r"\draw (5.5,0) to [current source] (5.5,4);",  # E3    9
            r"\draw (6.5,0) to [R] (6.5,4);",  # R3    10
            r"\draw (6,4) to [short] (4,4);",
            r"\draw (6,0) to [short] (8,0);",
            r"\draw (8,0) to [short] (8,4);",  # R4    13
            r"\draw (8,4) to [short] (6,4);",
            tex_environment="circuitikz",
            tex_template=tex_template,
            stroke_color=WHITE,
            stroke_width=2,
            fill_color=WHITE
        )

        R1 = MathTex("R_1",color=MAROON_B).move_to(circuit_eq[1])
        # I1 = VGroup()
        # I1.arrow = Arrow(start=DOWN, end=UP, tip_shape=StealthTip, stroke_width=0, color=MAROON_A, buff=0).move_to(
        #     circuit_eq[0].get_center() + UP * 1.5).set_length(0.001)
        # I1.text = MathTex("I_1=\dfrac{E_1}{R_1}",color=MAROON_B).next_to(I1.arrow, LEFT)
        # I1.add(I1.text,I1.arrow)
        I1=I_Arrow(start=DOWN,end=UP,text="I_1=\dfrac{E_1}{R_1}",place=circuit_eq[0].get_center() + UP * 1.5,direction_text=LEFT,color=MAROON_B,color_text=MAROON_B)
        R2 = MathTex("R_2").next_to(circuit_eq[3], RIGHT)
        I2 = I_Arrow(start=DOWN, end=UP, color=MAROON_B, text="I_2", direction_text=LEFT, place=circuit_eq[6].get_center() + UP * 1.5)
        I3 = I_Arrow(start=DOWN, end=UP, color=MAROON_B, color_text=MAROON_B, text="I_3=\dfrac{E_3}{R_3}", direction_text=LEFT, place=circuit_eq[9].get_center() + UP * 1.5)
        R3 = MathTex("R_3",color=MAROON_B).move_to(circuit_eq[10], LEFT)
        # R4 = MathTex("R_4").next_to(circuit[13], RIGHT)
        # I4 = VGroup()
        # I4.arrow = Arrow(start=UP, end=DOWN, tip_shape=StealthTip, stroke_width=0, color=TEAL_A, buff=0).move_to(
        #     circuit[13].get_center() + UP * 1.5).set_length(0.001)
        # I4.text = MathTex("I_4").next_to(I4.arrow, LEFT)
        # I4.add(I4.arrow, I4.text)
        INO = I_Arrow(start=UP, end=DOWN, text="I_{\\textrm{no}}", color=MAROON_A, color_text=MAROON_A,
                     place=circuit_eq[-2].get_center())

        circuit_eq_text = VGroup()
        circuit_eq_text.add(R1, I1, R2, I2, I3, R3, INO)
        circuit_eq_full = VGroup(circuit_eq,circuit_eq_text).scale_to_fit_height(circuit_res.height).next_to(arrow,DOWN)

        while abs(circuit_eq[0].get_x()-circuit_res[0].get_x()) > 0.01 :
            direc = (circuit_eq[0].get_x()-circuit_res[0].get_x())*(-0.01)
            circuit_eq_full.shift([direc,0,0])

        self.play(Create(circuit_eq),Write(circuit_eq_text))
        self.wait()

        correction=VGroup()
        for i in self.mobjects :
            #print(i)
            try :
                if i.get_x() > 0 :
                    correction.add(i)
            except :
                pass

        self.play(correction.animate.shift(UP*5))
        self.wait()

        INO_eq = MathTex(r"I_{\textrm{no}}",r"= I_1 + I_2 + I_3").next_to(circuit_eq,DOWN).scale(0.75)
        self.play(Write(INO_eq))
        self.wait()

        INO_eq2= MathTex(r"= \dfrac{E_1}{R_1} + I_2 + \dfrac{E_3}{R_3}").next_to(INO_eq, DOWN).scale(0.75).align_to(INO_eq[1],LEFT)

        self.play(Write(INO_eq2))
        self.wait(2)

        AN = Tex(r"Application numérique :").next_to(INO_eq2, DOWN).scale(0.5).align_to(page2,LEFT).shift(RIGHT*0.15)
        INO_AN = MathTex(r"= \dfrac{10}{60}+0,\! 1+\dfrac{7}{30}").next_to(AN, RIGHT).scale(0.75).align_to(INO_eq[1],LEFT)
        INO_AN2 = MathTex(r"I_{\textrm{no}} = 0,\! 5\, \textrm{A}").next_to(INO_AN, DOWN).scale(0.75).set_x(page2.get_center()[0]).shift(DOWN*0.5)
        entoure = Rectangle(color = TEAL_B, height = INO_AN2.get_height()+0.1, width = INO_AN2.get_width()+0.1).move_to(INO_AN2)
        self.play(Write(AN))
        self.play(Write(INO_AN))
        self.play(Write(INO_AN2), Create(entoure))
        self.wait(2)

        correction=VGroup()
        for i in self.mobjects :
            #print(i)
            try :
                if i.get_x() > 0 :
                    correction.add(i)
            except :
                pass

        self.play(correction.animate.shift(UP*5))
        self.wait()

        RNO_eq = MathTex(r"R_{\textrm{no}}",r"=R_1 \parallel R_2 \parallel R_3").next_to(entoure,DOWN).scale(0.75)
        RNO_eq2 = MathTex(r"=\dfrac{R_1R_2R_3}{R_1R_2+R_1R_3+R_2R_3}").next_to(RNO_eq, DOWN).scale(0.75).align_to(RNO_eq[1],LEFT)

        self.play(Write(RNO_eq))
        self.play(Write(RNO_eq2))
        self.wait(2)

        AN = Tex(r"Application numérique :").next_to(RNO_eq2, DOWN*1.2).scale(0.5).align_to(page2,LEFT).shift(RIGHT*0.15)
        RNO_AN = MathTex(r"= \dfrac{60 \cdot 100 \cdot 30}{60 \cdot 100 + 60 \cdot 30 + 100 \cdot 30}").next_to(AN, RIGHT).scale(0.75).align_to(RNO_eq[1],LEFT)
        RNO_AN2 = MathTex(r"R_{\textrm{no}} = 16,\! 7\, \mathrm{\Omega}").next_to(RNO_AN, DOWN).scale(0.75).set_x(page2.get_center()[0]).shift(DOWN*0.5)
        entoure = Rectangle(color = TEAL_B, height = RNO_AN2.get_height()+0.1, width = RNO_AN2.get_width()+0.1).move_to(RNO_AN2)

        self.play(Write(AN))
        self.play(Write(RNO_AN))
        self.play(Write(RNO_AN2), Create(entoure))
        self.wait(2)

        correction=VGroup()
        for i in self.mobjects :
            #print(i)
            try :
                if i.get_x() > 0 :
                    correction.add(i)
            except :
                pass

        self.play(correction.animate.shift(UP*5))
        self.wait()

        circuit_eq = MathTex(
            r"\draw (0,0) to [current source] (0,4);",  # I1      0
            r"\draw (2,0) to [R] (2,4);",  # Rno   1
            r"\draw (0,4) to [short] (4,4);",
            r"\draw (4,4) to [R] (4,0);",  # R4    3
            r"\draw (0,0) to [short] (4,0);",
            tex_environment="circuitikz",
            tex_template=tex_template,
            stroke_color=WHITE,
            stroke_width=2,
            fill_color=WHITE
        )

        Rno = MathTex(r"R_{\textrm{no}}",color=MAROON_B).next_to(circuit_eq[1],RIGHT)
        R4 = MathTex("R_4").next_to(circuit_eq[3], RIGHT)
        Ino = I_Arrow(start=DOWN, end=UP, text="I_{\\textrm{no}}", place=circuit_eq[0].get_center() + UP * 1.5,
                     direction_text=LEFT, color=MAROON_B, color_text=MAROON_B)
        I4 = I_Arrow(start=UP, end=DOWN, text="I_4", color=MAROON_A, color_text=MAROON_A,
                     place=circuit_eq[-2].get_center() + UP*1.5)

        circuit_eq_text = VGroup()
        circuit_eq_text.add(Rno, R4, Ino, I4)
        circuit_eq_full = VGroup(circuit_eq,circuit_eq_text).scale_to_fit_height(circuit_res.height).next_to(entoure,DOWN)

        # while abs(circuit_eq[0].get_x()-circuit_res[0].get_x()) > 0.01 :
        #     direc = (circuit_eq[0].get_x()-circuit_res[0].get_x())*(-0.01)
        #     circuit_eq_full.shift([direc,0,0])

        self.play(Create(circuit_eq),Write(circuit_eq_text))
        self.wait(2)

        I4_eq = MathTex(r"I_4",r"=\dfrac{R_{\textrm{no}}}{R_{\textrm{no}}+R_4}I_{\textrm{no}}").next_to(circuit_eq,DOWN).scale(0.75)

        AN = Tex(r"Application numérique :").next_to(I4_eq, DOWN*1.5).scale(0.5).align_to(page2,LEFT).shift(RIGHT*0.15)
        I4_AN = MathTex(r"= \dfrac{16,\! 7}{16,\! 7 + 40}\cdot 0,\! 5").next_to(AN, RIGHT).scale(0.75).align_to(I4_eq[1],LEFT)
        I4_AN2 = MathTex(r"I_4 = 0,\! 15 \, \textrm{A}").next_to(I4_AN, DOWN).scale(0.75).set_x(page2.get_center()[0]).shift(DOWN*0.5)
        entoure = Rectangle(color = TEAL_B, height = I4_AN2.get_height()+0.1, width = I4_AN2.get_width()+0.1).move_to(I4_AN2)

        self.play(Write(I4_eq))
        self.play(Write(AN), Write(I4_AN))
        self.play(Write(I4_AN2), Create(entoure))
        self.wait(4)


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
