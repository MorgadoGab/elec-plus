from manim import *

class Test(Scene):
    def construct(self):
        resolution = Text("Résolution de l'exercice", font="Brush Script MT", color=MAROON, font_size=20)

        self.play(Write(resolution))