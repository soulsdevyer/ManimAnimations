from manim import *
import numpy as np

"""
Animación didáctica (Manim Community ≥ 0.17)

Tema: Lanzamiento de jabalina (tiro parabólico) desde 1.75 m con V0 = 7.93 m/s a 45°.

Este archivo contiene:
- S1_VistaGeneralJabalina  -> vista general del movimiento (ya implementada previamente)
- S2_DescomposicionVelocidad -> justifica y calcula V0x y V0y (implementada aquí)
- S3–S7 -> stubs para las escenas siguientes

Comandos de render:
# manim -pql jabalina.py S2_DescomposicionVelocidad
# manim -pqh jabalina.py S2_DescomposicionVelocidad
"""

# ===================== Parámetros reutilizables ===================== #
G = 9.8  # m/s^2
V0 = 7.93
ANGLE_DEG = 45
Y0 = 1.75

# Colores y estilo
C_X = BLUE_D
C_Y = GREEN_D
C_RESULT = ORANGE
C_JAVELIN = GREY_E
C_TRACE = GREY_B

def flight_time(v0y: float, y0: float, g: float = G) -> float:
    """Tiempo total de vuelo resolviendo y(t)=0 con y(t)=y0+v0y t - 1/2 g t^2 (raíz positiva)."""
    disc = v0y**2 + 2 * g * y0
    return (v0y + np.sqrt(disc)) / g


