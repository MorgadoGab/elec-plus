import numpy
import numpy as np
from manim import *

config.background_color = WHITE
config["background_color"] = WHITE


class CircuitElectrons(Scene):

    def construct(self):

        # self.add(Circle(0.1).move_to([0, 0, 0])) # Origine de la Scene

        currentColor = ORANGE
        electronColor = BLUE
        tex_template = TexTemplate()
        tex_template.add_to_preamble(r"\usepackage[siunitx, RPvoltages, european]{circuitikz}")

        circuit = MathTex(
            r"\draw (0,0) to [american voltage source] (0,3);",
            r"\draw (0,3) to [short] (2,3);",
            r"\draw (2,3) to [R] (2,0);",
            r"\draw (2,0) to [short] (0,0);",
            r"\draw (-0.5,1.5) node (gen) [left] {générateur};",
            r"\draw (2.5,1.5) node (res) [right] {récepteur};",
            r"\draw (1,3) node (current) [above] {courant $I$};",
            r"\draw (1,0) node (electrons) [below] {$e^-$};",
            tex_environment="circuitikz",
            tex_template=tex_template,
            stroke_color=BLACK,
            stroke_width=1,
            fill_color=BLACK
        )

        circuit[6].set_color(currentColor)
        circuit[7].set_color(electronColor)

        self.add(circuit)
        numberOfElectrons = 40
        numberOfCurrentArrows = 5
        electrons = [
            Circle(0.1, fill_opacity=1, fill_color=electronColor, stroke_width=1, stroke_color=BLACK).next_to(
                circuit[0].get_center(), DOWN * 2.) for r in range(numberOfElectrons)
        ]

        current_arrows = []
        for r in range(numberOfCurrentArrows):
            current_arrows.append(
                Arrow(fill_opacity=1, color=currentColor, tip_shape=StealthTip, tip_length=0.2).set_length(length=0.001).next_to(
                    circuit[0].get_center(), UP * 2.))

        bottom_wire = Path(
            [electrons[-1].get_center(), circuit[0].get_bottom(), circuit[3].get_right(),
             circuit[2].get_center() + DOWN * 0.5]
        )

        top_wire = Path(
            [circuit[2].get_center() - DOWN * 0.5, circuit[2].get_top(), circuit[1].get_left(),
             circuit[0].get_center() + UP * 0.5]
        )

        topPathArrows = Path(top_wire.get_all_points())
        topPathArrows.reverse_points()

        bottomPathArrows = Path(bottom_wire.get_all_points())
        bottomPathArrows.reverse_points()

        def passage_electrons(x, alpha):
            x.move_to(circuit[2].get_center() - DOWN * (alpha - 0.5))

        def fin_electrons(x, alpha):
            x.set_opacity(1 - alpha)

        def angle_current(x,alpha):
            x.set_angle(90 * (np.heaviside(0.09 - alpha, 0) - np.heaviside(alpha - 0.91, 1)) * DEGREES)
            x.set_opacity((1-alpha)*alpha*20)

        def angle_current_bottom(x,alpha):
            x.set_angle((180 + 90 * (np.heaviside(0.09 - alpha, 0) - np.heaviside(alpha - 0.91, 1))) * DEGREES)
            x.set_opacity((1-alpha)*alpha*20)

        moving_electrons = []
        for e in electrons:
            moving_electrons.append(Succession(
                AnimationGroup(FadeIn(e, run_time=0.5),
                               MoveAlongPath(mobject=e, path=bottom_wire, rate_func=linear, run_time=4)),

                AnimationGroup(Indicate(e, color=RED, scale_factor=1),
                               UpdateFromAlphaFunc(e, update_function=passage_electrons, rate_func=linear), run_time=2,
                               rate_func=linear),

                AnimationGroup(MoveAlongPath(mobject=e, path=top_wire, rate_func=linear, run_time=8),
                               UpdateFromAlphaFunc(e, update_function=fin_electrons, run_time=1),
                               lag_ratio=0.9),
                lag_ratio=1))

        moving_current = []
        for c in current_arrows:
            moving_current.append(Succession(
                AnimationGroup(UpdateFromAlphaFunc(mobject=c, update_function=angle_current),
                               MoveAlongPath(mobject=c, path=topPathArrows, rate_func=linear), run_time=4),

                AnimationGroup(UpdateFromAlphaFunc(mobject=c, update_function=angle_current_bottom),
                               MoveAlongPath(mobject=c, path=bottomPathArrows, rate_func=linear), run_time=4),
                lag_ratio=1))

        self.play(AnimationGroup(AnimationGroup(*moving_electrons, lag_ratio=0.05),
                                 AnimationGroup(*moving_current, lag_ratio=0.5), lag_ratio=0), run_time=numberOfCurrentArrows*2)
        self.wait()


class Path(Polygram):
    def __init__(self, points, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_points_as_corners(points)

    def get_important_points(self):
        """Returns the important points of the curve."""
        # shot explanation: Manim uses quadratic Bézier curves to create paths
        # > each curve is determined by 4 points - 2 anchor and 2 control
        # > VMobject's builtin self.points returns *all* points
        # > we, however, only care about the anchors
        # > see https://en.wikipedia.org/wiki/Bézier_curve for more details
        return list(self.get_start_anchors()) + [self.get_end_anchors()[-1]]


class CircuitTest(Scene):
    def construct(self):
        circle = Circle(0.1, fill_color=BLUE, stroke_width=0, fill_opacity=1)

        tex_template = TexTemplate()
        tex_template.add_to_preamble(r"\usepackage[siunitx, RPvoltages, european]{circuitikz}")

        circuit = MathTex(
            r"\draw (0,0) to [american voltage source] (0,3);",
            r"\draw (0,3) to [short] (2,3);",
            r"\draw (2,3) to [R] (2,0);",
            r"\draw (2,0) to [short] (0,0);",
            tex_environment="circuitikz",
            tex_template=tex_template,
            stroke_color=WHITE,
            stroke_width=3
        )

        path = Path(
            [circuit[0].get_center(),
             circuit[0].get_bottom(),
             circuit[3].get_right(),
             circuit[2].get_top(),
             circuit[1].get_left(),
             circuit[0].get_center()
             ]
        )

        passageResistance = lambda x, dt: x.set_color(RED) if x.get_x() > 0 and abs(x.get_y()) < 0.5 else x.set_color(
            BLUE)

        circle.move_to(path.get_start())

        circle.add_updater(passageResistance)

        self.add(path, circle)
        self.play(AnimationGroup(FadeIn(circle, run_time=0.2), MoveAlongPath(circle, path)), rate_func=linear,
                  run_time=1)
        self.wait()
