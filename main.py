import numpy as np
from manimlib import *


# from manimlib.once_useful_constructs.graph_scene import GraphScene


class Animate(Scene):
    def construct(self):
        axes = Axes((-3, 10), (-1, 8))
        axes.add_coordinate_labels()

        self.play(Write(axes, lag_ratio=0.01, run_time=1))
        sin_graph = axes.get_graph(
            lambda x: 2 * math.sin(x),
            color=BLUE,
        )
        poly_graph = axes.get_graph(
            self.poly_func,
            color=GREEN,
        )
        const_graph = axes.get_graph(
            lambda x: 3,
            color=ORANGE
        )
        self.play(ShowCreation(poly_graph))
        left_dot = Dot(color=RED)
        right_dot = Dot(color=RED)
        left_dot.move_to(axes.i2gp(2, poly_graph))
        right_dot.move_to(axes.i2gp(2, poly_graph))

        left_line = always_redraw(lambda: axes.get_v_line(left_dot.get_bottom()))
        right_line = always_redraw(lambda: axes.get_v_line(right_dot.get_bottom()))

        self.play(FadeIn(left_dot, scale=0.5), FadeIn(right_dot, scale=0.5))
        self.play(ShowCreation(left_line), ShowCreation(right_line))

        left_tracker = ValueTracker(2)
        right_tracker = ValueTracker(2)
        f_always(
            left_dot.move_to,
            lambda: axes.i2gp(left_tracker.get_value(), poly_graph)
        )
        f_always(
            right_dot.move_to,
            lambda: axes.i2gp(right_tracker.get_value(), poly_graph)
        )
        self.play(left_tracker.animate.set_value(1), right_tracker.animate.set_value(5), run_time=2)
        # self.embed()
        left_dot.clear_updaters()
        right_dot.clear_updaters()
        self.play(ReplacementTransform(poly_graph, sin_graph),
                  left_dot.animate.move_to(axes.i2gp(1, sin_graph)),
                  right_dot.animate.move_to(axes.i2gp(5, sin_graph)))
        self.wait()
        self.play(ReplacementTransform(sin_graph, const_graph),
                  left_dot.animate.move_to(axes.i2gp(1, const_graph)),
                  right_dot.animate.move_to(axes.i2gp(5, const_graph)))
        const_rect = axes.get_riemann_rectangles(const_graph, [1, 5], dx=3.75, stroke_color=WHITE,
                                                 colors=(ORANGE, BLUE))
        right_brace = Brace(const_rect, RIGHT)
        top_brace = Brace(const_rect, UP)
        right_brace_label = right_brace.get_tex(
            r"\text{Height}"
        )
        top_brace_label = top_brace.get_tex(
            r"\text{Width}"
        )
        in_label = Tex(r"\text{Area}=\text{Height}\times\text{Width}").scale(0.7)
        in_label.move_to(const_rect)
        self.play(GrowFromCenter(right_brace), Write(right_brace_label))
        self.play(GrowFromCenter(top_brace), Write(top_brace_label))
        self.play(Write(const_rect), Write(in_label))

        self.wait()
        self.play(
            *[FadeOut(x) for x in [const_rect, right_brace, right_brace_label, top_brace_label, top_brace, in_label]])
        poly_graph = axes.get_graph(
            self.poly_func,
            color=GREEN,
        )
        self.play(ReplacementTransform(const_graph, poly_graph),
                  left_dot.animate.move_to(axes.i2gp(1, poly_graph)),
                  right_dot.animate.move_to(axes.i2gp(5, poly_graph)))

        # self.play(left_tracker.animate.set_value(-2), right_tracker.animate.set_value(0), run_time=3)
        self.wait()
        dx_list = [2, 1, 0.5, 0.25, 0.1, 0.05, 0.025]
        rects_list = VGroup(
            *[
                axes.get_riemann_rectangles(graph=poly_graph, x_range=[1, 5.01], stroke_width=0.05, stroke_color=GREEN,
                                            dx=dx)
                for dx in dx_list
            ]
        )
        first_approx = rects_list[0]
        self.play(Write(first_approx))
        for k in range(1, len(dx_list)):
            new_approx = rects_list[k]
            self.play(Transform(first_approx, new_approx), run_time=1)
            self.wait(0.5)
        self.wait()

    def poly_func(self, x):
        return (x ** 3 - 5 * x ** 2 + 2 * x + 30) / 8
