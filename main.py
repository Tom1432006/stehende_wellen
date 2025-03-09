from manim import *
from manim_physics import *
import numpy as np

class Title(Scene):
    def construct(self):
        title = Text('Stehende Wellen\nund\nWellenlängenbestimmung mit Ultraschall')
        author = Text("von Tom Reinisch", font_size=30).to_edge(DOWN)

        wave1 = StandingWave(4, length=14, color=YELLOW)
        content = VGroup(title, wave1).arrange(DOWN, buff=1.5)

        us_empf = Rectangle(width=.6, height=1.2).move_to(wave1)
        us_empf.set_fill(BLACK, opacity=0)

        # play animation
        self.play(Write(title), run_time=4)
        self.play(Write(author))
        self.play(Create(wave1), Create(us_empf))
        wave1.start_wave()

        self.wait(1)
        self.play(us_empf.animate.shift(3.5*RIGHT))
        self.wait(.3)
        self.play(us_empf.animate.shift(7*LEFT))
        self.wait(.5)
        self.play(
            us_empf.animate.scale(50).set_fill(BLACK, opacity=1),
            )
        
class Definition(Scene):
    def construct(self):
        title = Text("Definition").to_corner(UL)
        defi = Text(
            "örtlich konstante Punkte maximaler und minimaler Ausdehnung",
            t2c={"örtlich konstant": RED},
        ).scale(.6).to_corner(UL).shift(DOWN)
        wave = StandingWave(4, length=14, color=YELLOW).shift(2*DOWN)

        knoten = Text("Knoten")
        arrow_k= Arrow(start=knoten.get_bottom(), end= (0, -2, 0), stroke_width=4)

        bauch = Text("Bauch").move_to((3, 1, 0))
        arrow_b = Arrow(start=bauch.get_bottom(), end=(3.5/2, -1, 0), stroke_width=4)

        self.play(Write(title))
        self.play(Create(wave))
        self.wait(2)
        self.play(Write(defi))
        self.wait(6)
        self.play(Write(knoten), GrowArrow(arrow_k))
        self.wait(2)
        self.play(Write(bauch), GrowArrow(arrow_b))
        wave.start_wave()
        self.wait(5)

class Entstehung(Scene):
    def construct(self):
        left_boundary = ValueTracker(-PI)
        right_boundary = ValueTracker(2*PI)

        l_shift = ValueTracker(0)
        r_shift = ValueTracker(0)

        title = Text("Entstehung:").to_corner(UL)
        l1 = Text("eingehende Welle", font_size=25, color=RED)
        l2 = Text("reflektierte Welle", font_size=25, color=BLUE)
        l3 = Text("Überlagerung als stehende Welle", font_size=25, color=YELLOW)
        legend = VGroup(l1, l2, l3).arrange(DOWN, aligned_edge=RIGHT).to_corner(UR)

        ende_text_fest = Text("festes Ende", font_size=25).to_corner(UL).shift(1.5*DOWN)
        ende_text_frei = Text("freies Ende", font_size=25).to_corner(UL).shift(1.5*DOWN)

        def func1(t):
            if t > left_boundary.get_value(): return 0
            return 0.75*np.sin(t - l_shift.get_value()) 
        
        def func2(t):
            if t < right_boundary.get_value():
                return 0
            return -0.75*np.sin(t - r_shift.get_value()) 
        
        number_line = NumberLine()
        wall = Line(Point((2*PI, -1.5, 0)), Point((2*PI, 1.5, 0)), color=WHITE)
        laser = Rectangle(width=3, height=3).move_to(Point((-2*PI-1.5, 0, 0))).set_fill(BLACK, opacity=1)
        versuch = VGroup(number_line, laser, wall)

        line = Line(Point((-2*PI, -2, 0)), Point((2*PI, -2, 0)))
        end_lines = VGroup(
            Line(Point((-2*PI, -2.15, 0)), Point((-2*PI, -1.85, 0))),
            Line(Point((2*PI, -2.15, 0)), Point((2*PI, -1.85, 0)))
        )
        line_label = Tex(r"Länge $l$", font_size=45).move_to(line.get_bottom()).shift(0.5*DOWN)


        f1 = always_redraw(lambda: FunctionGraph(func1, color=RED, x_range=[-2*PI, 2*PI]))
        f2 = always_redraw(lambda: FunctionGraph(func2, color=BLUE, x_range=[-2*PI, 2*PI]))
        standing_wave = always_redraw(lambda: FunctionGraph(lambda t: func1(t) + func2(t), color=YELLOW, x_range=[-2*PI, 2*PI]))


        # Start
        self.play(Write(title))
        self.wait(.5)
        self.play(Write(legend))
        self.play(FadeIn(versuch))
        self.play(Create(line))
        self.play(Create(end_lines), Write(line_label))

        self.play(FadeIn(f1))

        self.wait(5)

        # eingehende Welle
        offset = 3
        self.play(
            left_boundary.animate.increment_value(offset*PI),
            l_shift.animate.increment_value(offset*PI),
            run_time=2*offset, rate_func=linear)
        
        self.wait(2)
        self.play(Write(ende_text_fest))
        self.wait(1.5)
        
        # Add stading wave
        self.add(f2, standing_wave)
        offset = 5
        self.play(
            l_shift.animate.increment_value(offset*PI),
            r_shift.animate.increment_value(-offset*PI),
            right_boundary.animate.increment_value(-offset*PI),
            run_time=2*offset, rate_func=linear)
        
        self.remove(f1, f2)
        
        # only show the standing wave
        self.play(
            l_shift.animate.increment_value(offset*PI),
            r_shift.animate.increment_value(-offset*PI),
            run_time=2*offset, rate_func=linear)
        
        self.wait(2)
        self.play(Transform(ende_text_fest, ende_text_frei), run_time=1)
        self.wait(1.5)

        l_shift.increment_value(-2*offset*PI)
        r_shift.increment_value(2*offset*PI)

        # redefinieren der reflektierten Welle für die reflecion am freien Ende
        def func2(t):
            if t < right_boundary.get_value():
                return 0
            return 0.75*np.sin(t - r_shift.get_value())
        
        self.play(FadeIn(f1, f2))

        offset = 5
        self.play(
            l_shift.animate.increment_value(offset*PI),
            r_shift.animate.increment_value(-offset*PI),
            right_boundary.animate.increment_value(-offset*PI),
            run_time=2*offset, rate_func=linear)
        
        self.remove(f1, f2)

        offset=10
        
        # only show the standing wave
        self.play(
            l_shift.animate.increment_value(offset*PI),
            r_shift.animate.increment_value(-offset*PI),
            run_time=2*offset, rate_func=linear)
        
        self.wait(3)

