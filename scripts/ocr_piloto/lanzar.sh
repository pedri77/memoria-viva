#!/usr/bin/env bash
# Lanza el piloto OCR en HF Jobs: LightOnOCR-3 0.8B y 4B sobre las 20 páginas.
#
# Por defecto solo hace --dry-run (gratis). Con --ejecutar lanza los dos jobs (DE PAGO,
# a10g-small, pay-as-you-go) en segundo plano y deja los resultados en datasets PRIVADOS.
#
# Requisitos: hf CLI >= 1.32 (`hf version`), `hf auth login`, crédito en la cuenta,
# y el dataset de entrada subido con: uv run scripts/ocr_piloto/preparar.py --push "$ENTRADA"
#
# Uso: scripts/ocr_piloto/lanzar.sh USUARIO [--ejecutar]
set -euo pipefail

USUARIO="${1:?Uso: lanzar.sh USUARIO_HF [--ejecutar]}"
MODO="${2:---dry-run}"
SCRIPT="https://huggingface.co/datasets/uv-scripts/ocr/raw/main/lighton-ocr3.py"
ENTRADA="$USUARIO/memoria-viva-ocr-piloto"

for MODELO in 0.8B 4B; do
  SALIDA="$USUARIO/memoria-viva-ocr-piloto-$(echo "$MODELO" | tr "[:upper:]" "[:lower:]")"
  ARGS=(
    --flavor a10g-small --timeout 1h
    "$SCRIPT" "$ENTRADA" "$SALIDA"
    --model "lightonai/LightOnOCR-3-$MODELO"
    --mode plain --private
    --max-tokens 6144   # páginas densas a tres columnas
  )
  if [[ "$MODO" == "--ejecutar" ]]; then
    hf jobs uv run --detach "${ARGS[@]}"
  else
    hf jobs uv run --dry-run "${ARGS[@]}"
  fi
done

[[ "$MODO" == "--ejecutar" ]] && echo "Seguimiento: hf jobs ps · hf jobs logs -f <id>"
