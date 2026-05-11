# LLM API Benchmark

> Last updated: 2026-05-07

## 한눈에 보기

| Task | 💰 가성비 Pick | 가격 | 🏆 품질 Pick | 가격 |
| --- | --- | --- | --- | --- |
| 텍스트 번역 | Gemini 3.1 Flash Lite Preview | `$0.25/$1.50` /1M tok | DeepL | `$25` /M chars |
| 텍스트 요약 | Gemini 3.1 Flash Lite Preview | `$0.25/$1.50` /1M tok | Claude Sonnet 4.6 | `$3.00/$15.00` /1M tok |
| 이미지 생성 | Imagen 4 Fast | `$0.020` /장 | Flux 2 Pro v1.1 | `$0.055` /장 |
| 오디오 전사 | GPT-4o Mini Transcribe | `$0.003` /분 | GPT-4o Transcribe | `$0.006` /분 |
| **음성 합성 (TTS)** | OpenAI tts-1 | `$15` /M chars | ElevenLabs Multilingual v2 | `1 credit/char` (~$22 /월) |
| 이미지 분석/OCR | Gemini 3.1 Flash Lite Preview | `$0.0008` /장 | Claude Sonnet 4.6 | `$0.006` /장 |
| 메뉴판 OCR+번역 | Gemini 3.1 Flash Lite Preview | `$0.0008` /장 | GPT-5.4 | `$0.007` /장 |

> [!tip] 핵심
> - **텍스트/비전** → Gemini가 거의 전부 가성비 1위 (AI Studio 무료 티어 있음)
> - **이미지 생성** → Imagen 4 Fast (`$0.020`/장), 무료 티어는 Gemini 3.1 Flash Image Preview
> - **오디오 전사** → OpenAI 독주 (Whisper / GPT-4o Transcribe)
> - **음성 합성 (TTS)** → 가성비는 OpenAI tts-1, 무료는 edge-tts, 음질은 ElevenLabs
> - **중국 모델** → DeepSeek V4 (`$0.14/$0.28`)가 가격 파괴 중, 안정성은 주의

## 무료 티어

| Provider | 무료 범위 |
| --- | --- |
| 🟢 Google AI Studio | Gemini Flash/Lite 무료, Gemini 3.1 Flash Image Preview 무료 |
| 🟢 Google Cloud Translation | 500K chars/월 (상시 무료) |
| 🟢 Google Cloud Vision | 1,000장/월 |
| 🟢 Google Cloud STT | 60분/월 + 신규 $300 크레딧 |
| 🔵 DeepL API Free | 500K chars/월 |
| 🟣 ElevenLabs Free | 10K credits/월 (TTS, **API에서는 library voice 못 씀** — paid plan 필요) |
| ⚪ edge-tts | **무한** (Microsoft 비공식, 사실상 Azure Neural 엔진. SLA 없음) |

## 비용 절감 팁

> [!info] 적용하면 바로 절감
> - **Batch API** — 대부분 50% 할인 (비동기 처리 허용 시)
> - **Prompt caching** — 반복 프롬프트에서 최대 90% 절감
> - **모델 다운그레이드** — 단순 task에 저가 모델 (Flash Lite, GPT-5.4-nano)
> - **1회 호출 통합** — OCR+번역 등 복합 task는 파이프라인보다 LLM 1회 호출이 저렴
> - **중국 모델 활용** — DeepSeek V4 캐시 히트 `$0.0014`/1M tok, 데이터 주권 확인 필수

---

# 상세 비교

## 📝 텍스트 번역 (EN → KO)

**LLM 기반**

| Model | $/1M tok (in → out) | 품질 | Latency | Free |
| --- | --- | --- | --- | --- |
| **⭐ Gemini 3.1 Flash Lite Preview** | `$0.25` → `$1.50` | 중상 | ~1-2s | ✅ |
| Qwen 3.5-Flash | `$0.10` → `$0.40` | 중상 | ~1-2s | ❌ |
| GPT-5.4-nano | `$0.20` → `$1.25` | 중 | ~1-2s | ❌ |
| GPT-5.4-mini | `$0.75` → `$4.50` | 중상 | ~1-3s | ❌ |
| DeepSeek V4 Flash | `$0.14` → `$0.28` | 중상 | ~2-5s | ❌ |
| Claude Haiku 4.5 | `$1.00` → `$5.00` | 상 | ~1-2s | ❌ |
| Claude Sonnet 4.6 | `$3.00` → `$15.00` | 최상 | ~1-2s | ❌ |
| GPT-5.4 | `$2.50` → `$15.00` | 최상 | ~1-3s | ❌ |

