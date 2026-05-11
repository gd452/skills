# setup-claude-telegram-bot

[Claude Code](https://claude.com/claude-code) ↔ Telegram 봇을 양방향 연결하는 스킬. **사용자는 폰과 Claude Code 채팅창만** — 터미널 X.

> **결과 예시** — 폰에서 "오늘 PR 상태 알려줘" 메시지 → 노트북의 Claude Code 가 처리 → 답이 폰으로 도착.

---

## 핵심 디자인

- **Conversational** — Claude Code 한테 자연어로 부탁하면 Claude 가 모든 쉘 명령 자체 실행
- **Multi-bot ready by default** — 봇 1개만 쓰더라도 처음부터 봇 이름 부여. 나중에 추가해도 마이그레이션 X
- **터미널 강요 X** — 디버깅 / 직접 확인 원할 때만 `tmux attach`

---

## 빠른 시작 (10분, 따라하기)

### 0. 준비 (30초)

| 필요한 것 | 확인 |
|---|---|
| macOS | — |
| Claude Code 설치 + 로그인 | [claude.com/download](https://claude.com/download) |
| Telegram 앱 (폰) | — |

`brew` / `tmux` / `bun` 은 Claude 가 알아서 안내. (Homebrew 없는 사용자도 OK — `curl bun.sh/install` 대안 제시)

### 1. 봇 만들기 (텔레그램, 2분)

폰 텔레그램에서:
1. [@BotFather](https://t.me/BotFather) 검색 → 채팅 시작
2. `/newbot` 입력
3. **Bot name** 입력 (사람용 이름) — 예: `My Dev Bot`
4. **Bot username** 입력 — 반드시 `bot` 또는 `_bot` 으로 끝. 예: `my_dev_bot`
5. BotFather 가 토큰 (`1234567890:ABC...XYZ`) 응답 → **이 줄 복사**

### 2. Claude Code 한테 부탁 (1줄)

Claude Code 채팅창에:
```
"setup-claude-telegram-bot 스킬 실행해줘 — 봇 이름 dev, 토큰은 1234567890:ABC...XYZ"
```

(또는 슬래시: `/setup-claude-telegram-bot` 후 Claude 가 묻는 대로 답변)

Claude 가 자동으로 처리:
1. 사전조건 (`brew`/`tmux`/`bun`/`claude`) 검증 + 빠진 거 안내
2. 토큰 안전 저장 (`~/.claude/channels/telegram-dev/.env`, chmod 600)
3. **봇 정보 자동 조회** — `https://t.me/my_dev_bot` 링크 출력 (BotFather 메시지 다시 안 봐도 됨)
4. 시작 스크립트 + 헬퍼 (`start-telegram-channel.sh`, `promote-pending.sh`, `cleanup-bot.sh`) 배치
5. tmux 세션 (`claude-dev`) spawn + 자동으로 plugin install + reload
6. "이제 폰에서 메시지 보내라" 안내

### 3. 페어링 (5분)

#### A. Claude 가 출력한 링크로 봇 채팅 열기 (폰)

`https://t.me/<username>` 누르면 봇 채팅 바로 열림.

#### B. 봇한테 **두 번** 메시지 ⚠️ 한 번만 보내면 안 됨

| 단계 | 보내기 | 봇 응답 |
|---|---|---|
| ① | `/start` | 사용 안내문만 (페어링 코드 아님) |
| ② | `hi` (아무 메시지) | 6자리 페어링 코드 (예: `ABC123`) |

#### C. Claude 한테 코드 알려주기

Claude Code 채팅창에:
```
"코드: ABC123"
```

Claude 가 자동으로 `promote-pending.sh dev ABC123` 호출 → 페어링 통과.

### 4. 검증

폰에서 봇한테 "안녕" 보내기 → Claude 응답이 폰으로 오면 성공 ✅

### 5. 재부팅 자동시작 (선택)

스킬 마지막 단계에서 Claude 가 "재부팅 시 자동 시작 등록할까요? (Y/n)" 물어봄. `Y` 면 LaunchAgent 자동 등록 → 다음 reboot 부터 봇 살아남.

---

## 봇 삭제

Claude Code 채팅창에:
```
"dev 봇 삭제해줘"
```

Claude 가 `cleanup-bot.sh dev` 호출:
- tmux 세션 종료 (`claude-dev`)
- LaunchAgent 제거
- 상태 디렉토리 (`~/.claude/channels/telegram-dev/`) 삭제 — 토큰·access.json 포함

(BotFather 의 봇 자체는 별도 — 텔레그램 @BotFather → `/deletebot`)

## 멀티 봇 운영

봇 여러 개 (dev / asset / family) 분리 운영:
- 각 봇마다 다른 이름으로 위 흐름 반복
- 자원 모두 자동 분리 (tmux session / state dir / LaunchAgent / 작업 디렉토리)
- 각 봇은 다른 BotFather 토큰 + 다른 작업 컨텍스트

자세한 패턴: [docs/MULTI_BOT.md](./docs/MULTI_BOT.md)

---

## 자주 막히는 지점

| 증상 | 원인 / 대응 |
|---|---|
| `/start` 보냈는데 코드 안 옴 | 정상. **추가 메시지 한 번 더 보내야 코드 옴** (위 3-B ②) |
| `Bun not installed` | `brew install oven-sh/bun/bun` 또는 `curl -fsSL https://bun.sh/install \| bash` |
| `Homebrew not found` | https://brew.sh 가서 설치 후 재시도 |
| 봇 채팅 못 찾음 | Claude 가 출력한 `https://t.me/<username>` 클릭 (BotFather 메시지 거꾸로 안 봐도 됨) |
| 폰 메시지 보냈는데 응답 없음 | "봇 X 상태 확인해줘" — Claude 가 tmux 세션 살아있는지 + access.json 의 allowFrom 확인 |
| 재부팅 후 봇 안 살아남 | "X 봇 자동시작 등록됐는지 확인해줘" — Claude 가 launchctl list 점검 |

전체 트러블슈팅: [SKILL.md](./SKILL.md) 의 트러블슈팅 섹션

---

## 보안

- **봇 토큰 = 누구나 봇 조작할 수 있는 키**. `.env` 만, `chmod 600` 만, **절대** git/clipboard/log 에 노출 X
- **`dmPolicy` 는 항상 `allowlist`** — 자기 텔레그램 user ID 만 `allowFrom` 에 추가
- `public` 모드는 절대 사용 금지

---

## 라이선스 / 출처

- MIT — 자유 사용·수정·재배포
- 작성: gd.on (B3RYS) · 2026-05-10
- 기반: 6개월+ 운영 중인 production Telegram bot 셋업의 패턴
