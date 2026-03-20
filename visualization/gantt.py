import matplotlib.pyplot as plt


def plot_gantt(gantt):
    fig, ax = plt.subplots(figsize=(14, 2.5))

    # Colores por proceso
    colors = {}
    cmap = plt.cm.tab20

    y = 0
    bar_height = 0.5

    # Obtener tiempo total
    max_time = max(entry.end for entry in gantt)

    for i, entry in enumerate(gantt):
        if entry.pid not in colors:
            colors[entry.pid] = cmap(len(colors))

        duration = entry.end - entry.start

        ax.barh(
            y,
            duration,
            left=entry.start,
            height=bar_height,
            color=colors[entry.pid],
            edgecolor="black"
        )

        # Label centrado
        ax.text(
            entry.start + duration / 2,
            y,
            entry.pid,
            va="center",
            ha="center",
            color="white",
            fontsize=10,
            fontweight="bold"
        )

    ax.set_yticks([])

    # Timeline (ticks)
    ax.set_xticks(range(0, max_time + 1))
    ax.set_xlabel("Tiempo")

    # Grid vertical (OS)
    ax.grid(axis="x", linestyle="--", alpha=0.5)

    # Quitar bordes innecesarios
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_visible(False)

    # Margen ajustado
    ax.set_ylim(-0.5, 0.5)

    ax.set_title("Diagrama de Gantt", fontsize=14, fontweight="bold")

    plt.tight_layout()

    return fig