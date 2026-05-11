---
name: gd-api-select
description: "AI API 엔진 선택 및 가격/비용 추적 가이드. references/benchmark.md 의 가격/성능 비교를 바탕으로 엔진 추천, 비용 측정 구현 지원. '/gd-api-select', 'API 선택', 'LLM 가격 비교' 요청 시 사용."
allowed-tools: Read, Glob, WebSearch, WebFetch
---

AI API 연동 시 `references/benchmark.md` 를 참조하여 엔진을 선택하거나, 비용 추적을 구현한다. 이 스킬은 self-contained — 외부 repo 의존 없음.

## 트리거 조건

다음 중 하나에 해당하면 이 스킬을 사용한다:
- AI API **엔진 선택** (어떤 모델을 쓸지)
- AI API **가격 조회** (특정 모델의 토큰/장 단가)
- AI API **비용 추적/측정 구현** (usage 추출, 비용 계산, 누적 저장)

## 순서

### A. 엔진 선택

1. 사용자에게 어떤 task인지 확인 (번역, 요약, 이미지 생성, 오디오 전사, OCR 등)
2. `references/benchmark.md` 를 Read 로 읽어 해당 task 의 가성비/품질 pick 확인
3. "한눈에 보기" 요약표와 상세 비교를 바탕으로 엔진 선택 계획 수립
4. 계획을 사용자에게 공유하고 **승인받은 뒤** 구현 진행

### B. 가격 조회 / 비용 추적 구현

1. `references/benchmark.md` 에서 해당 모델의 **단가** 확인
2. 프로젝트에 가격 상수가 있으면 benchmark.md 단가와 일치하는지 확인 (불일치 시 업데이트)
3. benchmark.md 하단의 **비용 추적 코드 스니펫** 섹션에서 해당 provider 의 usage 추출 방법 참조 (Python SDK / TypeScript REST 버전 모두 수록)
4. 가격 상수 + usage 추출 코드를 바탕으로 비용 계산 로직 구현

## 데이터 소스 / 갱신

`references/benchmark.md` 는 이 스킬 안의 `scripts/update_benchmark.py` 가 직접 갱신한다 (self-contained).

3단계 파이프라인:
1. **추출**: Gemini Flash-Lite 가 4개 provider 가격 페이지(Gemini, Claude, OpenAI, DeepSeek)를 크롤링해 JSON 으로 구조화
2. **검증**: 추출된 모델명이 원본 페이지에 실재하는지 cross-reference + 가격 sanity range 체크 (환각 차단)
3. **생성**: Claude Haiku 4.5 가 검증 통과 데이터로 `references/benchmark.md` 갱신

메인테이너 환경 (b3rys-private) 에서는 `.github/workflows/update-benchmark.yml` 이 매월 1일 자동 실행하여 PR 을 생성한다. 외부 사용자가 자기 환경에서 갱신하려면 `GOOGLE_API_KEY` + `ANTHROPIC_API_KEY` 환경변수 + `pip install -r scripts/requirements.txt` 후 직접 스크립트 실행.

## 참고

- 데이터가 오래됐으면 (3개월+) 웹 검색으로 최신 가격 확인 → 원본 데이터 소스 갱신 → 재동기화
- 외부 사용자: 자기 환경에서는 `references/benchmark.md` 를 직접 편집하거나, 자기만의 가격 추적 데이터로 교체해 사용
