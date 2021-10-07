import math

import numpy as np
from manimlib import *


# from manimlib.once_useful_constructs.graph_scene import GraphScene


class Animate(Scene):
    def construct(self):
        axes = Axes((-3, 10), (-1, 8), axis_config={
            "include_tip": False,
            "stroke_width":2,
            "tick_size":0.04
        })
        axes.set_stroke(opacity=10)
        axes.save_state()
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
        exp_sin_graph = axes.get_graph(
            lambda x: math.exp(math.sin(x)),
            color=YELLOW
        )
        exp_sin_graph_semi = axes.get_graph(
            lambda x: math.exp(0.5 * math.sin(x)),
            color=PURPLE
        )
        const_graph = axes.get_graph(
            lambda x: 3,
            color=ORANGE
        )
        self.play(ShowCreation(poly_graph))
        left_dot = Dot(color=RED)
        right_dot = Dot(color=RED)
        left_dot.move_to(axes.i2gp(3, poly_graph))
        right_dot.move_to(axes.i2gp(3, poly_graph))

        left_line = always_redraw(lambda: axes.get_v_line(left_dot.get_bottom()))
        right_line = always_redraw(lambda: axes.get_v_line(right_dot.get_bottom()))

        self.play(FadeIn(left_dot, scale=0.5), FadeIn(right_dot, scale=0.5))
        self.play(ShowCreation(left_line), ShowCreation(right_line))

        left_tracker = ValueTracker(3)
        right_tracker = ValueTracker(3)
        f_always(
            left_dot.move_to,
            lambda: axes.i2gp(left_tracker.get_value(), poly_graph)
        )
        f_always(
            right_dot.move_to,
            lambda: axes.i2gp(right_tracker.get_value(), poly_graph)
        )
        left_end = 2
        right_end = 6
        self.play(left_tracker.animate.set_value(left_end), right_tracker.animate.set_value(right_end), run_time=2)
        # self.embed()
        left_dot.clear_updaters()
        right_dot.clear_updaters()
        graph_list = [poly_graph, sin_graph, exp_sin_graph, exp_sin_graph_semi, const_graph]
        for i in range(len(graph_list) - 1):
            self.play(ReplacementTransform(graph_list[i], graph_list[i + 1]),
                      left_dot.animate.move_to(axes.i2gp(left_end, graph_list[i + 1])),
                      right_dot.animate.move_to(axes.i2gp(right_end, graph_list[i + 1])))
            self.wait()

        const_rect = axes.get_riemann_rectangles(const_graph, [left_end, right_end], dx=3.75, stroke_color=WHITE,
                                                 colors=(ORANGE, BLUE), fill_opacity=0.4)
        right_brace = Brace(const_rect, RIGHT)
        top_brace = Brace(const_rect, UP)
        right_brace_label = right_brace.get_text(
            "Height", font_size=24, gradient=(BLUE, GREEN)
        )
        top_brace_label = top_brace.get_text(
            "Width", font_size=24, gradient=(BLUE, GREEN)
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
                  left_dot.animate.move_to(axes.i2gp(left_end, poly_graph)),
                  right_dot.animate.move_to(axes.i2gp(right_end, poly_graph)))

        # self.play(left_tracker.animate.set_value(-2), right_tracker.animate.set_value(0), run_time=3)
        self.wait()
        dx_list = [1, 0.5, 0.25, 0.1, 0.05, 0.025, 0.01]
        rects_list = VGroup(
            *[
                axes.get_riemann_rectangles(graph=poly_graph, x_range=[left_end, right_end + .01], stroke_width=0,
                                            stroke_color=GREEN,
                                            dx=dx, fill_opacity=0.6)
                for dx in dx_list
            ]
        )
        first_approx = rects_list[0]
        start_rect = first_approx[0]
        start_rect.get_num_points()
        pieces = self.create_const_lines(2, 6, 1, axes, poly_graph, color=YELLOW, opacity=0.7)
        self.play(ShowCreation(pieces), run_time=2)
        self.play(FadeIn(start_rect), run_time=1)

        f_brace = Brace(start_rect, LEFT, buff=0).set_color(YELLOW)
        dx_brace = Brace(start_rect, DOWN, buff=0).set_color(ORANGE)
        f_brace.label = f_brace.get_tex(r'f(x_1)', buff=0).scale(0.8).set_color(f_brace.get_color())
        dx_brace.label = dx_brace.get_tex(r'\Delta x').scale(0.8).set_color(dx_brace.get_color())

        area_in_text = Tex(r'A_1').move_to(start_rect).scale(0.7)
        show_area_text, a1, a2, a3, a4 = Tex(r'\text{Area}\approx ', ' A_1', '+A_2', '+A_3', '+A_4')
        area_tex_list = [show_area_text, a1, a2, a3, a4]
        for x in area_tex_list:
            x.scale(0.7)
        show_area_text.to_corner(UP)
        for i in range(0, len(area_tex_list) - 1):
            area_tex_list[i + 1].next_to(area_tex_list[i])
        self.play(*list(map(GrowFromCenter, [f_brace, dx_brace])),
                  *list(map(Write, [f_brace.label, dx_brace.label])),
                  FadeIn(area_in_text), FadeIn(show_area_text),
                  FadeInFromPoint(area_tex_list[1], area_in_text.get_center()))

        # show_dx, val_show_dx = dx_label = VGroup(
        #     Tex("\Delta x = ", font_size=30),
        #     DecimalNumber(
        #         0,
        #         show_ellipsis=False,
        #         num_decimal_places=2,
        #         include_sign=False,
        #         font_size=30
        #     )
        # )
        # dx_label.arrange(RIGHT)
        # dx_label.to_edge(RIGHT/2)
        # val_show_dx.set_value(dx_list[0])
        # self.play(FadeInFromPoint(dx_label, dx_brace.get_center()))
        dx_brace_group = VGroup(dx_brace, dx_brace.label)
        last_brace = f_brace
        last_area_in_text = area_in_text
        to_remove = []
        for idx, rect in enumerate(first_approx[1:], 2):
            new_area_in_text = Tex(r'A_%d' % idx).move_to(rect).scale(0.7)
            f_next_brace = Brace(rect, LEFT, buff=0).set_color(f_brace.get_color())
            f_next_brace.label = f_next_brace.get_tex(r'f(x_%d)' % idx, buff=0).scale(0.8).set_color(
                f_brace.get_color())
            self.play(FadeIn(rect), dx_brace_group.animate.next_to(rect, DOWN, buff=0),
                      ReplacementTransform(last_brace, f_next_brace),
                      ReplacementTransform(last_brace.label, f_next_brace.label),
                      ReplacementTransform(last_area_in_text, new_area_in_text),
                      FadeInFromPoint(area_tex_list[idx], last_area_in_text.get_center())
                      )
            last_brace = f_next_brace
            last_area_in_text = new_area_in_text
        tex_rect = SurroundingRectangle(VGroup(*area_tex_list[1:]))
        tex_rect.set_stroke(BLUE, 2.5)
        self.play(ShowCreation(tex_rect))
        show_area_sum = Tex(r'Area ', r'\approx', r'\sum\limits_', r'{i=1}^', r'{n}', r'f(x_i)',
                            r'\Delta x',
                            font_size=35)
        show_area_sum[4].set_color(BLUE)
        show_area_sum[2].set_color(GREEN)
        # show_area_sum[5].set_color(YELLOW)
        # show_area_sum[6].set_color(ORANGE)
        # sas = TexText(r'Area ', r'$\approx$', r'$\sum_{i=1}^{n}$', r'$f(x_i)$', r'$\Delta x$', font_size=35)
        show_area_sum.next_to(tex_rect, DOWN)
        self.play(ReplacementTransform(tex_rect, show_area_sum), *list(map(FadeOut, area_tex_list)))
        # self.play(Transform(show_area_sum[0], TexText(r'$\int_a^b$')))
        n_tex, n_value = n_label = VGroup(
            Tex(r'n='),
            DecimalNumber(
                4,
                num_decimal_places=0
            )
        ).scale(0.7)
        dx_tex, dx_value = dx_label = VGroup(
            Tex(r'\Delta x='),
            DecimalNumber(
                1,
                num_decimal_places=2
            )
        ).scale(0.7)
        dx_label.arrange(RIGHT)
        n_label.arrange(RIGHT)
        n_dx_grp = VGroup(n_label, dx_label).arrange(DOWN)
        n_dx_grp.to_edge(RIGHT_SIDE).shift(RIGHT / 1.8)
        self.play(Write(n_dx_grp))

        to_remove += [last_area_in_text, last_brace, last_brace.label, dx_brace_group]
        self.play(*(list(map(FadeOut, to_remove))))
        int_start = TexText(r'$a$').set_color(BLUE)
        int_end = TexText(r'$b$').set_color(GREEN)
        int_start.move_to(axes.c2p(2, -.5))
        int_end.move_to(axes.c2p(6, -.5))
        self.play(axes.animate.restore(), Write(int_start), Write(int_end))
        for k in range(1, len(dx_list)):
            new_approx = rects_list[k]
            self.play(Transform(first_approx, new_approx), FadeOut(pieces),
                      n_value.animate.set_value(len(new_approx)),
                      dx_value.animate.set_value(dx_list[k]),
                      run_time=1)
            pieces = self.create_const_lines(2, 6, dx_list[k], axes, poly_graph, color=YELLOW, opacity=1)
            self.play(FadeIn(pieces), lag_ratio=0.5, time=1)
            self.wait(0.5)
        self.play(show_area_sum.animate.shift(UP))
        sum_rect = SurroundingRectangle(show_area_sum[2:5])
        sum_rect.set_stroke(BLUE, 2.5)
        integral_sign = Tex(r'\int', r'_a', r'^b', r'f(x)', r'\,dx', font_size=35)
        integral_sign[2].set_color(BLUE)
        integral_sign[1].set_color(GREEN)
        # integral_sign[3].set_color(YELLOW)
        # integral_sign[4].set_color(ORANGE)
        integral_sign.next_to(sum_rect, DOWN)
        self.play(ShowCreation(sum_rect))
        self.play(TransformFromCopy(show_area_sum[2:5], integral_sign[0:3]), Uncreate(sum_rect), run_time=1.5)
        fx_rect = SurroundingRectangle(show_area_sum[5])
        dx_rect = SurroundingRectangle(show_area_sum[6])
        fx_rect.set_stroke(BLUE, 2.5)
        dx_rect.set_stroke(BLUE, 2.5)
        self.play(ShowCreation(fx_rect))
        self.play(TransformFromCopy(show_area_sum[5], integral_sign[3]), Uncreate(fx_rect))
        self.play(ShowCreation(dx_rect))
        self.play(TransformFromCopy(show_area_sum[6], integral_sign[4]), Uncreate(dx_rect))
        self.play(ApplyWave(rects_list[-1], rate_func=linear, amplitude=0.7, time_width=0.1, ripples=4), run_time=3)
        int_rect = SurroundingRectangle(integral_sign)
        int_rect.set_stroke(GREEN, 2.5)
        summary = TexText(r'Area under the curve ', r'$f(x)$\\', r' from ', r'$x=$', r'$a$', ' to ', r'$x=$', r'$b$',
                          font_size=32)
        summary[4].set_color(BLUE)
        summary[7].set_color(GREEN)
        summary.next_to(int_rect, DOWN)
        self.play(ShowCreation(int_rect), run_time=2)
        self.play(Write(summary[0:2]))
        self.play(CircleIndicate(summary[1], color=YELLOW, run_time=1))
        self.play(Write(summary[2:5]))
        self.play(CircleIndicate(summary[4], color=BLUE, run_time=1))
        self.play(Write(summary[5:]))
        self.play(CircleIndicate(summary[7], color=GREEN, run_time=1))
        self.play(Uncreate(int_rect))
        self.wait()
        self.play(
            *[FadeOut(mob) for mob in self.mobjects]
        )
        thanks = Text('Thank you for watching!', font_size=35)
        thanks.set_color_by_gradient(BLUE, GREEN)
        self.play(Write(thanks))

    def create_const_lines(self, start, end, step, axes, graph, **kwargs):
        pieces = VGroup()
        for left_x in np.arange(start, end, step):
            y = graph.underlying_function(left_x)
            line = Line(axes.c2p(left_x, y), axes.c2p(left_x + step, y))
            line.set_stroke(**kwargs)
            pieces.add(line)
        return pieces

    def poly_func(self, x):
        return ((x - 1) ** 3 - 5 * (x - 1) ** 2 + 2 * (x - 1) + 30) / 8