class Grundschwingung(Scene):
    def construct(self):
        title = Text("Grundschwingung (n=0)").to_corner(UL)

        self.play(Write(title))

        # add one wave as an example
        wave = StehendeWelle(n = 0, length=7, height=2, color=YELLOW)
        self.add(wave)
        self.wait(1)
        self.play(wave.animate_wave(50), run_time=5, rate_func=linear)
    
        # add Image and Formulars
        image_buch = ImageMobject("grundschwingung.png").scale_to_fit_width(14)

        self.play(FadeIn(image_buch), FadeOut(wave))
        self.wait(9)

        f1 = Tex(r"$l = \frac{1}{2}\lambda_0$", font_size=50).shift(2*LEFT+2*DOWN)
        f2 = Tex(r"$l = \frac{1}{4}\lambda_0$", font_size=50).shift(2*RIGHT+2*DOWN)

        self.play(Write(f1))
        self.wait(4)
        self.play(Write(f2))
        self.wait(5)

class Oberschwingung(Scene):
    def construct(self):
        title = Text("Oberschwingung:").to_corner(UL)

        self.play(Write(title))

        # Create a Table
        waves = [
            [
                StehendeWelle(n = i, length=4, height=.8, color=YELLOW, end_left_type=FEST, end_right_type=FEST),
                StehendeWelle(n = i, length=4, height=.8, color=YELLOW, end_left_type=FREI, end_right_type=FREI),
                StehendeWelle(n = i, length=4, height=.8, color=YELLOW, end_left_type=FEST, end_right_type=FREI)
            ] for i in range(1, 4)
        ]

        waves_groups = [VGroup(*wave).arrange(DOWN).move_to(ORIGIN) for wave in waves]

        # save all the positions of every wave
        for wave_group in waves:
            for w in wave_group:
                w.save_pos()

        for i in range(0, 3):
            self.add(waves_groups[i])
            text = Text(f"n={i+1}").to_corner(UL).shift(DOWN)
            self.add(text)
            self.wait(1)
            self.play(*[w.animate_wave(5/(i+1)) for w in wave_group for wave_group in waves], run_time=5, rate_func=linear)
            if i != 2: self.remove(waves_groups[i])
            self.remove(text)
        
        # save all the positions of every wave
        waves_groups[2].move_to(ORIGIN).to_edge(LEFT)
        for w in waves_groups[2]:
            w.save_pos()
        waves_groups[2].move_to(ORIGIN)

        self.play(waves_groups[2].animate.to_edge(LEFT))

        self.wait(1)
        
        # show formulars
        f1 = Tex(r"$l = (n+1)\frac{\lambda_n}{2}$", font_size=50).shift(2*RIGHT+UP)
        f2 = Tex(r"$l = (2n+1)\frac{\lambda_n}{4}$", font_size=50).shift(2*RIGHT+DOWN)

        f1_u = Tex(r"$\lambda_n = \frac{2l}{n+1}$", font_size=50).shift(2*RIGHT+UP)
        f2_u = Tex(r"$\lambda_n = \frac{4l}{2n+1}$", font_size=50).shift(2*RIGHT+DOWN)

        self.play(Write(f1))
        self.play(Write(f2))

        self.wait(5)

        self.play(TransformMatchingShapes(f1, f1_u))
        self.play(TransformMatchingShapes(f2, f2_u))

        self.wait(5)