# ===================== S1 (ya existente) ===================== #
class S1_VistaGeneralJabalina(Scene):
    def construct(self):
        angle = np.deg2rad(ANGLE_DEG)
        v0x = V0 * np.cos(angle)
        v0y = V0 * np.sin(angle)
        T = flight_time(v0y, Y0, G)
        axes = Axes(
            x_range=[0, 10, 1], y_range=[0, 4.5, 0.5], x_length=10, y_length=5,
            axis_config={"include_numbers": True, "font_size": 28}, tips=False
        ).to_edge(DL).shift(RIGHT * 0.2 + UP * 0.2)
        x_label = MathTex("x\\,(\\text{m})", color=C_X).scale(0.6).next_to(axes.x_axis, RIGHT, buff=0.25)
        y_label = MathTex("y\\,(\\text{m})", color=C_Y).scale(0.6).next_to(axes.y_axis, UP, buff=0.25)
        base = axes.c2p(0, 0)
        start_pt = axes.c2p(0, Y0)
        height_bar = Line(base, start_pt, color=C_Y)
        height_lbl = MathTex("1.75\\,\\text{m}", color=C_Y).scale(0.6).next_to(height_bar, LEFT, buff=0.2)
        athlete = VGroup(
            Circle(radius=0.08, color=WHITE, fill_opacity=1).move_to(start_pt + LEFT * 0.25 + UP * 0.25),
            Line(start_pt + LEFT * 0.25, start_pt + RIGHT * 0.15, color=WHITE),
        )
        v0_arrow = Arrow(start_pt, start_pt + 0.6 * RIGHT + 0.6 * UP, buff=0, color=YELLOW)
        v0_tex = MathTex("\\vec{V}_0=7.93\\,\\text{m/s}\\;45^\\circ", color=YELLOW).scale(0.6)\
            .next_to(v0_arrow, UR, buff=0.15)
        vx_arrow = Arrow(start_pt, start_pt + 0.85 * RIGHT, buff=0, color=C_X)
        vy_arrow = Arrow(start_pt, start_pt + 0.85 * UP, buff=0, color=C_Y)
        vx_tex = MathTex("V_{0x}=V_0\\cos45^\\circ\\approx 5.6", color=C_X).scale(0.6)\
            .next_to(vx_arrow, DOWN, buff=0.1)
        vy_tex = MathTex("V_{0y}=V_0\\sin45^\\circ\\approx 5.6", color=C_Y).scale(0.6)\
            .next_to(vy_arrow, LEFT, buff=0.1)
        t_tracker = ValueTracker(0.0)
        t_disp = always_redraw(
            lambda: MathTex("t=\\,{:.2f}\\,\\text{{s}}".format(t_tracker.get_value())).scale(0.6).to_corner(UR).shift(LEFT * 0.5)
        )
        v_disp = VGroup(
            MathTex("V_{0x}=5.6\\,\\text{m/s}", color=C_X).scale(0.55),
            MathTex("V_{0y}=5.6\\,\\text{m/s}", color=C_Y).scale(0.55),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.05).next_to(t_disp, DOWN, buff=0.2).shift(LEFT * 0.1)
        javelin = Line(ORIGIN, 0.35 * RIGHT, stroke_width=6, color=C_JAVELIN)
        tip = Triangle(stroke_width=0, fill_opacity=1, fill_color=C_JAVELIN).scale(0.06).next_to(javelin, RIGHT, buff=0)
        javelin_grp = VGroup(javelin, tip).move_to(start_pt).set_z_index(2)

        def pos_at(t):
            x = v0x * t
            y = Y0 + v0y * t - 0.5 * G * t**2
            return axes.c2p(x, y)

        def update_javelin(mob):
            t = t_tracker.get_value()
            p = pos_at(t)
            dt = 1e-3
            p2 = pos_at(min(t + dt, T))
            direction = p2 - p
            angle = np.arctan2(direction[1], direction[0])
            mob.move_to(p)
            mob.set_angle(angle)
            return mob

        javelin_grp.add_updater(update_javelin)
        trace = TracedPath(lambda: javelin_grp.get_center(), stroke_color=C_TRACE, stroke_width=3)
        eq_y = MathTex("y=y_0+V_{0y}t-\\tfrac{1}{2}gt^2", "\\Rightarrow", "0=1.75+5.6\\,t-4.9\\,t^2")\
            .scale(0.65).to_corner(UL).shift(DOWN * 0.2)
        eq_x = MathTex("x=x_0+V_{0x}t", "=", "5.6\\,t").scale(0.65).next_to(eq_y, DOWN, aligned_edge=LEFT, buff=0.2)

        self.play(Create(axes), FadeIn(x_label, y_label), run_time=1.1)
        self.play(LaggedStart(FadeIn(height_bar), Write(height_lbl), FadeIn(athlete), lag_ratio=0.3), run_time=1.6)
        self.play(GrowArrow(v0_arrow), Write(v0_tex), run_time=1.6, rate_func=smooth)
        self.play(ReplacementTransform(v0_arrow.copy(), vx_arrow), Write(vx_tex), run_time=1.2)
        self.play(ReplacementTransform(v0_arrow.copy(), vy_arrow), Write(vy_tex), run_time=1.2)
        self.wait(0.4)
        self.play(FadeOut(vx_arrow, vy_arrow, vx_tex, vy_tex), run_time=0.6)
        self.play(FadeIn(javelin_grp), run_time=0.4)
        self.add(trace, t_disp, v_disp)
        self.play(Write(eq_y), run_time=1.0)
        self.play(Write(eq_x), run_time=0.8)
        self.play(t_tracker.animate.set_value(flight_time(v0y, Y0)), run_time=5.0, rate_func=rate_functions.ease_in_out_sine)
        self.wait(0.3)
        self.play(Circumscribe(eq_y[2], color=C_RESULT, time_width=0.6), run_time=0.8)
        self.play(Circumscribe(eq_x[2], color=C_RESULT, time_width=0.6), run_time=0.8)
        self.wait(0.6)


