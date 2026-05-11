---
name: setup-claude-telegram-bot
description: Mac 사용자의 Claude Code 와 Telegram 봇을 양방향 연결해주는 셋업 스킬. 사용자는 폰과 Claude Code 채팅창만 사용 — 터미널 안 엶. Claude 가 모든 쉘 명령(BotFather 토큰 받기·tmux 세션 spawn·plugin 설치·페어링 통과·LaunchAgent 등록)을 대신 실행. 사용 시점 — "텔레그램 봇 만들어줘", "claude code 텔레그램 연결", "내 폰에서 claude code 쓰고 싶어", "claude bot 자동 시작", "봇 삭제해줘" 등을 언급할 때. macOS 한정 (LaunchAgent 사용). 항상 named state dir 사용 (multi-bot ready by default).
---

> **출처**: 작성 gd.on (B3RYS) · 2026-05-10. 라이선스 MIT (자유 사용·수정·재배포)

# setup-claude-telegram-bot

Mac 의 Claude Code 를 Telegram 으로 양방향 연결. **사용자는 폰 / Claude Code 채팅창만** — 터미널 X.

## 핵심 디자인

- **Conversational** — 사용자가 "봇 셋업해줘" 하면 Claude 가 자체적으로 모든 쉘 명령 실행. 사용자는 BotFather 와 대화 + 페어링 코드 알려주는 정도만.
- **Multi-bot by default** — 처음부터 named state dir (`telegram-<name>/`) 사용. 봇 1개만 쓰더라도 동일. 나중에 봇 추가해도 마이그레이션 없음.
- **항상 promote-pending.sh** — `/telegram:access` 슬래시 명령은 plugin 의 한계 (default state dir 만 봄) 로 미사용. Claude 가 helper 호출.

## 동작 흐름 (사용자 ↔ Claude 대화)

```
사용자 (Claude Code 에): "텔레그램 봇 셋업해줘"
   ↓
Claude:
   1. 사전 준비 검증 (brew/tmux/bun/claude). 빠진 거 있으면 사용자에게 안내
   2. "봇 이름 정하세요 (예: dev, mbp). 단일 봇이어도 의미 있는 이름 권장." 물어봄
   3. "BotFather (@BotFather) 와 다음 단계 진행해주세요" 안내:
        ① /newbot
        ② Bot name 입력 (사람용 이름, 예: "Dev Bot")
        ③ Bot username 입력 (`bot` 또는 `_bot` 으로 끝, 예: my_dev_bot)
        ④ 받은 토큰을 알려달라
   ↓
사용자: "토큰: 1234567890:ABC..."
   ↓
Claude:
   4. 토큰 안전 저장 (~/.claude/channels/telegram-<name>/.env, chmod 600)
   5. Telegram getMe API 호출 → 봇 username + URL 자동 출력
       "✅ 봇 확인됨: @my_dev_bot · 링크: https://t.me/my_dev_bot"
   6. 스킬 안 scripts/ 의 start-telegram-channel.sh 호출 (자체 패키지 — 외부 복사 X)
   7. tmux 세션 spawn (claude-<name>)
   8. 자동으로 send-keys 실행:
        - Trust 폴더 prompt → Enter
        - /plugin install telegram@claude-plugins-official → Enter → Enter (user-scope)
        - /reload-plugins → Enter
   9. "이제 폰에서 https://t.me/my_dev_bot 열어 두 번 메시지 보내주세요:
        ① /start (안내문만 옴, 정상)
        ② 'hi' 같은 아무 메시지 → 6자리 페어링 코드 응답
       그 6자리 코드 알려주세요"
   ↓
사용자: "코드: ABC123"
   ↓
Claude:
   10. promote-pending.sh <name> ABC123 호출 → access.json 갱신
   11. "재부팅 시 자동 시작 등록할까요? (Y/n)" 물어봄
   ↓
사용자: "Y"
   ↓
Claude:
   12. LaunchAgent plist 생성 + launchctl load
   13. "✅ 셋업 완료. 폰에서 봇한테 메시지 보내보세요."
```

## 입력 (Claude 가 사용자에게 물어봄)