**전용 번역 API** (1M tokens ≈ 4M chars)

| Model | 가격 | 환산 $/1M tok | 품질 | Free |
| --- | --- | --- | --- | --- |
| Google Cloud Translation v2 | `$20`/M chars | ~$80 | 중 | 500K chars/월 |
| **⭐ DeepL API Pro** | `$25`/M chars + $5.49/월 | ~$100 | 상 | 500K chars/월 |

> [!note] 참고
> - LLM이 전용 번역 API 대비 **~200배 저렴**, 문맥 인식도 가능
> - DeepL은 EN→KO 자연스러움이 가장 높지만 대량 처리에는 비용 부담
> - 한중일 번역 특화 → Qwen 3.5-Flash가 Gemini 대비 강점
> - Batch API 50% 할인, Prompt caching 최대 90% 절감 가능

---

## 📝 텍스트 요약

| Model | $/1M tok (in → out) | 품질 | Context | Free |
| --- | --- | --- | --- | --- |
| **⭐ Gemini 3.1 Flash Lite Preview** | `$0.25` → `$1.50` | 중 | 1M | ✅ |
| GPT-5.4-nano | `$0.20` → `$1.25` | 중 | 1M | ❌ |
| Gemini 3.1 Flash Preview | `$0.50` → `$3.00` | 상 | 1M | ✅ |
| DeepSeek V4 Flash | `$0.14` → `$0.28` | 중상 | 1M | ❌ |
| GPT-5.4-mini | `$0.75` → `$4.50` | 중상 | 1M | ❌ |
| Claude Haiku 4.5 | `$1.00` → `$5.00` | 상 | 200K | ❌ |
| Claude Sonnet 4.6 | `$3.00` → `$15.00` | 최상 | 200K | ❌ |

> [!note] 참고
> - 긴 문서 → Gemini 시리즈 (1M context)
> - 추론이 필요한 요약 → Gemini 3.1 Flash Pro thinking 모드
> - 최고 품질 요약 → Claude Sonnet 4.6 (비용은 높음)
> - 가성비 극한 → DeepSeek V4 Flash (output이 `$0.28`로 압도적 저렴)

---

## 🎨 이미지 생성

> [!warning] 모델명 혼동 주의
> Gemini 이미지 모델이 2종류 있음. **가격이 4배 차이**나므로 반드시 정확한 모델명 확인 필요.
> - Gemini **3.1 Flash** Image Preview: `$0.50` (1K, 중가)
> - Gemini **3 Pro** Image Preview: `$2.00` (1K, 최고 품질)

| Model | $/장 | 품질 (Elo) | 해상도 | Free |
| --- | --- | --- | --- | --- |
| GPT Image 1 Mini (low) | `$0.005` | ~1,150 | 1K | ❌ |
| Flux 2 Schnell | `$0.015` | ~1,200 | 1K | ❌ |
| **⭐ Imagen 4 Fast** | `$0.020` | ~1,200 | 1K | ❌ |
| Flux 2 Dev | `$0.025` | ~1,230 | 1K | ❌ |
| GPT Image 1 (medium) | `$0.042` | ~1,230 | 1K | ❌ |
| Imagen 4 Standard | `$0.040` | ~1,230 | 1K | ❌ |
| Flux 2 Pro v1.1 | `$0.055` | **1,265** | 1K | ❌ |
| Imagen 4 Ultra | `$0.060` | ~1,250 | 4K | ❌ |
| SD 3.5 Large | `$0.065` | ~1,200 | 1K | 25 크레딧 |
| Stable Image Ultra | `$0.080` | ~1,220 | 1K | 25 크레딧 |
| FLUX Kontext [max] | `$0.080` | ~1,250 | 1K | ❌ |
| Gemini 3.1 Flash Image Preview | `$0.50` | ~1,230 | 1K | ✅ |
| GPT Image 1 (high) | `$0.167` | ~1,250 | 1K | ❌ |
| **Gemini 3 Pro Image Preview** | **`$2.00`** | **1,252** | 1K | ✅ |

