# Linear MCP 도구 레퍼런스

## 조회 도구

### linear_getTeams
팀 목록 조회. 이슈 생성 시 `teamId` 필요.

### linear_getViewer
현재 인증된 사용자 정보. 기본 담당자 ID로 사용.

### linear_getWorkflowStates
팀별 워크플로우 상태 목록. `type: "unstarted"`, `name: "Todo"` 찾아서 `stateId`로 사용.

```
필요 파라미터: teamId
```

### linear_getCycles
사이클 목록. 오늘 날짜가 `startsAt` ~ `endsAt` 범위에 있는 사이클이 현재 사이클.

```
필요 파라미터: teamId (선택)
```

### linear_getProjects
프로젝트 목록. `state: "started"` 또는 `state: "planned"`가 active 프로젝트.

### linear_getUsers
사용자 목록. 담당자 명시적 지정 시 검색용.

## 생성/수정 도구

### linear_createIssue

```
필수: title, teamId
선택: description, stateId, assigneeId, projectId, cycleId, dueDate, priority
```

### linear_updateIssue

```
필수: id (이슈 ID 또는 식별자, 예: "EDU-1234")
선택: title, description, stateId, assigneeId, projectId, cycleId, dueDate
```

## 사이클 매핑 로직

```
오늘 = 2026-01-30

사이클 목록:
- Cycle 74: 2026-01-30 ~ 2026-02-06 ← 현재
- Cycle 75: 2026-02-06 ~ 2026-02-13 ← 다음

이슈 예상 시점별 매핑:
- 즉시, 이번 주 → 현재 사이클
- 다음 주, 2주 내 → 다음 사이클
- 범위 밖 (ex: 3월 1일) → cycleId 없이 dueDate 사용
```

## 이슈 URL에서 ID 추출

```
URL: https://linear.app/geniefy/issue/EDU-5580/제목
ID: EDU-5580
```

`linear_updateIssue`의 `id` 파라미터에 "EDU-5580" 형태로 전달.

## 확장 도구 (@daht-mad/linear-mcp-plus)

### linear_projectUpdateCreate
프로젝트 업데이트 생성. 주간/스프린트 진행 보고용.

```
필수: projectId, body (마크다운)
선택: health (onTrack | atRisk | offTrack)
```

### linear_initiativeUpdateCreate
이니셔티브 업데이트 생성. 상위 이니셔티브 진행 보고용.

```
필수: initiativeId, body (마크다운)
선택: health (onTrack | atRisk | offTrack)
```

### linear_documentCreate
Linear 문서 생성. 프로젝트 Resources에 문서 추가.

```
필수: title, content (마크다운)
선택: projectId (프로젝트에 연결 시)
```

### linear_getProjectUpdates
프로젝트 업데이트 목록 조회.

```
필수: projectId
선택: limit (기본: 25)
```

### linear_updateProjectLead
프로젝트 리드 변경.

```
필수: projectId, leadId (null이면 리드 제거)
```

### linear_getInitiatives
이니셔티브 목록 조회.

```
선택: includeArchived (기본: false), limit (기본: 50)
```

### linear_getInitiativeProjects
이니셔티브에 연결된 프로젝트 목록 조회.

```
필수: initiativeId
선택: includeArchived (기본: false)
```
