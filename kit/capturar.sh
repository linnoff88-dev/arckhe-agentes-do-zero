#!/usr/bin/env bash
# Roda os blocos (kit/blocos/*.sh) em ordem, como o aluno: um HOME temporário só, que começa vazio.
# O a1a clona o kit do GitHub, então capture DEPOIS do push. Grava kit/saidas/<bloco>.txt.
#   bash kit/capturar.sh
# Cada bloco pega a SUA vaga gpu da máquina (fila-vaga) e solta ao terminar: as rotinas (clima 24h, virais) entram entre
# dois blocos. Não embrulhe o script inteiro em `fila-vaga gpu …` (14/11/2026: o lote segurou a vaga das 04:45 às 06:16
# e a voz do Clima 24h desistiu às 06:10). Sem a fila instalada, roda direto.
set -uo pipefail
K=$(cd "$(dirname "$0")" && pwd); T=$(mktemp -d /tmp/adz.XXXX); trap 'rm -rf "$T"' EXIT
FILA="${VAGA_CMD:-$HOME/projetos/wifi/scripts/fila-vaga}"
vaga() { if [ -x "$FILA" ]; then "$FILA" gpu "agentes-do-zero-$1" -- "${@:2}"; else "${@:2}"; fi; }
mkdir -p "$T/h"
# modelo preso na CPU (14/11/2026: llama3.2 ficou 100% CPU depois de um teste com num_gpu 0 e cada bloco levou ~10× mais):
# para antes de pegar vaga, com o comando que resolve
CPU=$(ollama ps 2>/dev/null | awk 'NR>1 && /CPU/ {print $1}' | tr '\n' ' ')
[ -n "$CPU" ] && { echo "modelo carregado na CPU: $CPU— rode: ollama stop $CPU e capture de novo" >&2; exit 3; }
for b in $(cd "$K/blocos" && ls *.sh | sed 's/\.sh$//'); do
  # a vaga fica fora do HOME temporário (a fila mora em ~/.cache do usuário de verdade)
  ( cd "$T/h" && vaga "$b" env HOME="$T/h" OLLAMA_MODELS="${OLLAMA_MODELS:-}" timeout 900 bash "$K/blocos/$b.sh" < /dev/null ) 2>&1 \
    | sed -E 's/\x1b\[[0-9;?]*[a-zA-Z]//g' | tr -d '\r' | sed "s#$T/h#~#g; s#$T#/tmp#g; s#$HOME#~#g" | cat -s > "$T/$b.txt"
  RC=${PIPESTATUS[0]}
  [ "$RC" = 75 ] && { echo "$b: GPU ocupada além da espera (fila-vaga saiu 75); saidas/ não foi mexida, rode de novo" >&2; exit 75; }
  mv "$T/$b.txt" "$K/saidas/$b.txt"
  echo "$b: $(wc -l < "$K/saidas/$b.txt") linhas"
done
