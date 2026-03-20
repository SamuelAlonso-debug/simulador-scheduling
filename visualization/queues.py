import matplotlib.pyplot as plt


def plot_queues(queue_history):
    fig, ax = plt.subplots(figsize=(14, 4))

    levels = sorted(queue_history[0][1].keys())

    colors = {}
    cmap = plt.cm.tab20

    for level_index, level in enumerate(levels):
        prev_time = None
        prev_state = None

        for time, snapshot in queue_history:
            state = tuple(snapshot[level])

            if prev_state is None:
                prev_time = time
                prev_state = state
                continue

            # Si cambia el estado, dibuja bloque
            if state != prev_state:
                duration = time - prev_time

                if prev_state:
                    label = ",".join(prev_state)

                    if label not in colors:
                        colors[label] = cmap(len(colors))

                    ax.barh(
                        level_index,
                        duration,
                        left=prev_time,
                        height=0.5,
                        color=colors[label],
                        edgecolor="black"
                    )

                    ax.text(
                        prev_time + duration / 2,
                        level_index,
                        label,
                        ha="center",
                        va="center",
                        fontsize=8,
                        color="white"
                    )

                prev_time = time
                prev_state = state

        # último bloque
        if prev_state:
            duration = queue_history[-1][0] - prev_time + 1
            label = ",".join(prev_state)

            if label not in colors:
                colors[label] = cmap(len(colors))

            ax.barh(
                level_index,
                duration,
                left=prev_time,
                height=0.5,
                color=colors[label],
                edgecolor="black"
            )

            ax.text(
                prev_time + duration / 2,
                level_index,
                label,
                ha="center",
                va="center",
                fontsize=8,
                color="white"
            )

    # Estilo
    ax.set_yticks(range(len(levels)))
    ax.set_yticklabels([f"Cola {lvl}" for lvl in levels])

    ax.set_xlabel("Tiempo")
    ax.set_title("Evolución de las colas")

    ax.grid(axis="x", linestyle="--", alpha=0.4)

    plt.tight_layout()

    return fig