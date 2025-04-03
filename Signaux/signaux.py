import sys

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
        self.origin_point = None
        self.circle = None

    def construct(self):
        self.next_section(skip_animations=False)
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

        U0 = eq[1].copy()

        self.play(U0.animate.next_to(amplitude, RIGHT).set_color(YELLOW_E))
        self.wait(2)

        amplitude_txt = Tex("Amplitude", font_size=24).set_color(U0.get_color())

        amplitude_zoomed_camera = self.zoomed_camera
        zoomed_display = self.zoomed_display
        frame = amplitude_zoomed_camera.frame
        zoomed_display_frame = zoomed_display.display_frame

        frame.move_to(self.ax.c2p(3.1415 / 2, 2, 0))
        frame.set_color(PURPLE)
        zoomed_display_frame.set_color(RED)

        frame_text = Text("Frame", color=PURPLE, font_size=67)

        self.wait(2)

        self.play(self.camera.frame.animate.scale(1 / 0.7))

        zoomed_display.next_to(self.ax, LEFT * 1.5).shift(UP * 1.5)
        self.play(Create(frame))
        self.activate_zooming()

        self.play(self.get_zoomed_display_pop_out_animation())
        self.play(frame.animate.set_stroke(opacity=0), Write(amplitude_txt.next_to(zoomed_display, UP)))
        self.wait(2)

        amplitude_image = ImageMobject(amplitude_zoomed_camera.get_image())
        amplitude_image.scale_to_fit_height(zoomed_display.height)
        amplitude_image_frame = Rectangle(RED).scale_to_fit_height(zoomed_display.height)
        amplitude_image.add(amplitude_image_frame)
        amplitude_image.move_to(zoomed_display)

        self.remove(zoomed_display)
        self.add(amplitude_image)

        amplitude_frame = Group(amplitude_image, amplitude_txt)

        self.play(self.camera.frame.animate.scale(1.2).shift(RIGHT * 1.65), Uncreate(amplitude), Unwrite(U0))
        self.wait(2)
        self.next_section("period",skip_animations=False)

        period_arrow = DoubleArrow(self.ax.get_origin(), self.ax.c2p(3.14159 * 2, 0, 0), buff=0.05, tip_length=0.1,
                                   tip_shape=StealthTip).set_color(PINK).set_stroke(width=4)

        self.play(FadeIn(period_arrow, shift=UP))

        eq_t = MathTex(r"T {{=}} { {{2\pi}} \over {{\omega}} }").scale(0.8).set_color(PINK).next_to(
            period_arrow.get_center() + RIGHT * 0.5, UP)
        periode_txt = Tex("Période", font_size=24).set_color(eq_t.get_color())
        T = eq_t[0].copy()
        T.add_updater(lambda x: x.next_to(period_arrow, UP))

        self.play(Write(T))
        self.wait(2)

        period_arrow.save_state()

        self.play(period_arrow.animate.move_to(self.ax.c2p(3 * PI / 2, 5, 0)))
        self.wait(2)

        self.play(period_arrow.animate.move_to(self.ax.c2p(5 * PI / 2, -5, 0)))
        self.wait(2)

        self.play(Restore(period_arrow))
        T.clear_updaters()
        self.play(T.animate.move_to(eq_t[0]), Write(eq_t[1:5]))

        omega = eq[3].copy()
        self.play(omega.animate.move_to(eq_t[5]).set_color(PINK).scale_to_fit_height(eq_t[5].height))
        self.wait(2)

        frame.move_to(self.ax.c2p(3.14159, 0, 0)).scale(1.2)

        zoomed_display.next_to(amplitude_image, DOWN).set_z_index(1)

        self.play(frame.animate.set_stroke(opacity=1).set_z_index(0))

        self.play(self.get_zoomed_display_pop_out_animation())

        period_image = ImageMobject(amplitude_zoomed_camera.get_image())
        period_image.scale_to_fit_height(zoomed_display.height)
        period_image_frame = Rectangle(RED).scale_to_fit_height(zoomed_display.height)
        period_image.add(period_image_frame)
        period_image.move_to(zoomed_display)

        self.remove(zoomed_display)
        self.add(period_image)

        period_frame = Group(period_image, periode_txt)
        periode_txt.add_updater(lambda x: x.next_to(period_image, DOWN))

        self.play(frame.animate.set_stroke(opacity=0), Write(periode_txt))

        self.wait(2)
        # print(type(self.curve))
        self.remove(T, omega)
        self.add(eq_t[0], eq_t[5])
        # self.play(FadeOut(self.ax),FadeOut(self.ax.labels))
        self.play(FadeOut(period_arrow, eq_t, eq), FadeOut(self.sine_curve))
        self.play(amplitude_txt.set_z_index(2).animate.next_to(amplitude_image, DOWN))

        amplitude_txt.add_updater(lambda x: x.next_to(amplitude_image, DOWN))
        self.play(AnimationGroup(Restore(self.camera.frame),
                                 Group(amplitude_image, period_image).animate.scale(0.8).arrange().to_edge(UP),
                                 amplitude_txt.animate.scale(0.8),
                                 periode_txt.animate.scale(0.8)))

        self.wait(2)
        self.next_section("angfreq", skip_animations=False)
        self.play(self.camera.frame.animate.shift(LEFT * 1.25))
        self.show_circle()
        self.move_dot_and_draw_sin()

        frame.move_to(self.ax.c2p(1, 0.75, 0)).scale(1.15)
        zoomed_display.to_edge(RIGHT, buff=3).set_z_index(1)

        self.play(frame.animate.set_stroke(opacity=1).set_z_index(0))
        self.play(self.get_zoomed_display_pop_out_animation())

        angfreq_txt = Tex("Pulsation", font_size=24).set_color(GREEN_A)

        angfreq_image = ImageMobject(amplitude_zoomed_camera.get_image())
        angfreq_image.scale_to_fit_height(zoomed_display.height)
        angfreq_image_frame = Rectangle(RED).scale_to_fit_height(zoomed_display.height)
        angfreq_image.add(angfreq_image_frame)
        angfreq_image.move_to(zoomed_display)

        angfreq_frame = Group(angfreq_image, angfreq_txt.next_to(angfreq_image, DOWN))
        angfreq_txt.add_updater(lambda x: x.next_to(angfreq_image, DOWN))

        # frames = Group(amplitude_frame,period_frame,angfreq_frame).arrange().to_edge(UP)

        self.remove(zoomed_display)
        self.add(angfreq_image)

        self.play(frame.animate.set_stroke(opacity=0), Write(angfreq_txt))

        self.wait(4)

        self.play(FadeOut(self.sine_curve_line), FadeOut(self.pulsation), FadeOut(self.origin_to_circle_line),
                  FadeOut(self.dot_to_curve_line))

        self.wait(2)
        self.play(angfreq_frame.animate.scale(0.8))
        self.play(Group(amplitude_image, period_image, angfreq_image).animate.arrange().to_edge(UP))
        self.wait(2)
        self.next_section("dephasage", skip_animations=False)
        self.move_dot_and_draw_curve()

        frame.move_to(self.ax.c2p(1, 0.75, 0)).scale(1.15)
        zoomed_display.to_edge(RIGHT, buff=3).set_z_index(1)

        self.play(frame.animate.set_stroke(opacity=1).set_z_index(0))
        self.play(self.get_zoomed_display_pop_out_animation())

        dephasage_txt = Tex("Déphasage", font_size=24).set_color(TEAL)

        dephasage_image = ImageMobject(amplitude_zoomed_camera.get_image())
        dephasage_image.scale_to_fit_height(zoomed_display.height)
        dephasage_image_frame = Rectangle(RED).scale_to_fit_height(zoomed_display.height)
        dephasage_image.add(dephasage_image_frame)
        dephasage_image.move_to(zoomed_display)

        dephasage_frame = Group(dephasage_image, dephasage_txt.next_to(dephasage_image, DOWN))
        dephasage_txt.add_updater(lambda x: x.next_to(dephasage_image, DOWN))

        # frames = Group(amplitude_frame,period_frame,angfreq_frame).arrange().to_edge(UP)

        self.remove(zoomed_display)
        self.add(dephasage_image)

        self.play(frame.animate.set_stroke(opacity=0), Write(dephasage_txt))

        self.wait(4)

        self.play(FadeOut(self.sine_curve_line), FadeOut(self.origin_to_circle_line),
                  FadeOut(self.dot_to_curve_line), FadeOut(self.circle), FadeOut(self.ax), FadeOut(self.ax.labels))

        self.wait(2)

        self.play(dephasage_frame.animate.scale(0.8))
        self.play(AnimationGroup(Restore(self.camera.frame),
                                 Group(amplitude_image, period_image, angfreq_image,
                                       dephasage_image).animate.arrange().move_to([0, 0, 0])))

        self.wait(4)

    def show_axis(self):
        self.ax = Axes(
            x_range=[0, 15], y_range=[-10, 10, 2], axis_config={"include_tip": False}
        )
        self.ax.labels = self.ax.get_axis_labels(x_label="", y_label="u(t)")

        self.play(Create(self.ax), Write(self.ax.labels))

        self.origin_point = self.ax.c2p(0, 0, 0)

    def move_curve(self):
        self.t_offset = 0.05
        rate = 2
        self.curve = VGroup()

        def shift_curve(mob, dt):
            self.t_offset += (rate * dt) % (2 * PI)
            # print(self.t_offset)

        def plot_curve():
            self.curve = self.ax.plot(lambda x: 5 * np.sin(x - self.t_offset), color=BLUE).set_stroke(
                opacity=self.t_offset)
            return self.curve

        self.sine_curve = always_redraw(plot_curve)
        self.add(self.sine_curve)
        self.ax.add_updater(shift_curve)
        self.wait_until(lambda: self.sine_curve.get_start()[1] < 0.01 and self.sine_curve.get_start()[1] > -0.01)
        #self.wait(8)
        self.ax.remove_updater(shift_curve)

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
        # self.play(Create(circle))
        self.circle = circle

    def move_dot_and_draw_sin(self):
        orbit = self.circle
        origin_point = self.origin_point

        dot_A = Dot(radius=0.08, color=BLUE_D)

        dot_A.move_to(orbit.point_from_proportion(0))

        dot_A.t_offset = orbit.proportion_from_point(dot_A.get_center())
        self.old_offset = dot_A.t_offset
        rate = ValueTracker(0.5)

        def go_around_circle(mob, dt):
            mob.t_offset += (dt * rate.get_value())
            # print(self.t_offset)
            mob.move_to(orbit.point_from_proportion(mob.t_offset % 1))
            # print("temps =", mob.t_offset, " s")

        def get_line_to_circle():
            lines = VGroup()
            lines.add(Line(orbit.get_center(), dot_A.get_center(), color=dot_A.color))

            # phase_shift = Angle(lines[0], lines[1], 0.5, color=YELLOW_E)
            # phi = MathTex(r"\varphi", color=YELLOW_E).scale(0.6).move_to(
            #     Angle(lines[0], lines[1], 30.75).point_from_proportion(0.5))
            # lines.add(phase_shift)
            # lines.add(phi)
            return lines

        def get_line_to_curve():
            lines = VGroup()
            lines.add(DashedLine(dot_A.get_center(), dot_A.curve[-1].get_end(), color=dot_A.color, stroke_width=2))
            return lines

        dot_A.curve = VGroup()
        dot_A.curve_start = self.origin_point
        dot_A.curve.add(Line(dot_A.curve_start, dot_A.curve_start, color=dot_A.color))
        dot_A.old_x = self.origin_point[0]

        def get_curve():

            curves = VGroup()
            dot_A.last_line = dot_A.curve[-1]
            x = dot_A.old_x + (dot_A.t_offset - self.old_offset) / rate.get_value()

            self.old_offset = dot_A.t_offset
            y = dot_A.get_center()[1]
            new_line = Line(dot_A.last_line.get_end(), np.array([x, y, 0]), color=dot_A.color)
            dot_A.curve.add(new_line)

            if x > self.ax.c2p(14, 0, 0)[0]:
                delta_x = x - self.ax.c2p(14, 0, 0)[0]
                for c in dot_A.curve:
                    c.shift(LEFT * delta_x)
                    # print(c, " ", x, " ", delta_x)
                    if c.get_start()[0] <= self.ax.c2p(0, 0, 0)[0]:
                        c.set_opacity(0)

            dot_A.old_x = dot_A.curve[-1].get_end()[0]
            curves.add(dot_A.curve)
            return curves

        self.origin_to_circle_line = always_redraw(get_line_to_circle)
        # origin_to_circle_line.add_updater(lambda x: x.set_color(BLUE_C))

        self.sine_curve_line = always_redraw(get_curve)
        self.dot_to_curve_line = always_redraw(get_line_to_curve)

        dots = [dot_A]
        # self.play(Create(*dots))
        for dot in dots:
            dot.set_z_index(1)
            self.play(FadeIn(dot), Create(orbit), Create(self.sine_curve_line), Create(self.origin_to_circle_line),
                      Create(self.dot_to_curve_line))
            dot.add_updater(go_around_circle)

        self.wait_until(lambda: dot_A.t_offset >= 0.17)

        puls_color = GREEN_A
        pulsation_arrow = Arc(radius=self.circle.radius * 1.2, start_angle=PI / 3, angle=PI / 3,
                              arc_center=self.circle.get_center(), color=puls_color)
        pulsation_arrow = CurvedArrow(start_point=pulsation_arrow.get_start(), end_point=pulsation_arrow.get_end(),
                                      radius=self.circle.radius * 1.2, arc_center=self.circle.get_center(),
                                      color=puls_color, tip_length=0.2)
        pulsation_text = MathTex("\omega=").set_color(pulsation_arrow.color)
        ang_freq = DecimalNumber(rate.get_value() * 2, num_decimal_places=1, unit=r"\pi \textrm{rad.s}^{-1}",
                                 unit_buff_per_font_unit=0.003, color=puls_color).next_to(pulsation_text, RIGHT).shift(
            UP * 0.1)
        pulsation_text.add(ang_freq).scale(0.5)
        self.pulsation = VGroup(pulsation_arrow, pulsation_text.next_to(pulsation_arrow, UP))
        self.play(Write(self.pulsation))

        self.wait_until(lambda: dot_A.t_offset >= 0.75)

        ang_freq.add_updater(lambda x: x.set_value(rate.get_value() * 2))
        self.play(rate.animate.set_value(2), run_time=5)

        self.wait(2)

        self.play(rate.animate.set_value(0.5), run_time=4)

        self.wait(5)

        for dot in dots:
            dot.remove_updater(go_around_circle)
            self.play(FadeOut(dot))

    def move_dot_and_draw_curve(self):
        orbit = self.circle
        self.origin_point = self.ax.c2p(0, 0, 0)

        dot_A = Dot(radius=0.08, color=BLUE_D)
        dot_B = dot_A.copy().set_color(RED_D)

        dots = [dot_A, dot_B]

        dot_A.move_to(orbit.point_from_proportion(0))
        dot_B.move_to(orbit.point_from_proportion(1 / 8))

        dot_A.t_offset = orbit.proportion_from_point(dot_A.get_center())
        dot_B.t_offset = orbit.proportion_from_point(dot_B.get_center())
        self.old_offset = dot_A.t_offset
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
            self.phi = MathTex(r"\varphi", color=YELLOW_E).scale(0.6).move_to(
                Angle(lines[0], lines[1], 0.75).point_from_proportion(0.5))
            lines.add(phase_shift)
            lines.add(self.phi)
            return lines

        for dot in dots:
            dot.curve = VGroup()
            x = self.origin_point[0]
            y = dot.get_center()[1]
            curve_start = np.array([x, y, 0])
            dot.curve.add(Line(curve_start, curve_start, color=dot.color).set_opacity(0))

        def get_line_to_curve():
            lines = VGroup()
            for dot in dots:
                lines.add(DashedLine(dot.get_center(), dot.curve[-1].get_end(), color=dot.color, stroke_width=2))
            return lines

        dot_A.old_x = self.origin_point[0]

        def get_curve():

            curves = VGroup()
            for dot in dots:
                x = dot_A.old_x + (dot_A.t_offset - self.old_offset) / rate
                y = dot.get_center()[1]
                if x != dot_A.old_x:
                    new_line = Line(dot.curve[-1].get_end(), np.array([x, y, 0]), color=dot.color)
                    dot.curve.add(new_line)

                if x > self.ax.c2p(13.5, 0, 0)[0]:
                    delta_x = x - self.ax.c2p(13.5, 0, 0)[0]
                    for c in dot.curve:
                        c.shift(LEFT * delta_x)
                        if c.get_start()[0] <= self.ax.c2p(0, 0, 0)[0]:
                            c.set_opacity(0)

            curves.add(dot_A.curve, dot_B.curve)
            self.old_offset = dot_A.t_offset
            dot_A.old_x = dot_A.curve[-1].get_end()[0]
            return curves

        self.origin_to_circle_line = always_redraw(get_line_to_circle)
        self.sine_curve_line = always_redraw(get_curve)
        self.dot_to_curve_line = always_redraw(get_line_to_curve)

        for dot in dots:
            self.play(FadeIn(dot))
            dot.set_z_index(1)
        self.play(Create(self.origin_to_circle_line), Create(self.dot_to_curve_line))
        self.add(self.sine_curve_line)

        for dot in dots:
            dot.add_updater(go_around_circle)

        self.wait_until(lambda: dot_A.t_offset >= 4.5)

        u_eq = MathTex(r"u(t)=U_0\sin(\omega t)", color=dot_A.color).next_to(self.ax.c2p(0, 5, 0), RIGHT).scale(0.6)
        v_eq = MathTex(r"v(t)=V_0\sin(\omega t", r"+", r"\varphi", r")", color=dot_B.color).next_to(
            self.ax.c2p(0, -5, 0), RIGHT).scale(0.6)

        phib = self.phi.copy()
        self.play(Write(u_eq), Write(v_eq[:-1]), Write(v_eq[-1]),
                  phib.animate.set_color(dot_B.color).move_to(v_eq[-2].get_center()))

        self.wait_until(lambda: dot_A.t_offset >= 4)

        for dot in dots:
            dot.remove_updater(go_around_circle)

        delta_t_arrow = DoubleArrow(self.ax.c2p(0.35, 0, 0), self.ax.c2p(1, 0, 0), buff=0.05, tip_length=0.1,
                                    tip_shape=StealthTip).set_color(PINK).set_stroke(width=4)
        delta_t_txt = MathTex(r"\Delta t", color=PINK).next_to(delta_t_arrow, DOWN).scale(0.6)
        delta_t = Group(delta_t_txt, delta_t_arrow)
        eq_dt = MathTex(r"\varphi = \omega", r"\Delta t", color=PINK).next_to(v_eq, DOWN).scale(0.6)

        self.wait(1)

        self.play(FadeIn(delta_t, shift=UP))

        self.wait(1)
        self.play(Write(eq_dt), delta_t_txt.animate.move_to(eq_dt[-1]))

        self.wait(2)

        for dot in dots:
            self.play(FadeOut(dot))
        self.remove(phib)
        self.play(FadeOut(u_eq), FadeOut(v_eq))
        self.play(FadeOut(delta_t, eq_dt))


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
                Angle(lines[0], lines[1], 30.75).point_from_proportion(0.5))
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


