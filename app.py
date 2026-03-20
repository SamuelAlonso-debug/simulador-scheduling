import streamlit as st
import pandas as pd

from models.process import Process
from core.scheduler import run_scheduler
from utils.metrics import calculate_metrics
from visualization.gantt import plot_gantt
from visualization.queues import plot_queues

st.set_page_config(page_title="Simulador de Scheduling", layout="wide")

st.title("Simulador de Planificación de Procesos")

# -----------------------------
# Sidebar → Configuración
# -----------------------------
st.sidebar.header("Configuración")

num_processes = st.sidebar.number_input(
    "Número de procesos",
    min_value=1,
    max_value=20,
    value=3
)

num_queues = st.sidebar.number_input(
    "Número de colas",
    min_value=1,
    max_value=5,
    value=2
)

# -----------------------------
# Configuración de colas
# -----------------------------
st.sidebar.subheader("Configuración de colas")

queues_config = {}

for i in range(num_queues):
    st.sidebar.markdown(f"**Cola {i}**")

    algo = st.sidebar.selectbox(
        f"Algoritmo cola {i}",
        ["fcfs", "rr", "sjf"],
        key=f"algo_{i}"
    )

    if algo == "rr":
        quantum = st.sidebar.number_input(
            f"Quantum cola {i}",
            min_value=1,
            value=2,
            key=f"quantum_{i}"
        )
        queues_config[i] = {"type": "rr", "quantum": quantum}
    else:
        queues_config[i] = {"type": algo}

# -----------------------------
# Tabla de procesos
# -----------------------------
st.subheader("Procesos")

data = []

for i in range(num_processes):
    col1, col2, col3, col4 = st.columns(4)

    pid = col1.text_input(f"PID {i}", f"P{i+1}", key=f"pid_{i}")
    arrival = col2.number_input(f"Arrival {i}", min_value=0, value=i, key=f"arr_{i}")
    burst = col3.number_input(f"Burst {i}", min_value=1, value=3, key=f"burst_{i}")
    queue = col4.number_input(
        f"Queue {i}",
        min_value=0,
        max_value=num_queues - 1,
        value=0,
        key=f"queue_{i}"
    )

    data.append({
        "pid": pid,
        "arrival": arrival,
        "burst": burst,
        "queue": queue
    })

# -----------------------------
# Ejecutar simulación
# -----------------------------
if st.button("Ejecutar simulación"):

    processes = [
        Process(
            pid=p["pid"],
            arrival_time=p["arrival"],
            burst_time=p["burst"],
            remaining_time=p["burst"],
            queue_level=p["queue"]
        )
        for p in data
    ]

    gantt, queue_history = run_scheduler(processes, queues_config)
    metrics = calculate_metrics(processes, gantt)

    # -------------------------
    # Gantt
    # -------------------------
    st.subheader("Diagrama de Gantt")
    fig = plot_gantt(gantt)
    st.pyplot(fig)

    # -------------------------
    # Colas
    # -------------------------
    st.subheader("Evolución de las colas")
    fig_queues = plot_queues(queue_history)
    st.pyplot(fig_queues)

    # -------------------------
    # Métricas por proceso
    # -------------------------
    st.subheader("Métricas por proceso")

    results = [
        {
            "PID": p.pid,
            "Turnaround": metrics["turnaround_time"][p.pid],
            "Waiting": metrics["waiting_time"][p.pid]
        }
        for p in processes
    ]

    df = pd.DataFrame(results)
    st.dataframe(df, use_container_width=True)

    # -------------------------
    #  PROMEDIOS
    # -------------------------
    st.subheader("Promedios")

    col1, col2 = st.columns(2)

    col1.metric(
        "Turnaround Promedio",
        f"{metrics['avg_turnaround']:.2f}"
    )

    col2.metric(
        "Waiting Promedio",
        f"{metrics['avg_waiting']:.2f}"
    )