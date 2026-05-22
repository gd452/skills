# gd's Claude Code Skills

[Claude Code](https://claude.com/claude-code) 글로벌 스킬 모음. 개별 스킬을 던지지 않고 **함께 쓰이는 워크플로우** 단위로 묶었습니다.

> 이 저장소는 작업 저장소에서 자동 동기화되는 단방향 미러입니다. 이슈/PR 은 받지만, 머지된 변경은 원본에 반영 후 다음 동기화에 포함됩니다.

## 친구 저장소

비슷한 결의 다른 스킬 컬렉션:

- [revfactory/skills](https://github.com/revfactory/skills) — 동료 로빈의 스킬 (codex-cli, hwp, agent-research 등)
- [revfactory/harness](https://github.com/revfactory/harness) — 하네스(Agent Team Architect) 의 원본
- [anthropics/skills](https://github.com/anthropics/skills) — Anthropic 공식 (skill-creator 등)

---

## 🛠 워크플로우 1 — 소프트웨어 프로젝트 처음부터 배포까지

> 새 프로젝트를 시작해서 운영까지. 큰 프로젝트일수록 앞 단계까지 다 쓰고, 작은 프로젝트는 뒷부분만 씀.

```
프롬프트 (의도)
   │
   ▼  ← 복잡할 때만
gd-write-spec      "무엇을 만들지" — XML 구조화된 SPEC.md 생성
   │  ⭐ gd-multi-ai-review (큰 spec 권장) — 가정·누락 외부 모델 검증
   │
   ▼
gd-start-project   "어디서 시작할지" — TODO/CLAUDE/MEMORY/README 골격 생성
   │
   ▼  ← 다단계 자동화 필요할 때만
harness            "어떻게 협업할지" — 도메인 에이전트 팀 + 보조 스킬 구성
   │               (revfactory/harness 기반 로컬 커스텀)
   │  ⭐ gd-multi-ai-review (에이전트 팀 설계 검토 권장)
   │
   ▼
(코딩 + Claude Code 협업)
   │
   ▼
gd-review          배포 전 SPEC 대조 + 코드 품질 + 테스트 점검
   │  ⭐ gd-multi-ai-review (Phase 7 — 배포 직전 외부 모델 마지막 점검)
   │
   ▼
gd-deploy          push + CI 검증 + 배포 결과 보고
```

> 💡 **횡단 스킬**: [`gd-multi-ai-review`](./gd-multi-ai-review) 는 워크플로우 2 의 메인이지만, **워크플로우 1 의 모든 게이트포인트** (spec / harness 설계 / review) 에 끼워 쓰면 단독 Claude 판단의 echo chamber 를 회피할 수 있다. 큰 결정일수록 권장.

| 스킬 | 무엇을 정의하나 | 산출물 |
|---|---|---|
| [gd-write-spec](./gd-write-spec) | "무엇을" — 상세 명세 | `SPEC.md` (XML 구조) |
| [gd-start-project](./gd-start-project) | "어디서" — 폴더/파일 골격 | `TODO.md` + `CLAUDE.md` + `MEMORY.md` + `README.md` |
| [harness](./harness) | "어떻게" — 에이전트 팀 + 도메인 스킬 | `.claude/agents/` + `.claude/skills/` |
| [gd-review](./gd-review) | 배포 전 검증 | 점검 보고서 |
| [gd-deploy](./gd-deploy) | 배포 실행 | push + CI + 결과 |

**규모별 사용**
- 작은 스크립트: `gd-start-project` 만
- 중간: `gd-write-spec` → `gd-start-project` → 코딩 → `gd-review` → `gd-deploy`
- 큰 프로젝트: 전체 흐름 + `harness` 추가

---

## 🤝 워크플로우 2 — Claude 외 다른 모델로 교차검증

> 중요한 설계 결정·아키텍처 선택 등에 단독 Claude 의견에 의존하지 않기 위함. Gemini + GPT(Codex) 둘 다 호출해서 합의·이견 종합.

```
중요한 판단 / 설계 결정
   │
   ▼
gd-multi-ai-review  Gemini + Codex 를 병렬 호출 → 합의/이견/추가 이슈 종합
   │
   ├─ codex-cli      Codex CLI 비대화형 호출 가이드 (sandbox, JSON, MCP 등 모든 패턴)
   └─ codex-image    Codex 의 image_generation 툴로 최대 5장 병렬 생성
```

| 스킬 | 용도 |
|---|---|
| [gd-multi-ai-review](./gd-multi-ai-review) | 외부 모델 교차검증의 메인 워크플로우 |
| [codex-cli ↗](https://github.com/revfactory/skills/tree/main/codex-cli) | Codex CLI 호출 패턴 카탈로그 (다른 스킬도 참조) — 외부 (revfactory/skills), 이 미러엔 미포함 |
| [codex-image ↗](https://github.com/revfactory/skills/tree/main/codex-image) | Codex 로 병렬 이미지 생성 (단순 이미지 외 → 별도 스킬) — 외부 (revfactory/skills), 이 미러엔 미포함 |

> ℹ️ `codex-cli` · `codex-image` 의 원본은 동료 로빈의 [revfactory/skills](https://github.com/revfactory/skills) 입니다. 원본 출처를 존중해 이 미러엔 재배포하지 않고 외부 링크로만 연결합니다. `gd-multi-ai-review` 가 이 둘을 내부적으로 호출합니다.

---

## 🎯 워크플로우 3 — 세션 운영 / 가성비 판단 / 콘텐츠 산출물

| 스킬 | 언제 쓰나 |
|---|---|
| [gd-briefing](./gd-briefing) | 새 세션 시작 시 — git 상태 + TODO 진행률 + MEMORY 미결 + 교차검증 한눈에 |
| [gd-api-select](./gd-api-select) | LLM API 엔진 선택 / 가격 비교 — `references/benchmark.md` 내장 (월별 자동 갱신) |
| [gd-write-business-plan](./gd-write-business-plan) | Sequoia/YC 템플릿 기반 사업계획서·피치덱 작성 |

> 💡 장문 산출물 (사업계획서·기획서) 초안 후 [`gd-multi-ai-review`](./gd-multi-ai-review) 로 사실성·논리·시장 가정 cross-check 권장.

---

## 🔧 워크플로우 4 — Claude Code + Telegram 봇 셋업 (macOS)

| 스킬 | 언제 쓰나 |
|---|---|
| [setup-claude-telegram-bot](./setup-claude-telegram-bot) | Mac Claude Code ↔ Telegram 봇 양방향 연결 자동 셋업. BotFather 토큰 → Channels plugin + tmux + LaunchAgent 까지 한 번에. **macOS 한정** (LaunchAgent). Linux/Windows 는 일부 단계 수동 변환 필요 |

---

## 설치

`~/.claude/skills/` 에 심볼릭 링크하거나 직접 클론.

```bash
# 옵션 1: 통째로 클론
git clone https://github.com/gd452/skills.git ~/.claude/skills-gd
ln -s ~/.claude/skills-gd/gd-briefing ~/.claude/skills/gd-briefing
# 원하는 스킬만 골라서 심링크

# 옵션 2: 개별 스킬만 받기 (sparse checkout)
git clone --depth 1 --filter=blob:none --sparse https://github.com/gd452/skills.git ~/skills-tmp
cd ~/skills-tmp && git sparse-checkout set gd-briefing gd-multi-ai-review
cp -r gd-briefing gd-multi-ai-review ~/.claude/skills/
```

설치 후 Claude Code 재시작하면 자동 인식됩니다 (description 매칭으로 발동).

## 네이밍 규칙

`gd-` 접두어는 **저자 시그니처 + Claude Code 빌트인(`/review`, `/init` 등)과의 충돌 회피** 용도입니다. 외부에서 가져와 그대로 쓰는 스킬(codex-cli, codex-image 등)은 원본 이름 유지로 추적성 확보.

## 라이선스

[MIT](./LICENSE). 마음껏 fork·수정·재배포 환영. 외부에서 가져온 스킬(codex-cli, codex-image, gd-write-spec, harness 등)은 각 SKILL.md 의 출처 블록 참조.

## 의존성 요약

| 스킬 | 외부 도구 |
|---|---|
| gd-multi-ai-review, codex-cli, codex-image | `codex` CLI + ChatGPT OAuth 또는 OpenAI API |
| gd-multi-ai-review | + `gemini` CLI + ChatGPT-식 OAuth 또는 `GEMINI_API_KEY` |
| gd-deploy | `gh` CLI (GitHub Actions 결과 확인) |
| gd-api-select | (없음 — `references/benchmark.md` 내장) |
| 그 외 | 표준 git + 셸만 |
