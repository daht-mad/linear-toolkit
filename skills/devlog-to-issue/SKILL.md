---
name: devlog-to-issue
description: DEVLOG.md 파일을 분석하여 Linear 이슈로 변환. 완료된 작업 기록 및 향후 계획 이슈 생성. "/devlog-to-issue", "데브로그 이슈로", "DEVLOG Linear 변환" 등으로 호출.
---

# DEVLOG → Linear 이슈 변환

DEVLOG.md 파일을 분석하여 Linear 이슈를 생성/업데이트한다.

## 기본값

| 항목 | 기본값 | 예외 |
|------|--------|------|
| 담당자 | 스킬 사용자 (me) | 명시적 지정 시 다른 사람 |
| 상태 | Todo | - |
| 사이클 | 오늘 날짜 기준 현재 사이클 | 범위 밖이면 dueDate |
| 프로젝트 | active 프로젝트 중 추천 → 사용자 확인 | - |

## 이슈 형식

```markdown
## 배경
[왜 해야 하는지]

## 상세내용
[구체적 맥락, 관련 데이터, 참고 문서]

## To Do
- [x] 완료된 항목 (DEVLOG 기반 완료 작업)
- [ ] 미완료 항목 (향후 계획)
```

## 워크플로우

### Phase 1: DEVLOG 분석

1. DEVLOG.md 파일 경로 받기
2. 파일 읽기
3. 핵심 정보 추출:
   - 배경/문제 인식
   - 진행한 작업 목록 (완료된 것들)
   - 주요 결정 사항
   - 미완료/후속 작업

### Phase 2: 완료된 작업 이슈 생성/업데이트

**분기**: 기존 이슈 URL 있는가?

| 케이스 | 동작 |
|--------|------|
| URL 있음 | `linear_updateIssue`로 description 업데이트 |
| URL 없음 | `linear_createIssue`로 새 이슈 생성 + 메타데이터 설정 |

이슈 description 작성:
- **배경**: 왜 이 작업을 했는지
- **상세내용**: 구체적 맥락, 주요 결정 사항
- **To Do**: Phase별 체크리스트 (**`- [x]` 체크된 상태**)

### Phase 3: 향후 계획 도출

1. DEVLOG에서 후속 작업 파악
2. 사용자에게 추가 할 일 질문
3. 할 일 목록 제안 (예상 시점 포함)
4. 사용자 확인 및 조정

### Phase 4: 개별 이슈 내용 작성

각 할 일별 세부내용 작성:
- **배경**: 왜 해야 하는지
- **상세내용**: 구체적 맥락, 관련 데이터
- **To Do**: 체크리스트 (**`- [ ]` 미체크 상태**)

사용자 승인 후 진행.

### Phase 5: 메타데이터 정보 수집

1. 필요 정보 조회 (병렬):
   - `linear_getTeams` → 팀 ID
   - `linear_getWorkflowStates` → Todo 상태 ID
   - `linear_getCycles` → 오늘 날짜 기준 현재 사이클
   - `linear_getProjects` → active 프로젝트 목록
   - `linear_getViewer` → 기본 담당자 ID

2. 프로젝트 추천:
   - active 프로젝트 중 DEVLOG 내용과 관련성 높은 것 추천
   - 사용자에게 확인

3. 담당자 결정:
   - 기본: 스킬 사용자 (`linear_getViewer`)
   - 명시적 요청 시: `linear_getUsers`로 다른 사용자 검색

4. 사이클 결정:
   - 오늘 날짜 기준 현재 사이클 식별
   - 각 이슈별 예상 시점에 맞는 사이클 매핑
   - 사이클 범위 밖이면 dueDate 설정

### Phase 6: Linear 이슈 생성

`linear_createIssue` × N개 병렬 호출:
- title
- teamId
- description (배경/상세내용/To Do)
- stateId (Todo)
- assigneeId (담당자)
- projectId (선택한 프로젝트)
- cycleId 또는 dueDate

### Phase 7: 결과 요약

생성/업데이트된 이슈 목록 테이블 출력:

| 이슈 | 제목 | 담당자 | 프로젝트 | 사이클 |
|------|------|--------|----------|--------|
| [EDU-1234](링크) | 제목 | 담당자 | 프로젝트 | Cycle N |

## Linear MCP 도구 레퍼런스

도구 상세 사용법은 [references/linear-mcp-tools.md](references/linear-mcp-tools.md) 참조.
