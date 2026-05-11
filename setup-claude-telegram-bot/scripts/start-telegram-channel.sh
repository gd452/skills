#!/usr/bin/env bash
# Start Claude Code Telegram Channel session in tmux.
#
# 디자인 원칙: 항상 named state dir (multi-bot ready by default).
#   봇 1개 운영 시에도 명시적 이름 사용 → 봇 추가 시 migration 없음.
#
# Usage:
#   start-telegram-channel.sh <name>         # 봇 이름 필수 (예: dev, mbp, asset)
#   start-telegram-channel.sh                # 이름 비우면 default = "claude"
#
# 자원 매핑 (name 별):
#   - tmux session   : claude-<name>
#   - State dir      : ~/.claude/channels/telegram-<name>/
#   - Token          : ~/.claude/channels/telegram-<name>/.env
#   - Working dir    : 우선순위 — env WORKDIR > ~/Development/<name>/ > $HOME
#
# 페어링:
#   - 항상 promote-pending.sh <name> <code> 사용 (slash 명령은 plugin 한계로 미지원)
#
# 환경변수:
#   WORKDIR — Claude Code 가 시작할 디렉토리 명시 지정
#             예: WORKDIR=~/Development/myapp ./start-telegram-channel.sh dev
#
# Idempotent: if the target session already exists, prints attach hint and exits 0.
# Safe to call from launchd at every login.

set -euo pipefail

BOT_NAME="${1:-claude}"   # 비우면 default = "claude" (multi-bot ready)
PLUGIN="telegram@claude-plugins-official"

SESSION_NAME="claude-$BOT_NAME"
STATE_DIR="$HOME/.claude/channels/telegram-$BOT_NAME"

# WORKDIR 결정 — 우선순위:
#   1) 환경변수 WORKDIR (사용자가 명시적으로 지정)
#   2) ~/Development/$BOT_NAME (있으면)
#   3) $HOME (fallback)
if [[ -n "${WORKDIR:-}" ]]; then
  : # 그대로 사용
elif [[ -n "$BOT_NAME" && -d "$HOME/Development/$BOT_NAME" ]]; then
  WORKDIR="$HOME/Development/$BOT_NAME"
else
  WORKDIR="$HOME"
fi
if [[ ! -d "$WORKDIR" ]]; then
  echo "ERROR: WORKDIR '$WORKDIR' 디렉토리가 없습니다."
  exit 1
fi

PLUGIN_ENV="$STATE_DIR/.env"

# ─── Pre-flight ───────────────────────────────────────────────────────────

if [[ ! -f "$PLUGIN_ENV" ]]; then
  echo "ERROR: $PLUGIN_ENV missing. Plugin token not configured."
  echo ""
  echo "First-time setup:"
  echo "  1. BotFather: /newbot → save the token"
  echo "  2. mkdir -p $STATE_DIR"
  echo "  3. echo 'TELEGRAM_BOT_TOKEN=<token>' > $PLUGIN_ENV"
  echo "  4. chmod 600 $PLUGIN_ENV"
  echo "  5. Re-run this script"
  exit 1
fi

if ! command -v tmux >/dev/null 2>&1; then
  echo "ERROR: tmux not installed."
  if command -v brew >/dev/null 2>&1; then
    echo "  brew install tmux"
  else
    echo "  Homebrew (https://brew.sh) 또는 MacPorts 로 설치 필요."
  fi
  exit 1
fi

if ! command -v bun >/dev/null 2>&1; then
  echo "ERROR: Bun not installed. Channels Telegram plugin requires Bun."
  if command -v brew >/dev/null 2>&1; then
    echo "  brew install oven-sh/bun/bun"
  else
    echo "  Homebrew 가 없으면: curl -fsSL https://bun.sh/install | bash"
    echo "  설치 후 ~/.bun/bin 을 PATH 에 추가해야 함."
  fi
  exit 1
fi

if command -v claude >/dev/null 2>&1; then
  CLAUDE_BIN="$(command -v claude)"
else
  CLAUDE_BIN="$HOME/.local/bin/claude"
  if [[ ! -x "$CLAUDE_BIN" ]]; then
    echo "ERROR: claude binary not found"
    exit 1
  fi
fi

# ─── Idempotent: skip if session already exists ───────────────────────────

if tmux has-session -t "$SESSION_NAME" 2>/dev/null; then
  echo "Session '$SESSION_NAME' already running."
  echo "Attach: tmux attach -t $SESSION_NAME"
  exit 0
fi

# ─── Spawn ────────────────────────────────────────────────────────────────

# Quote-safe inline command for tmux: use printf %q on paths.
# TELEGRAM_STATE_DIR tells the channels plugin which state dir to use.
INNER_CMD=$(printf 'TELEGRAM_STATE_DIR=%q %q --channels plugin:%s' \
  "$STATE_DIR" "$CLAUDE_BIN" "$PLUGIN")

tmux new-session -d -s "$SESSION_NAME" -c "$WORKDIR" "$INNER_CMD"

echo "Started tmux session: $SESSION_NAME"
echo "  State dir   : $STATE_DIR"
echo "  Working dir : $WORKDIR"
echo "Attach: tmux attach -t $SESSION_NAME"

# ─── First-time pairing hint ──────────────────────────────────────────────

if [[ ! -s "$STATE_DIR/access.json" ]] \
  || ! grep -q '"allowFrom"' "$STATE_DIR/access.json" 2>/dev/null; then
  echo ""
  echo "─── 첫 셋업 — 다음 단계 ───────────────────────────────────────"
  echo ""
  echo "[A] tmux 세션 attach (새 터미널 권장):"
  echo "    tmux attach -t $SESSION_NAME"
  echo ""
  echo "[B] 안에서 trust 폴더 prompt 가 뜨면 'Enter' 로 trust 선택"
  echo ""
  echo "[C] plugin 설치 + 활성화 (한 줄씩 입력):"
  echo "    /plugin install $PLUGIN"
  echo "    (user-scope 선택, Enter)"
  echo "    /reload-plugins"
  echo ""
  echo "[D] 텔레그램 폰에서 봇 채팅 열기:"
  if [[ -n "${TELEGRAM_BOT_USERNAME:-}" ]]; then
    echo "    https://t.me/$TELEGRAM_BOT_USERNAME"
  else
    echo "    @<your-bot-username>  # BotFather 가 알려준 username"
  fi
  echo ""
  echo "[E] 봇에 두 번 메시지:"
  echo "    1) /start  → 사용 안내문 옴 (정상)"
  echo "    2) 'hi' (또는 아무 메시지) → 6자리 페어링 코드 응답"
  echo ""
  echo "[F] 페어링 통과 (Claude Code 한테 \"코드 <code> 통과시켜줘\" 또는 셸에서):"
  echo "    ~/.claude/skills/setup-claude-telegram-bot/scripts/promote-pending.sh '$BOT_NAME' '<코드>'"
  echo ""
  echo "[G] 다시 텔레그램 → 메시지 보내면 Claude 응답이 폰으로 도착 ✅"
fi
