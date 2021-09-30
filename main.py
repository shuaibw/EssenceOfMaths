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
        relu_graph = axes.get_graph(
            lambda x: max(x, 0),
            use_smoothing=False,
            color=YELLOW,
        )
        poly_graph = axes.get_graph(
            self.poly_func,
            color=GREEN,
        )
        self.play(ShowCreation(poly_graph))
        left_lim = Dot(color=RED)
        right_lim = Dot(color=RED)
        left_lim.move_to(axes.i2gp(2, poly_graph))
        right_lim.move_to(axes.i2gp(2, poly_graph))

        left_start = 1
        right_start = 5
        left_line = always_redraw(lambda: axes.get_v_line(left_lim.get_bottom()))
        right_line = always_redraw(lambda: axes.get_v_line(right_lim.get_bottom()))

        self.play(FadeIn(left_lim, scale=0.5), FadeIn(right_lim, scale=0.5))
        self.play(ShowCreation(left_line), ShowCreation(right_line))
        left_tracker = ValueTracker(2)
        right_tracker = ValueTracker(2)
        f_always(
            left_lim.move_to,
            lambda: axes.i2gp(left_tracker.get_value(), poly_graph)
        )
        f_always(
            right_lim.move_to,
            lambda: axes.i2gp(right_tracker.get_value(), poly_graph)
        )
        self.play(left_tracker.animate.set_value(left_start), right_tracker.animate.set_value(right_start), run_time=2)

        sin_label = axes.get_graph_label(sin_graph, "\\sin(x)")
        relu_label = axes.get_graph_label(relu_graph, Text("Linear"))
        poly_label = axes.get_graph_label(poly_graph, Text("Poly"), x=4)
        self.play(ReplacementTransform(poly_graph, sin_graph), FadeIn(sin_label, RIGHT),
                  left_tracker.animate.move_to(axes.i2gp(left_start, sin_graph)),
                  right_tracker.animate.move_to(axes.i2gp(right_start, sin_graph)))
        self.play(left_lim.animate.move_to(axes.i2gp(left_start, sin_graph)))
        self.wait()
        self.play(ReplacementTransform(sin_graph, relu_graph), FadeTransform(sin_label, relu_label),
                  left_lim.animate.move_to(axes.i2gp(left_start, sin_graph)),
                  right_lim.animate.move_to(axes.i2gp(right_start, sin_graph)))
        self.wait()
        self.play(ReplacementTransform(relu_graph, poly_graph), FadeTransform(relu_label, poly_label),
                  left_lim.animate.move_to(axes.i2gp(left_start, sin_graph)),
                  right_lim.animate.move_to(axes.i2gp(right_start, sin_graph)))

        # self.play(left_tracker.animate.set_value(-2), right_tracker.animate.set_value(0), run_time=3)
        self.wait()

    def poly_func(self, x):
        return (x ** 3 - 5 * x ** 2 + 2 * x + 30) / 8
