# manim -pql jabalina.py S2_DatosYConversion
# manim -pqh jabalina.py S2_DatosYConversion
# (cambia el nombre de la clase para renderizar otra escena)

from manim import *
import numpy as np

"""
Animación didáctica (Física 1): Lanzamiento de jabalina como movimiento parabólico.
Esta versión implementa S2_DatosYConversion (público universitario).
Datos de partida:
    θ = 33.01°,
    Vi = 105.70 km/h = 29.361 m/s,
    V0x = 24.621 m/s,
    V0y = 15.995 m/s,
    h0 ≈ 1.9 m,
    g = 9.8 m/s^2,
    t ≈ 3.38 s,
    alcance ≈ 83.22 m.
"""

# =========================
# Parámetros reutilizables
# =========================
THEME = {
    "bg": "#0f1117",
    "text": WHITE,
    "v0": BLUE_B,
    "v0x": GREEN_C,
    "v0y": GOLD_B,
    "highlight": GRAY_B,
    "ground": "#2b2f3a",
}

# Datos numéricos del problema
THETA_DEG = 33.01
VI_KMH = 105.70
VI_MS = 29.361
V0X = 24.621
V0Y = 15.995
H0 = 1.9
G = 9.8
T_FLIGHT = 3.38
RANGE_X = 83.22


def deg_to_rad(deg: float) -> float:
    return deg * np.pi / 180.0

def y_of_t(t):
    return H0 + V0Y * t - 0.5 * G * t * t


# =========================
# S1 (ya implementada previamente)
# =========================
class S1_Intro(Scene):
    def construct(self):
        self.camera.background_color = THEME["bg"]

        title = Tex(
            r"Lanzamiento de jabalina: movimiento parabólico",
            color=THEME["text"],
        ).scale(0.9)
        subtitle = Tex(
            r"Datos experimentales y modelado (Física 1)",
            color=THEME["highlight"],
        ).scale(0.6)
        header = VGroup(title, subtitle).arrange(DOWN, buff=0.2).to_edge(UP)
        self.play(Write(title), run_time=1.6, rate_func=smooth)
        self.play(FadeIn(subtitle, shift=UP * 0.2), run_time=0.8)

        plane = NumberPlane(
            x_range=[-2, 16, 2],
            y_range=[-1, 8, 1],
            x_length=10,
            y_length=5.5,
            background_line_style={"stroke_opacity": 0.2, "stroke_width": 1},
        ).to_edge(LEFT, buff=0.6).shift(DOWN * 0.2)
        ground = Line(
            plane.c2p(-2, 0), plane.c2p(16, 0), color=THEME["ground"], stroke_width=6
        )
        self.play(Create(plane), FadeIn(ground), run_time=1.4)

        launch_point = plane.c2p(0, H0 / 1.0)
        peg = Dot(launch_point, color=THEME["text"]).set_z_index(3)
        h_brace = BraceBetweenPoints(plane.c2p(0, 0), launch_point, direction=LEFT)
        h_label = MathTex(r"h_0 \approx 1.9\,\mathrm{m}", color=THEME["text"]).scale(
            0.6
        )
        h_label.next_to(h_brace, LEFT, buff=0.15)
        self.play(FadeIn(peg, scale=0.8), run_time=0.6)
        self.play(GrowFromCenter(h_brace), FadeIn(h_label, shift=LEFT * 0.2), run_time=0.8)

        theta = deg_to_rad(THETA_DEG)
        v0_len = 3.5
        v0_vec = Arrow(
            start=launch_point,
            end=launch_point + v0_len * np.array([np.cos(theta), np.sin(theta), 0]),
            buff=0,
            stroke_width=6,
            max_tip_length_to_length_ratio=0.12,
            color=THEME["v0"],
        ).set_z_index(3)

        angle_arc = Arc(
            radius=0.8,
            start_angle=0,
            angle=theta,
            arc_center=launch_point,
            color=THEME["text"],
            stroke_opacity=0.8,
        )
        theta_label = MathTex(r"\theta = 33.01^\circ", color=THEME["text"]).scale(0.6)
        theta_label.next_to(angle_arc.get_center() + 1.0 * UP + 0.9 * RIGHT, UR, buff=0)

        v0_label = MathTex(r"\vec v_0 = 29.361\ \mathrm{m/s}", color=THEME["v0"]).scale(0.6)
        v0_label.next_to(v0_vec.get_end(), UR, buff=0.15)

        self.play(Create(angle_arc), run_time=0.8)
        self.play(GrowArrow(v0_vec, rate_func=smooth), run_time=1.2)
        self.play(Write(theta_label), FadeIn(v0_label, shift=UP * 0.1), run_time=0.8)

        card = RoundedRectangle(corner_radius=0.2, height=3.9, width=5.8, stroke_opacity=0.4)
        card.set_fill(color="#1a1f2b", opacity=0.7)
        card.to_edge(RIGHT, buff=0.6).shift(DOWN * 0.2)

        items = VGroup(
            MathTex(r"\theta = 33.01^\circ", color=THEME["text"]),
            MathTex(r"V_i = 105.70\ \frac{\mathrm{km}}{\mathrm{h}}", color=THEME["text"]),
            MathTex(r"V_i = \frac{105.70}{3.6} = 29.361\ \mathrm{m/s}", color=THEME["text"]).scale(0.9),
            MathTex(r"V_{0x} = 29.361\cos\theta = 24.621\ \mathrm{m/s}", color=THEME["v0x"]).scale(0.9),
            MathTex(r"V_{0y} = 29.361\sin\theta = 15.995\ \mathrm{m/s}", color=THEME["v0y"]).scale(0.9),
            MathTex(r"h_0 \approx 1.9\ \mathrm{m}", color=THEME["text"]),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).set_z_index(4)
        items.move_to(card.get_center()).shift(0.1 * UP)

        self.play(FadeIn(card, shift=RIGHT * 0.2), run_time=0.6)
        self.play(LaggedStart(*[Write(m) for m in items], lag_ratio=0.18, run_time=2.4, rate_func=smooth))

        note = Tex(
            r"\textbf{Idea clave: } El movimiento es parabólico con $a_y=-g$ y $a_x=0$",
            color=THEME["text"],
        ).scale(0.6)
        note.next_to(card, DOWN, buff=0.35).align_to(card, LEFT)
        self.play(FadeIn(note, shift=DOWN * 0.1), run_time=0.7)

        box = SurroundingRectangle(VGroup(v0_label, theta_label), color=THEME["highlight"], buff=0.15)
        self.play(Create(box), run_time=0.6)
        self.wait(0.6)
        self.play(FadeOut(box), run_time=0.4)
        self.wait(1.0)


