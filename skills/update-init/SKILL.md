---
name: update-init
description: 이니셔티브의 Cycle 기반 업데이트를 하위 프로젝트 업데이트를 종합하여 자동 생성하고 Linear에 직접 등록. "/update-init", "이니셔티브 업데이트 써줘", "이니셔티브 업데이트 작성" 등으로 호출. 프로젝트별 성과를 이니셔티브 관점으로 재해석.
---

# update-init

이니셔티브 Cycle 업데이트를 **하위 프로젝트 업데이트 종합**하여 자동 생성 → Linear에 직접 등록

## 핵심 원칙

- 프로젝트 업데이트 복붙 ❌ → 이니셔티브 관점에서 "무엇이 달라졌는지" 중심
- 프로젝트별 1줄 요약만 (핵심 성과/이슈 선별)
- 팀 전체가 이해할 수 있는 비즈니스 언어
- Health는 하위 프로젝트 health 기반 자동 종합

## 워크플로우

### Step 1: 이니셔티브 선택

**Linear MCP 사용:**
```
linear_getInitiatives() → 이니셔티브 목록
```
- 내가 owner인 이니셔티브 필터링 (status: inProgress, notStarted)
- 사용자에게 목록 제시 → 선택받기

### Step 2: 하위 프로젝트 업데이트 수집

**Linear MCP 사용:**
```
linear_getInitiativeProjects(initiativeId) → 프로젝트 목록
```

**스크립트 사용** (MCP에 없음):
```bash
# 각 프로젝트의 최근 업데이트
python ~/.claude/plugins/linear-toolkit/skills/update-init/scripts/linear_api.py project-updates <project_id> --limit 3
```

수집 항목:
- 이니셔티브에 연결된 프로젝트 목록 (활성 상태만) - MCP
- 각 프로젝트의 최근 업데이트 (body, health, createdAt) - 스크립트
- 각 프로젝트의 현재 health 상태

### Step 3: 업데이트 내용 작성

**하이라이트 중심 포맷:**
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

**Health 자동 종합 로직:**
- 모든 프로젝트가 onTrack → 🟢 onTrack
- 1개라도 atRisk → 🟡 atRisk
- 1개라도 offTrack → 🔴 offTrack

작성 가이드: [writing-guide.md](references/writing-guide.md)
출력 포맷 예시: [output-format.md](references/output-format.md)

### Step 4: Linear 등록

업데이트 내용 확인 후:
1. "Linear에 바로 올릴까요?" 질문
2. health 상태 확인 (자동 종합 결과 또는 수동 선택)
3. **스크립트로 등록**:
```bash
# 업데이트 내용을 임시 파일에 저장 후
python ~/.claude/plugins/linear-toolkit/skills/update-init/scripts/linear_api.py create-initiative-update <initiative_id> /tmp/update.md --health onTrack
```
4. 등록 완료 시 URL 반환

## 환경 설정

`.env` 파일에 토큰 설정 (스크립트용):
```
LINEAR_API_TOKEN=lin_api_xxxxxxxxxxxxx
```

## API 사용 방식

| 작업 | 방법 | 이유 |
|------|------|------|
| 이니셔티브 조회 | **Linear MCP** | `linear_getInitiatives()` |
| 이니셔티브-프로젝트 연결 | **Linear MCP** | `linear_getInitiativeProjects()` |
| 프로젝트 업데이트 조회 | **스크립트** | MCP에 없음 |
| `initiativeUpdateCreate` | **스크립트** | MCP에 없음 |

## 주의사항

1. 프로젝트 업데이트 그대로 복붙 안함 - 이니셔티브 관점으로 재해석
2. 이슈 번호 포함 안함 - 가독성 저하
3. 너무 상세하게 쓰지 않기 - 핵심만 (프로젝트별 1-2줄)
4. Health 자동 종합 후 실제 상황과 다르면 수동 조정 가능
5. Linear 등록 전 반드시 내용 확인받기
