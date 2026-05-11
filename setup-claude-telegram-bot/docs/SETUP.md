# SETUP.md — 수동 셋업 fallback

스킬 자동 흐름이 실패하거나 (권한 문제 · 스킬 미지원 환경 등) Claude Code 없이 셋업하고 싶을 때.

## 0. 사전 준비

```bash
# Homebrew (없으면 설치)
which brew || /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# tmux + bun
brew install tmux oven-sh/bun/bun

# Claude Code (없으면 https://claude.com/download)
which claude || echo "Claude Code 설치 필요"
```

## 1. BotFather 에서 봇 생성

1. Telegram 앱 → `@BotFather` 검색 → 대화 시작
2. `/newbot` → 봇 이름 입력 (예: "Yang Dev Bot") → username 입력 (예: `yang_dev_bot`)
3. **토큰 복사** — `123456789:ABCdef...` 같은 형식. 노출 금지!

## 2. 상태 디렉토리 + 토큰 저장

기본 봇:
```bash
mkdir -p ~/.claude/channels/telegram
cat > ~/.claude/channels/telegram/.env <<'EOF'
TELEGRAM_BOT_TOKEN=<여기에 토큰 붙여넣기>
EOF
chmod 600 ~/.claude/channels/telegram/.env
```

Named 봇 (예: yang-dev):
```bash
mkdir -p ~/.claude/channels/telegram-yang-dev
cat > ~/.claude/channels/telegram-yang-dev/.env <<'EOF'
TELEGRAM_BOT_TOKEN=<토큰>
EOF
chmod 600 ~/.claude/channels/telegram-yang-dev/.env
```

## 3. 스크립트 위치 확인 (자체 패키지 — 복사 X)

스크립트는 스킬 폴더 안에 그대로 있음. 직접 호출:

```bash
SKILL=~/.claude/skills/setup-claude-telegram-bot
ls -la "$SKILL/scripts/"   # start-telegram-channel.sh, promote-pending.sh, cleanup-bot.sh
```

## 4. tmux 세션 spawn

```bash
SKILL=~/.claude/skills/setup-claude-telegram-bot

# 봇 (이름 필수, default = "claude")
"$SKILL/scripts/start-telegram-channel.sh" yang-dev
```

성공하면 다음 출력:
```
Started tmux session: claude-telegram
  State dir   : ~/.claude/channels/telegram
  Working dir : ~/
Attach: tmux attach -t claude-telegram
```

## 5. 첫 페어링

1. **텔레그램 앱** → BotFather 가 알려준 봇 username 검색 → `/start` 메시지 보내기
2. 봇이 6자리 pairing code 응답
3. **터미널** → tmux 세션 attach: `tmux attach -t claude-telegram`
4. Claude Code 안에서:
   ```
   /telegram:access pair <6자리 코드>
   /telegram:access policy allowlist
   ```
5. 다시 텔레그램에서 메시지 → 정상 처리되면 성공
6. tmux detach: `Ctrl+b` 누른 후 `d`

## 6. (선택) 재부팅 자동시작

```bash
# LaunchAgent 템플릿 변수 치환
USER="$(whoami)"
LABEL="com.$USER.claude-telegram"

sed -e "s|{{LABEL}}|$LABEL|g" \
    -e "s|{{SCRIPT_PATH}}|$HOME/.claude/skills/setup-claude-telegram-bot/scripts/start-telegram-channel.sh|g" \
    -e "s|{{BOT_NAME}}||g" \
    -e "s|{{HOME}}|$HOME|g" \
    assets/launchd-template.plist > ~/Library/LaunchAgents/$LABEL.plist

# 등록 + 시작
launchctl load -w ~/Library/LaunchAgents/$LABEL.plist
launchctl start $LABEL
```

검증:
```bash
launchctl list | grep claude-telegram
tail /tmp/$LABEL.out.log /tmp/$LABEL.err.log
```

## 7. 헬스체크

```bash
# tmux 세션 살아있는지
tmux ls | grep claude-telegram

# Channels plugin 응답 확인 (text input → output 흐름)
# 텔레그램에서 "ping" 보내면 봇이 응답해야 함

# 토큰 권한 확인 (chmod 600 이어야 함)
ls -la ~/.claude/channels/telegram/.env
```

## 트러블슈팅

| 증상 | 대응 |
|---|---|
| `tmux has-session` 매번 fail | 세션 이름 충돌 — 다른 BOT_NAME 으로 재실행 |
| 봇이 메시지 응답 X | tmux attach → Channels plugin 로딩 메시지 확인 / `/plugin install telegram@claude-plugins-official` |
| LaunchAgent 안 뜸 | `launchctl list \| grep telegram` · `tail /tmp/<label>.err.log` |
| 권한 에러 | macOS Settings → Privacy & Security → Full Disk Access 에 tmux/terminal 추가 |
| 토큰 잘못 입력 | `.env` 수정 → 세션 kill (`tmux kill-session -t claude-<name>`) → 스크립트 재실행 |

## 보안

- **봇 토큰 = 누구나 봇을 조작할 수 있는 키**. `.env` 외 어디에도 두지 말 것 (chmod 600 필수)
- **`/telegram:access policy`**: 항상 `allowlist` 모드. `public` 절대 금지
- 첫 페어링 후 `/telegram:access list` 로 누가 허용됐는지 확인 습관
