#!/usr/bin/env bash
# Copy canonical skill into the marketplace plugin bundle (release-time only).
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SRC="${ROOT}/.claude/skills/ros2-doctor"
DEST="${ROOT}/plugins/ros2-doctor/skills/ros2-doctor"

if [[ ! -d "${SRC}" ]]; then
  echo "error: canonical skill not found at ${SRC}" >&2
  exit 1
fi

rm -rf "${DEST}"
mkdir -p "$(dirname "${DEST}")"
cp -R "${SRC}" "${DEST}"
echo "Synced ${SRC} -> ${DEST}"
