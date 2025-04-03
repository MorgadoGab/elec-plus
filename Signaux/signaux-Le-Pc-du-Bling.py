from manim import *


class SignalUnique(ZoomedScene):

    def __init__(self, **kwargs):
        ZoomedScene.__init__(
            self,
            zoom_factor=1.5,
            zoomed_display_height=1.5,
            zoomed_display_width=3,
            image_frame_stroke_width=20,
            zoomed_camera_config={
                "default_frame_stroke_width": 3,
            },
            **kwargs
        )

    def construct(self):
        self.show_axis()
        self.move_curve()
        self.camera.frame.save_state()
        self.wait(2)

        self.play(self.camera.frame.animate.scale(0.7).move_to(self.ax.c2p(3.1415 / 2, 0, 0)))

        amplitude = self.ax.get_vertical_line(self.ax.c2p(3.1415 / 2, 5, 0),
                                              line_config={"dashed_ratio": 1.2}).set_stroke(width=4, color=YELLOW_E)
        self.wait(2)
        self.play(GrowFromPoint(amplitude, amplitude.get_bottom()))
        self.wait(2)

        eq = MathTex(r"u(t) =", r"U_0", r"\sin (", r"\omega", r"t)").next_to(amplitude, UP).scale(0.6).set_color(BLUE)
        self.play(Write(eq))
        self.wait(2)

        self.play(eq[1].copy().animate.next_to(amplitude, RIGHT).set_color(YELLOW_E))
        self.wait(2)

        amplitude_zoomed_camera = self.zoomed_camera
        zoomed_display = self.zoomed_display
        frame = amplitude_zoomed_camera.frame
        zoomed_display_frame = zoomed_display.display_frame

        frame.move_to(self.ax.c2p(3.1415 / 2, 2, 0))
        frame.set_color(PURPLE)
        zoomed_display_frame.set_color(RED)

        frame_text = Text("Frame", color=PURPLE, font_size=67)

        self.wait(2)

        self.play(self.camera.frame.animate.scale(1 / 0.7).shift(LEFT * 0.25))

        zoomed_display.next_to(self.ax, LEFT*1.5).shift(UP*1.5)
        self.play(Create(frame))
        self.activate_zooming()

        self.play(self.get_zoomed_display_pop_out_animation())
        self.play(frame.animate.set_stroke(opacity=0))
        self.wait(2)

        self.play(self.camera.frame.animate.scale(1).shift(RIGHT*2))
        self.wait(2)

        period_arrow = DoubleArrow(self.ax.get_origin(),self.ax.c2p(3.14159 * 2,0,0),buff=0.05,tip_length=0.1,tip_shape=StealthTip).set_color(PURPLE_B).set_stroke(width=4)
        self.play(FadeIn(period_arrow,shift=UP))
        self.wait(2)

        eq_t = MathTex(r"T = { {{2\pi}} \over {{\omega}} }").next_to(period_arrow, DOWN).scale(0.6).set_color(PURPLE)
        self.play(Write(eq_t[:3]))
        self.wait(2)

        self.play(eq[3].copy().animate.move_to(eq_t[3]).set_color(PURPLE))
        self.wait(2)


    def show_axis(self):
        self.ax = Axes(
            x_range=[0, 10], y_range=[-10, 10, 2], axis_config={"include_tip": False}
        )
        labels = self.ax.get_axis_labels(x_label="t", y_label="u(t)")

        self.play(Create(self.ax), Write(labels))

    def move_curve(self):
        self.t_offset = 0.05
        rate = 2
        self.curve = VGroup()

        def shift_curve(mob, dt):
            self.t_offset += rate * dt
            # print(self.t_offset)

        def plot_curve():
            self.curve = self.ax.plot(lambda x: 5 * np.sin(x - self.t_offset), color=BLUE).set_stroke(
                opacity=self.t_offset)
            return self.curve

        sine_curve = always_redraw(plot_curve)
        self.add(sine_curve)
        self.ax.add_updater(shift_curve)
        self.wait_until(lambda: sine_curve.get_start()[1] < 0.01 and sine_curve.get_start()[1] > -0.01)
        self.ax.remove_updater(shift_curve)