# ===================== S2 (implementada) ===================== #
class S2_DescomposicionVelocidad(Scene):
    """
    Justifica y calcula las componentes V0x y V0y a partir de V0 y el ángulo de 45°.
    Fórmulas aparecen, se usan, y desaparecen secuencialmente para evitar
    sobreposiciones y mantener el foco visual.
    """
    def construct(self):
        angle_rad = np.deg2rad(ANGLE_DEG)

        # --- Título ---
        title = Tex("Descomposición de la velocidad inicial").to_edge(UP)
        self.play(Write(title), run_time=1.0)

        # --- Vector inicial y triángulo ---
        origin = ORIGIN + LEFT * 3 + DOWN * 1
        v0_vec = 3.0 * np.array([np.cos(angle_rad), np.sin(angle_rad), 0.0])

        hyp = Arrow(origin, origin + v0_vec, buff=0, color=YELLOW)
        cat_x = Arrow(origin, origin + np.array([v0_vec[0], 0, 0]), buff=0, color=C_X)
        cat_y = Arrow(origin, origin + np.array([0, v0_vec[1], 0]), buff=0, color=C_Y)
        arc = Arc(start_angle=0, angle=angle_rad, radius=0.6, color=WHITE).move_arc_center_to(origin)
        ang_lbl = MathTex("45^\\circ").scale(0.7).next_to(arc, RIGHT, buff=0.15)

        v0_lbl = MathTex("\\vec{V}_0 = 7.93\\,\\text{m/s}").scale(0.8).next_to(hyp.get_end(), UR, buff=0.2).set_color(YELLOW)

        self.play(GrowArrow(hyp), Create(arc), FadeIn(ang_lbl), run_time=1.4)
        self.play(Write(v0_lbl), run_time=0.6)

        # --- Componentes visuales ---
        self.play(GrowArrow(cat_x), GrowArrow(cat_y), run_time=0.8)
        vx_txt = MathTex("V_{0x}").set_color(C_X).scale(0.8).next_to(cat_x, DOWN, buff=0.1)
        vy_txt = MathTex("V_{0y}").set_color(C_Y).scale(0.8).next_to(cat_y, LEFT, buff=0.1)
        self.play(FadeIn(vx_txt), FadeIn(vy_txt), run_time=0.4)

        # --- Fórmula simbólica V0x ---
        f_vx_sym = MathTex("V_{0x} = V_0 \\cos\\theta", color=C_X).to_edge(RIGHT).shift(UP * 1.5)
        self.play(Write(f_vx_sym), run_time=0.8)

        # Sustitución numérica V0x
        f_vx_num = MathTex("V_{0x} = 7.93 \\cos 45^\\circ", color=C_X).move_to(f_vx_sym)
        self.play(TransformMatchingTex(f_vx_sym, f_vx_num), run_time=0.8)

        # Evaluación numérica V0x
        f_vx_res = MathTex("V_{0x} \\approx 5.6\\,\\text{m/s}", color=C_X).move_to(f_vx_num)
        self.play(TransformMatchingTex(f_vx_num, f_vx_res), run_time=0.8)
        self.play(Circumscribe(f_vx_res, color=C_X), run_time=0.6)

        # Reemplazar etiqueta en el triángulo
        vx_len = MathTex("5.6", color=C_X).scale(0.8).next_to(cat_x, DOWN, buff=0.05)
        self.play(Transform(vx_txt, vx_len), run_time=0.6)

        # --- Limpiar zona antes de V0y ---
        self.play(FadeOut(f_vx_res), run_time=0.4)

        # --- Fórmula simbólica V0y ---
        f_vy_sym = MathTex("V_{0y} = V_0 \\sin\\theta", color=C_Y).to_edge(RIGHT).shift(UP * 1.5)
        self.play(Write(f_vy_sym), run_time=0.8)

        # Sustitución numérica V0y
        f_vy_num = MathTex("V_{0y} = 7.93 \\sin 45^\\circ", color=C_Y).move_to(f_vy_sym)
        self.play(TransformMatchingTex(f_vy_sym, f_vy_num), run_time=0.8)

        # Evaluación numérica V0y
        f_vy_res = MathTex("V_{0y} \\approx 5.6\\,\\text{m/s}", color=C_Y).move_to(f_vy_num)
        self.play(TransformMatchingTex(f_vy_num, f_vy_res), run_time=0.8)
        self.play(Circumscribe(f_vy_res, color=C_Y), run_time=0.6)

        # Reemplazar etiqueta en el triángulo
        vy_len = MathTex("5.6", color=C_Y).scale(0.8).next_to(cat_y, LEFT, buff=0.05)
        self.play(Transform(vy_txt, vy_len), run_time=0.6)

        # --- Cierre ---
        self.play(FadeOut(f_vy_res), run_time=0.4)
        box = SurroundingRectangle(VGroup(vx_len, vy_len), color=C_RESULT, buff=0.2, corner_radius=0.08)
        self.play(Create(box), Flash(vx_len), Flash(vy_len), run_time=1.0)
        self.wait(0.8)



