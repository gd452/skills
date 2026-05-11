"""
LLM API Benchmark 자동 업데이트 스크립트

3단계 파이프라인:
  1단계: Gemini Flash-Lite로 가격 페이지에서 구조화된 JSON 추출 ($0)
  2단계: 검증 — 추출된 모델명이 원본 페이지에 실재하는지 cross-check (환각 차단)
  3단계: Claude Haiku 4.5로 benchmark.md 업데이트 생성 ($0.06)

필요 환경변수:
  GOOGLE_API_KEY   - Google AI Studio API key
  ANTHROPIC_API_KEY - Anthropic API key

사용법 (b3rys-private 루트에서):
  python members/gd/claude/skills/gd-api-select/scripts/update_benchmark.py
  python members/gd/claude/skills/gd-api-select/scripts/update_benchmark.py --dry-run

GitHub Actions: .github/workflows/update-benchmark.yml 가 매월 1일 자동 실행 + 수동 트리거 가능.
"""

import argparse
import json
import os
import re
import sys
from datetime import date
from pathlib import Path

import requests
from bs4 import BeautifulSoup
from google import genai
import anthropic

BENCHMARK_PATH = Path(__file__).parent.parent / "references" / "benchmark.md"
WARNINGS_PATH = Path(__file__).parent.parent / ".benchmark_warnings.json"
PRICING_DATA_PATH = Path(__file__).parent.parent / ".benchmark_pricing_data.json"

PRICE_RANGES = {
    "input_per_1m": (0.0, 100.0),
    "output_per_1m": (0.0, 500.0),
    "batch_input": (0.0, 100.0),
    "batch_output": (0.0, 500.0),
}

PRICING_KEYWORDS = ["price", "pric", "$", "per 1m", "per million", "/m tokens", "tokens"]

PRICING_SOURCES = {
    "gemini": "https://ai.google.dev/gemini-api/docs/pricing",
    "claude": "https://platform.claude.com/docs/en/about-claude/pricing",
    "openai": "https://developers.openai.com/api/docs/pricing",
    "deepseek": "https://api-docs.deepseek.com/quick_start/pricing",
}

HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; llm-playbook-updater/1.0)"
}


def fetch_pricing_pages() -> dict[str, str]:
    """각 provider의 가격 페이지를 크롤링하여 텍스트로 변환."""
    results = {}
    for name, url in PRICING_SOURCES.items():
        try:
            resp = requests.get(url, headers=HEADERS, timeout=30)
            resp.raise_for_status()
            soup = BeautifulSoup(resp.text, "html.parser")
            for tag in soup(["script", "style", "nav", "footer", "header"]):
                tag.decompose()
            text = soup.get_text(separator="\n", strip=True)
            # 너무 길면 앞부분만 (토큰 절약)
            results[name] = text[:15000]
            print(f"  [OK] {name}: {len(results[name])} chars")
        except Exception as e:
            print(f"  [FAIL] {name}: {e}")
            results[name] = ""
    return results


def extract_pricing_json(pages: dict[str, str]) -> dict:
    """Gemini Flash-Lite로 가격 데이터를 구조화된 JSON으로 추출."""
    client = genai.Client()

    prompt = """아래는 LLM API provider들의 가격 페이지 텍스트다.
각 provider에서 모델별 API 가격을 추출하여 JSON으로 정리해줘.

출력 형식 (JSON만 출력, 다른 텍스트 없이):
{
  "gemini": [
    {"model": "모델명", "input_per_1m": 0.10, "output_per_1m": 0.40, "context": "1M", "batch_input": 0.05, "batch_output": 0.20, "free": true, "notes": "비고"}
  ],
  "openai": [...],
  "claude": [...],
  "deepseek": [...]
}

규칙:
- 가격은 USD, per 1M tokens 기준
- batch 가격이 없으면 null
- deprecated 모델 제외
- 같은 모델의 날짜 변형 제외 (예: gpt-4o-2024-05-13 → gpt-4o만)
- free tier 여부 표시

"""
    for name, text in pages.items():
        if text:
            prompt += f"\n--- {name.upper()} ---\n{text}\n"

    response = client.models.generate_content(
        model="gemini-2.5-flash-lite",
        contents=prompt,
        config={"temperature": 0.0},
    )

    raw = response.text.strip()
    # JSON 블록 추출
    if "```json" in raw:
        raw = raw.split("```json")[1].split("```")[0]
    elif "```" in raw:
        raw = raw.split("```")[1].split("```")[0]

    return json.loads(raw)


def _model_keywords(model_name: str) -> list[str]:
    """모델명을 검색 가능한 키워드로 분해. 'gemini-2.5-flash-lite' → ['gemini','2.5','flash','lite']."""
    parts = re.split(r"[\s\-_/()]+", model_name.lower())
    return [p for p in parts if len(p) >= 2]


