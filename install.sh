#!/usr/bin/env bash
# Symlink sci-journal-selection into Cursor / Codex / Claude skill directories.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")" && pwd)"
SRC="${ROOT}/skills/sci-journal-selection"

if [[ ! -f "${SRC}/SKILL.md" ]]; then
  echo "error: missing ${SRC}/SKILL.md" >&2
  exit 1
fi

usage() {
  cat <<USAGE
Usage: $0 [--project DIR] [--user] [--copy]

  --project DIR   Symlink into DIR/.agents|/.cursor|/.claude|/.codex /skills/
  --user          Symlink into ~/.agents|~/.cursor|~/.claude|~/.codex /skills/
  --copy          Copy instead of symlink
  (default: --project .)
USAGE
}

MODE="project"
TARGET="."
COPY=0

while [[ $# -gt 0 ]]; do
  case "$1" in
    --project) MODE="project"; TARGET="${2:-.}"; shift 2 ;;
    --user) MODE="user"; shift ;;
    --copy) COPY=1; shift ;;
    -h|--help) usage; exit 0 ;;
    *) echo "unknown arg: $1" >&2; usage; exit 1 ;;
  esac
done

link_one() {
  local dest_parent="$1"
  mkdir -p "${dest_parent}"
  local dest="${dest_parent}/sci-journal-selection"
  if [[ "${COPY}" -eq 1 ]]; then
    rm -rf "${dest}"
    cp -R "${SRC}" "${dest}"
    echo "copied -> ${dest}"
  else
    ln -sfn "${SRC}" "${dest}"
    echo "linked -> ${dest}"
  fi
}

if [[ "${MODE}" == "user" ]]; then
  BASE="${HOME}"
  link_one "${BASE}/.agents/skills"
  link_one "${BASE}/.cursor/skills"
  link_one "${BASE}/.claude/skills"
  link_one "${BASE}/.codex/skills"
else
  BASE="$(cd "${TARGET}" && pwd)"
  link_one "${BASE}/.agents/skills"
  link_one "${BASE}/.cursor/skills"
  link_one "${BASE}/.claude/skills"
  link_one "${BASE}/.codex/skills"
fi

echo "done. Skill name: sci-journal-selection"
