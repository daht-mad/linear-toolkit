---
name: devlog-to-issue
description: DEVLOG.md 파일을 분석하여 Linear 이슈로 변환. 완료된 작업 기록 및 향후 계획을 맥락까지 포함한 이슈로 생성. "/devlog-to-issue", "데브로그 이슈로", "DEVLOG Linear 변환" 등으로 호출.
---

# DEVLOG → Linear 이슈 변환

DEVLOG.md 파일을 분석하여 **맥락이 포함된 Linear 이슈**를 생성/업데이트한다.

## 핵심 기능

DEVLOG에서 추출한 "다음에 할 일"을 단순 제목이 아닌 **맥락까지 포함한 완전한 이슈**로 변환:

- **배경**: 왜 이 작업이 필요한지 (DEVLOG의 문제 인식에서 추출)
- **상세내용**: 구체적 맥락, 결정 사항, 관련 데이터 (DEVLOG 내용에서 추출)
- **To Do**: 실행 가능한 체크리스트

> 나중에 이슈만 봐도 "왜 해야 하는지", "어떤 맥락인지" 바로 파악 가능

## 이슈 템플릿

모든 이슈는 아래 템플릿으로 description 작성:

```markdown
## 배경
[왜 해야 하는지 - DEVLOG의 문제 인식, 필요성에서 추출]

## 상세내용
[구체적 맥락, 관련 데이터, 참고 문서, 결정 사항 - DEVLOG 내용에서 추출]

## To Do
- [x] 완료된 항목 (DEVLOG 기반 완료 작업)
- [ ] 미완료 항목 (향후 계획)
```

## 기본값

| 항목 | 기본값 | 예외 |
|------|--------|------|
| 담당자 | 스킬 사용자 (me) | 명시적 지정 시 다른 사람 |
| 상태 | Todo | - |
| 사이클 | 오늘 날짜 기준 현재 사이클 | 범위 밖이면 dueDate |
| 프로젝트 | active 프로젝트 중 추천 → 사용자 확인 | - |

## 워크플로우

### Phase 1: DEVLOG 분석

1. DEVLOG.md 파일 경로 받기
2. 파일 읽기
3. 핵심 정보 추출:
   - 배경/문제 인식 → 이슈 "배경" 섹션으로
   - 진행한 작업 목록 (완료된 것들) → "To Do"의 `[x]` 항목으로
   - 주요 결정 사항 → "상세내용" 섹션으로
   - 미완료/후속 작업 → 별도 이슈의 "To Do"로

### Phase 2: 완료된 작업 이슈 생성/업데이트

**분기**: 기존 이슈 URL 있는가?

| 케이스 | 동작 |
|--------|------|
| URL 있음 | `linear_updateIssue`로 description 업데이트 |
| URL 없음 | `linear_createIssue`로 새 이슈 생성 + 메타데이터 설정 |

### Phase 3: 향후 계획 → 개별 이슈 생성

1. DEVLOG에서 후속 작업 파악
2. 각 할 일에 대해 **맥락 포함한 이슈** 작성:
   - **배경**: 왜 해야 하는지 (원래 DEVLOG의 맥락에서 추출)
   - **상세내용**: 구체적 맥락, 관련 데이터
   - **To Do**: 체크리스트 (`- [ ]` 미체크 상태)
3. 사용자 확인 및 조정

### Phase 4: 메타데이터 수집 및 이슈 생성

1. 필요 정보 조회 (병렬):
   - `linear_getTeams` → 팀 ID
   - `linear_getWorkflowStates` → Todo 상태 ID
   - `linear_getCycles` → 오늘 날짜 기준 현재 사이클
   - `linear_getProjects` → active 프로젝트 목록
   - `linear_getViewer` → 기본 담당자 ID

2. `linear_createIssue` × N개 호출

### Phase 5: 결과 요약

생성/업데이트된 이슈 목록 테이블 출력:

| 이슈 | 제목 | 담당자 | 프로젝트 | 사이클 |
|------|------|--------|----------|--------|
| [EDU-1234](링크) | 제목 | 담당자 | 프로젝트 | Cycle N |

## Linear MCP 도구 레퍼런스

도구 상세 사용법은 [references/linear-mcp-tools.md](references/linear-mcp-tools.md) 참조.