# ===================== Stubs (sin lógica) ===================== #
class S3_ModeloHorizontal(Scene):
    """
    Explica el modelo horizontal del lanzamiento:
    - No hay aceleración horizontal: a_x = 0
    - Velocidad horizontal constante: Vx = V0x
    - Posición: x = x0 + V0x * t
    Presenta cada idea de forma secuencial, usando y limpiando el área para evitar sobreposiciones.
    """
    def construct(self):
        # --- Título ---
        title = Tex("Movimiento horizontal en el lanzamiento").to_edge(UP)
        self.play(Write(title), run_time=1.0)

        # --- Primer concepto: a_x = 0 ---
        ax_eq = MathTex("a_x = 0", color=C_X).scale(1.2).shift(UP * 1)
        note_const = Tex("No hay aceleración horizontal").scale(0.8).next_to(ax_eq, DOWN)
        self.play(Write(ax_eq), FadeIn(note_const), run_time=1.0)
        self.play(Circumscribe(ax_eq, color=C_X), run_time=0.8)

        # Limpiar para siguiente paso
        self.play(FadeOut(ax_eq), FadeOut(note_const), run_time=0.5)

        # --- Segundo concepto: Vx constante ---
        vx_eq = MathTex("V_x = V_{0x}", color=C_X).scale(1.1).shift(UP * 1)
        sub_vx = MathTex("V_x = 5.6\\,\\text{m/s}", color=C_X).scale(1.1).move_to(vx_eq)
        self.play(Write(vx_eq), run_time=0.8)
        self.play(TransformMatchingTex(vx_eq, sub_vx), run_time=0.8)
        self.play(Circumscribe(sub_vx, color=C_X), run_time=0.6)

        # Limpiar para siguiente paso
        self.play(FadeOut(sub_vx), run_time=0.5)

        # --- Tercer concepto: posición horizontal ---
        x_eq_sym = MathTex("x = x_0 + V_{0x} t", color=C_X).scale(1.0).shift(UP * 1)
        self.play(Write(x_eq_sym), run_time=0.8)

        # Sustitución con x0 = 0 y V0x = 5.6
        x_eq_num = MathTex("x = 0 + 5.6\\,t", color=C_X).scale(1.0).move_to(x_eq_sym)
        self.play(TransformMatchingTex(x_eq_sym, x_eq_num), run_time=0.8)

        # Resaltar forma final
        self.play(Circumscribe(x_eq_num, color=C_X), run_time=0.6)

        # Limpiar fórmulas y cerrar
        self.play(FadeOut(x_eq_num), run_time=0.5)

        # --- Diagrama visual de apoyo ---
        axes = Axes(
            x_range=[0, 10, 2],
            y_range=[0, 1, 1],
            x_length=8,
            y_length=1.5,
            tips=False
        ).shift(DOWN * 1.5)
        dot = Dot(axes.c2p(0, 0), color=C_RESULT)
        self.play(Create(axes), FadeIn(dot), run_time=1.0)

        # Movimiento constante en x
        self.play(dot.animate.move_to(axes.c2p(8, 0)), run_time=4.0, rate_func=linear)
        self.wait(0.5)

