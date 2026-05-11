# MULTI_BOT.md — 한 사용자가 여러 봇 운영

## 시나리오

- `yang-dev` — 일상 dev 작업 (작업 디렉토리 = `~/Development/yang-dev/`)
- `yang-asset` — 자산/투자 관련 봇 (`~/Development/yang-asset/`)
- `yang-family` — 가족 일정 / 노트 봇

각 봇은 **다른 BotFather 토큰 + 다른 tmux 세션 + 다른 상태 디렉토리** 로 완전 분리. 서로 영향 없음.

## 셋업 (각 봇마다)

각 봇마다 setup-claude-telegram-bot 스킬을 다시 호출. 봇 이름만 바꾸면 자동 분리:

```
"setup-claude-telegram-bot 스킬 — 봇 이름 yang-asset 로 실행해줘"
```

스킬이 자동으로 다음을 분리:
| 자원 | 기본 봇 (이름 없음) | yang-asset |
|---|---|---|
| tmux 세션 | `claude-telegram` | `claude-asset` (또는 `claude-yang-asset`) |
| 상태 디렉토리 | `~/.claude/channels/telegram/` | `~/.claude/channels/telegram-yang-asset/` |
| `.env` 토큰 | `<dir>/.env` | `<dir>/.env` (다른 토큰) |
| LaunchAgent label | `com.<user>.claude-telegram` | `com.<user>.claude-telegram-yang-asset` |
| 작업 디렉토리 | `~/` | `~/Development/yang-asset/` (있으면) |

## 봇 별 컨텍스트 분리

각 봇의 작업 디렉토리에 자체 `CLAUDE.md` / `TODO.md` / `MEMORY.md` 두면 봇별로 다른 페르소나 / 컨텍스트로 동작:

```
~/Development/yang-asset/
├── CLAUDE.md       # "이 봇은 자산 관리 전용. 매수/매도 결정 시 항상 ..."
├── TODO.md         # 자산 관련 작업 트래커
└── MEMORY.md       # 자산 관련 세션 컨텍스트
```

봇이 시작될 때 그 디렉토리에서 시작하므로 자동으로 그 컨텍스트 적용.

## 운영 명령어

| 작업 | 명령 |
|---|---|
| 봇 시작 (수동) | `start-telegram-channel.sh <name>` |
| 봇 세션 진입 | `tmux attach -t claude-<name>` |
| 봇 detach | `Ctrl+b` 후 `d` |
| 봇 종료 | `tmux kill-session -t claude-<name>` |
| 모든 봇 세션 보기 | `tmux ls \| grep claude-` |
| LaunchAgent 다시 시작 | `launchctl kickstart -k gui/$(id -u)/com.<user>.claude-telegram-<name>` |

## 토큰 / 권한 관리

각 봇마다:
- 별도 BotFather 토큰 (한 BotFather 계정으로 봇 여러 개 생성 가능)
- 별도 `.env` 파일 (`chmod 600`)
- 정책은 봇별로 독립된 `access.json` 에 — `allowlist` 모드 + 자기만 추가 권장

## 페어링 — promote-pending.sh

이 스킬은 **항상 named state dir** 사용 (single bot 이라도 동일). plugin 의 `/telegram:access` 슬래시 명령은 default state dir 만 보기 때문에, 페어링 통과는 항상 헬퍼로:

```bash
~/.claude/skills/setup-claude-telegram-bot/scripts/promote-pending.sh <bot_name> <code>
```

(스킬 폴더 안 자체 패키지 — 외부 위치 복사 X)

내부 동작:
1. `~/.claude/channels/telegram-<bot_name>/access.json` 찾기
2. `pending["<code>"].senderId` 를 `allowFrom` 에 추가
3. `dmPolicy` 를 `"allowlist"` 로 변경
4. `pending` 에서 그 항목 삭제
5. 봇 server 가 변경 감지 → 즉시 적용

> 💡 **사용자는 보통 직접 호출 안 함** — Claude Code 한테 "코드 ABC123 통과시켜줘" 하면 Claude 가 자동 호출.

## 봇 끄기 / 삭제

### 권장: cleanup-bot.sh 헬퍼

Claude Code 한테:
```
"<name> 봇 삭제해줘"
```

Claude 가 `cleanup-bot.sh <name> --yes` 자동 호출. 한 방에 정리:
- tmux 세션 종료 (`claude-<name>`)
- LaunchAgent unload + plist 제거
- 상태 디렉토리 (`~/.claude/channels/telegram-<name>/`) 삭제 — **토큰 + access.json 포함**

### 수동 (셸에서 직접)

```bash
SKILL=~/.claude/skills/setup-claude-telegram-bot
"$SKILL/scripts/cleanup-bot.sh" <name>           # 확인 prompt 후 삭제
"$SKILL/scripts/cleanup-bot.sh" <name> --yes     # prompt 없이
```

### BotFather 의 봇 자체

cleanup-bot.sh 는 로컬 자원만 제거. BotFather 의 봇은 별도 — 텔레그램 @BotFather → `/deletebot` → `@<bot_username>`

## 비용 / 리소스 고려

- 봇마다 별도 tmux + claude code 프로세스 → 메모리 ~500MB ~ 1GB / 봇
- Mac mini M4 Pro 64GB 면 봇 10개 + 다른 작업 동시 OK
- 가벼운 노트북이면 봇 2~3개로 제한 권장