class SineCurveUnitCircle(Scene):
    # contributed by heejin_park, https://infograph.tistory.com/230
    def construct(self):
        self.show_axis()
        self.show_circle()
        self.move_dot_and_draw_curve()
        self.wait()

    def show_axis(self):

        color = GRAY_A
        self.color = color
        x_start = np.array([-4, 0, 0])
        x_end = np.array([6, 0, 0])

        y_start = np.array([-4, -2, 0])
        y_end = np.array([-4, 2, 0])

        x_axis = Arrow(x_start, x_end, tip_shape=StealthTip, color=self.color, buff=0)
        y_axis = Arrow(y_start, y_end, tip_shape=StealthTip, color=self.color, buff=0)

        self.add(x_axis, y_axis)
        self.add_x_labels()

        self.origin_point = np.array([-4, 0, 0])

    def add_x_labels(self):
        x_labels = [
            MathTex("\pi"), MathTex("2 \pi"),
            MathTex("3 \pi"), MathTex("4 \pi"),
        ]

        for i in range(len(x_labels)):
            x_labels[i].next_to(np.array([-2 + 2 * i, 0, 0]), DOWN)
            self.add(x_labels[i])

    def show_circle(self):
        circle = Circle(radius=1, color=WHITE)
        circle.next_to(self.origin_point, direction=LEFT)
        self.add(circle)
        self.circle = circle

    def move_dot_and_draw_curve(self):
        orbit = self.circle
        origin_point = self.origin_point

        dot_A = Dot(radius=0.08, color=BLUE_D)
        dot_B = dot_A.copy().set_color(RED_D)

        dots = [dot_A, dot_B]

        dot_A.move_to(orbit.point_from_proportion(0))
        dot_B.move_to(orbit.point_from_proportion(1 / 8))

        dot_A.t_offset = orbit.proportion_from_point(dot_A.get_center())
        dot_B.t_offset = orbit.proportion_from_point(dot_B.get_center())
        rate = 0.25

        def go_around_circle(mob, dt):
            mob.t_offset += (dt * rate)
            # print(self.t_offset)
            mob.move_to(orbit.point_from_proportion(mob.t_offset % 1))

        def get_line_to_circle():
            lines = VGroup()
            for dot in dots:
                lines.add(Line(orbit.get_center(), dot.get_center(), color=dot.color))

            phase_shift = Angle(lines[0], lines[1], 0.5, color=YELLOW_E)
            phi = MathTex(r"\varphi", color=YELLOW_E).scale(0.6).move_to(
                Angle(lines[0], lines[1], 0.75).point_from_proportion(0.5))
            lines.add(phase_shift)
            lines.add(phi)
            return lines

        def get_line_to_curve():
            lines = VGroup()
            for dot in dots:
                x = dot.curve_start[0] + dot_A.t_offset * 4
                y = dot.get_center()[1]
                lines.add(DashedLine(dot.get_center(), np.array([x, y, 0]), color=dot.color, stroke_width=2))
            return lines

        for dot in dots:
            dot.curve = VGroup()
            x = -4
            y = dot.get_center()[1]
            dot.curve_start = np.array([x, y, 0])
            dot.curve.add(Line(dot.curve_start, dot.curve_start, color=dot.color))

        def get_curve():

            curves = VGroup()
            for dot in dots:
                dot.last_line = dot.curve[-1]
                x = dot.curve_start[0] + dot_A.t_offset * 4
                y = dot.get_center()[1]
                new_line = Line(dot.last_line.get_end(), np.array([x, y, 0]), color=dot.color)
                dot.curve.add(new_line)
                curves.add(dot.curve)

            return curves

        origin_to_circle_line = always_redraw(get_line_to_circle)
        # origin_to_circle_line.add_updater(lambda x: x.set_color(BLUE_C))

        dot_to_curve_line = always_redraw(get_line_to_curve)
        sine_curve_line = always_redraw(get_curve)

        self.add(*dots)
        for dot in dots:
            dot.set_z_index(1)
        self.add(orbit, origin_to_circle_line, dot_to_curve_line, sine_curve_line)

        self.wait(1)

        for dot in dots:
            dot.add_updater(go_around_circle)

        self.wait_until(lambda: dot_A.t_offset >= 1.5)

        for dot in dots:
            dot.remove_updater(go_around_circle)
