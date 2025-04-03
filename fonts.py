from manim import *
from manim_fonts import *


class Example(Scene):
    def construct(self):
        with RegisterFont("Caveat") as fts:
            # print(fts)
            a = Text("Hello World", font=fts[0])
            self.play(Write(a))