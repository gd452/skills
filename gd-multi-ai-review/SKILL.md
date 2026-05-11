---
name: gd-multi-ai-review
description: "Gemini와 GPT(Codex CLI)로 병렬 교차 리뷰를 받아 합의·이견·신규 이슈를 종합하는 스킬. 중요한 설계·아키텍처·스킬 작성·긴 글 초안에 대해 '교차검증', '다중 AI 리뷰', '외부 모델 리뷰', '제미나이/코덱스한테도 물어봐', '피어 리뷰', 'cross review', '집단지성' 같은 요청이 있거나, 사용자가 '다른 모델 의견도 궁금하다'는 뉘앙스를 보이면 반드시 이 스킬을 사용한다. Claude 단독 판단에 의존하지 말고 외부 검증이 유효한 경우 자동으로 제안할 것."
---

# Multi-AI Review — 병렬 외부 모델 교차검증

Claude의 판단을 Gemini와 GPT(Codex)로 교차검증하여 **합의·이견·추가 이슈**를 도출한다. 중요한 설계 판단이나 스킬 설계 직후, 외부 관점이 품질을 크게 높일 때 사용.

## 언제 쓰는가

| 상황 | 사용 여부 |
|---|---|
| 아키텍처/스킬 설계 결정 | ✅ 강권 |
| 장문 산출물(사업계획서, 리뷰 문서) 초안 | ✅ 권장 |
| 복잡한 기술 판단 (모델 선택, 인프라 선택) | ✅ 권장 |
| 단순 질문·코딩 작업 | ❌ 과함 |
| 민감 정보(비밀키, 사내 코드, PII) 포함 | ❌ 사용 금지 |

## 전제 조건

- `gemini` CLI (`/opt/homebrew/bin/gemini`) + `GEMINI_API_KEY`
- `codex` CLI (`/opt/homebrew/bin/codex`) + `OPENAI_API_KEY`
- 둘 중 하나라도 없으면 사용자에게 알리고 가능한 한쪽만 실행 or 중단

## 워크플로우

### Phase 1: 브리프 준비

교차검증할 주제를 **자체 완결된 브리프**로 정리한다. 외부 모델은 현재 대화 맥락을 모르므로 다음을 포함:

1. **대상**: 무엇을 리뷰할지 (URL/파일/인라인 내용)
2. **Claude의 현재 판단**: 내가 이미 도출한 결론/이슈
3. **질문**: 타당성 / 대안 / 놓친 부분

브리프 파일 저장 위치: `{작업디렉토리}/reports/multi-ai-review-{YYYYMMDD-HHMM}-{topic-slug}/brief.md`

**topic-slug 규칙**: 주제를 영문 소문자 + 하이픈으로 12~30자 내외 슬러그화 (예: `codex-cli-integration`, `harness-design-review`). 같은 날 여러 리뷰가 쌓일 때 폴더만 보고도 주제를 식별 가능.

> 민감 정보 포함 여부를 **반드시** 사용자에게 확인한다. API 키, 사내 전용 코드, PII가 브리프에 들어가면 외부로 유출된다.

### Phase 2: 병렬 발송

**한 메시지에서 두 Bash 호출을 `run_in_background: true`로 동시 발사**한다. 순차 호출은 느려진다.

**Gemini** (stdin 파이프):
```bash
cat {brief-path} | gemini -p "{질문}" 2>&1 | tee {reports-dir}/gemini.txt
```

**Codex** (인자 전달, `--sandbox read-only` + `--skip-git-repo-check` 필수, `-o` 로 최종 답만 파일 캡처):
```bash
codex exec \
  --sandbox read-only \
  --skip-git-repo-check \
  -o {reports-dir}/codex.txt \
  "$(cat {brief-path})

---

{질문}"
```

> codex 호출 옵션 상세(샌드박스 모드, 안티패턴, 트러블슈팅, JSON 스트림 등)는 `codex-cli` 스킬 참고. 본 스킬은 read-only 분석 패턴만 사용한다.

호출 후 두 task-id를 기억하고 **폴링하지 않고 완료 알림을 기다린다**.

### Phase 3: 응답 수집

두 완료 알림이 도착하면 각 output 파일을 Read로 읽는다. 실패 유형별 대응:

| 증상 | 원인 | 대응 |
|---|---|---|
| `Not inside a trusted directory` | Codex git-repo 체크 | `--skip-git-repo-check` 추가해 재실행 |
| `auth required` / 401 | API 키 만료 | 사용자에게 키 갱신 요청 |
| 타임아웃 (>5분) | 과도한 입력 | 브리프 축약 후 재시도 |
| 한쪽만 성공 | 일시 오류 | 성공한 결과로 진행, 누락 명시 |

### Phase 3.5: 멀티라운드 (선택)

단발성(1회)으로 부족하면 2-3라운드로 확장한다. 사용자가 요청하거나, 이견이 크면 자동 제안.

**라운드 구조:**
- Round 1: 각자 독립 답변 (Phase 2-3)
- Round 2: 상대방 답변을 포함한 프롬프트로 재호출 → 반론/보완
- Round 3 (선택): 최종 입장 정리

