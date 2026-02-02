---
name: update-proj
description: Linear 프로젝트의 Cycle 기반 업데이트를 결과물 중심으로 자동 생성하고 Linear에 직접 등록. "/update-proj", "프로젝트 업데이트 써줘", "프로젝트 업데이트 작성" 등으로 호출. 이슈 나열이 아닌 '무엇이 달라졌는지' 중심으로 작성.
---

# update-proj

Linear 프로젝트 주간 업데이트를 **결과물 중심**으로 자동 생성 → Linear에 직접 등록

## 핵심 원칙

- 이슈 나열 ❌ → 뭐가 달라졌는지/달라질지 중심
- 맥락 포함 → 기존 문제 → 변경 사항 → 완료 작업
- 이슈 번호 생략, ~요/~합니다 말투 사용 안함

## 워크플로우

### 1. 프로젝트 선택

**스크립트 사용** (MCP에 멤버 정보 없음):
```bash
python ~/.claude/skills/update-proj/scripts/linear_api.py my-projects
```

**필터링 조건:**
- `state == "started"` 인 프로젝트만 표시 (in progress 상태)
- 내가 **리드**이거나 **멤버**로 포함된 프로젝트만 표시
- 리드 프로젝트 먼저, 멤버 프로젝트 나중에 정렬

사용자에게 목록 제시 (역할 표시) → 선택받기

### 2. Cycle/이슈 수집

**스크립트 사용** (Linear MCP의 state 필드 버그로 인해 직접 API 호출):
```bash
python ~/.claude/skills/update-proj/scripts/linear_api.py active-cycle <team_id>
python ~/.claude/skills/update-proj/scripts/linear_api.py cycles <team_id>
python ~/.claude/skills/update-proj/scripts/linear_api.py project-issues <project_id>
```
- 현재 Cycle = **만든 결과**
- 다음 Cycle = **만들 결과**
- 이슈 상태(state.name, state.type)와 Cycle 정보 포함

### 3. 업데이트 작성

이슈들을 그룹핑하여 결과물 중심으로 작성:
- 말머리/이모지 가이드: [writing-guide.md](references/writing-guide.md)
- 출력 포맷 예시: [output-format.md](references/output-format.md)

**만든 결과** 포맷:
```markdown
## 🔧 [말머리] 결과물 제목

**한 줄 요약**: X를 Y로 개선

**기존 문제**
- 문제점

**변경 사항**
| 구분 | AS-IS | TO-BE |
|------|-------|-------|
| 항목 | 기존 | **변경** |

**완료된 작업**
- 작업 내용
```

**만들 결과** 포맷:
```markdown
## 🔧 [말머리] 결과물 제목

**목표**: 한 줄 설명

- [ ] 할 일
```

### 4. Linear 등록

업데이트 내용 확인 후:
1. "Linear에 바로 올릴까요?" 질문
2. health 상태 선택: 🟢 onTrack / 🟡 atRisk / 🔴 offTrack
3. **스크립트로 등록** (MCP에 projectUpdateCreate 없음):
```bash
python ~/.claude/plugins/linear-toolkit/skills/update-proj/scripts/linear_api.py create-update <project_id> /tmp/update.md --health onTrack
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
| 조회 (viewer, projects, issues, cycles) | **스크립트** | MCP의 state 필드 버그 (하위 필드 누락) |
| `projectUpdateCreate` | **스크립트** | MCP에 없음 |

> **참고**: Linear MCP의 이슈 조회 시 `state` 필드가 `{}`로 반환되는 버그 있음. 직접 GraphQL API 호출로 해결.

## 주의사항

1. 이슈 번호 포함 안함 - 가독성 저하
2. 너무 기술적으로 쓰지 않기 - 팀원 누구나 이해 가능하게
3. 맥락 없이 변경사항만 나열 안함 - 왜 했는지 포함
4. Linear 등록 전 반드시 내용 확인받기