def validate_pricing_data(pricing_data: dict, pages: dict[str, str]) -> tuple[list[str], list[str]]:
    """추출된 데이터를 원본 페이지에 대조하여 환각·이상치 차단.

    Returns:
        (errors, warnings) — errors 가 있으면 fatal (abort), warnings 는 PR 라벨링용.
    """
    errors: list[str] = []
    warnings: list[str] = []

    # 1) Provider 누락
    expected_providers = set(PRICING_SOURCES.keys())
    missing_providers = expected_providers - set(pricing_data.keys())
    for p in missing_providers:
        warnings.append(f"[{p}] 추출 결과에서 누락됨")

    # 2) 페이지 무결성: 비어있거나 가격 키워드가 없으면 그 provider의 모델은 모두 의심
    suspect_providers: set[str] = set()
    for provider in pricing_data.keys():
        text = (pages.get(provider) or "").lower()
        if not text:
            errors.append(f"[{provider}] 원본 페이지를 가져오지 못함 (fetch 실패) — 추출 결과는 모두 환각 가능")
            suspect_providers.add(provider)
            continue
        if not any(k in text for k in PRICING_KEYWORDS):
            warnings.append(f"[{provider}] 원본 페이지에 가격 키워드가 없음 — 동적 페이지일 가능성")
            suspect_providers.add(provider)

    # 3) 모델별 cross-reference + 가격 sanity
    for provider, models in pricing_data.items():
        if provider in suspect_providers:
            # 페이지 자체가 의심스러우면 model-level 검증 무의미
            continue
        page_text = (pages.get(provider) or "").lower()
        for m in models:
            name = (m.get("model") or "").strip()
            if not name:
                warnings.append(f"[{provider}] 빈 모델명 항목 발견")
                continue
            keywords = _model_keywords(name)
            if not keywords:
                warnings.append(f"[{provider}/{name}] 모델명 토큰화 실패")
                continue
            missing = [k for k in keywords if k not in page_text]
            # 핵심 키워드 (provider 이름·버전 숫자) 가 빠지면 환각 가능
            # 절반 이상 누락이면 환각으로 간주
            if len(missing) >= max(2, len(keywords) // 2):
                errors.append(
                    f"[{provider}/{name}] 원본 페이지에 모델명 키워드 {missing} 누락 → 환각 의심"
                )
            elif missing:
                warnings.append(f"[{provider}/{name}] 모델명 키워드 일부 누락: {missing}")

            for field, (lo, hi) in PRICE_RANGES.items():
                v = m.get(field)
                if v is None:
                    continue
                try:
                    fv = float(v)
                except (TypeError, ValueError):
                    warnings.append(f"[{provider}/{name}] {field} 가 숫자가 아님: {v!r}")
                    continue
                if fv < lo or fv > hi:
                    errors.append(
                        f"[{provider}/{name}] {field}={fv} 가 sanity range [{lo},{hi}] 벗어남"
                    )

    return errors, warnings


def generate_updated_markdown(
    current_md: str, pricing_data: dict, today: str
) -> str:
    """Claude Haiku 4.5로 업데이트된 benchmark.md를 생성."""
    client = anthropic.Anthropic()

    prompt = f"""현재 benchmark.md와 최신 가격 데이터를 비교하여 업데이트된 benchmark.md를 생성해줘.

## 절대 규칙 (위반 시 출력 폐기)
- **기존 Changelog 섹션 ("## 2026-XX" 항목들) 의 모든 줄을 단 하나도 수정/요약/삭제하지 말 것**.
  과거 항목은 그대로 보존하고 맨 위에 새 "## {today[:7]}" 섹션만 추가.
- 표·문단의 모든 텍스트는 가격/모델명 변경이 필요한 경우에만 그 부분만 교체.
  설명 문구(`> [!tip]`, `> [!info]` 등)와 헤더는 그대로 유지.
- 가격 데이터에 없는 모델(예: DeepL, Imagen, Flux, Whisper, Qwen 등 외부 모델)은 그대로 유지.

## 업데이트 규칙
1. "Last updated" 날짜를 {today}로 변경
2. 가격 데이터에 등장한 모델 중, 현재 문서에 같은 모델명이 있으면 가격만 갱신
3. 가격 데이터의 신모델 중 표/섹션에 자연스럽게 들어갈 수 있는 것만 추가 (preview/실험적 모델은 메모와 함께)
4. 가격 데이터에 안 보이는 provider 모델은 deprecated 가능성 — 그대로 두고 별도 표시 없이 보존
5. 한눈에 보기 테이블의 가성비/품질 Pick은 가격 변동이 1위 자리를 바꿀 때만 재평가
6. Changelog 추가는 다음 형태로:
   ```
   ## {today[:7]}
   - (변경 내용 한 줄씩 bullet)
   ```
   기존 Changelog 항목들 위에 새 섹션을 추가하고, 기존 항목 본문은 글자 하나도 바꾸지 말 것.
7. 변경사항이 없으면 "NO_CHANGES"만 출력
8. 전체 markdown 파일을 출력 (변경사항이 있을 경우)

## 최신 가격 데이터
```json
{json.dumps(pricing_data, ensure_ascii=False, indent=2)}
```

## 현재 benchmark.md
```markdown
{current_md}
```

업데이트된 전체 markdown을 출력해줘. markdown 코드블록 없이 raw markdown으로."""

    response = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=16384,
        messages=[{"role": "user", "content": prompt}],
    )

    if response.stop_reason == "max_tokens":
        raise RuntimeError(
            "Haiku 응답이 max_tokens 한계로 잘렸음. "
            "max_tokens 추가 증액 또는 증분 갱신 방식 도입 필요."
        )
    return response.content[0].text