class S4_ModeloVertical(Scene):
    """
    Explica el modelo vertical del lanzamiento:
    - Movimiento uniformemente acelerado con aceleración = -g.
    - Ecuación: y = y0 + V0y * t - (1/2) g t^2
    - Sustitución de valores y forma final que se usará para calcular el tiempo de vuelo.
    Incluye apoyo visual de la trayectoria parabólica.
    """
    def construct(self):
        # --- Título ---
        title = Tex("Movimiento vertical en el lanzamiento").to_edge(UP)
        self.play(Write(title), run_time=1.0)

        # --- Ejes y trayectoria ---
        axes = Axes(
            x_range=[0, 9, 1],
            y_range=[0, 4.5, 0.5],
            x_length=8,
            y_length=4,
            tips=False
        ).shift(DOWN * 1.5)

        angle_rad = np.deg2rad(ANGLE_DEG)
        v0x = V0 * np.cos(angle_rad)
        v0y = V0 * np.sin(angle_rad)

        def x_t(t): return v0x * t
        def y_t(t): return Y0 + v0y * t - 0.5 * G * t**2

        T = (v0y + np.sqrt(v0y**2 + 2 * G * Y0)) / G

        traj = axes.plot_parametric_curve(
            lambda t: [x_t(t), y_t(t), 0],
            t_range=[0, T],
            color=YELLOW
        )

        dot = Dot(color=C_RESULT).move_to(axes.c2p(0, Y0))

        self.play(Create(axes), run_time=1.0)
        self.play(Create(traj), FadeIn(dot), run_time=1.2)

        # --- Ecuación general del MRUA vertical ---
        eq_sym = MathTex("y = y_0 + V_{0y} t - \\tfrac{1}{2} g t^2", color=C_Y).scale(1.0).shift(UP * 1)
        self.play(Write(eq_sym), run_time=1.0)

        # Sustitución de valores
        eq_sub1 = MathTex(
            "y = 1.75 + 5.6\\,t - 4.9\\,t^2", color=C_Y
        ).move_to(eq_sym)
        self.play(TransformMatchingTex(eq_sym, eq_sub1), run_time=1.0)

        # Resaltar que describe la altura en función del tiempo
        self.play(Circumscribe(eq_sub1, color=C_Y), run_time=0.8)

        # Limpiar ecuación para siguiente paso
        self.play(FadeOut(eq_sub1), run_time=0.5)

        # --- Caso para encontrar el tiempo de vuelo ---
        eq_time_sym = MathTex(
            "0 = 1.75 + 5.6\\,t - 4.9\\,t^2", color=C_Y
        ).shift(UP * 1)
        note = Tex("Condición: impacto en el suelo $(y=0)$").scale(0.8).next_to(eq_time_sym, DOWN)
        self.play(Write(eq_time_sym), FadeIn(note), run_time=1.2)
        self.play(Circumscribe(eq_time_sym, color=C_Y), run_time=0.8)

        # Mantener la ecuación de tiempo para enlazar con S5
        self.wait(0.5)

        # --- Movimiento del punto sincronizado con parábola ---
        t_tracker = ValueTracker(0.0)
        dot.add_updater(lambda m: m.move_to(axes.c2p(x_t(t_tracker.get_value()), y_t(t_tracker.get_value()))))
        self.play(t_tracker.animate.set_value(T), run_time=4.0, rate_func=linear)
        dot.clear_updaters()
        self.wait(0.5)


