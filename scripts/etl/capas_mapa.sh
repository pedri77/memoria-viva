#!/usr/bin/env bash
# F2 · Capas del atlas a partir de mapSpainHist (CC BY 4.0).
# Genera en site/public/data/v1/:
#   provincias_1930.geojson  (cod_unit, nombre)                       simplificada
#   municipios_1930.geojson  (cod_ine, nombre, phec1930)              simplificada, carga diferida
# y data/external/mapspainhist/prov_1930_centroides.csv (punto interior real, sin desplazar).
# Canarias (provincias 35 y 38) se desplaza SOLO en las capas de dibujo (recuadro), +6 lon, +7 lat.
set -euo pipefail
cd "$(dirname "$0")/../.."
SRC=data/external/mapspainhist
OUT=site/public/data/v1
TMP=$(mktemp -d)
[ -f $SRC/mapSpainHist_geometries_v1.0.0.topojson ] || gunzip -k $SRC/mapSpainHist_geometries_v1.0.0.topojson.gz
TOPO=$SRC/mapSpainHist_geometries_v1.0.0.topojson
MS="npx --no-install mapshaper"
CANARIAS_DX=6; CANARIAS_DY=7

# Población de hecho 1930 por municipio
python3 -I - "$SRC/censos.csv" "$TMP/phec1930.csv" <<'PY'
import csv, sys
rows = [r for r in csv.DictReader(open(sys.argv[1], encoding="utf-8")) if r["censo"] == "1930" and r["phec"] != "NA"]
w = csv.writer(open(sys.argv[2], "w", newline="", encoding="utf-8")); w.writerow(["cod_ine", "nombre", "phec1930"])
for r in rows: w.writerow([r["cod_ine"], r["municipio"], r["phec"]])
PY

$MS -i $TOPO -target prov_hist_1930 -proj wgs84 -points inner -each 'lon=+this.x.toFixed(4),lat=+this.y.toFixed(4)' \
  -filter-fields cod_unit,lon,lat -o $SRC/prov_1930_centroides.csv format=csv

$MS -i $TOPO -target prov_hist_1930 -proj wgs84 -simplify 4% keep-shapes \
  -rename-fields nombre=nom -filter-fields cod_unit,nombre \
  -affine where='cod_unit=="35"||cod_unit=="38"' shift=$CANARIAS_DX,$CANARIAS_DY \
  -o $OUT/provincias_1930.geojson format=geojson precision=0.0001

$MS -i $TOPO -target map_muni_es_hist_1930 -proj wgs84 -simplify 8% keep-shapes \
  -join $TMP/phec1930.csv keys=cod_ine,cod_ine string-fields=cod_ine \
  -filter-fields cod_ine,nombre,phec1930 \
  -affine where='cod_ine.slice(0,2)=="35"||cod_ine.slice(0,2)=="38"' shift=$CANARIAS_DX,$CANARIAS_DY \
  -o $OUT/municipios_1930.geojson format=geojson precision=0.0001
rm -rf "$TMP"
ls -la $OUT