> [!note] 용도별 추천
> - **대량 생성 (가성비)** → Imagen 4 Fast (`$0.020`) — 100장 = $2
> - **최고 품질** → Flux 2 Pro v1.1 (`$0.055`, Elo 1,265)
> - **무료 프로토타이핑** → Gemini 3.1 Flash Image Preview (AI Studio 무료)
> - **텍스트 렌더링 / 대화형 편집** → Gemini 3 Pro Image Preview (`$2.00`, 고가 주의)
> - **이미지 편집 / 참조 기반** → FLUX Kontext [max]
> - **4K 고해상도** → Imagen 4 Ultra (`$0.060`)
>
> **비용 함정 주의**: Gemini 3 Pro Image Preview는 Imagen 4 Fast 대비 **100배 비쌈**. 100장 기준 $2 vs $200.

---

## 🎙️ 오디오 전사 / 번역

| Model | $/분 | 품질 | 특징 | Free |
| --- | --- | --- | --- | --- |
| **⭐ GPT-4o Mini Transcribe** | `$0.003` | 상 | 실시간 | ❌ |
| Whisper API | `$0.006` | 상 | 업계 표준 | ❌ |
| GPT-4o Transcribe | `$0.006` | 최상 | 화자 분리 | ❌ |
| Gemini 3.1 Flash Live Preview (audio) | `$0.005` | 중상 | 실시간 스트리밍 | ✅ |
| Google Cloud STT v2 | `$0.016` | 상 | 스트리밍 | 60분/월 |
| Google Cloud STT Batch | `$0.004` | 상 | 비동기 | 60분/월 |

> [!note] 참고
> - **전사+번역 동시** → Gemini (1회 호출로 처리, 파이프라인 불필요)
> - **실시간 스트리밍** → Gemini 3.1 Flash Live Preview (무료 티어 포함)
> - **Self-hosting** → Whisper 오픈소스 (비용 $0, GPU 필요)

---

## 🗣️ 음성 합성 (TTS)

월 ~53K chars (한국어 5분 대본 × 22일) 기준.

| Model | 단가 | 월 비용 | 한국어 품질 | instruction 톤 | Free |
| --- | --- | --- | --- | --- | --- |
| **⭐ OpenAI tts-1** | `$15`/M chars | `$0.79` | 중상 | ❌ | ❌ |
| OpenAI tts-1-hd | `$30`/M chars | `$1.59` | 상 | ❌ | ❌ |
| OpenAI gpt-4o-mini-tts | `$0.60`/M in tok + `$12`/M audio out tok | ~`$4.4` | 중상 | ✅ | ❌ |
| **edge-tts** (비공식) | `$0` | `$0` | 중상 | ❌ | 무한 |
| Azure TTS Neural | `$16`/M chars | ~`$1` | 상 | ❌ | 0.5M chars/월 (12개월) |
| Azure TTS HD | `$30`/M chars | ~`$1.6` | 최상 | ❌ | 100K chars/월 (12개월) |
| Google Cloud TTS Neural2 | `$16`/M chars | ~`$1` | 상 | ❌ | 1M chars/월 |
| Google Cloud TTS Studio | `$160`/M chars | ~`$8.5` | 최상 | ❌ | 100K chars/월 |
| ElevenLabs Flash v2.5 | `0.5 credit/char` (Creator $22/월 200K credits) | ~`$11` | 상 | ❌ | API 무료 X (10K credits 무료지만 **library voice는 paid only**) |
| **🏆 ElevenLabs Multilingual v2** | `1 credit/char` | ~`$22` | 최상 | ❌ | ↑ 동일 |

> [!note] 한국어 노하우
> - **gpt-4o-mini-tts shimmer는 한국어에 어색** — `alloy`/`onyx`/`nova` 권장
> - **tts-1·tts-1-hd는 instructions 인자 미지원** (gpt-4o-* 만). 코드에서 `model.startswith("gpt-4o")` 체크로 자동 분기 필요
> - **edge-tts voice 매핑** — OpenAI 이름 ↔ Azure ko-KR voice
>   - alloy → `ko-KR-HyunsuNeural` (남, 차분)
>   - onyx/echo → `ko-KR-InJoonNeural` (남, 또렷)
>   - nova/shimmer → `ko-KR-SunHiNeural` (여, 발랄)
> - **ElevenLabs 무료 티어 함정** — API에서 library voice(Rachel/Adam 등) 못 씀. 무료로 들어보려면 웹 UI 필요. Multilingual v2가 한국어 최상이지만 paid plan부터.
> - **Self-hosting** — piper(MIT, 빠름)·Kokoro TTS·OpenVoice V2. GitHub Actions 표준 runner는 GPU 없어 5분 음성 합성에 10~30분 → 외부 API가 더 현실적

