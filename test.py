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

        sin_label = axes.get_graph_label(sin_graph, "\\sin(x)")
        relu_label = axes.get_graph_label(relu_graph, Text("Linear"))
        poly_label = axes.get_graph_label(poly_graph, Text("Poly"), x=4)

        self.play(
            ShowCreation(sin_graph),
            FadeIn(sin_label, RIGHT),
        )
        self.wait()
        self.play(
            ReplacementTransform(sin_graph, relu_graph),
            FadeTransform(sin_label, relu_label),
        )
        self.wait()
        self.play(
            ReplacementTransform(relu_graph, poly_graph),
            FadeTransform(relu_label, poly_label),
        )
        self.wait()