def main():
    parser = argparse.ArgumentParser(description="LLM API Benchmark 자동 업데이트")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="변경사항 미리보기만 (파일 수정 안 함)",
    )
    args = parser.parse_args()

    # 환경변수 체크 (여러 키 이름 지원)
    google_key = os.environ.get("GOOGLE_API_KEY") or os.environ.get("GEMINI_API_KEY")
    anthropic_key = os.environ.get("ANTHROPIC_API_KEY") or os.environ.get("ANTHROPIC_API_KEY_B3RYS")
    if not google_key:
        print("ERROR: GOOGLE_API_KEY 또는 GEMINI_API_KEY 환경변수가 필요합니다.")
        sys.exit(1)
    if not anthropic_key:
        print("ERROR: ANTHROPIC_API_KEY 또는 ANTHROPIC_API_KEY_B3RYS 환경변수가 필요합니다.")
        sys.exit(1)
    os.environ["GOOGLE_API_KEY"] = google_key
    os.environ["ANTHROPIC_API_KEY"] = anthropic_key

    today = date.today().isoformat()
    print(f"=== LLM Benchmark 업데이트 ({today}) ===\n")

    # 1. 크롤링
    print("[1/4] 가격 페이지 크롤링...")
    pages = fetch_pricing_pages()
    fetched = sum(1 for v in pages.values() if v)
    if fetched == 0:
        print("ERROR: 가격 페이지를 하나도 가져오지 못했습니다.")
        sys.exit(1)
    print(f"  → {fetched}/{len(PRICING_SOURCES)} 페이지 수집 완료\n")

    # 2. Gemini로 구조화 추출
    print("[2/4] Gemini Flash-Lite로 가격 데이터 추출...")
    pricing_data = extract_pricing_json(pages)
    total_models = sum(len(v) for v in pricing_data.values())
    print(f"  → {total_models}개 모델 추출 완료")
    for provider, models in pricing_data.items():
        names = [m.get("model", "?") for m in models]
        print(f"    {provider} ({len(models)}): {', '.join(names)}")
    PRICING_DATA_PATH.write_text(
        json.dumps(pricing_data, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(f"  → 추출 결과 저장: {PRICING_DATA_PATH.name}")
    print()

    # 3. 검증 (환각·이상치 차단)
    print("[3/4] 추출 결과 검증 (cross-reference + sanity)...")
    errors, warnings = validate_pricing_data(pricing_data, pages)
    if errors:
        print(f"  [FATAL] {len(errors)}개 오류 발견:")
        for e in errors:
            print(f"    × {e}")
    if warnings:
        print(f"  [WARN] {len(warnings)}개 경고:")
        for w in warnings:
            print(f"    ! {w}")
    if not errors and not warnings:
        print("  → 검증 통과")
    print()

    # 검증 결과는 항상 파일로 저장 (워크플로우가 PR body에 포함)
    WARNINGS_PATH.write_text(
        json.dumps(
            {"errors": errors, "warnings": warnings, "checked_at": today},
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )

    if errors:
        # fatal 시 markdown 갱신 차단. 워크플로우는 WARNINGS_PATH 를 읽어 알림 처리.
        print("ERROR: 검증 단계에서 fatal 오류 발생. benchmark.md 업데이트를 중단합니다.")
        sys.exit(2)

    # 4. Haiku로 markdown 생성
    print("[4/4] Claude Haiku 4.5로 benchmark.md 업데이트 생성...")
    current_md = BENCHMARK_PATH.read_text(encoding="utf-8")
    updated_md = generate_updated_markdown(current_md, pricing_data, today)

    if "NO_CHANGES" in updated_md and len(updated_md) < 50:
        print("  → 변경사항 없음. 업데이트 불필요.")
        return

    if args.dry_run:
        print("\n[DRY RUN] 생성된 markdown:\n")
        print(updated_md[:2000])
        print(f"\n... (총 {len(updated_md)} chars)")
    else:
        BENCHMARK_PATH.write_text(updated_md, encoding="utf-8")
        print(f"  → {BENCHMARK_PATH} 업데이트 완료!")

    print("\n=== 완료 ===")


if __name__ == "__main__":
    main()