class Axess(Scene):

    def construct(self):
        self.show_axis()
        self.wait(2)

    def show_axis(self):
        self.ax = Axes(x_range=[0, 15], y_range=[-10, 10, 2], axis_config={"include_tip": False})
        self.ax.labels = self.ax.get_axis_labels(x_label="", y_label="u(t)")

        self.play(Create(self.ax), run_time=5)
        self.play(Write(self.ax.labels))

        self.origin_point = self.ax.c2p(0, 0, 0)


class Freq(Scene):

    def construct(self):
        text = Tex("Et la fréquence alors ?")

        self.play(Write(text))
        self.wait(1)
        self.play(text.animate.to_edge(UP))
        self.show_circle()
        self.move_dot()
        self.wait(1)

    def show_circle(self):
        circle = Circle(radius=1, color=WHITE)
        self.play(Create(circle))
        self.circle = circle

    def move_dot(self):
        orbit = self.circle

        dot = Dot(radius=0.08, color=BLUE_D)

        dot.move_to(orbit.point_from_proportion(0))

        dot.t_offset = orbit.proportion_from_point(dot.get_center())
        self.proportion = 0
        rate = ValueTracker(0.75)

        def go_around_circle(mob, dt):
            mob.t_offset += (dt * rate.get_value())
            self.proportion = mob.t_offset % 1
            mob.move_to(orbit.point_from_proportion(self.proportion))

        self.play(FadeIn(dot), run_time=0.5)
        dot.set_z_index(1)
        dot.add_updater(go_around_circle)

        a = 0
        freq_num = DecimalNumber(0, num_decimal_places=0).add_updater(lambda x: x.set_value(a)).next_to(orbit, RIGHT)
        self.play(Write(freq_num))
        for i in range(4):
            self.wait_until(lambda: self.proportion >= 0.95)
            a += 1
            self.play(Flash(orbit.get_right()), run_time=0.5, rate_func=rush_from)

        puls_color = GREEN_A
        pulsation_arrow = Arc(radius=self.circle.radius * 1.2, start_angle=PI / 3, angle=PI / 3,
                              arc_center=self.circle.get_center(), color=puls_color)
        pulsation_arrow = CurvedArrow(start_point=pulsation_arrow.get_start(), end_point=pulsation_arrow.get_end(),
                                      radius=self.circle.radius * 1.2, arc_center=self.circle.get_center(),
                                      color=puls_color, tip_length=0.2)
        pulsation_text = MathTex("\omega=").set_color(pulsation_arrow.color)
        ang_freq = DecimalNumber(rate.get_value() * 2, num_decimal_places=1, unit=r"\pi \textrm{rad.s}^{-1}",
                                 unit_buff_per_font_unit=0.003, color=puls_color).next_to(pulsation_text, RIGHT).shift(
            UP * 0.1)
        pulsation_text.add(ang_freq).scale(0.5)

        self.pulsation = VGroup(pulsation_arrow, pulsation_text.next_to(pulsation_arrow, UP))
        self.play(Write(self.pulsation), FadeOut(freq_num))
        freq_color = PURPLE_A
        freq_text = MathTex("f=\dfrac{\omega}{2\pi}=").set_color(freq_color)
        freq_num = DecimalNumber(ang_freq.get_value() / 2. / PI, num_decimal_places=1, unit=r" \textrm{Hz}",
                                 unit_buff_per_font_unit=0.003, color=freq_color).next_to(freq_text, RIGHT).shift(
            UP * 0.1).add_updater(lambda x: x.set_value(ang_freq.get_value() / 2.))
        freq_text.add(freq_num).scale(0.5).next_to(orbit, DOWN)

        self.play(Write(freq_text))
        self.wait(1)
        ang_freq.add_updater(lambda x: x.set_value(rate.get_value() * 2))

        self.play(rate.animate.set_value(2), run_time=5)

        self.wait(2)

class CArray(VGroup):
    def __init__(self, p_size, values=[], name='Tab', **kwargs):
        super().__init__(**kwargs)
        self.p_size = p_size
        self.values = values

class CArrayElement(VMobject):
    def __init__(self, value, index, **kwargs: any):
        super().__init__(**kwargs)
        self.value = Tex(str(value))
        self.index = Tex(str(index))

        self.square = Square(side_length=1)
        self.value.move_to(self.square.get_center())
        self.index.next_to(self.square,UP)
        self.add(self.square,self.value,self.index)

class Tableau(Scene):
    def construct(self):
        element = CArrayElement(value="0",index="tab")
        self.play(Create(element))
        self.wait(2)
