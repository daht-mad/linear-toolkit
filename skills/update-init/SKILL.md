---
name: update-init
description: 이니셔티브의 Cycle 기반 업데이트를 하위 프로젝트 업데이트를 종합하여 자동 생성하고 Linear에 직접 등록. "/update-init", "이니셔티브 업데이트 써줘", "이니셔티브 업데이트 작성" 등으로 호출. 프로젝트별 성과를 이니셔티브 관점으로 재해석.
---

# update-init

이니셔티브 업데이트를 **하위 프로젝트 종합**하여 자동 생성 → Linear 등록

## 핵심 원칙

- 프로젝트 업데이트 복붙 ❌ → 이니셔티브 관점에서 "무엇이 달라졌는지"
- 프로젝트별 1줄 요약만 (핵심 성과/이슈 선별)
- 팀 전체가 이해할 수 있는 비즈니스 언어
- Health는 하위 프로젝트 기반 자동 종합

## MCP 도구

| 용도 | MCP 도구 |
|------|----------|
| 현재 사용자 | `linear_getViewer` |
| 이니셔티브 목록 | `linear_getInitiatives` |
| 이니셔티브 프로젝트 | `linear_getInitiativeProjects(initiativeId)` |
| 프로젝트 업데이트 조회 | `linear_getProjectUpdates(projectId, limit?)` |
| 업데이트 생성 | `linear_initiativeUpdateCreate(initiativeId, body, health?)` |

## 워크플로우

### 1. 이니셔티브 선택

`linear_getInitiatives` + `linear_getViewer`로 내가 owner인 `status: "Active"` 또는 `"Planned"` 이니셔티브 조회 → 사용자 선택

### 2. 하위 프로젝트 업데이트 수집

- `linear_getInitiativeProjects`로 프로젝트 목록
- `linear_getProjectUpdates`로 각 프로젝트의 최근 업데이트 조회

### 3. 업데이트 작성

하이라이트 중심으로 작성. 작성법:

- **작성 가이드**: [references/writing-guide.md](references/writing-guide.md) 참조
- **출력 포맷 예시**: [references/output-format.md](references/output-format.md) 참조

**포맷:**
```markdown
## 📊 이니셔티브 현황

**Health**: 🟢 onTrack / 🟡 atRisk / 🔴 offTrack

---

### ✅ 이번 Cycle 핵심 성과
- [프로젝트A] 성과 요약
- [프로젝트B] 성과 요약

### ⚠️ 주요 이슈/리스크
- 이슈 내용 → 대응 방안

### 📋 다음 Cycle 중점
- 계획 요약

---

### 프로젝트별 상세
| 프로젝트 | Health | 핵심 진행 |
|----------|--------|-----------|
| 프로젝트A | 🟢 | 한줄 요약 |
```

**Health 자동 종합:**
- 모든 프로젝트 onTrack → 🟢 onTrack
- 1개라도 atRisk → 🟡 atRisk
- 1개라도 offTrack → 🔴 offTrack

### 4. Linear 등록

1. 사용자 확인: "Linear에 바로 올릴까요?"
2. health 선택 (자동 종합 결과 또는 수동)
3. `linear_initiativeUpdateCreate` MCP 도구 호출
4. 등록된 URL 반환
