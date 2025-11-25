# ---------------------------------------------------------------
# Michelson Interferometer Simulator
# ---------------------------------------------------------------
# This code was developed collaboratively by
# Prof. Francisco Geraldo and assistant ChatGPT,

# within the scope of the Physics Laboratory of the State University of Ceará (UECE).

# Objective:
# To implement an interactive simulation of the operating principle
# of a Michelson interferometer, including:
# - wave superposition;
# - phase variation induced by mirror displacement;
# - resulting intensity at each position;
# - intensity at the center as a function of displacement.

#
# Creation date: November 25, 2025
# Last modification: November 25, 2025
#
# Note: This code is part of the effort to develop computational teaching materials
# for teaching optical interferometry
# in the Physics course at UECE.

# ---------------------------------------------------------------


import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

# ----------------------------------------------------------
# Parâmetros físicos da onda (Laser He-Ne do EQ073)
# ----------------------------------------------------------
A = 1.0                       # amplitude das ondas individuais
lambda_0 = 632.8e-9           # comprimento de onda (m)
k = 2 * np.pi / lambda_0      # número de onda k = 2π/λ

# Eixo x em metros: centrado em zero, de -1,5 λ a +1,5 λ
x = np.linspace(-1.5 * lambda_0, 1.5 * lambda_0, 2000)
idx_centro = len(x) // 2      # índice do ponto x ≈ 0

# Faixa de deslocamento do espelho (em nm) para o slider e para o gráfico inferior
D_MIN_NM = 0.0
D_MAX_NM = 2000.0
D_INIT_NM = 0.0


# ----------------------------------------------------------
# Função que gera as ondas para um dado deslocamento d
# ----------------------------------------------------------
def ondas(d_m):
    """
    d_m = deslocamento do espelho em metros.
    Em um Michelson:
        φ = 4π d / λ
    """
    phi = 4 * np.pi * d_m / lambda_0

    y1 = A * np.sin(k * x)          # onda 1
    y2 = A * np.sin(k * x + phi)    # onda 2 (depende de d)
    y3 = y1 + y2                    # soma
    return y1, y2, y3, phi


# Ondas para o deslocamento inicial
d_init_m = D_INIT_NM * 1e-9
y1, y2, y3, phi0 = ondas(d_init_m)
I_x = y3**2                         # intensidade ao longo de x

# ----------------------------------------------------------
# Intensidade no centro em função de d (gráfico inferior)
# ----------------------------------------------------------
d_vals_nm = np.linspace(D_MIN_NM, D_MAX_NM, 800)
d_vals_m = d_vals_nm * 1e-9

I_centro_vals = []
for d_m in d_vals_m:
    _, _, y3_tmp, _ = ondas(d_m)
    I_centro_vals.append(y3_tmp[idx_centro] ** 2)

I_centro_vals = np.array(I_centro_vals)

# Intensidade no centro para o d inicial (para o marcador)
I_centro_init = I_x[idx_centro]


# ----------------------------------------------------------
# Configuração da figura e eixos
# ----------------------------------------------------------
plt.close("all")
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 7), sharex=False)
fig.subplots_adjust(bottom=0.22, hspace=0.3)

# ---- Gráfico superior: ondas e soma ----
line1, = ax1.plot(x, y1, label="Onda 1 (vermelha)", linewidth=2, color="red")
line2, = ax1.plot(x, y2, label="Onda 2 (azul)", linewidth=2, color="blue")
line3, = ax1.plot(x, y3, label="Soma (preta tracejada)",
                  linewidth=2, linestyle="--", color="black")

ax1.set_ylabel("Amplitude (u.a.)", fontsize=12)
ax1.set_title("Interferência (Michelson): ondas e soma\nλ = 632,8 nm", fontsize=14)
ax1.set_ylim(-2, 2)
ax1.grid(True, alpha=0.3)
ax1.legend(loc="upper right", fontsize=9)

# Caixa de texto com info de d e φ
text_info = ax1.text(
    0.02, 0.95, "",
    transform=ax1.transAxes,
    fontsize=10,
    verticalalignment="top",
    bbox=dict(boxstyle="round", facecolor="white", alpha=0.8)
)

def atualiza_texto(d_m, phi, I_c):
    text_info.set_text(
        r"$\varphi = \frac{4\pi d}{\lambda}$" + "\n"
        rf"$d = {d_m*1e9:6.1f}\,\text{{nm}}$" + "\n"
        rf"$\varphi = {phi:6.3f}\,\text{{rad}}$" + "\n"
        rf"$I_\text{{centro}} \propto {I_c:5.2f}$"
    )

atualiza_texto(d_init_m, phi0, I_centro_init)

# ---- Gráfico inferior: intensidade no centro vs deslocamento ----
lineIc, = ax2.plot(d_vals_nm, I_centro_vals, linewidth=2)
ax2.set_xlabel("Deslocamento do espelho d (nm)", fontsize=12)
ax2.set_ylabel("Intensidade no centro (u.a.)", fontsize=12)
ax2.set_title("Intensidade no centro em função do deslocamento do espelho", fontsize=13)
ax2.grid(True, alpha=0.3)
ax2.set_xlim(D_MIN_NM, D_MAX_NM)
ax2.set_ylim(0, 4.2)  # máximo ≈ (2A)^2

# Linha vertical e ponto que marcam o d atual
vline = ax2.axvline(D_INIT_NM, color="red", linestyle="--", linewidth=1.5)
ponto, = ax2.plot([D_INIT_NM], [I_centro_init], 'ro')


# ----------------------------------------------------------
# Slider de deslocamento do espelho
# ----------------------------------------------------------
ax_d = plt.axes([0.15, 0.08, 0.70, 0.03])

slider_d = Slider(
    ax=ax_d,
    label="Deslocamento do espelho d (nm)",
    valmin=D_MIN_NM,
    valmax=D_MAX_NM,
    valinit=D_INIT_NM,
)


# ----------------------------------------------------------
# Callback do slider
# ----------------------------------------------------------
def on_d_change(val):
    d_nm = slider_d.val
    d_m = d_nm * 1e-9

    # Recalcula ondas e intensidade em x
    y1_new, y2_new, y3_new, phi = ondas(d_m)
    I_x_new = y3_new**2
    I_c_new = I_x_new[idx_centro]

    # Atualiza curvas no gráfico superior
    line1.set_ydata(y1_new)
    line2.set_ydata(y2_new)
    line3.set_ydata(y3_new)

    # Atualiza marcador no gráfico inferior
    vline.set_xdata([d_nm, d_nm])   # <- AQUI ESTAVA O ERRO: precisa ser sequência
    ponto.set_data([d_nm], [I_c_new])

    # Atualiza texto
    atualiza_texto(d_m, phi, I_c_new)

    fig.canvas.draw_idle()


slider_d.on_changed(on_d_change)

plt.show()