# =========================
# S2 (implementada en esta entrega)
# =========================
class S2_DatosYConversion(Scene):
    """
    Paso 1: Recordatorio mínimo de datos (θ, h0, g) -> se elimina.
    Paso 2: Conversión Vi en km/h con factor (1000 m / 3600 s) -> se elimina.
    Paso 3: Vi = (105.70/3.6) m/s -> se elimina.
    Paso 4: Resultado final Vi = 29.361 m/s (se mantiene, sin otros elementos).
    """
    def construct(self):
        self.camera.background_color = THEME["bg"]

        # -------- Título persistente (no se elimina) --------
        title = Tex("Conversión de unidades", color=THEME["text"]).scale(0.9)
        title.to_edge(UP)
        self.play(Write(title), run_time=0.9)

        # Utilidad para limpiar un grupo de objetos
        def clear_group(group, rt=0.6):
            self.play(*[FadeOut(m, shift=0.1*DOWN) for m in group], run_time=rt)

        # =======================================
        # Paso 1: Recordatorio mínimo (se elimina)
        # =======================================
        step1 = VGroup(
            MathTex(r"\theta = 33.01^\circ", color=THEME["text"]),
            MathTex(r"h_0 \approx 1.9\ \mathrm{m}", color=THEME["text"]),
            MathTex(r"g = 9.8\ \mathrm{m/s^2}", color=THEME["text"]),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).scale(0.95)
        step1.next_to(title, DOWN, buff=0.6).to_edge(LEFT, buff=1.2)

        self.play(LaggedStart(*[Write(b) for b in step1], lag_ratio=0.2, run_time=1.4))
        self.wait(0.3)
        clear_group(step1)

        # =======================================
        # Paso 2: Vi en km/h con factor (se elimina)
        # =======================================
        expr_kmh = MathTex(
            r"V_i = 105.70\ \frac{\mathrm{km}}{\mathrm{h}}",
            color=THEME["v0"]
        ).scale(1.1).next_to(title, DOWN, buff=0.8)
        expr_kmh.to_edge(LEFT, buff=1.2)

        factor = MathTex(
            r"\times\ \frac{1000\ \mathrm{m}}{3600\ \mathrm{s}}",
            color=THEME["text"]
        ).scale(1.0).next_to(expr_kmh, RIGHT, buff=0.35)

        hint = Tex(
            r"\small Equivale a dividir por $3.6$",
            color=THEME["highlight"]
        ).scale(0.8).next_to(factor, DOWN, buff=0.2).align_to(factor, LEFT)

        self.play(Write(expr_kmh), run_time=0.8)
        self.play(FadeIn(factor, shift=DOWN*0.1), run_time=0.6)
        self.play(FadeIn(hint), run_time=0.4)
        self.wait(0.2)

        # Limpia TODO el paso 2
        clear_group(VGroup(hint, factor, expr_kmh))

        # =======================================
        # Paso 3: Reescritura como división (se elimina)
        # =======================================
        expr_div = MathTex(
            r"V_i = \frac{105.70}{3.6}\ \frac{\mathrm{m}}{\mathrm{s}}",
            color=THEME["v0"]
        ).scale(1.25).next_to(title, DOWN, buff=1.0)
        self.play(Write(expr_div), run_time=0.9)

        note_sig = Tex(
            r"\small Cifras significativas coherentes con el dato inicial",
            color=THEME["text"]
        ).scale(0.7).next_to(expr_div, DOWN, buff=0.25)
        self.play(FadeIn(note_sig), run_time=0.4)
        self.wait(0.2)

        # Limpia TODO el paso 3
        clear_group(VGroup(note_sig, expr_div))

        # =======================================
        # Paso 4: Resultado final (se mantiene)
        # =======================================
        expr_res = MathTex(
            r"V_i = 29.361\ \mathrm{m/s}",
            color=THEME["v0"]
        ).scale(1.4).next_to(title, DOWN, buff=1.0).shift(0.2*UP)

        box = SurroundingRectangle(expr_res, color=THEME["v0"], buff=0.18)
        sub = Tex(
            r"\small $\dfrac{1000}{3600}=\dfrac{1}{3.6}$; conversión exacta de km/h a m/s.",
            color=THEME["text"]
        ).scale(0.7).next_to(expr_res, DOWN, buff=0.3)

        self.play(Write(expr_res), Create(box), run_time=0.9)
        self.play(FadeIn(sub), run_time=0.5)
        self.wait(1.0)

        # (Fin de la escena: sólo queda el resultado final, sin elementos superpuestos)
        self.wait(0.6)