class S5_CalculoTiempo(Scene):
    """
    Resuelve la ecuación cuadrática 0 = 1.75 + 5.6 t - 4.9 t^2 para hallar el tiempo de vuelo.
    - Presenta la ecuación obtenida en S4.
    - Aplica la fórmula general paso a paso.
    - Muestra el resultado positivo t ≈ 1.40 s, limpiando fórmulas intermedias.
    """
    def construct(self):
        # --- Título ---
        title = Tex("Cálculo del tiempo de vuelo").to_edge(UP)
        self.play(Write(title), run_time=1.0)

        # --- Ecuación inicial (heredada de S4) ---
        eq_ini = MathTex("0 = 1.75 + 5.6\\,t - 4.9\\,t^2", color=C_Y).shift(UP * 1)
        self.play(Write(eq_ini), run_time=1.0)

        # --- Reordenar términos ---
        eq_ord = MathTex("0 = -4.9\\,t^2 + 5.6\\,t + 1.75", color=C_Y).move_to(eq_ini)
        self.play(TransformMatchingTex(eq_ini, eq_ord), run_time=1.0)

        # Limpiar para siguiente paso
        self.play(FadeOut(eq_ord), run_time=0.5)

        # --- Fórmula general ---
        formula_gen = MathTex(
            "t = \\frac{-b \\pm \\sqrt{b^2 - 4ac}}{2a}"
        ).scale(1.0).shift(UP * 1)
        self.play(Write(formula_gen), run_time=1.2)

        # Sustituir a, b, c
        subs_abc = MathTex(
            "t = \\frac{ -5.6 \\pm \\sqrt{(5.6)^2 - 4(-4.9)(1.75)} }{ 2(-4.9) }"
        ).scale(1.0).move_to(formula_gen)
        self.play(TransformMatchingTex(formula_gen, subs_abc), run_time=1.4)

        # Limpiar para cálculo discriminante
        self.play(FadeOut(subs_abc), run_time=0.5)

        # --- Calcular discriminante ---
        disc_eq = MathTex(
            "\\Delta = (5.6)^2 - 4(-4.9)(1.75)"
        ).scale(1.0).shift(UP * 1)
        self.play(Write(disc_eq), run_time=1.0)

        disc_val = MathTex(
            "\\Delta = 31.36 + 34.3 = 65.66"
        ).scale(1.0).move_to(disc_eq)
        self.play(TransformMatchingTex(disc_eq, disc_val), run_time=1.2)

        # Limpiar antes de siguiente paso
        self.play(FadeOut(disc_val), run_time=0.5)

        # --- Sustituir discriminante en la fórmula ---
        form_disc = MathTex(
            "t = \\frac{-5.6 \\pm \\sqrt{65.66}}{-9.8}"
        ).scale(1.0).shift(UP * 1)
        self.play(Write(form_disc), run_time=1.0)

        # Evaluar raíz
        form_sqrt = MathTex(
            "t = \\frac{-5.6 \\pm 8.10}{-9.8}"
        ).scale(1.0).move_to(form_disc)
        self.play(TransformMatchingTex(form_disc, form_sqrt), run_time=1.0)

        # Limpiar antes de resolver los dos casos
        self.play(FadeOut(form_sqrt), run_time=0.5)

        # --- Caso 1: signo +
        case_plus = MathTex(
            "t_1 = \\frac{-5.6 + 8.10}{-9.8}"
        ).scale(1.0).shift(UP * 1)
        self.play(Write(case_plus), run_time=1.0)

        case_plus_val = MathTex(
            "t_1 = \\frac{2.50}{-9.8} \\approx -0.26\\,\\text{s}"
        ).scale(1.0).move_to(case_plus)
        self.play(TransformMatchingTex(case_plus, case_plus_val), run_time=1.0)
        self.play(FadeOut(case_plus_val), run_time=0.5)

        # --- Caso 2: signo -
        case_minus = MathTex(
            "t_2 = \\frac{-5.6 - 8.10}{-9.8}"
        ).scale(1.0).shift(UP * 1)
        self.play(Write(case_minus), run_time=1.0)

        case_minus_val = MathTex(
            "t_2 = \\frac{-13.7}{-9.8} \\approx 1.40\\,\\text{s}"
        ).scale(1.0).move_to(case_minus)
        self.play(TransformMatchingTex(case_minus, case_minus_val), run_time=1.0)
        self.play(Circumscribe(case_minus_val, color=C_RESULT), run_time=0.8)

        # Destacar resultado final
        res_time = MathTex("t \\approx 1.40\\,\\text{s}", color=C_RESULT).scale(1.2).shift(DOWN * 1)
        self.play(Write(res_time), Flash(res_time, flash_radius=0.5), run_time=1.2)
        self.wait(0.8)


