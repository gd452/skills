#!/usr/bin/env bash
# promote-pending.sh — multi-bot 환경에서 페어링 코드를 access.json 에 직접 적용
#
# 왜 필요한가:
#   plugin 의 /telegram:access 슬래시 명령은 default state dir
#   (~/.claude/channels/telegram/) 만 본다. 봇 이름을 단 named state dir
#   (~/.claude/channels/telegram-<name>/) 는 인식 못 함.
#   이 헬퍼가 그 한계를 우회 — 직접 access.json 편집.
#
# 사용법:
#   promote-pending.sh <bot_name> <pairing_code>
#
# 예:
#   promote-pending.sh gd_mbp_bot 9e143a
#
# 동작:
#   1) ~/.claude/channels/telegram-<bot_name>/access.json 찾기
#   2) pending["<code>"].senderId 를 allowFrom 에 추가
#   3) dmPolicy 를 "allowlist" 로 변경
#   4) pending 에서 그 항목 삭제
#   5) 봇 server 가 access.json 변경 감지 → 즉시 적용

set -euo pipefail

if [[ $# -ne 2 ]]; then
  cat >&2 <<EOF
Usage: $(basename "$0") <bot_name> <pairing_code>

예: $(basename "$0") gd_mbp_bot 9e143a

봇 이름이 "telegram" (default) 이면 이 헬퍼 대신 슬래시 명령 사용 가능:
  /telegram:access pair <code>
EOF
  exit 1
fi

BOT_NAME="$1"
CODE="$2"
ACCESS="$HOME/.claude/channels/telegram-$BOT_NAME/access.json"

if [[ ! -f "$ACCESS" ]]; then
  echo "ERROR: $ACCESS 가 없습니다." >&2
  echo "  봇이 한 번도 실행되지 않았거나 봇 이름이 틀렸을 수 있음." >&2
  exit 2
fi

python3 - "$ACCESS" "$CODE" <<'PYEOF'
import json, pathlib, sys

access_path = pathlib.Path(sys.argv[1])
code = sys.argv[2]

data = json.loads(access_path.read_text())
data.setdefault("pending", {})
data.setdefault("allowFrom", [])
data.setdefault("groups", {})

entry = data["pending"].pop(code, None)
if entry is None:
    print(f"❌ pending code '{code}' not found in {access_path}", file=sys.stderr)
    print(f"   현재 pending: {list(data['pending'].keys())}", file=sys.stderr)
    sys.exit(3)

sender = entry.get("senderId")
if not sender:
    print(f"❌ pending entry has no senderId: {entry}", file=sys.stderr)
    sys.exit(4)

if sender not in data["allowFrom"]:
    data["allowFrom"].append(sender)

data["dmPolicy"] = "allowlist"

access_path.write_text(json.dumps(data, indent=2))
print(f"✅ promoted senderId={sender} → allowFrom; dmPolicy → allowlist")
print(f"   파일: {access_path}")
print(f"   이제 텔레그램에서 그 봇한테 메시지 보내면 Claude 응답이 옴.")
PYEOF
