"""
Sistema Experto – Servicio Social
Interfaz gráfica moderna con Tkinter
"""
import tkinter as tk
from tkinter import ttk
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from serviciosocialexperta import (
    SistemaServicioSocial, Goal, GoalKind, Alumno, Conclusion, Missing,
)

# ── Paleta de colores (tema oscuro) ───────────────────────────────────────────
BG     = "#0d1117"
CARD   = "#161b22"
BORDER = "#30363d"
ACCENT = "#1f6feb"
GREEN  = "#3fb950"
RED    = "#f85149"
YELLOW = "#e3b341"
FG     = "#c9d1d9"
FG_DIM = "#8b949e"
WHITE  = "#f0f6fc"
SIDE   = "#090d12"

_PLACEHOLDER = "Ej. Juan Pérez García"


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sistema Experto — Servicio Social")
        self.configure(bg=BG)
        self.resizable(True, True)
        self.minsize(720, 520)
        self.state("zoomed")   # inicia maximizado en Windows

        # Estilo del scrollbar para tema oscuro
        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure(
            "Dark.Vertical.TScrollbar",
            background=BORDER, troughcolor=BG,
            arrowcolor=FG_DIM, bordercolor=BG,
            lightcolor=BORDER, darkcolor=BORDER,
        )

        self._nombre_entry = None   # referencia guardada para reset
        self._result_outer = None
        self._dyn_labels   = []      # (label, padding_horizontal) → wraplength dinámico
        self._build()

    # ──────────────────────────────────────────────────────────────────────────
    #  Construcción de la interfaz
    # ──────────────────────────────────────────────────────────────────────────

    def _build(self):
        # ── Sidebar ─────────────────────────────────────────────────────────
        sb = tk.Frame(self, bg=SIDE, width=240)
        sb.pack(side="left", fill="y")
        sb.pack_propagate(False)

        tk.Label(sb, text="🎓", font=("Segoe UI Emoji", 36),
                 bg=SIDE, fg=WHITE).pack(pady=(36, 6))
        tk.Label(sb, text="Servicio Social",
                 font=("Segoe UI Semibold", 13), bg=SIDE, fg=WHITE).pack()
        tk.Label(sb, text="Sistema Experto",
                 font=("Segoe UI", 9), bg=SIDE, fg=FG_DIM).pack(pady=(2, 24))

        tk.Frame(sb, bg=BORDER, height=1).pack(fill="x", padx=20, pady=(0, 16))

        tk.Label(sb, text="INTEGRANTES", font=("Segoe UI", 7, "bold"),
                 bg=SIDE, fg=FG_DIM).pack()

        for m in [
            "Barrón Álvarez M.F.",
            "Benitez Marín L.M.",
            "Guzmán Solís G.",
            "Martínez López H.",
            "Merino Garfias L.",
            "Villalobos Araiza J.L.",
        ]:
            tk.Label(sb, text=f"• {m}", font=("Segoe UI", 8),
                     bg=SIDE, fg=FG_DIM).pack(anchor="w", padx=20, pady=1)

        tk.Label(sb, text="Sistemas Expertos Probabilísticos",
                 font=("Segoe UI", 7), bg=SIDE, fg="#444c56",
                 wraplength=200, justify="center").pack(side="bottom", pady=12)

        # ── Panel principal ──────────────────────────────────────────────────
        main = tk.Frame(self, bg=BG)
        main.pack(side="left", fill="both", expand=True)

        # Barra de encabezado
        hdr = tk.Frame(main, bg=CARD, height=56)
        hdr.pack(fill="x")
        hdr.pack_propagate(False)
        tk.Label(
            hdr,
            text="Evaluación de Elegibilidad para Servicio Social",
            font=("Segoe UI Semibold", 13), bg=CARD, fg=WHITE,
        ).pack(side="left", padx=20, pady=14)

        self._build_scroll(main)

    def _build_scroll(self, parent):
        body = tk.Frame(parent, bg=BG)
        body.pack(fill="both", expand=True)

        canvas = tk.Canvas(body, bg=BG, highlightthickness=0)
        sb = ttk.Scrollbar(body, orient="vertical", command=canvas.yview,
                           style="Dark.Vertical.TScrollbar")
        canvas.configure(yscrollcommand=sb.set)
        sb.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        sf = tk.Frame(canvas, bg=BG)
        win_id = canvas.create_window((0, 0), window=sf, anchor="nw")

        canvas.bind("<Configure>",
                    lambda e: canvas.itemconfig(win_id, width=e.width))
        sf.bind("<Configure>", lambda e: self._on_sf_resize(e, canvas))
        canvas.bind_all("<MouseWheel>",
                        lambda e: canvas.yview_scroll(-1 * (e.delta // 120), "units"))

        self._build_form(sf)

    def _on_sf_resize(self, e, canvas):
        """Actualiza scrollregion y wraplength de todos los labels dinámicos."""
        canvas.configure(scrollregion=canvas.bbox("all"))
        w = e.width
        for lbl, hpad in self._dyn_labels:
            try:
                lbl.config(wraplength=max(200, w - hpad))
            except tk.TclError:
                pass  # widget destruido

    def _build_form(self, parent):
        # ── Nombre ──────────────────────────────────────────────────────────
        self._section(parent, "Datos del Alumno")
        self._label(parent, "Nombre completo del alumno")
        self._nombre_entry = self._entry(parent)

        # ── Créditos ────────────────────────────────────────────────────────
        self._section(parent, "Avance Académico")
        self._label(parent, "Ingresa tus créditos escolares para calcular el porcentaje (Art. 146)")

        # Contenedor con dos columnas
        cred_container = tk.Frame(parent, bg=BG)
        cred_container.pack(fill="x", padx=22, pady=(8, 0))

        # Columna izquierda: inputs
        left_col = tk.Frame(cred_container, bg=BG)
        left_col.pack(side="left", fill="both", expand=False, padx=(0, 16))

        tk.Label(left_col, text="Total de créditos de tu carrera:",
                 font=("Segoe UI", 9), bg=BG, fg=FG).pack(anchor="w", pady=(0, 4))
        self.creditos_total_entry = tk.Entry(
            left_col, font=("Segoe UI", 11), bg=CARD, fg=WHITE,
            insertbackground=WHITE, relief="flat",
            highlightthickness=1, highlightbackground=BORDER,
            highlightcolor=ACCENT, width=15
        )
        self.creditos_total_entry.pack(fill="x", ipady=8, pady=(0, 12))
        self.creditos_total_entry.insert(0, "400")
        self.creditos_total_entry.bind("<KeyRelease>", lambda e: self._calc_percentage())

        tk.Label(left_col, text="Créditos que ya completaste:",
                 font=("Segoe UI", 9), bg=BG, fg=FG).pack(anchor="w", pady=(0, 4))
        self.creditos_obtenidos_entry = tk.Entry(
            left_col, font=("Segoe UI", 11), bg=CARD, fg=WHITE,
            insertbackground=WHITE, relief="flat",
            highlightthickness=1, highlightbackground=BORDER,
            highlightcolor=ACCENT, width=15
        )
        self.creditos_obtenidos_entry.pack(fill="x", ipady=8)
        self.creditos_obtenidos_entry.insert(0, "200")
        self.creditos_obtenidos_entry.bind("<KeyRelease>", lambda e: self._calc_percentage())

        # Columna derecha: resultado
        right_col = tk.Frame(cred_container, bg=BG)
        right_col.pack(side="left", fill="both", expand=True)

        tk.Label(right_col, text="Porcentaje calculado:",
                 font=("Segoe UI", 9), bg=BG, fg=FG_DIM).pack(anchor="w", pady=(0, 8))

        result_row = tk.Frame(right_col, bg=CARD,
                             highlightthickness=1, highlightbackground=BORDER)
        result_row.pack(fill="x", ipady=12, padx=2)

        self._pct_lbl = tk.Label(
            result_row, text="50%", font=("Segoe UI Semibold", 26),
            bg=CARD, fg=YELLOW
        )
        self._pct_lbl.pack(side="left", padx=12)

        self._cred_status = tk.Label(result_row, font=("Segoe UI", 9),
                                     bg=CARD, fg=FG_DIM)
        self._cred_status.pack(side="left", padx=(0, 12))

        self.creditos_var = tk.IntVar(value=50)
        self._calc_percentage()

        # ── Inducción ───────────────────────────────────────────────────────
        self._section(parent, "Curso de Inducción")
        self._label(parent, "¿Ha completado el curso de inducción a Servicio Social? (Art. 148-I)")
        self.induccion_var = tk.StringVar(value="si")
        self._toggle(parent, self.induccion_var)

        # ── Semestre ────────────────────────────────────────────────────────
        self._section(parent, "Situación Académica")
        self._label(parent, "¿En qué semestre te encuentras?")
        semestre_frame = tk.Frame(parent, bg=BG)
        semestre_frame.pack(fill="x", padx=22, pady=(0, 4))
        self.semestre_var = tk.IntVar(value=6)
        for s in range(5, 11):
            tk.Radiobutton(
                semestre_frame, text=f"{s}to", variable=self.semestre_var, value=s,
                font=("Segoe UI", 10), bg=CARD, fg=ACCENT,
                activebackground=CARD, relief="flat", padx=10, pady=8,
                cursor="hand2", indicatoron=False, width=4,
                highlightthickness=1, highlightbackground=BORDER,
            ).pack(side="left", padx=4)

        # ── Lugar ────────────────────────────────────────────────────────
        self._section(parent, "Institución de Servicio (Art. 126)")
        self._label(parent, "¿Realizará su servicio en una institución pública o asociación civil?")
        self.lugar_var = tk.StringVar(value="si")
        self._toggle(parent, self.lugar_var)

        # ── Tipo Institución ───────────────────────────────────────────
        self._label(parent, "¿Es pública o sin fines de lucro? (No puede ser privada)")
        self.institucion_publica_var = tk.StringVar(value="si")
        self._toggle(parent, self.institucion_publica_var)

        # ── Actividad Válida ───────────────────────────────────────────
        self._section(parent, "Tipo de Actividad")
        self._label(parent, "¿Es una actividad válida? (No: reciclaje, boteo, donativos)")
        self.actividad_valida_var = tk.StringVar(value="si")
        self._toggle(parent, self.actividad_valida_var)

        # ── Botones ─────────────────────────────────────────────────────────
        btns = tk.Frame(parent, bg=BG)
        btns.pack(fill="x", padx=22, pady=(22, 8))

        tk.Button(
            btns, text="Limpiar formulario",
            font=("Segoe UI", 10), bg=CARD, fg=FG_DIM,
            relief="flat", padx=14, pady=10, cursor="hand2",
            activebackground=BORDER, activeforeground=FG,
            command=self._reset,
        ).pack(side="right", padx=(0, 10))

        tk.Button(
            btns, text="  Evaluar elegibilidad  →",
            font=("Segoe UI Semibold", 11), bg=ACCENT, fg=WHITE,
            relief="flat", padx=18, pady=10, cursor="hand2",
            activebackground="#388bfd", activeforeground=WHITE,
            command=self._evaluate,
        ).pack(side="right")

        # ── Área de resultados ───────────────────────────────────────────────
        self._result_outer = tk.Frame(parent, bg=BG)
        # Se muestra sólo después de evaluar

    # ──────────────────────────────────────────────────────────────────────────
    #  Helpers de widgets
    # ──────────────────────────────────────────────────────────────────────────

    def _section(self, p, text):
        f = tk.Frame(p, bg=BG)
        f.pack(fill="x", padx=22, pady=(18, 4))
        tk.Label(f, text=text.upper(), font=("Segoe UI", 8, "bold"),
                 bg=BG, fg=FG_DIM).pack(side="left")
        tk.Frame(f, bg=BORDER, height=1).pack(
            side="left", fill="x", expand=True, padx=(10, 0), pady=2)

    def _label(self, p, text):
        lbl = tk.Label(p, text=text, font=("Segoe UI", 10),
                       bg=BG, fg=FG, wraplength=560, justify="left")
        lbl.pack(anchor="w", padx=22, pady=(0, 4))
        self._dyn_labels.append((lbl, 44))   # 22px padding × 2

    def _entry(self, p):
        e = tk.Entry(
            p, font=("Segoe UI", 11), bg=CARD, fg=FG_DIM,
            insertbackground=WHITE, relief="flat",
            highlightthickness=1, highlightbackground=BORDER,
            highlightcolor=ACCENT,
        )
        e.pack(fill="x", padx=22, ipady=9)
        e.insert(0, _PLACEHOLDER)

        def _fi(_):
            if e.get() == _PLACEHOLDER:
                e.delete(0, tk.END)
                e.config(fg=WHITE)

        def _fo(_):
            if not e.get().strip():
                e.insert(0, _PLACEHOLDER)
                e.config(fg=FG_DIM)

        e.bind("<FocusIn>",  _fi)
        e.bind("<FocusOut>", _fo)
        return e

    def _toggle(self, p, var):
        f = tk.Frame(p, bg=BG)
        f.pack(anchor="w", padx=22, pady=(0, 4))
        for label, val, col in [("  ✓  Sí  ", "si", GREEN),
                                 ("  ✗  No  ", "no", RED)]:
            tk.Radiobutton(
                f, text=label, variable=var, value=val,
                font=("Segoe UI", 10, "bold"),
                bg=CARD, fg=col, selectcolor="#1c2733",
                activebackground=CARD, activeforeground=col,
                relief="flat", padx=12, pady=8, cursor="hand2",
                indicatoron=False, width=8,
                highlightthickness=1, highlightbackground=BORDER,
                highlightcolor=col,
            ).pack(side="left", padx=(0, 8))

    def _calc_percentage(self):
        """Calcula el porcentaje a partir de los campos de entrada."""
        try:
            total = float(self.creditos_total_entry.get().strip())
            obtenidos = float(self.creditos_obtenidos_entry.get().strip())
            if total <= 0:
                raise ValueError()
            pct = int((obtenidos / total) * 100)
            pct = max(0, min(100, pct))  # limita a [0, 100]
        except (ValueError, ZeroDivisionError):
            pct = 0

        self.creditos_var.set(pct)
        self._pct_lbl.config(text=f"{pct}%")

        if pct >= 70:
            self._pct_lbl.config(fg=GREEN)
            self._cred_status.config(
                text=f"✓ Cumple el 70% requerido", fg=GREEN)
        else:
            self._pct_lbl.config(fg=RED)
            self._cred_status.config(
                text=f"✗ Faltan {70 - pct}% (Art. 146)", fg=RED)

    # ──────────────────────────────────────────────────────────────────────────
    #  Lógica del sistema experto
    # ──────────────────────────────────────────────────────────────────────────

    def _evaluate(self):
        nombre = self._nombre_entry.get().strip()
        if not nombre or nombre == _PLACEHOLDER:
            self._show("warn", "⚠ Campo requerido",
                       "Por favor ingresa tu nombre completo antes de continuar.")
            return

        creditos  = self.creditos_var.get()
        induccion = self.induccion_var.get() == "si"
        lugar     = self.lugar_var.get() == "si"
        semestre  = self.semestre_var.get()
        institucion_publica = self.institucion_publica_var.get() == "si"
        actividad_valida    = self.actividad_valida_var.get() == "si"

        # Respuestas pre-cargadas (mismo flujo que el loop de terminal)
        answers = {
            "nombre":              nombre,
            "porcentaje_creditos": creditos,
            "induccion":           induccion,
            "lugar_valido":        lugar,
            "semestre":            semestre,
            "institucion_publica": institucion_publica,
            "actividad_valida":    actividad_valida,
        }

        engine = SistemaServicioSocial()
        engine.reset()
        engine.declare(Goal.create(GoalKind.CAN_ENROLL))
        engine.declare(Alumno(
            nombre=nombre,
            porcentaje_creditos=creditos,
            induccion=induccion,
            lugar_valido=lugar,
            semestre=semestre,
            institucion_publica=institucion_publica,
            actividad_valida=actividad_valida,
        ))
        engine.run()

        _, conclusion = engine.get_fact(Conclusion)
        conclusion_text = conclusion["text"] if conclusion else "No fue posible llegar a una conclusión."

        if "APROBADO" in conclusion_text:
            self._show("success", f"¡{nombre}, eres elegible!", conclusion_text)
        elif any(k in conclusion_text for k in ("RECHAZO", "PROHIBIDO", "REQUISITO")):
            self._show("error", "No elegible", conclusion_text)
        else:
            self._show("info", "Resultado", conclusion_text)

    def _show(self, kind, title, message):
        for w in self._result_outer.winfo_children():
            w.destroy()

        palettes = {
            "success": (GREEN,  "#0d2318"),
            "error":   (RED,    "#2a0d0d"),
            "warn":    (YELLOW, "#2a200d"),
            "info":    (ACCENT, "#0d1a2a"),
        }
        accent, bg = palettes.get(kind, (FG_DIM, CARD))

        card = tk.Frame(self._result_outer, bg=bg,
                        highlightthickness=2, highlightbackground=accent)
        card.pack(fill="x")

        # Barra de color lateral
        tk.Frame(card, bg=accent, width=4).pack(side="left", fill="y")

        inner = tk.Frame(card, bg=bg)
        inner.pack(side="left", fill="both", expand=True, padx=16, pady=14)

        tk.Label(inner, text=title, font=("Segoe UI Semibold", 13),
                 bg=bg, fg=accent).pack(anchor="w", pady=(0, 6))
        msg_lbl = tk.Label(inner, text=message, font=("Segoe UI", 10),
                            bg=bg, fg=FG, wraplength=500, justify="left")
        msg_lbl.pack(anchor="w")
        # Actualiza wraplength cuando el panel de resultado cambia de tamaño
        inner.bind("<Configure>",
                   lambda e, l=msg_lbl: l.config(wraplength=max(200, e.width - 8)))

        self._result_outer.pack(fill="x", padx=22, pady=(10, 28))

    def _reset(self):
        self._nombre_entry.delete(0, tk.END)
        self._nombre_entry.insert(0, _PLACEHOLDER)
        self._nombre_entry.config(fg=FG_DIM)
        self.creditos_total_entry.delete(0, tk.END)
        self.creditos_total_entry.insert(0, "400")
        self.creditos_obtenidos_entry.delete(0, tk.END)
        self.creditos_obtenidos_entry.insert(0, "200")
        self._calc_percentage()
        self.semestre_var.set(6)
        self.induccion_var.set("si")
        self.lugar_var.set("si")
        self.institucion_publica_var.set("si")
        self.actividad_valida_var.set("si")
        self._result_outer.pack_forget()


if __name__ == "__main__":
    App().mainloop()