class Ultraschall(Scene):
    def construct(self):
        title = Text("Wellenlängenbestimmung mit \neinem US-Empfänger:").to_corner(UL)
        self.play(Write(title), run_time=3)

        wave = StandingWave(n=5, length=14, amplitude=2, color=YELLOW)

        self.play(Create(wave))
        self.wait()

        us_empf = Rectangle(width=.6, height=1.2).move_to(Point((-6, 0, 0))).set_fill(BLACK, opacity=.5)
        us_label = Text("US", font_size=30)
        def text_updater(m):
            m.move_to(us_empf.get_center())
        us_label.add_updater(text_updater)

        nl = NumberLine(include_numbers=True,).to_edge(DOWN)

        self.play(Create(us_empf), Create(nl))
        self.play(Write(us_label))

        wave.start_wave()

        self.wait(3)

        # save the different mesurement
        m = [
            DecimalNumber(2.82),
            DecimalNumber(2.81),
            DecimalNumber(2.77)
        ]
        dots = [Dot() for _ in range(3)]
        refrence_points_for_measurements = VGroup(*dots).arrange(DOWN, buff=.3).to_corner(UR).shift(.5*LEFT)

        d_knoten = 14/5

        # animate the measuring
        self.play(us_empf.animate.shift((d_knoten-1)*RIGHT))
        self.wait(4)
        for i in range(3):
            self.play(us_empf.animate.shift(d_knoten*RIGHT), rate_func=rate_functions.ease_out_sine)
            m[i].move_to(us_empf.get_center())
            self.add(m[i])
            self.play(m[i].animate.move_to(dots[i].get_center()))
            if i == 0: self.wait(5)
            self.wait()
        
        measurements = VGroup(*[m[i] for i in range(3)])
        result = DecimalNumber(2.8).to_corner(UR)
        double_result = DecimalNumber(5.6).to_corner(UR)

        self.play(Transform(measurements, result))
        self.wait(5)
        self.play(FadeIn(double_result), FadeOut(measurements))
        self.wait(.1)
        self.play(Circumscribe(double_result))
        self.wait()
    
class Realitaet(Scene):
    def construct(self):
        title = Text("Stehende Wellen in der Realität: ").to_corner(UL)
        self.play(Write(title))

        seil = ImageMobject("seil.png").scale_to_fit_width(7)
        gitarre = ImageMobject("guitar-2119_1920.jpg").scale_to_fit_width(4)

        images = Group(seil, gitarre).arrange(DOWN).to_edge(DOWN)

        self.play(FadeIn(seil))
        self.wait(10)
        self.play(FadeIn(gitarre))
        self.wait(7)