# =========================
# Stubs de escenas siguientes
# =========================
class S3_ComponentesVelocidad(Scene):
    """
    Objetivo: Descomponer el vector velocidad inicial en sus componentes
    horizontal y vertical, y presentar las expresiones simbólicas junto con
    los valores numéricos: V0x=24.621 m/s, V0y=15.995 m/s.
    """
    def construct(self):
        self.camera.background_color = THEME["bg"]

        # -------- Título --------
        title = Tex("Descomposición de $\\vec v_0$ en componentes", color=THEME["text"]).scale(0.9)
        title.to_edge(UP)
        self.play(Write(title), run_time=1.0)

        # -------- Ejes --------
        axes = Axes(
            x_range=[0, 10, 1],
            y_range=[0, 6, 1],
            x_length=10,
            y_length=5.8,
            axis_config={"include_tip": True, "include_numbers": False, "stroke_opacity": 0.8},
        ).to_edge(LEFT, buff=0.6).shift(DOWN * 0.2)

        x_lab = MathTex("x\\ (\\mathrm{m})", color=THEME["text"]).scale(0.6).next_to(axes.x_axis, RIGHT, buff=0.1)
        y_lab = MathTex("y\\ (\\mathrm{m})", color=THEME["text"]).scale(0.6).next_to(axes.y_axis, UP, buff=0.1)

        self.play(Create(axes), FadeIn(x_lab), FadeIn(y_lab), run_time=1.2)

        # -------- Vector v0 y ángulo θ --------
        theta = deg_to_rad(THETA_DEG)
        # longitud visual proporcional al módulo (escala arbitraria para encajar)
        scale = 0.18
        v0_vec = Arrow(
            axes.c2p(0, 0),
            axes.c2p(VI_MS * np.cos(theta) * scale, VI_MS * np.sin(theta) * scale),
            buff=0,
            color=THEME["v0"],
            stroke_width=6,
            max_tip_length_to_length_ratio=0.12,
        )
        angle_arc = Angle(axes.x_axis, v0_vec, radius=0.8, other_angle=False, color=THEME["text"])
        theta_tex = MathTex("\\theta=33.01^{\\circ}", color=THEME["text"]).scale(0.7).next_to(angle_arc, UR, buff=0.05)

        self.play(GrowArrow(v0_vec), Create(angle_arc), FadeIn(theta_tex), run_time=1.4)

        v0_label = MathTex("\\vec v_0=29.361\\ \\mathrm{m/s}", color=THEME["v0"]).scale(0.7)
        v0_label.next_to(v0_vec.get_end(), UR, buff=0.15)
        self.play(Write(v0_label), run_time=0.6)

        # -------- Proyecciones: V0x y V0y --------
        # Pies de proyección
        end = v0_vec.get_end()
        proj_x = axes.c2p(axes.p2c(end)[0], 0)
        proj_y = axes.c2p(0, axes.p2c(end)[1])

        dash_x = DashedLine(end, proj_x, color=THEME["highlight"], dash_length=0.12)
        dash_y = DashedLine(end, proj_y, color=THEME["highlight"], dash_length=0.12)

        # Componentes como flechas sobre ejes
        comp_x = Arrow(axes.c2p(0, 0), proj_x, buff=0, color=THEME["v0x"], stroke_width=6)
        comp_y = Arrow(axes.c2p(0, 0), proj_y, buff=0, color=THEME["v0y"], stroke_width=6)

        self.play(Create(dash_x), Create(dash_y), run_time=0.6)
        self.play(GrowArrow(comp_x), GrowArrow(comp_y), run_time=1.0)

        # Etiquetas de componentes
        label_vx = MathTex("V_{0x}", color=THEME["v0x"]).scale(0.7).next_to(comp_x, DOWN, buff=0.15)
        label_vy = MathTex("V_{0y}", color=THEME["v0y"]).scale(0.7).next_to(comp_y, LEFT, buff=0.15)
        self.play(FadeIn(label_vx), FadeIn(label_vy), run_time=0.5)

        # -------- Panel con fórmulas y valores --------
        card = RoundedRectangle(width=5.8, height=4.5, corner_radius=0.2, stroke_opacity=0.4)
        card.set_fill(color="#1a1f2b", opacity=0.7)
        card.to_edge(RIGHT, buff=0.6).shift(DOWN * 0.2)

        # Expresiones simbólicas
        vx_sym = MathTex("V_{0x}=V_0\\cos\\theta", color=THEME["v0x"])
        vy_sym = MathTex("V_{0y}=V_0\\sin\\theta", color=THEME["v0y"])

        # Sustitución con números
        vx_num = MathTex(
            "V_{0x}=29.361\\cos(33.01^{\\circ})=24.621\\ \\mathrm{m/s}",
            color=THEME["v0x"],
        ).scale(0.95)
        vy_num = MathTex(
            "V_{0y}=29.361\\sin(33.01^{\\circ})=15.995\\ \\mathrm{m/s}",
            color=THEME["v0y"],
        ).scale(0.95)

        group_sym = VGroup(vx_sym, vy_sym).arrange(DOWN, aligned_edge=LEFT, buff=0.4)
        group_sym.move_to(card.get_center() + 0.9*UP)
        group_num = VGroup(vx_num, vy_num).arrange(DOWN, aligned_edge=LEFT, buff=0.35)
        group_num.next_to(group_sym, DOWN, buff=0.5).align_to(group_sym, LEFT)

        self.play(FadeIn(card, shift=RIGHT * 0.2), run_time=0.6)
        self.play(LaggedStart(Write(vx_sym), Write(vy_sym), lag_ratio=0.2, run_time=1.2))

        # Transformaciones que muestran sustitución y cálculo
        self.play(TransformMatchingTex(vx_sym.copy(), vx_num, path_arc=20 * DEGREES), run_time=1.2)
        self.play(TransformMatchingTex(vy_sym.copy(), vy_num, path_arc=-20 * DEGREES), run_time=1.2)

        # Resaltado de resultados
        box_vx = SurroundingRectangle(vx_num, color=THEME["v0x"], buff=0.12)
        box_vy = SurroundingRectangle(vy_num, color=THEME["v0y"], buff=0.12)
        self.play(Create(box_vx), Create(box_vy), run_time=0.6)

        # -------- Vincular flechas con fórmulas (pedagógico) --------
        brace_x = Brace(comp_x, direction=DOWN, color=THEME["v0x"])
        val_x = MathTex("24.621\\ \\mathrm{m/s}", color=THEME["v0x"]).scale(0.7).next_to(brace_x, DOWN, buff=0.1)
        brace_y = Brace(comp_y, direction=LEFT, color=THEME["v0y"])
        val_y = MathTex("15.995\\ \\mathrm{m/s}", color=THEME["v0y"]).scale(0.7).next_to(brace_y, LEFT, buff=0.1)

        self.play(GrowFromCenter(brace_x), FadeIn(val_x, shift=DOWN*0.1), run_time=0.7)
        self.play(GrowFromCenter(brace_y), FadeIn(val_y, shift=LEFT*0.1), run_time=0.7)

        # Nota: ax=0, ay=-g
        note = Tex(
            "\\small En un tiro ideal: $a_x=0$ (componente constante), $a_y=-g$.",
            color=THEME["text"],
        ).scale(0.8).to_edge(DOWN)
        self.play(FadeIn(note), run_time=0.6)

        self.wait(1.0)

