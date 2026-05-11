#!/usr/bin/env bash
# cleanup-bot.sh — 한 봇의 로컬 자원 일괄 삭제 (idempotent)
#
# 삭제 대상:
#   1. tmux 세션 (claude-<name>)
#   2. LaunchAgent (~/Library/LaunchAgents/com.<user>.claude-telegram-<name>.plist)
#   3. 상태 디렉토리 (~/.claude/channels/telegram-<name>/) — 토큰·access.json 포함
#
# Usage:
#   cleanup-bot.sh <name>           # 확인 prompt 후 삭제
#   cleanup-bot.sh <name> --yes     # prompt 없이 삭제 (자동화용)
#
# 안전:
#   - 토큰을 다른 곳에 백업해뒀는지 사용자가 미리 확인 권장 (.env 사라짐)
#   - BotFather 의 봇 자체는 삭제 안 함 (사용자가 별도로 /deletebot)

set -uo pipefail

if [[ $# -lt 1 ]]; then
  echo "Usage: $(basename "$0") <name> [--yes]" >&2
  echo "" >&2
  echo "예: $(basename "$0") gd_mbp_bot" >&2
  exit 1
fi

BOT_NAME="$1"
ASSUME_YES="${2:-}"

USER_NAME="$(whoami)"
SESSION="claude-$BOT_NAME"
STATE_DIR="$HOME/.claude/channels/telegram-$BOT_NAME"
LAUNCHD_LABEL="com.$USER_NAME.claude-telegram-$BOT_NAME"
LAUNCHD_PLIST="$HOME/Library/LaunchAgents/$LAUNCHD_LABEL.plist"

# 검사: 어떤 자원이 살아있나
echo "── 봇 '$BOT_NAME' 의 로컬 자원 ──"
HAS_SESSION=false
HAS_LAUNCHD=false
HAS_STATE=false

if /opt/homebrew/bin/tmux has-session -t "$SESSION" 2>/dev/null \
  || tmux has-session -t "$SESSION" 2>/dev/null; then
  echo "  • tmux 세션: $SESSION (살아있음)"
  HAS_SESSION=true
fi
if [[ -f "$LAUNCHD_PLIST" ]]; then
  echo "  • LaunchAgent: $LAUNCHD_LABEL"
  HAS_LAUNCHD=true
fi
if [[ -d "$STATE_DIR" ]]; then
  size=$(du -sh "$STATE_DIR" 2>/dev/null | cut -f1)
  echo "  • State dir: $STATE_DIR ($size)"
  echo "    └─ 안 내용: $(ls "$STATE_DIR" | tr '\n' ' ')"
  HAS_STATE=true
fi

if ! $HAS_SESSION && ! $HAS_LAUNCHD && ! $HAS_STATE; then
  echo "  (자원 없음 — 이미 정리됨 또는 봇 이름 오타)"
  exit 0
fi

echo ""
if [[ "$ASSUME_YES" != "--yes" ]]; then
  read -r -p "위 자원을 모두 삭제할까요? (y/N) " yn
  case "$yn" in
    [Yy]*) ;;
    *) echo "취소"; exit 0 ;;
  esac
fi

echo ""
echo "── 삭제 실행 ──"

# 1. tmux 세션 종료
if $HAS_SESSION; then
  if /opt/homebrew/bin/tmux kill-session -t "$SESSION" 2>/dev/null \
    || tmux kill-session -t "$SESSION" 2>/dev/null; then
    echo "  ✅ tmux 세션 종료: $SESSION"
  else
    echo "  ⚠️  tmux 세션 종료 실패 (수동: tmux kill-session -t $SESSION)"
  fi
fi

# 2. LaunchAgent
if $HAS_LAUNCHD; then
  launchctl unload -w "$LAUNCHD_PLIST" 2>/dev/null || true
  rm -f "$LAUNCHD_PLIST"
  echo "  ✅ LaunchAgent 제거: $LAUNCHD_LABEL"
fi

# 3. 상태 디렉토리 (토큰 포함 — 사용자 동의로만)
if $HAS_STATE; then
  rm -rf "$STATE_DIR"
  echo "  ✅ State dir 삭제 (토큰·access.json 포함): $STATE_DIR"
fi

echo ""
echo "── 완료 ──"
echo "  추가 정리 (선택):"
echo "    • BotFather 에서 봇 자체 삭제: 텔레그램 @BotFather → /deletebot → '@<bot_username>'"
echo "    • 스킬 자체를 삭제하려면 ~/.claude/skills/setup-claude-telegram-bot/ 폴더 제거"