> [!tip] 픽 가이드
> - **무료 + 운영 안정성↑** → Azure TTS Neural (12개월 0.5M chars/월 무료, 이후 `$1`/월)
> - **유료 가성비** → OpenAI tts-1 + alloy 보이스 (`$0.79`/월, 한국어 무난, 코드 단순)
> - **음질 우선** → ElevenLabs Multilingual v2 (`$22`/월)
> - **instruction 톤 지정 필요** → gpt-4o-mini-tts only (`$4.4`/월)
> - **검증·실험** → edge-tts (무료, SLA 없음 주의)

> [!warning] TTS 가격은 **chars / token / minute / credit** 단위가 모두 달라 직접 비교 어려움
> - chars: tts-1, Azure, Google
> - token: gpt-4o-mini-tts (input + audio output 별도)
> - credit: ElevenLabs (모델별 credit/char 비율 다름)
> - 코드 작성 시 모델별 분기 필수

---

## 👁️ 이미지 분석 / OCR

이미지 1장 + 응답 ~300 tokens 기준:

| Model | 합계 $/장 | 품질 | Free |
| --- | --- | --- | --- |
| **⭐ Gemini 3.1 Flash Lite Preview** | `$0.0008` | 상 | ✅ |
| Google Cloud Vision (OCR) | `$0.0015` | 상 (OCR 특화) | 1,000장/월 |
| GPT-5.4 (low detail) | `$0.0008` | 상 | ❌ |
| GPT-5.4 (high detail) | `$0.0015` | 최상 | ❌ |
| Claude Sonnet 4.6 | `$0.006` | 최상 | ❌ |

**복합 Task: 메뉴판 OCR + 번역**

| 방식 | $/장 | $/1달러당 | 비고 |
| --- | --- | --- | --- |
| **⭐ Gemini 1회 호출** | `$0.0008` | 1,250장 | OCR + 번역 + 구조화 |
| Vision API + Flash Lite | `$0.0023` | 435장 | 2단계 파이프라인 |
| GPT-5.4 1회 호출 | `$0.007` | 143장 | 최고 정확도 |

> [!note] 참고
> - **복합 task** → LLM 1회 호출이 파이프라인보다 저렴하고 단순
> - **손글씨/예술 폰트** → GPT-5.4 (high detail) 또는 Claude Sonnet 4.6
> - **대량 문서** → Gemini 1M context로 멀티페이지 일괄 처리
> - **구조화 출력** (bounding box, 언어 감지) → Google Cloud Vision

---

# 참고: 중국 LLM API

> Last updated: 2026-05-07

중국 모델은 가격이 매우 저렴하지만, 데이터 주권·API 안정성·가격 변동성을 고려해야 한다.
대부분 **OpenAI 호환 API** 포맷을 지원하므로 코드 변경은 최소화된다.

## 주요 모델 가격

| 회사 | 모델 | $/1M tok (in → out) | Context | 비고 |
| --- | --- | --- | --- | --- |
| **DeepSeek** | V4 Flash | `$0.14` → `$0.28` | 1M | 캐시 히트 시 input `$0.0028` (98% 할인) |
| | V4 Pro | `$1.74` → `$3.48` | 1M | 추론 모드, 2026-05-31까지 75% 할인 중 |
| **Alibaba (Qwen)** | Qwen 3.5-Plus | `$0.40` → `$2.40` | 128K | 아시아 언어(중일한) 최강급 |
| | Qwen 3.5-Flash | `$0.10` → `$0.40` | 128K | Gemini Flash-Lite급 가성비 |
| **Zhipu** | GLM-4.7 | `$0.54` → `$2.40` | 128K | 2026-02 가격 30% 인상 |
| **Moonshot** | Kimi K2.5 | `$0.60` → `$3.00` | 128K | 긴 컨텍스트 특화 |
| **ByteDance** | Doubao 2.0 Pro | `$0.47` → `$2.37` | 128K | 멀티모달 (텍스트+이미지+영상) |
| | Doubao 2.0 Mini | `$0.03` → `$0.31` | 32K | 초저가 경량 모델 |
| **MiniMax** | M2 | `$0.30` → `$1.20` | 128K | Sonnet 대비 ~8% 비용 |

