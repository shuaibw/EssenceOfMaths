from manimlib import *


class PlayGround(Scene):
    def construct(self):
        txt = Tex(
            r'LaTeX এ বাংলায় লেখা খুবই সহজ। এটা ব্যবহার করে গানিতিক সূত্রাবলী খুব সহজেই লেখা যায়। এই যেমন আলবার্ট আইনস্টাইনের জনপ্রিয় সমীকরণ-')
        self.play(Write(txt))