class S4_Final(MovingCameraScene):
    """
    1) Derivación breve del tiempo de vuelo (limpio)
    2) Animación de la trayectoria con marcador y alcance
    3) Recap final de resultados
    """
    def construct(self):
        self.camera.background_color = THEME["bg"]

        # -------- Título persistente --------
        title = Tex(
            "Tiempo de vuelo, trayectoria y alcance — resumen",
            color=THEME["text"]
        ).scale(0.9).to_edge(UP)
        self.play(Write(title), run_time=0.9)

        # Utilidad para limpiar un grupo
        def clear_group(group, rt=0.6):
            self.play(*[FadeOut(m, shift=0.1*DOWN) for m in group], run_time=rt)

        # =======================================
        # (1) TIEMPO DE VUELO — derivación breve
        # =======================================
        step_eq = VGroup(
            MathTex(r"y(t)=h_0+V_{0y}t-\tfrac{1}{2}gt^2", color=THEME["text"]),
            MathTex(r"0=h_0+V_{0y}t-\tfrac{1}{2}gt^2", r"\ \ \ (y=0)", color=THEME["text"]),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).next_to(title, DOWN, buff=0.7).to_edge(LEFT, buff=0.9)

        subs = MathTex(
            r"0=1.9+15.995\,t-4.9\,t^2", color=THEME["text"]
        ).next_to(step_eq, DOWN, buff=0.35).align_to(step_eq, LEFT)

        sol = MathTex(
            r"t \approx 3.38\ \mathrm{s}", color=THEME["v0"]
        ).scale(1.1).next_to(subs, DOWN, buff=0.35).align_to(subs, LEFT)

        box_sol = SurroundingRectangle(sol, color=THEME["v0"], buff=0.12)

        self.play(Write(step_eq[0]), run_time=0.8)
        self.play(TransformMatchingTex(step_eq[0].copy(), step_eq[1]), run_time=0.8)
        self.play(Write(subs), run_time=0.8)
        self.play(Write(sol), Create(box_sol), run_time=0.9)
        self.wait(0.4)
        clear_group(VGroup(step_eq, subs, box_sol))  # dejamos solo el título y (temporalmente) el valor
        # dejamos el valor del tiempo unos frames más para enlazar con la animación
        self.wait(0.2)
        self.play(FadeOut(sol, shift=0.1*DOWN), run_time=0.4)

        # =======================================
        # (2) TRAYECTORIA Y ALCANCE — animación
        # =======================================
        # Ejes para cubrir ~90 m en x y ~16 m en y
        axes = Axes(
            x_range=[0, 90, 10],
            y_range=[0, 16, 2],
            x_length=10.5,
            y_length=5.8,
            axis_config={"include_tip": True, "stroke_opacity": 0.9},
            tips=False,
        ).to_edge(LEFT, buff=0.6).shift(DOWN*0.2)
        x_label = MathTex("x\\ (\\mathrm{m})", color=THEME["text"]).scale(0.6).next_to(axes.x_axis, RIGHT, buff=0.1)
        y_label = MathTex("y\\ (\\mathrm{m})", color=THEME["text"]).scale(0.6).next_to(axes.y_axis, UP, buff=0.1)
        ground = Line(axes.c2p(0,0), axes.c2p(90,0), color=THEME["ground"], stroke_width=6)

        self.play(Create(axes), FadeIn(x_label), FadeIn(y_label), FadeIn(ground), run_time=1.1)

        # Curva y(x) = h0 + tanθ x - (g/(2 V0x^2)) x^2
        tan_theta = V0Y / V0X
        k = G / (2 * V0X * V0X)

        traj = axes.plot(
            lambda x: H0 + tan_theta * x - k * x * x,
            x_range=[0, RANGE_X],
            color=THEME["v0"],
            stroke_width=4,
        )
        self.play(Create(traj), run_time=1.2, rate_func=smooth)

        # Marcador de la jabalina moviéndose con el tiempo físico
        t_tracker = ValueTracker(0.0)
        dot = Dot(color=THEME["v0"]).scale(0.9)

        def dot_updater(mobj):
            t = t_tracker.get_value()
            x = V0X * t
            y = y_of_t(t)
            mobj.move_to(axes.c2p(x, max(0, y)))  # clamp en suelo

        dot.add_updater(dot_updater)
        self.add(dot)

        # Paneo ligero de cámara a lo largo de la trayectoria
        self.play(self.camera.frame.animate.set_width(axes.width*1.05).move_to(axes), run_time=0.6)
        self.play(t_tracker.animate.set_value(T_FLIGHT), run_time=2.4, rate_func=linear)
        dot.remove_updater(dot_updater)

        # Punto de caída y alcance
        landing = axes.c2p(RANGE_X, 0)
        fall_mark = Dot(landing, color=THEME["v0"]).scale(1.0)
        reach_line = DashedLine(axes.c2p(0,0), landing, color=THEME["highlight"], dash_length=0.2)
        reach_brace = Brace(reach_line, direction=DOWN, color=THEME["text"])
        reach_label = MathTex(
            r"x = V_{0x}\,t \approx 24.621\times 3.38 \approx 83.22\ \mathrm{m}",
            color=THEME["text"]
        ).scale(0.7).next_to(reach_brace, DOWN, buff=0.15)

        self.play(FadeIn(fall_mark, scale=1.2), Create(reach_line), run_time=0.8)
        self.play(GrowFromCenter(reach_brace), Write(reach_label), run_time=0.9)
        self.wait(0.6)

        # Limpieza para el recap
        clear_group(VGroup(dot, fall_mark, reach_line, reach_brace, reach_label, traj, x_label, y_label))
        self.play(FadeOut(axes), FadeOut(ground), run_time=0.6)

        # =======================================
        # (3) CIERRE — recapitulación de resultados
        # =======================================
        card = RoundedRectangle(width=10.8, height=4.8, corner_radius=0.25, stroke_opacity=0.4)
        card.set_fill(color="#1a1f2b", opacity=0.75)
        card.next_to(title, DOWN, buff=0.6)

        items = VGroup(
            MathTex(r"\vec v_0 = 29.361\ \mathrm{m/s}", color=THEME["v0"]).scale(0.95),
            MathTex(r"V_{0x} = 24.621\ \mathrm{m/s}", color=THEME["v0x"]).scale(0.95),
            MathTex(r"V_{0y} = 15.995\ \mathrm{m/s}", color=THEME["v0y"]).scale(0.95),
            MathTex(r"t_{\text{vuelo}} \approx 3.38\ \mathrm{s}", color=THEME["text"]).scale(0.95),
            MathTex(r"alcance\ x \approx 83.22\ \mathrm{m}", color=THEME["text"]).scale(0.95),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.34).move_to(card.get_center())

        # Grupos de color para pequeñas iluminaciones
        box_v0x = SurroundingRectangle(items[1], color=THEME["v0x"], buff=0.12)
        box_v0y = SurroundingRectangle(items[2], color=THEME["v0y"], buff=0.12)

        self.play(FadeIn(card, shift=UP*0.1), run_time=0.5)
        self.play(LaggedStart(*[Write(m) for m in items], lag_ratio=0.15, run_time=1.6))
        self.play(Create(box_v0x), Create(box_v0y), run_time=0.6)
        self.wait(1.0)

        # Fin
        self.play(FadeOut(box_v0x), FadeOut(box_v0y), run_time=0.3)
        self.wait(0.6)