class S6_Alcance(Scene):
    """
    Calcula el alcance horizontal usando:
        x = x0 + V0x * t
    - Sustitución numérica con t ≈ 1.40 s.
    - Resultado final x ≈ 7.84 m resaltado.
    - Animación de la jabalina desplazándose en horizontal durante t segundos.
    """
    def construct(self):
        # --- Título ---
        title = Tex("Cálculo del alcance horizontal").to_edge(UP)
        self.play(Write(title), run_time=1.0)

        # --- Ecuación general ---
        eq_sym = MathTex("x = x_0 + V_{0x} t", color=C_X).shift(UP * 1)
        self.play(Write(eq_sym), run_time=0.8)

        # Sustituir x0=0, V0x=5.6
        eq_num1 = MathTex("x = 0 + 5.6\\,t", color=C_X).move_to(eq_sym)
        self.play(TransformMatchingTex(eq_sym, eq_num1), run_time=0.8)

        # Sustituir t ≈ 1.40
        eq_num2 = MathTex("x = 5.6 \\times 1.40", color=C_X).move_to(eq_num1)
        self.play(TransformMatchingTex(eq_num1, eq_num2), run_time=0.8)

        # Calcular resultado
        eq_res = MathTex("x \\approx 7.84\\,\\text{m}", color=C_RESULT).move_to(eq_num2)
        self.play(TransformMatchingTex(eq_num2, eq_res), run_time=0.8)
        self.play(Circumscribe(eq_res, color=C_RESULT), run_time=0.8)

        # Limpiar ecuaciones
        self.play(FadeOut(eq_res), run_time=0.5)

        # --- Visualización del movimiento horizontal ---
        axes = Axes(
            x_range=[0, 9, 1],
            y_range=[0, 1, 1],
            x_length=8,
            y_length=1.5,
            tips=False
        ).shift(DOWN * 1.5)
        self.play(Create(axes), run_time=1.0)

        # Punto inicial y final
        start = axes.c2p(0, 0)
        end = axes.c2p(7.84, 0)

        # Jabalina simplificada (flecha horizontal)
        javelin = Line(ORIGIN, 0.6 * RIGHT, stroke_width=6, color=C_JAVELIN)
        tip = Triangle(stroke_width=0, fill_opacity=1, fill_color=C_JAVELIN).scale(0.12).next_to(javelin, RIGHT, buff=0)
        javelin_grp = VGroup(javelin, tip).move_to(start)

        self.play(FadeIn(javelin_grp), run_time=0.5)

        # Animación de desplazamiento constante durante 1.4 s
        self.play(javelin_grp.animate.move_to(end), run_time=1.4, rate_func=linear)
        self.wait(0.3)

        # Resaltar alcance
        alcance_lbl = MathTex("7.84\\,\\text{m}", color=C_RESULT).next_to(end, UP, buff=0.2)
        self.play(Write(alcance_lbl), Flash(alcance_lbl, flash_radius=0.5), run_time=1.0)
        self.wait(0.5)


