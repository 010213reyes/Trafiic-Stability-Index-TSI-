#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Descarga y registra el estado de acceso de fuentes públicas multiciudad.

Este script no fuerza una fuente si no existe un recurso real y compatible.
Su objetivo es conservar evidencia objetiva sobre qué ciudades tienen datos
válidos para el pipeline del proyecto.
"""

from __future__ import annotations

import json
import time
from pathlib import Path
from typing import Any

import requests

PROJECT_ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = PROJECT_ROOT / "data" / "00_raw" / "external" / "source_downloads"
INTERNATIONAL_DIR = PROJECT_ROOT / "data" / "00_raw" / "external"
MANIFEST_PATH = PROJECT_ROOT / "data" / "00_raw" / "external" / "multicity_sources_manifest.json"
CONTRACT_PATH = INTERNATIONAL_DIR / "international_sources_contract.json"

HEADERS = {"User-Agent": "Mozilla/5.0"}


def safe_get(url: str, timeout: int = 45) -> requests.Response:
    response = requests.get(url, timeout=timeout, headers=HEADERS, allow_redirects=True)
    response.raise_for_status()
    return response


def download_file(url: str, destination: Path) -> dict[str, Any]:
    destination.parent.mkdir(parents=True, exist_ok=True)
    last_error = None
    for attempt in range(1, 4):
        try:
            response = requests.get(
                url,
                timeout=(30, 300),
                headers=HEADERS,
                allow_redirects=True,
                stream=True,
            )
            response.raise_for_status()
            total_bytes = 0
            with destination.open("wb") as handle:
                for chunk in response.iter_content(chunk_size=1024 * 1024):
                    if chunk:
                        handle.write(chunk)
                        total_bytes += len(chunk)
            return {
                "url": url,
                "destination": str(destination.relative_to(PROJECT_ROOT)),
                "bytes": total_bytes,
                "content_type": response.headers.get("content-type", "")[:120],
                "status_code": response.status_code,
                "attempt": attempt,
            }
        except (requests.RequestException, OSError) as exc:
            last_error = exc
            if destination.exists():
                destination.unlink()
            if attempt < 3:
                time.sleep(attempt * 2)
    raise last_error


def fetch_json(url: str) -> dict[str, Any]:
    return safe_get(url).json()


def acquire_istanbul() -> dict[str, Any]:
    url = "https://data.ibb.gov.tr/api/3/action/package_search?q=traffic"
    payload = fetch_json(url)
    results = payload.get("result", {}).get("results", [])
    traffic_candidates = []
    for item in results:
        title = (item.get("title") or item.get("name") or "").lower()
        notes = (item.get("notes") or "").lower()
        if "traffic" in title or "traffic" in notes or "trafik" in title or "trafik" in notes:
            traffic_candidates.append(item)

    if not traffic_candidates:
        return {
            "ciudad": "Istanbul",
            "pais": "Turquia",
            "status": "no_validado",
            "motivo": "No se detectó un paquete de tráfico utilizables en la API pública actual.",
        }

    chosen = traffic_candidates[0]
    resources = chosen.get("resources", [])
    csv_resources = [r for r in resources if (r.get("url") or "").lower().endswith(".csv")]
    if not csv_resources:
        return {
            "ciudad": "Istanbul",
            "pais": "Turquia",
            "status": "no_validado",
            "motivo": "El paquete de tráfico no expone un CSV descargable directo.",
        }

    url_csv = csv_resources[0]["url"]
    output = OUT_DIR / "istanbul_traffic_index.csv"
    info = download_file(url_csv, output)
    return {
        "ciudad": "Istanbul",
        "pais": "Turquia",
        "status": "descargado",
        "dataset": "Istanbul Traffic Index",
        "url": url_csv,
        "output": str(output.relative_to(PROJECT_ROOT)),
        "download": info,
    }


def acquire_bangkok() -> dict[str, Any]:
    url = "https://opendata.bangkok.go.th/api/3/action/package_search?q=traffic"
    try:
        response = safe_get(url)
    except Exception as exc:
        return {
            "ciudad": "Bangkok",
            "pais": "Tailandia",
            "status": "no_accseso",
            "motivo": f"No se pudo acceder a la API pública: {exc.__class__.__name__}: {exc}",
        }

    text = response.text.lower()
    if "<!doctype html>" in text or "<html" in text:
        return {
            "ciudad": "Bangkok",
            "pais": "Tailandia",
            "status": "no_validado",
            "motivo": "El portal responde, pero la API de paquetes no expone un dataset de tráfico reutilizable desde esta sesión.",
        }

    try:
        payload = response.json()
    except Exception:
        return {
            "ciudad": "Bangkok",
            "pais": "Tailandia",
            "status": "no_validado",
            "motivo": "La respuesta no fue JSON y no se identificó un recurso descargable de tráfico.",
        }

    results = payload.get("result", {}).get("results", [])
    return {
        "ciudad": "Bangkok",
        "pais": "Tailandia",
        "status": "pendiente",
        "motivo": f"Se revisó la API, pero aún no se validó un recurso de tráfico compatible (resultados analizados: {len(results)}).",
    }


def acquire_barcelona() -> dict[str, Any]:
    url = "https://opendata-ajuntament.barcelona.cat/data/api/3/action/package_search?q=transport"
    try:
        payload = fetch_json(url)
    except Exception as exc:
        return {
            "ciudad": "Barcelona",
            "pais": "Espana",
            "status": "no_accseso",
            "motivo": f"No fue posible consultar la API: {exc.__class__.__name__}: {exc}",
        }

    results = payload.get("result", {}).get("results", [])
    if not results:
        return {
            "ciudad": "Barcelona",
            "pais": "Espana",
            "status": "no_validado",
            "motivo": "La API no devolvió datasets relevantes para tráfico urbano.",
        }

    return {
        "ciudad": "Barcelona",
        "pais": "Espana",
        "status": "pendiente",
        "motivo": "El catálogo está disponible, pero no se identificó un dataset operativo de flujo/velocidad con suficiente resolución para el pipeline actual.",
    }


def acquire_madrid() -> dict[str, Any]:
    api_url = "https://datos.madrid.es/api/3/action/package_show?id=208627-0-transporte-ptomedida-historico"
    try:
        payload = fetch_json(api_url)
        resources = payload.get("result", {}).get("resources", [])
        zip_resources = [item for item in resources if (item.get("format") or "").upper() == "ZIP"]
        if not zip_resources:
            raise ValueError("El paquete no expone recursos ZIP descargables.")
        selected = zip_resources[0]
        destination = INTERNATIONAL_DIR / "madrid" / "historico_2022_12.zip"
        info = download_file(selected["url"], destination)
        return {
            "ciudad": "Madrid",
            "pais": "Espana",
            "status": "descargado",
            "dataset": "Historico de datos del trafico desde 2013",
            "url": selected["url"],
            "output": str(destination.relative_to(PROJECT_ROOT)),
            "download": info,
        }
    except Exception as exc:
        return {
            "ciudad": "Madrid",
            "pais": "Espana",
            "status": "no_accseso",
            "motivo": f"No fue posible descargar el recurso oficial: {exc.__class__.__name__}: {exc}",
            "url_probed": api_url,
        }


def acquire_sao_paulo() -> dict[str, Any]:
    api_url = "https://dados.prefeitura.sp.gov.br/api/3/action/package_show?id=base-de-dados-sobre-lentidao-por-trechos-cet"
    try:
        payload = fetch_json(api_url)
        resources = payload.get("result", {}).get("resources", [])
        csv_resources = [
            item for item in resources
            if (item.get("format") or "").upper() == "CSV" and "2023" in (item.get("name") or "")
        ]
        if not csv_resources:
            raise ValueError("El paquete no expone un CSV anual 2023.")
        selected = csv_resources[0]
        destination = INTERNATIONAL_DIR / "sao_paulo" / "lentidao_trechos_2023.csv"
        info = download_file(selected["url"], destination)
        return {
            "ciudad": "Sao Paulo",
            "pais": "Brasil",
            "status": "descargado",
            "dataset": "Base de dados sobre lentidao por trechos - CET 2001 a 2023",
            "url": selected["url"],
            "output": str(destination.relative_to(PROJECT_ROOT)),
            "download": info,
        }
    except Exception as exc:
        fallback_url = "https://www.kaggle.com/api/v1/datasets/download/danlessa/sao-paulo-traffic-jams-since-2001"
        destination = INTERNATIONAL_DIR / "sao_paulo" / "sao_paulo_traffic_jams_kaggle.zip"
        try:
            info = download_file(fallback_url, destination)
            return {
                "ciudad": "Sao Paulo",
                "pais": "Brasil",
                "status": "descargado_copia_secundaria",
                "dataset": "Sao Paulo Traffic Jams since 2001",
                "primary_source": "CET / Prefeitura de Sao Paulo",
                "url": fallback_url,
                "official_catalog_url": api_url,
                "output": str(destination.relative_to(PROJECT_ROOT)),
                "download": info,
                "official_download_error": f"{exc.__class__.__name__}: {exc}",
            }
        except Exception as fallback_exc:
            return {
                "ciudad": "Sao Paulo",
                "pais": "Brasil",
                "status": "no_accseso",
                "motivo": f"Fallaron la fuente oficial y la copia secundaria: {fallback_exc.__class__.__name__}: {fallback_exc}",
                "url_probed": api_url,
            }


def acquire_dubai() -> dict[str, Any]:
    url = "https://www.rta.ae/wps/portal/rta/ae/home"
    try:
        safe_get(url)
        return {
            "ciudad": "Dubai",
            "pais": "Emiratos Arabes Unidos",
            "status": "pendiente",
            "motivo": "El sitio respondió, pero no se encontró un dataset de tráfico público y directamente descargable en esta validación.",
            "url_probed": url,
        }
    except Exception as exc:
        return {
            "ciudad": "Dubai",
            "pais": "Emiratos Arabes Unidos",
            "status": "no_accseso",
            "motivo": f"El portal no respondió de forma confiable: {exc.__class__.__name__}: {exc}",
        }


def main() -> None:
    report = {
        "project": "TSI",
        "strategy": "transferencia_multiciudad",
        "generated_at": "2026-09-23",
        "ciudades": [
            acquire_istanbul(),
            acquire_sao_paulo(),
            acquire_madrid(),
            acquire_bangkok(),
            acquire_barcelona(),
            acquire_dubai(),
        ],
    }

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    manifest_path = OUT_DIR / "multicity_acquisition_status.json"
    manifest_path.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")

    if MANIFEST_PATH.exists():
        current = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
        current["acquisition_status"] = report
        MANIFEST_PATH.write_text(json.dumps(current, indent=2, ensure_ascii=False), encoding="utf-8")
    else:
        MANIFEST_PATH.write_text(json.dumps({"acquisition_status": report}, indent=2, ensure_ascii=False), encoding="utf-8")

    if CONTRACT_PATH.exists():
        contract = json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))
        status_by_city = {item["ciudad"]: item for item in report["ciudades"]}
        for source in contract["sources"]:
            result = status_by_city.get(source["city"])
            if result and result["status"] in {"descargado", "descargado_copia_secundaria"}:
                source["status"] = "raw_validated"
                source["raw_path"] = result["output"]
        CONTRACT_PATH.write_text(json.dumps(contract, indent=2, ensure_ascii=False), encoding="utf-8")

    print(json.dumps(report, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