> [!tip] 가성비 주목
> - **DeepSeek V4 Flash** — 캐시 활용 시 input `$0.0028`/1M tok, 서양 모델 대비 1,000배 이상 저렴
> - **Qwen 3.5-Flash** — `$0.10`/`$0.40`으로 Gemini Flash-Lite와 동급, 한중일 번역에 더 강함
> - **Doubao 2.0 Mini** — `$0.03`/`$0.31`로 최저가 경량 모델

> [!warning] 사용 시 주의
> - **데이터 주권** — 대부분 중국 서버 경유. 민감 데이터 처리 시 확인 필요
> - **API 안정성** — DeepSeek V4는 수요 폭증으로 속도 저하/다운 가능성 있음
> - **가격 변동** — GLM-5처럼 갑자기 30% 인상하는 경우 있음
> - **리전별 가격 차이** — Qwen 등은 중국 내 가격이 글로벌 대비 절반 수준

---

# 비용 추적 코드 스니펫

API 호출 후 토큰 사용량을 추출하고 비용을 계산하는 코드.

## Google Gemini (google-genai SDK)

```python
response = client.models.generate_content(model=model, contents=contents, config=config)

# usage 추출
input_tokens = response.usage_metadata.prompt_token_count or 0
output_tokens = response.usage_metadata.candidates_token_count or 0
```

## OpenAI (openai SDK)

```python
response = client.chat.completions.create(model=model, messages=messages)

# usage 추출
input_tokens = response.usage.prompt_tokens
output_tokens = response.usage.completion_tokens
```

## Anthropic Claude (anthropic SDK)

```python
response = client.messages.create(model=model, messages=messages)

# usage 추출
input_tokens = response.usage.input_tokens
output_tokens = response.usage.output_tokens
```

## Google Gemini (REST API / TypeScript)

```typescript
const data = await response.json();

// usage 추출
const inputTokens = data.usageMetadata?.promptTokenCount ?? 0;
const outputTokens = data.usageMetadata?.candidatesTokenCount ?? 0;
```

## OpenAI (REST API / TypeScript)

```typescript
const data = await response.json();

// usage 추출
const inputTokens = data.usage?.prompt_tokens ?? 0;
const outputTokens = data.usage?.completion_tokens ?? 0;
```

## Anthropic Claude (REST API / TypeScript)

```typescript
const data = await response.json();

// usage 추출
const inputTokens = data.usage?.input_tokens ?? 0;
const outputTokens = data.usage?.output_tokens ?? 0;
```

## 비용 계산 공통 패턴

```python
# 가격 상수 ($/token) — api-pricing.md "한눈에 보기" 참조
INPUT_PRICE = input_price_per_1m / 1_000_000
OUTPUT_PRICE = output_price_per_1m / 1_000_000

def calculate_cost(input_tokens: int, output_tokens: int) -> float:
    return input_tokens * INPUT_PRICE + output_tokens * OUTPUT_PRICE
```

```typescript
// TypeScript 버전
const INPUT_PRICE = inputPricePer1M / 1_000_000;
const OUTPUT_PRICE = outputPricePer1M / 1_000_000;

function calculateCost(inputTokens: number, outputTokens: number): number {
  return inputTokens * INPUT_PRICE + outputTokens * OUTPUT_PRICE;
}
```

---

# Changelog

## 2026-05