class S7_Resumen(Scene):
    """
    Recapitula todos los resultados obtenidos en las escenas anteriores.
    - Panel con V0x, V0y, t y alcance.
    - Repetición rápida de la animación de la jabalina.
    - El panel se mueve a la esquina superior derecha al iniciar la gráfica.
    """
    def construct(self):
        # --- Título ---
        title = Tex("Resumen del lanzamiento de jabalina").to_edge(UP)
        self.play(Write(title), run_time=1.0)

        # --- Panel de resultados ---
        res_vx = MathTex("V_{0x} = 5.6\\,\\text{m/s}", color=C_X).scale(1.0)
        res_vy = MathTex("V_{0y} = 5.6\\,\\text{m/s}", color=C_Y).scale(1.0)
        res_t  = MathTex("t \\approx 1.40\\,\\text{s}", color=C_RESULT).scale(1.0)
        res_x  = MathTex("x \\approx 7.84\\,\\text{m}", color=C_RESULT).scale(1.0)

        panel = VGroup(res_vx, res_vy, res_t, res_x).arrange(DOWN, aligned_edge=LEFT, buff=0.4)
        panel_box = SurroundingRectangle(panel, color=WHITE, buff=0.4, corner_radius=0.1)
        panel_group = VGroup(panel_box, panel)

        self.play(FadeIn(panel_box), LaggedStart(*[Write(item) for item in panel], lag_ratio=0.3), run_time=2.0)
        self.wait(0.5)

        # --- Ejes y trayectoria para la repetición ---
        axes = Axes(
            x_range=[0, 9, 1],
            y_range=[0, 4.5, 0.5],
            x_length=8,
            y_length=4,
            tips=False
        ).to_edge(DOWN)

        angle_rad = np.deg2rad(ANGLE_DEG)
        v0x = V0 * np.cos(angle_rad)
        v0y = V0 * np.sin(angle_rad)

        def x_t(t): return v0x * t
        def y_t(t): return Y0 + v0y * t - 0.5 * G * t**2

        T = (v0y + np.sqrt(v0y**2 + 2 * G * Y0)) / G

        traj = axes.plot_parametric_curve(
            lambda t: [x_t(t), y_t(t), 0],
            t_range=[0, T],
            color=YELLOW
        )

        # Jabalina simplificada
        javelin = Line(ORIGIN, 0.35 * RIGHT, stroke_width=6, color=C_JAVELIN)
        tip = Triangle(stroke_width=0, fill_opacity=1, fill_color=C_JAVELIN).scale(0.06).next_to(javelin, RIGHT, buff=0)
        javelin_grp = VGroup(javelin, tip).move_to(axes.c2p(0, Y0))

        def update_javelin(mob):
            t = t_tracker.get_value()
            mob.move_to(axes.c2p(x_t(t), y_t(t)))
            dt = 1e-3
            p1 = axes.c2p(x_t(t), y_t(t))
            p2 = axes.c2p(x_t(t + dt), y_t(t + dt))
            direction = p2 - p1
            mob.set_angle(np.arctan2(direction[1], direction[0]))
            return mob

        t_tracker = ValueTracker(0.0)
        javelin_grp.add_updater(update_javelin)

        # --- Mover el panel a la esquina superior derecha ---
        panel_target = panel_group.copy().scale(0.8).to_corner(UR).shift(DOWN * 0.5 + LEFT * 0.5)
        self.play(
            panel_group.animate.scale(0.8).to_corner(UR).shift(DOWN * 0.5 + LEFT * 0.5),
            Create(axes),
            run_time=1.5
        )

        # --- Trazo y jabalina ---
        self.play(Create(traj), FadeIn(javelin_grp), run_time=1.2)

        # Animación rápida del vuelo completo
        self.play(t_tracker.animate.set_value(T), run_time=3.0, rate_func=linear)
        javelin_grp.clear_updaters()

        # Resaltar alcance final
        alcance_lbl = MathTex("7.84\\,\\text{m}", color=C_RESULT).next_to(axes.c2p(7.84, 0), UP, buff=0.2)
        self.play(Write(alcance_lbl), Flash(alcance_lbl, flash_radius=0.5), run_time=1.0)
        self.wait(0.5)

        # --- Cierre ---
        final_text = Tex("¡Fin del análisis!").scale(1.2).to_edge(DOWN)
        self.play(Write(final_text), run_time=1.0)
        self.wait(1.0)