class Zusammenfassung(Scene):
    def construct(self):
        title = Text("Zusammenfassung: ").to_corner(UL)
        self.play(Write(title))

        defi = Text(
            "• Wellen mit örtlich konstanten Punkte maximaler\n  und minimaler Ausdehnung",
            t2c={"örtlich konstanten": RED},
        ).scale(.6).to_corner(UL).shift(DOWN)
        wave = StandingWave(4, length=14, color=YELLOW).shift(2*DOWN)

        knoten = Text("Knoten").move_to((-3.5, 0, 0))
        arrow_k= Arrow(start=knoten.get_bottom(), end= (-3.5, -2, 0), stroke_width=4)

        bauch = Text("Bauch").move_to((-5, 1, 0))
        arrow_b = Arrow(start=bauch.get_bottom(), end=(-7+3.5/2, -1, 0), stroke_width=4)

        self.play(Create(wave))
        self.wait(2)
        self.play(Write(defi))
        self.wait(2)
        self.play(Write(knoten), GrowArrow(arrow_k))
        self.wait()
        self.play(Write(bauch), GrowArrow(arrow_b))
        wave.start_wave()
        self.wait(3)

        # Line
        line_height = -3.2
        line = Line(Point((-7, line_height, 0)), Point((7, line_height, 0)))
        end_lines = VGroup(
            Line(Point((-7, line_height-.15, 0)), Point((-7, line_height+.15, 0))),
            Line(Point((7, line_height-.15, 0)), Point((7, line_height+.15, 0)))
        )
        line_label = Tex(r"Länge $l$", font_size=45).move_to(line.get_bottom()).shift(0.5*DOWN)

        self.play(Create(line))
        self.play(Create(end_lines), Write(line_label))

        self.wait(6)

        # show formulars
        f1 = Tex(r"$l = (n+1)\frac{\lambda_n}{2}$", font_size=50).shift(2*RIGHT+UP)
        f2 = Tex(r"$l = (2n+1)\frac{\lambda_n}{4}$", font_size=50).shift(2*RIGHT)

        f1_u = Tex(r"$\lambda_n = \frac{2l}{n+1}$", font_size=50).shift(2*RIGHT+UP)
        f2_u = Tex(r"$\lambda_n = \frac{4l}{2n+1}$", font_size=50).shift(2*RIGHT)

        self.play(Write(f1))
        self.play(Write(f2))
        self.wait(3)
        self.play(TransformMatchingShapes(f1, f1_u), TransformMatchingShapes(f2, f2_u))
        self.wait(3)

class Outro(Scene):
    def construct(self):
        t = Text("Viel Erfolg beim Lernen :)")
        self.play(Write(t))
        self.wait(3)

FEST, FREI, = 0, 1

class StehendeWelle(VMobject):
    left_boundary = 0
    right_boundary = 0
    n = 0
    height = 0

    end_left_type = FEST
    end_right_type = FEST

    shift_w = ValueTracker(0)

    current_position = ORIGIN

    standing_wave = None

    def __init__(self, n=0, length=1, height=1, color=WHITE, end_left_type=FEST, end_right_type=FEST, **kwargs):
        super().__init__(**kwargs)

        self.n = n
        self.height = height
        self.end_left_type = end_left_type
        self.end_right_type = end_right_type

        # calculate the wavelength and the range of the wave
        if end_left_type == end_right_type:
            wavelength = (2*length) / (n+1)
            x_range = [0, length]
            if end_left_type == FREI: x_range = [wavelength/4, (wavelength/4)+length]
        else:
            wavelength = (4*length) / (2*n+1)
            if end_left_type==FREI: x_range = [0, length]
            elif end_left_type==FEST: x_range = [-length, 0]
        
        if n == 0: x_range = None

        def func1(t):
            return 0.5*height*np.sin(2*PI*(t - self.shift_w.get_value()) / wavelength) 
        
        def func2(t):
            return 0.5*height*np.sin(2*PI*(t + self.shift_w.get_value()) / wavelength) 

        # shift wave to the middle, if the end types aren't the same,
        # because then, is isn't symmetrical around the y-Axis
        correct_to_center = 0
        if end_left_type != end_right_type:
            if end_left_type==FREI: correct_to_center = 0.5*length*LEFT
            elif end_left_type==FEST: correct_to_center = 0.5*length*RIGHT
        else:
            if end_left_type == FEST: correct_to_center = 0.5*length*LEFT
            else: correct_to_center = 0.5*length*LEFT + (wavelength/4)*LEFT

        self.standing_wave = always_redraw(
            lambda: FunctionGraph(
                lambda t: func1(t) + func2(t),
                color=color, x_range=x_range)
                .move_to(self.current_position)
                .shift(correct_to_center)
        )

        correct_to_center = 0

        self.add(self.standing_wave)

        # add rectangles for the n = 0 case, because when using x_range it is not
        # centerd properly and does not swing the way it is supposed to
        if n == 0:
            rect1 = Rectangle(height=height*2, width=10, color=BLACK).set_fill(BLACK).set_opacity(1).shift((5+length/2)*LEFT)

            rect2 = Rectangle(height=height*2, width=10, color=BLACK).set_fill(BLACK).set_opacity(1).shift((5+length/2)*RIGHT)

            self.add(rect1, rect2)
        
        self.save_pos()
    
    def save_pos(self):
        self.current_position = self.standing_wave.get_center()
    
    def animate_wave(self, offset=1):
        if self.end_left_type != self.end_right_type:
            offset *= 4
        return self.shift_w.animate.increment_value(offset)