**상대방 답변 공유 프롬프트:**
```
# Round 2: 상대방 답변을 읽고 반론하세요.

## 상대방 핵심 주장:
{상대방 R1 답변 요약}

## 질문:
1. 동의하는 부분과 반론할 부분은?
2. 당신의 입장을 수정할 부분이 있는가?
```

**산출물**: `{reports-dir}/gemini-r{N}.txt`, `{reports-dir}/codex-r{N}.txt`

**Codex stdin 주의**: `cat file | codex`는 불안정. `codex exec "$(cat file)"` 방식 사용. 멀티라운드도 동일하게 `--sandbox read-only --skip-git-repo-check -o {reports-dir}/codex-r{N}.txt` 적용.

**CLI 폴백**: CLI 실패 시 API 호출로 대체 가능 (동일한 stateless 멀티라운드 구조).

### Phase 4: 합성

세 관점(Claude·Gemini·Codex)을 **합의·이견·추가 이슈** 3섹션으로 정리한다. 멀티라운드 시 논의 과정(각 라운드에서 입장이 어떻게 변했는지)을 반드시 포함한다.

**합성 표 템플릿**:

```markdown
## 합성 결과

### 합의된 이슈 (3자 모두 유효 판정)
| 이슈 | Claude | Gemini | Codex | 최종 우선순위 |

### 이견 (판정 갈린 이슈)
| 이슈 | Claude | Gemini | Codex | 판단 근거 |

### 외부 모델이 추가로 제기한 이슈
| 이슈 | 제기자 | 수용 여부 | 근거 |
```

**판단 원칙**:
- 2자 이상 동의면 수용 검토
- 3자 모두 동의하면 즉시 반영
- 이견이면 근거 강한 쪽 채택 (단순 모델별 선호 차이는 기록만)
- 외부 모델이 Claude가 놓친 이슈 제기 시 **정직하게 인정**하고 우선순위에 편입

### Phase 5: 보존 및 보고

산출물 구조:

```
reports/multi-ai-review-{YYYYMMDD-HHMM}-{topic-slug}/
├── brief.md           # Phase 1 브리프
├── gemini-r1.txt      # Gemini Round 1
├── codex-r1.txt       # Codex Round 1
├── gemini-r2.txt      # Gemini Round 2 (멀티라운드 시)
├── codex-r2.txt       # Codex Round 2 (멀티라운드 시)
└── synthesis.md       # Phase 4 합성 결과 (논의 과정 포함)
```

사용자에게 **합성 결과**와 **다음 액션 제안**만 보고한다. 원본 응답은 파일 경로로만 안내.

## 호출 예시

**사용자**: "이 하네스 스킬 리뷰가 타당한지 Gemini/Codex한테도 물어봐줘"

1. Phase 1: 기존 리뷰를 브리프로 정리 → `reports/multi-ai-review-20260419-2145-harness-skill-review/brief.md`
2. Phase 2: Bash 한 메시지에서 gemini + codex 병렬 발사 (run_in_background)
3. Phase 3: 두 완료 알림 수신, 응답 Read
4. Phase 4: 합성 표 작성 → `synthesis.md`
5. Phase 5: 사용자에게 합성 결과 보고, 원본은 파일 경로로 안내

## 비용 가이드

| 규모 | 입력 | 출력 | 1회 비용 (두 모델 합계) |
|---|---|---|---|
| 소형 브리프 | 1~2K 토큰 | 1K 토큰 | ~$0.02 |
| 중형 (스킬 리뷰) | 3~5K 토큰 | 2~3K 토큰 | ~$0.05 |
| 대형 (장문 문서) | 10K+ 토큰 | 5K+ 토큰 | $0.20~0.50 |

일반적인 리뷰는 회당 $0.05 내외. 하루 5회 사용해도 $1 이하.

## 주의사항

1. **민감 정보 보호**: API 키, 사내 전용 코드, 미공개 비즈니스 정보는 브리프에서 제거하거나 추상화. 확신 없으면 사용자에게 확인.
2. **외부 모델의 환각**: Codex는 `revfactory/harness` 같은 잘못된 URL을 추측할 수 있다. 외부 모델 응답의 URL·파일 경로·API 이름은 Claude가 직접 검증.
3. **편향 인식**: 외부 모델도 자기 모델 생태계 선호를 보인다 (Gemini가 Google 툴 권장, Codex가 OpenAI 모델 권장). 기술 선택 판단 시 이 편향을 고려.
4. **Claude의 입장**: 외부 모델이 다수 의견이어도 Claude가 근거 있는 반대 의견이면 유지한다. 거수기가 아니라 검증 도구.

## 트러블슈팅

**Codex가 git 체크로 실패**: `--skip-git-repo-check` 추가
**Codex 가 파일 쓰기 시도하다 실패**: `--sandbox read-only` 는 의도적 — 분석만 시키는 모드. 패치가 필요하면 `codex-cli` 스킬의 `workspace-write` 패턴으로 별도 호출
**Gemini가 긴 입력 거부**: 브리프를 요약하거나 핵심 섹션만 발췌
**두 모델 모두 타임아웃**: 브리프가 너무 크거나 질문이 모호함. 분할해서 재시도
**응답이 한국어/영어 섞임**: 질문에 "한국어로 답해줘" 명시