```
1. 봇 이름 (필수, 비우면 default = "claude")
   → 예: dev, mbp, asset, family
   → 단일 봇이라도 의미 있는 이름 권장 (다른 봇 추가 시 모호함 회피)

2. BotFather 단계 (사용자가 텔레그램 앱에서 손으로):
   ① @BotFather 검색 → /newbot
   ② "Bot name" 입력 (예: "Dev Bot") — 사람에게 보일 이름
   ③ "Bot username" 입력 (예: my_dev_bot) — 반드시 'bot' 또는 '_bot' 으로 끝
   ④ BotFather 가 토큰 + URL 응답 → 토큰을 Claude 에게 알려줌

3. 작업 디렉토리 (선택)
   → Claude 가 시작할 폴더 — CLAUDE.md/TODO.md/MEMORY.md 그 디렉토리꺼 적용
   → 우선순위: 사용자 명시 입력 > ~/Development/<bot_name> > $HOME

4. 재부팅 자동시작? (Y/n)
   → Y → LaunchAgent 등록, 다음 reboot 부터 봇 자동 시작
```

## 단계별 자동 실행 (Claude 가 셸로 처리)

### Step 1 — 사전 준비 검증

```bash
[[ "$(uname)" == "Darwin" ]] || { echo "macOS 한정"; exit 1; }
command -v tmux  >/dev/null || { echo "ERROR: tmux 필요. brew install tmux 또는 https://brew.sh"; exit 1; }
command -v bun   >/dev/null || { echo "ERROR: bun 필요. brew install oven-sh/bun/bun 또는 curl -fsSL https://bun.sh/install | bash"; exit 1; }
command -v claude >/dev/null || { echo "ERROR: Claude Code 설치 필요: https://claude.com/download"; exit 1; }
```

빠진 거 있으면 Claude 가 사용자에게 알리고 설치 안내.

### Step 2 — 토큰 안전 저장 + 봇 정보 자동 조회

```bash
NAME="${BOT_NAME:-claude}"
STATE_DIR="$HOME/.claude/channels/telegram-$NAME"
mkdir -p "$STATE_DIR"
echo "TELEGRAM_BOT_TOKEN=<TOKEN>" > "$STATE_DIR/.env"
chmod 600 "$STATE_DIR/.env"

# 봇 username + URL 자동 출력 (사용자가 BotFather 메시지 거꾸로 안 봐도 됨)
USERNAME=$(curl -s "https://api.telegram.org/bot<TOKEN>/getMe" \
  | python3 -c "import json,sys; print(json.load(sys.stdin)['result']['username'])")
echo "✅ 봇: @$USERNAME · 링크: https://t.me/$USERNAME"
```

> **민감 정보 보호**: 토큰은 절대 커밋/출력/공유 X. `.env` 만, chmod 600 만.

### Step 3 — tmux 세션 spawn + plugin 자동 설치

> **자체 패키지** — 스킬 폴더 안 스크립트 직접 호출, 외부 복사 X.

```bash
SKILL_DIR="$HOME/.claude/skills/setup-claude-telegram-bot"

"$SKILL_DIR/scripts/start-telegram-channel.sh" "$NAME"
sleep 3
# Trust prompt 통과
tmux send-keys -t "claude-$NAME" Enter
sleep 3
# Plugin install
tmux send-keys -t "claude-$NAME" "/plugin install telegram@claude-plugins-official" Enter
sleep 8
tmux send-keys -t "claude-$NAME" Enter   # user-scope 확정
sleep 5
tmux send-keys -t "claude-$NAME" "/reload-plugins" Enter
sleep 3
```

### Step 4 — 페어링 (사용자 폰 + Claude 가 대신 호출)

Claude 가 안내:
```
폰에서 https://t.me/<username> 열기 → 두 번 메시지:
  ① /start  → 안내문만 옴 (정상)
  ② 아무 메시지 (예: 'hi') → 6자리 페어링 코드 응답

그 6자리 코드 알려주세요.
```

사용자가 코드 알려주면 Claude 가 자동 실행:
```bash
"$SKILL_DIR/scripts/promote-pending.sh" "$NAME" "<코드>"
```

### Step 5 — (선택) 재부팅 자동시작