- **새 모델 신규 추가**
  - Gemini 3.1 Pro Preview: `$2.00/$12.00` (신규)
  - Gemini 3.1 Flash Live Preview: `$0.75/$4.50` (신규, 실시간 오디오 스트리밍)
  - Gemini 3.1 Flash TTS Preview: `$1.00/$20.00` (신규, TTS 전용)
  - Gemini 3.1 Flash Lite Preview: `$0.25/$1.50` (신규, 기존 Flash Lite 대체)
  - Gemini 3.1 Flash Preview: `$0.50/$3.00` (신규, 기존 Flash 대체)
  - Gemini 3.1 Flash Image Preview: `$0.50` (신규)
  - Gemini 3 Pro Image Preview: `$2.00` (신규)
  - OpenAI GPT-5.5: `$5.00/$30.00` (신규)
  - OpenAI GPT-5.5-pro: `$30.00/$180.00` (신규)
  - OpenAI gpt-realtime-1.5: `$4.00/$16.00` (신규)
  - OpenAI gpt-realtime-mini: `$0.60/$2.40` (신규)
  - OpenAI gpt-image-2: `$5.00/$30.00` (신규)
  - OpenAI gpt-image-1.5: `$5.00/$10.00` (신규)
  - OpenAI gpt-image-1-mini: `$2.00` text input (신규)
  - OpenAI o3-deep-research: `$5.00/$20.00` (신규)
  - OpenAI o4-mini-deep-research: `$1.00/$4.00` (신규)
  - OpenAI computer-use-preview: `$1.50/$6.00` (신규)
  - OpenAI chat-latest: `$5.00/$30.00` (신규)
  - OpenAI gpt-5.3-codex: `$1.75/$14.00` batch (`$3.50/$28.00`) (신규)
  - Claude Opus 4.7: `$5.00/$25.00` (신규)
  - Claude Sonnet 4.6: cache pricing 명시 (`$3.75` write, `$0.30` hit)
  - Claude Haiku 4.5: cache pricing 추가
  - DeepSeek V4 Flash: `$0.14/$0.28` (신규)
  - DeepSeek V4 Pro: `$1.74/$3.48` (신규)

- **🗣️ 음성 합성 (TTS) 섹션 신규 추가**
  - 한눈에 보기 표에 TTS 라인 추가 — 가성비 OpenAI tts-1 (`$15/M chars`), 음질 ElevenLabs Multilingual v2
  - 무료 티어 표에 ElevenLabs Free + edge-tts (Microsoft 비공식) 추가
  - 상세 비교 표: OpenAI(tts-1/tts-1-hd/gpt-4o-mini-tts) + Azure Neural/HD + Google Neural2/Studio + ElevenLabs(Flash v2.5/Multilingual v2) + edge-tts
  - 한국어 노하우: voice 매핑(alloy↔ko-KR-HyunsuNeural 등), instructions 인자는 gpt-4o-* 만 지원, ElevenLabs 무료 티어는 API에서 library voice 못 씀
  - 픽 가이드 및 경고 섹션 추가

- **모델 버전 업데이트**
  - DeepSeek V3.2 → V4 Flash/Pro 교체
  - DeepSeek V4 Pro: 75% 할인 중 명시 (2026-05-31까지)
  - 캐시 히트 가격 재계산: V3.2 `$0.028` → V4 Flash `$0.0028` (더욱 저렴)

- **텍스트 번역 표 업데이트**
  - Gemini 3.1 Flash Lite Preview 추가 및 가성비 Pick으로 선정
  - DeepSeek V3.2 → V4 Flash 교체 (`$0.28/$0.42` → `$0.14/$0.28`)

- **텍스트 요약 표 업데이트**
  - Gemini 3.1 Flash Lite Preview / Flash Preview 모델명 정확화
  - DeepSeek 모델 버전 업데이트

- **이미지 분석/OCR 표 업데이트**
  - Gemini 3.1 Flash Lite Preview: `$0.0008` (기존 Flash Lite 대체)
  - 메뉴판 OCR+번역 복합 Task 비용 재계산: `$0.0006` → `$0.0008`

- **이미지 생성 섹션 업데이트**
  - Gemini 모델명 정확화: 3.1 Flash Image / 3 Pro Image Preview만 기재
  - Gemini 3.1 Flash Image Preview: `$0.50` 추가
  - Gemini 3 Pro Image Preview: `$2.00` 신규
  - 경고 섹션 업데이트 (4배 → 100배 차이)

- **오디오 섹션 업데이트**
  - Gemini 3.1 Flash Live Preview: `$0.005`/분 추가 (실시간 스트리밍 무료 티어 포함)

- **중국 LLM API 섹션 업데이트**
  - DeepSeek V3.2 → V4 Flash/Pro 교체
  - DeepSeek V4 Pro: 75% 할인 중 명시 (2026-05-31까지)
  - 캐시 히트 가격 재계산: `$0.028` → `$0.0028`
  - 주목 섹션에서 "1,000배" → "1,000배 이상" 강조 추가

## 2026-04

- 한눈에 보기 테이블 재평가
  - 텍스트 요약: 품질 Pick을 "Gemini 2.5 Flash" → "Claude Sonnet 4.6" 변경
  - 메뉴판 OCR+번역: 품질 Pick을 "GPT-5.2" → "GPT-5.4" 변경 (신규 가격 적용)
