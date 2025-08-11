# -*- coding: utf-8 -*-
"""
Manim scenes to animate the physics of a javelin throw, based on provided calculations.
This file contains all scenes for the project.
"""
from manim import *
import numpy as np

# =============================================================================
# --- CONFIGURACIÓN Y CONSTANTES REUTILIZABLES ---
# =============================================================================
# --- Colores ---
COLOR_VEC_V = YELLOW         # Vector de velocidad
COLOR_VEC_X = TEAL           # Componente X de la velocidad
COLOR_VEC_Y = ORANGE         # Componente Y de la velocidad
COLOR_POS = WHITE            # Posición y ejes
COLOR_TEXT = WHITE           # Color del texto por defecto
COLOR_ACCEL = RED            # Vector de aceleración

# --- Constantes Físicas ---
H_INICIAL = 1.75             # Altura inicial en metros
V_INICIAL_MAG = 7.93         # Magnitud de la velocidad inicial en m/s
ANGULO_GRADOS = 45           # Ángulo de lanzamiento en grados
ANGULO_RAD = np.deg2rad(ANGULO_GRADOS)
G = 9.81                     # Aceleración gravitacional

class S1_Planteamiento(MovingCameraScene):
    """
    ESCENA 1: Presenta el problema, el sistema de coordenadas y las condiciones iniciales.
    """
    def construct(self):
        # --- Título de la escena ---
        title = Tex("Planteamiento del Problema").to_edge(UP)

        # --- Ejes y sistema de coordenadas ---
        axes = Axes(
            x_range=[-1, 10, 1],
            y_range=[-2, 6, 1],
            x_length=9,
            y_length=7,
            axis_config={"color": BLUE, "include_tip": True},
            x_axis_config={"numbers_to_include": np.arange(0, 10, 2)},
            y_axis_config={"numbers_to_include": np.arange(0, 7, 2)},
        )
        # CORRECCIÓN: Usar raw strings (r"...") para las etiquetas con LaTeX
        x_label = axes.get_x_axis_label(r"x \text{ (m)}")
        y_label = axes.get_y_axis_label(r"y \text{ (m)}")
        
        # --- Elementos visuales del lanzamiento ---
        p_inicial = axes.c2p(0, H_INICIAL) # Punto de lanzamiento
        atleta = Line(axes.c2p(0, 0), p_inicial, color=GREEN, stroke_width=6)
        punto_lanzamiento = Dot(p_inicial, color=YELLOW)

        # --- Vector de velocidad y sus etiquetas ---
        v_vector = Vector(
            V_INICIAL_MAG * np.array([np.cos(ANGULO_RAD), np.sin(ANGULO_RAD), 0]),
            color=COLOR_VEC_V
        ).scale(0.5, about_point=ORIGIN).shift(p_inicial) # Se escala para mejor visualización
        
        # --- Etiquetas de las condiciones iniciales ---
        brace_h = Brace(atleta, direction=LEFT, buff=0.2)
        # CORRECCIÓN: Usar raw f-string (fr"...") para formatear
        label_h = brace_h.get_tex(fr"h_0 = {H_INICIAL:.2f} \text{ m}")

        linea_horizontal = DashedLine(p_inicial, p_inicial + RIGHT * 1.5)
        angulo_arco = Angle(linea_horizontal, v_vector, radius=0.8)
        label_angulo = MathTex(fr"\theta = {ANGULO_GRADOS:.0f}^\circ").next_to(angulo_arco, RIGHT, buff=0.2)
        
        # CORRECCIÓN: Usar raw f-string (fr"...") aquí también
        label_velocidad = MathTex(fr"|\vec{{v}}_0| = {V_INICIAL_MAG:.2f} \text{ m/s}", color=COLOR_VEC_V)
        label_velocidad.next_to(v_vector.get_end(), UP, buff=0.15).scale(0.8)

        # --- Animaciones ---
        self.play(Write(title))
        self.wait(0.5)
        
        self.camera.frame.save_state()
        self.play(self.camera.frame.animate.set(width=14).move_to(axes.c2p(3, 2)))
        
        self.play(Create(axes), Write(x_label), Write(y_label), run_time=2)
        self.play(Create(atleta), Create(punto_lanzamiento), run_time=1)
        
        self.play(
            LaggedStart(
                Create(brace_h),
                Write(label_h),
                lag_ratio=0.7
            )
        )
        self.wait(1)
        
        self.play(Create(v_vector))
        self.play(
            LaggedStart(
                Create(linea_horizontal),
                Create(angulo_arco),
                Write(label_angulo),
                Write(label_velocidad),
                lag_ratio=0.5
            )
        )
        
        self.play(FadeOut(linea_horizontal))
        self.wait(3)

# =============================================================================
# --- STUBS PARA ESCENAS FUTURAS ---
# =============================================================================

class S2_DescomposicionVectorial(MovingCameraScene):
    # TODO: Implementar la descomposición del vector velocidad
    pass

class S3_AnalisisVertical(Scene):
    # TODO: Implementar el análisis del movimiento vertical y el cálculo del tiempo
    pass
    
class S4_AnalisisHorizontal(Scene):
    # TODO: Implementar el análisis del movimiento horizontal y el cálculo del alcance
    pass

class S5_ResultadoFinal(MovingCameraScene):
    # TODO: Implementar la visualización de la trayectoria y el resumen final
    pass

# --- Comandos para renderizar cada escena por separado ---
# manim -pql main.py S1_Planteamiento
# manim -pql main.py S2_DescomposicionVectorial
# manim -pql main.py S3_AnalisisVertical
# manim -pql main.py S4_AnalisisHorizontal
# manim -pql main.py S5_ResultadoFinal