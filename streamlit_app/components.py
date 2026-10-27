from __future__ import annotations

import streamlit as st

from services.pipeline import run_pipeline


PHASES = [
    ("home", "Mapa", "Recorrido completo"),
    ("mineria", "01", "Mineria de datos"),
    ("ingenieria", "02", "Ingenieria de datos"),
    ("analisis", "03", "Analisis"),
    ("ciencia", "04", "Ciencia de datos"),
    ("mlops", "05", "MLOps"),
]


def inject_styles() -> None:
    st.markdown(
        """
        <style>
        :root { --ink:#18222c; --muted:#687783; --line:#dbe4e8; --accent:#0f766e; --accent-light:#ccfbf1; --warm:#f59e0b; --panel:#f6f8f9; --nav:#ffffff; }
        .stApp { background:#f6f8f9; color:var(--ink); }
        [data-testid="stSidebar"] { background:var(--nav); border-right:1px solid var(--line); }
        [data-testid="stSidebar"] * { color:var(--ink); }
        [data-testid="stSidebar"] .tsi-kicker { color:var(--accent); }
        [data-testid="stSidebar"] button { border:1px solid transparent; background:transparent; text-align:left; }
        [data-testid="stSidebar"] button:hover { border-color:#b7d9d4; color:var(--accent); background:#effaf8; }
        .block-container { max-width: 1280px; padding-top: 1.4rem; }
        .tsi-hero { padding:2.3rem 2.5rem; border:1px solid var(--line); background:white; border-radius:6px; margin-bottom:1.5rem; box-shadow:0 10px 24px rgba(24,34,44,.04); }
        .tsi-kicker { color: var(--accent); font-size: .78rem; font-weight: 700; letter-spacing: .08em; text-transform: uppercase; }
        .tsi-hero h1 { color: var(--ink); margin: .35rem 0 .45rem; }
        .tsi-hero p { color: var(--muted); margin: 0; max-width: 760px; }
        .tsi-workspace-bar { display:flex; justify-content:space-between; align-items:center; border-bottom:1px solid var(--line); padding-bottom:.8rem; margin-bottom:1.2rem; color:var(--muted); font-size:.82rem; }
        .tsi-workspace-bar strong { color:var(--ink); font-size:.9rem; }
        .tsi-explanation { background:white; border:1px solid var(--line); border-left:4px solid var(--accent); padding:1.1rem 1.3rem; margin:1.2rem 0 1.5rem; border-radius:4px; }
        .tsi-explanation h3 { margin:.1rem 0 .4rem; color:var(--ink); font-size:1.05rem; }
        .tsi-explanation p { margin:0; color:var(--muted); line-height:1.55; }
        .tsi-contract { display:grid; grid-template-columns:repeat(2, minmax(0, 1fr)); gap:.65rem; margin-top:.9rem; }
        .tsi-contract div { background:var(--panel); padding:.65rem .8rem; border-radius:3px; }
        .tsi-contract small { display:block; color:var(--muted); text-transform:uppercase; font-size:.66rem; letter-spacing:.06em; }
        .tsi-contract strong { display:block; margin-top:.2rem; color:var(--ink); font-size:.86rem; }
        .tsi-workspace-card { background:white; border:1px solid var(--line); border-radius:5px; padding:1rem 1.1rem; height:100%; }
        .tsi-workspace-card h3 { margin:.1rem 0 .45rem; color:var(--ink); font-size:1rem; }
        .tsi-workspace-card p { color:var(--muted); font-size:.9rem; line-height:1.5; }
        .tsi-run-console { background:#202c33; color:#dce7ea; border-radius:5px; padding:1rem 1.15rem; margin:1.2rem 0 1.5rem; font-family:ui-monospace, SFMono-Regular, Consolas, monospace; }
        .tsi-run-console h3 { color:white; font-size:.95rem; margin:0 0 .8rem; font-family:inherit; }
        .tsi-run-line { display:flex; gap:.7rem; align-items:center; padding:.45rem 0; border-top:1px solid #34434b; font-size:.8rem; }
        .tsi-run-line:first-of-type { border-top:0; }
        .tsi-run-status { color:#76e2c1; min-width:90px; }
        .tsi-run-detail { color:#aabdc4; }
        .tsi-run-result { color:white; margin-top:.8rem; padding-top:.7rem; border-top:1px solid #34434b; font-family:inherit; }
        .tsi-process { display:flex; align-items:center; gap:0; margin:2rem 0; overflow-x:auto; padding: .5rem .2rem 1rem; }
        .tsi-node { min-width:155px; text-align:center; position:relative; animation: tsi-rise .55s both; }
        .tsi-node:nth-child(2){animation-delay:.12s}.tsi-node:nth-child(3){animation-delay:.24s}.tsi-node:nth-child(4){animation-delay:.36s}.tsi-node:nth-child(5){animation-delay:.48s}
        .tsi-dot { width:58px; height:58px; margin:auto; display:grid; place-items:center; border-radius:50%; background:var(--accent); color:white; font-weight:800; box-shadow:0 0 0 8px var(--accent-light); }
        .tsi-node strong { display:block; margin-top:1rem; color:var(--ink); }
        .tsi-node small { display:block; color:var(--muted); margin-top:.25rem; }
        .tsi-link { height:2px; min-width:42px; background:linear-gradient(90deg, var(--accent), var(--warm)); animation: tsi-flow 1.4s infinite linear; }
        .tsi-phase { border:1px solid var(--line); border-radius:10px; padding:1rem; min-height:130px; background:white; }
        .tsi-phase-num { color:var(--accent); font-weight:800; font-size:.8rem; }
        .tsi-phase h3 { margin:.25rem 0 .35rem; color:var(--ink); font-size:1.05rem; }
        .tsi-phase p { margin:0; color:var(--muted); font-size:.9rem; }
        @keyframes tsi-rise { from { opacity:0; transform:translateY(12px); } to { opacity:1; transform:translateY(0); } }
        @keyframes tsi-flow { 0% { opacity:.35; } 50% { opacity:1; } 100% { opacity:.35; } }
        @media (prefers-reduced-motion: reduce) { *, *::before, *::after { animation-duration:.01ms !important; animation-iteration-count:1 !important; } }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_process_animation() -> None:
    labels = [("01", "Mineria", "Fuentes"), ("02", "Ingenieria", "Pipeline"), ("03", "Analisis", "TSI"), ("04", "Ciencia", "Modelo"), ("05", "MLOps", "Operacion")]
    parts = []
    for index, (number, title, detail) in enumerate(labels):
        parts.append(f'<div class="tsi-node"><div class="tsi-dot">{number}</div><strong>{title}</strong><small>{detail}</small></div>')
        if index < len(labels) - 1:
            parts.append('<div class="tsi-link"></div>')
    st.markdown(f'<div class="tsi-process">{"".join(parts)}</div>', unsafe_allow_html=True)


def render_pipeline_runner() -> None:
    st.markdown('<div class="tsi-kicker">Pipeline control</div>', unsafe_allow_html=True)
    st.subheader("Ejecucion del pipeline")
    st.caption("Entrena el modelo, crea una nueva version y actualiza inferencia y monitoreo.")
    model_options = {
        "Todos los modelos": "all",
        "Random Forest": "random_forest",
        "Ridge": "ridge",
        "Baseline de persistencia": "baseline",
    }
    selected_label = st.selectbox("Modelo a ejecutar", list(model_options), key="pipeline_model_selector")
    selected_model = model_options[selected_label]
    run_requested = st.session_state.pop("auto_run_pipeline", False)
    if st.button("Entrenar y registrar nueva version", type="primary", use_container_width=False):
        run_requested = True
    if run_requested:
        with st.status("Entrenando y registrando nueva version...", expanded=True) as status:
            success, output = run_pipeline(selected_model)
            if output:
                st.code(output[-6000:], language="text")
            if success:
                status.update(label="Version registrada correctamente", state="complete")
            else:
                status.update(label="El pipeline termino con errores", state="error")
        if success:
            st.session_state.pipeline_run_completed = True
            st.session_state.last_pipeline_model = selected_model
            st.session_state.page = "mlops"
            st.rerun()
    elif st.session_state.get("pipeline_run_completed"):
        st.success("Ultima ejecucion registrada disponible. Puedes consultar el historial en MLOps.")


def render_workspace_bar(section: str, state: str = "Ejecucion documentada") -> None:
    st.markdown(
        f'<div class="tsi-workspace-bar"><span><strong>TSI WORKSPACE</strong> &nbsp;/&nbsp; {section}</span><span>{state}</span></div>',
        unsafe_allow_html=True,
    )


def render_phase_header(number: str, title: str, description: str) -> None:
    render_workspace_bar(f"Fase {number}")
    st.markdown(f'<div class="tsi-kicker">Fase {number}</div><h1>{title}</h1><p>{description}</p>', unsafe_allow_html=True)


def render_phase_explanation(title: str, description: str, input_text: str, output_text: str) -> None:
    st.markdown(
        f'<div class="tsi-explanation"><h3>{title}</h3><p>{description}</p><div class="tsi-contract"><div><small>Entrada</small><strong>{input_text}</strong></div><div><small>Salida</small><strong>{output_text}</strong></div></div></div>',
        unsafe_allow_html=True,
    )


def navigate_to(page: str) -> None:
    st.session_state.page = page
    st.rerun()


def render_phase_navigation(current: str) -> None:
    previous = {phase[0]: PHASES[index - 1][0] for index, phase in enumerate(PHASES) if index > 0}
    following = {phase[0]: PHASES[index + 1][0] for index, phase in enumerate(PHASES[:-1])}
    left, center, right = st.columns([1, 2, 1])
    with left:
        if current in previous and st.button("Anterior", use_container_width=True):
            navigate_to(previous[current])
    with center:
        st.caption(" / ".join(phase[1] for phase in PHASES if phase[0] == current))
    with right:
        if current in following and st.button("Siguiente", use_container_width=True):
            navigate_to(following[current])