- 텍스트 번역 섹션 업데이트
  - GPT-5 Nano → GPT-5.4-nano 모델명 정확화 (가격: `$0.025/$0.20` → `$0.20/$1.25`)
  - GPT-5 Mini → GPT-5.4-mini (가격: `$0.125/$1.00` → `$0.75/$4.50`)
  - Claude Sonnet 4.6 (`$3.00/$15.00`) 추가
  - GPT-5.4 (`$2.50/$15.00`) 추가
- 텍스트 요약 섹션 업데이트
  - GPT-5 Nano → GPT-5.4-nano
  - GPT-5 Mini → GPT-5.4-mini
  - Claude Sonnet 4.6 추가 및 재평가
- 이미지 분석/OCR 섹션 업데이트
  - GPT-5.2 → GPT-5.4 모델명 정확화
  - 가격 업데이트: low detail `$0.003` → `$0.0008`, high detail `$0.006` → `$0.0015`
- 복합 Task (메뉴판 OCR+번역) 가격 업데이트
  - GPT-5.2 1회 호출 → GPT-5.4 1회 호출
  - 가격: `$0.006` → `$0.007` /장
  - $/1달러당: 167 → 143장

## 2026-03

- 이미지 생성 섹션 전면 업데이트
  - Imagen 3 → Imagen 4 (Fast/Standard/Ultra) 교체
  - DALL-E 3 → GPT Image 1 (Mini/Medium/High) 교체
  - FLUX.2 → Flux 2 (Schnell/Dev/Pro v1.1) 교체
  - Gemini 이미지 모델 3종 모두 기재 (2.5 Flash / 3.1 Flash / 3 Pro) — 모델명 혼동 방지
  - Elo 품질 점수 추가, 가성비 Pick을 Imagen 4 Fast ($0.020)로 변경
- 전체 모델/가격 업데이트
  - **Gemini 신규/변경**: 3.1 Pro/Flash-Lite/Flash-Image, 3 Pro-Image, 2.5 Pro 추가
    - 2.5 Flash: `$0.15/$0.60` → `$0.30/$2.50`
    - 2.5 Flash Lite: `$0.075/$0.3` → `$0.10/$0.40`
  - **OpenAI GPT-5 계열 신규**: 5.4, 5.2, 5.1, 5 (base), 5-mini, 5-nano
    - GPT-5.4: `$2.50/$15.00`
    - GPT-5.4-mini: `$0.75/$4.50`
    - GPT-5.4-nano: `$0.20/$1.25`
    - GPT-5.2: `$1.75/$14.00`
  - **OpenAI 레거시**: gpt-4.1, gpt-4.1-mini, gpt-4.1-nano 추가 (일부 중복)
  - **OpenAI 오디오/실시간**: gpt-realtime, gpt-realtime-1.5, gpt-realtime-mini 추가
  - **OpenAI 이미지**: gpt-image-1.5, gpt-image-1, gpt-image-1-mini 가격 상향
  - **OpenAI o-시리즈**: o1, o1-pro, o1-mini 가격 2배 상향
  - **OpenAI o3 계열**: o3-pro, o3, o3-deep-research, o3-mini 신규/가격 상향
  - **OpenAI o4 계열**: o4-mini, o4-mini-deep-research 신규
  - **Claude**: 4.6 시리즈 (Opus/Sonnet), Haiku 4.5 추가
    - Claude Opus 4.6: `$5.00/$25.00`
    - Claude Opus 4.1: `$15.00/$75.00`
    - Claude Sonnet 4.6: `$3.00/$15.00`
    - Claude Haiku 4.5: `$1.00/$5.00`
    - Claude Haiku 3.5: `$0.8/$4.0` (신규)
  - **DeepSeek**: V3.2 chat/reasoner 추가 (`$0.28/$0.42`)
- 번역/요약 비교 테이블에 GPT-5 Nano, 3.1 Flash-Lite 추가
- 오디오 전사 표에서 GPT-4o Mini Transcribe 가격 유지 (`$0.003`/분)

## 2026-02 (초기 작성)

- 초기 벤치마크 데이터 수집
- 대상: Google (Gemini), OpenAI, Anthropic, DeepL, Google Cloud, Stability AI, Black Forest Labs
- Gemini 2.5 Flash Lite가 텍스트 task 전반에서 가성비 1위
- Imagen 3이 이미지 생성 가성비 1위 (1,500장/일 무료)
- 오디오는 OpenAI 독주 (GPT-4o Mini Transcribe $0.003/분)