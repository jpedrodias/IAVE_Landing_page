#!/usr/bin/env bash
set -euo pipefail

BASE="https://assets.iave.pt/production/vm-images"
PREFIX="iave-offline-production"
OUT="available_versions.txt"

: > "$OUT"

for major in $(seq 0 10); do
  for minor in $(seq 0 10); do
    for patch in $(seq 0 10); do
      ver="v${major}-${minor}-${patch}"
      url="${BASE}/${PREFIX}-${ver}.ova"

      if wget -q --spider "$url"; then
        echo "$ver  ->  $url"
        echo "$ver $url" >> "$OUT"
      fi
    done
  done
done

echo "Feito. Versões encontradas em: $OUT"
