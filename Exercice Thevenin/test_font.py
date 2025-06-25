from manim import *

class Test(Scene):
    def construct(self):
        resolution = Text("Résolution de l'exercice", font="Birthstone", color=MAROON, font_size=32)
        res_2 = Text("Résolution de l'exercice", color=MAROON, font_size=20).next_to(resolution,DOWN)

        self.play(Write(resolution),Write(res_2))