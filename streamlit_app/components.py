from __future__ import annotations

import streamlit as st


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
        :root { --ink:#17212b; --muted:#66727d; --line:#d9e2e8; --accent:#0f766e; --accent-light:#ccfbf1; --warm:#f59e0b; }
        .block-container { max-width: 1220px; padding-top: 2rem; }
        .tsi-hero { padding: 2rem 2.2rem; border: 1px solid var(--line); background: linear-gradient(120deg, #f8fafc, #ecfeff); border-radius: 12px; margin-bottom: 1.5rem; }
        .tsi-kicker { color: var(--accent); font-size: .78rem; font-weight: 700; letter-spacing: .08em; text-transform: uppercase; }
        .tsi-hero h1 { color: var(--ink); margin: .35rem 0 .45rem; }
        .tsi-hero p { color: var(--muted); margin: 0; max-width: 760px; }
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


def render_phase_header(number: str, title: str, description: str) -> None:
    st.markdown(f'<div class="tsi-kicker">Fase {number}</div><h1>{title}</h1><p>{description}</p>', unsafe_allow_html=True)


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
