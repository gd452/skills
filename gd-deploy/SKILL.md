---
name: gd-deploy
description: "배포 실행. push + CI 검증 + 배포 결과 확인. '/gd-deploy', '배포해줘', 'push하고 확인해줘', '배포 진행' 요청 시 사용."
---

# Deploy — 배포 실행 및 검증

`/gd-review` 통과 후 코드를 원격에 푸시하고, CI/CD 파이프라인 결과를 확인한다.

## 실행 절차

### 1. 사전 확인

```bash
git status --short
git log origin/$(git branch --show-current)..HEAD --oneline
```

- 미커밋 변경사항이 있으면 사용자에게 알리고 중단
- push할 커밋이 없으면 알리고 중단
- `/gd-review`를 먼저 실행했는지 확인 (안 했으면 권장)

### 2. 원격에 푸시

```bash
git push origin $(git branch --show-current)
```

- push 실패 시 (reject, conflict 등) 원인 파악 후 사용자에게 안내
- force push는 사용자 명시적 요청 없이 절대 하지 않는다

### 3. CI/CD 확인

GitHub Actions가 있는 경우:
```bash
gh run list --limit 1 --branch $(git branch --show-current)
```

- 워크플로우 실행 대기 → 완료 시 결과 확인
- 실패 시 `gh run view <id> --log-failed`로 에러 추출

Vercel/Netlify 등 자동 배포가 있는 경우:
- 배포 URL 확인 (`gh api` 또는 프로젝트 설정 기반)
- Preview URL이 있으면 사용자에게 공유

### 4. 결과 보고

```
## 배포 결과

- Push: ✅ origin/{branch} ({N}커밋)
- CI: ✅ 통과 / ❌ 실패 (에러 요약)
- 배포 URL: {있으면 표시}

→ TODO.md 갱신 필요 여부 확인
```

### 5. 실패 시 대응

- **CI 실패**: 에러 로그에서 원인 추출 → 수정 제안 → 사용자 승인 후 수정 → 재push
- **배포 실패**: 플랫폼별 로그 확인 방법 안내
- **롤백 필요**: 사용자 명시적 요청 시에만 `git revert` 수행. force push는 하지 않는다.

## 주의사항

- main/master 브랜치에 직접 push하기 전에 반드시 사용자에게 확인
- force push (`--force`, `-f`)는 사용자가 명시적으로 요청해야만 실행
- 배포 후 TODO.md 해당 항목 갱신 (`[~]` → `[x]`)