```bash
USER_NAME="$(whoami)"
LABEL="com.$USER_NAME.claude-telegram-$NAME"
SCRIPT_PATH="$SKILL_DIR/scripts/start-telegram-channel.sh"

sed -e "s|{{LABEL}}|$LABEL|g" \
    -e "s|{{SCRIPT_PATH}}|$SCRIPT_PATH|g" \
    -e "s|{{HOME}}|$HOME|g" \
    -e "s|{{BOT_NAME}}|$NAME|g" \
    "$SKILL_DIR/assets/launchd-template.plist" > "$HOME/Library/LaunchAgents/$LABEL.plist"
launchctl load -w "$HOME/Library/LaunchAgents/$LABEL.plist"
```

### Step 7 — 헬스체크

```bash
tmux ls | grep "claude-$NAME"        # 세션 살아있나
[ -f "$STATE_DIR/access.json" ]      # 페어링 통과됐나
launchctl list | grep "$LABEL"       # LaunchAgent (선택했으면)
```

## 봇 삭제 / 다른 이름으로 재셋업

사용자: "X 봇 지워줘"
   →
Claude 가 cleanup-bot.sh 호출:
```bash
"$SKILL_DIR/scripts/cleanup-bot.sh" "<name>" --yes
```

삭제 대상:
- tmux 세션 (`claude-<name>`)
- LaunchAgent (`com.<user>.claude-telegram-<name>.plist`)
- 상태 디렉토리 (`~/.claude/channels/telegram-<name>/` — 토큰 + access.json 포함)

추가 정리 (선택, Claude 가 안내만):
- BotFather 에서 봇 자체 삭제: 텔레그램 @BotFather → /deletebot → @<bot_username>

## 멀티 봇 운영

같은 머신에서 봇 여러 개 동시 운영:
- 각 봇마다 다른 이름으로 위 흐름 반복
- tmux session / state dir / LaunchAgent label / 작업 디렉토리 자동 분리
- 각 봇은 다른 BotFather 토큰 + 다른 .env

자세한 패턴: `docs/MULTI_BOT.md`

## 트러블슈팅

| 증상 | 원인 / Claude 가 처리 |
|---|---|
| `/start` 보냈는데 코드 안 옴 | 정상 — 추가 메시지 한 번 더 보내야 코드 옴 |
| `Bun not installed` | brew 또는 curl 으로 자동 설치 안내 |
| 페어링 통과 안 됨 (메시지 무응답) | `cat ~/.claude/channels/telegram-<name>/access.json` 확인 — `allowFrom` 에 본인 ID 있나 |
| 봇 채팅 못 찾음 | Claude 가 출력한 https://t.me/<username> 클릭 |
| 재부팅 후 봇 안 살아남 | `launchctl list \| grep claude-telegram` — 등록됐나 확인 |

## 보안

- **봇 토큰 = 누구나 봇 조작할 수 있는 키**. `.env` 만, `chmod 600` 만, **절대** git/clipboard/log 노출 X
- **dmPolicy = `allowlist`** — `allowFrom` 에 본인만. `public` 모드 절대 사용 금지
- 첫 페어링 후 `cat access.json` 으로 누가 허용됐는지 확인 권장

## 파일 목록

```
setup-claude-telegram-bot/
├── SKILL.md              # (이 파일)
├── README.md             # 사용자용 짧은 설명 (10분 빠른 시작)
├── scripts/              # 실행 가능 스크립트 (Anthropic Skills 표준)
│   ├── start-telegram-channel.sh   # tmux 세션 spawn
│   ├── promote-pending.sh          # 페어링 코드 → access.json 적용
│   └── cleanup-bot.sh              # 봇 자원 일괄 삭제
├── assets/               # 정적 파일 (템플릿 등, 실행 X)
│   └── launchd-template.plist      # LaunchAgent 템플릿
└── docs/
    ├── SETUP.md          # 수동 셋업 fallback
    └── MULTI_BOT.md      # 멀티 봇 패턴
```

> **자체 패키지 디자인** — 모든 실행 파일이 스킬 폴더 안. `~/.local/bin/` 등 외부 위치에 복사 X. 스킬 폴더 삭제 = 모든 자원 정리.
