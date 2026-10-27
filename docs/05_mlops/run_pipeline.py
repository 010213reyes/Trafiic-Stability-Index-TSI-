"""Ejecuta el ciclo MLOps local completo en orden."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
VERSION_SCRIPT = ROOT / "docs" / "05_mlops" / "01_versionado_modelo" / "versionar_modelo.py"
COMPARISON_SCRIPT = ROOT / "docs" / "05_mlops" / "01_versionado_modelo" / "registrar_modelos_comparacion.py"
INFERENCE_SCRIPT = ROOT / "docs" / "05_mlops" / "02_inferencia_reproducible" / "inferir_tsi.py"
MONITORING_SCRIPT = ROOT / "docs" / "05_mlops" / "03_monitoreo" / "monitorear_flujo.py"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--model-version", help="Version manual opcional para los tres pasos")
    parser.add_argument(
        "--model",
        choices=["all", "random_forest", "ridge", "baseline"],
        default="all",
        help="Modelo o conjunto de modelos que se entrena y registra",
    )
    return parser.parse_args()


def run_step(label: str, script: Path, model_version: str | None = None) -> None:
    command = [sys.executable, str(script)]
    if model_version:
        command.extend(["--model-version", model_version])
    print(f"\n=== {label} ===")
    subprocess.run(command, cwd=ROOT, check=True)


def main() -> None:
    args = parse_args()
    if args.model in {"all", "random_forest"}:
        run_step("VERSIONADO RANDOM FOREST", VERSION_SCRIPT, args.model_version)
        run_step("INFERENCIA", INFERENCE_SCRIPT, args.model_version)
        run_step("MONITOREO", MONITORING_SCRIPT, args.model_version)
    if args.model in {"all", "ridge", "baseline"}:
        comparison_command = [sys.executable, str(COMPARISON_SCRIPT), "--model", args.model if args.model != "all" else "all"]
        print("\n=== REGISTRO COMPARATIVO ===")
        subprocess.run(comparison_command, cwd=ROOT, check=True)
    print("\nCiclo MLOps completado correctamente.")


if __name__ == "__main__":
    main()
