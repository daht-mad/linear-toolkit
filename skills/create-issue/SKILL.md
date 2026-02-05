---
name: create-issue
description: "[MANDATORY - NEVER BYPASS] MUST use this skill for ALL Linear issue creation. NEVER call linear_createIssue MCP directly - doing so creates issues as Triage instead of Todo. Triggers: 'create issue', 'Linear issue', '/create-issue', '이슈 생성', '이슈 만들어'. Requires: @daht-mad/linear-mcp-plus MCP."
---

# create-issue

맥락이 포함된 Linear 이슈를 생성

---

## Prerequisites (MANDATORY - DO NOT SKIP)

### Step 0: MCP 설치 확인

**이 스킬 실행 전 반드시 확인**:

1. `linear_getViewer` MCP 도구 호출 시도
2. **성공** → Step 1로 진행
3. **실패 (도구 없음)** → 아래 안내 출력 후 **즉시 중단**

#### MCP 미설치 시 출력할 안내

```
❌ Linear MCP가 설치되지 않았습니다.

이 스킬은 @daht-mad/linear-mcp-plus MCP가 필수입니다.

📦 설치 방법:

1. 기존 Linear MCP 확인 및 제거:
   claude mcp list | grep -i linear
   # 결과가 있으면 제거:
   claude mcp remove [기존-linear-mcp-이름]

2. linear-mcp-plus 설치:
   claude mcp add linear -- npx -y @daht-mad/linear-mcp-plus

3. Linear API 토큰 설정:
   - https://linear.app/settings/api 에서 토큰 발급
   - 환경변수 LINEAR_API_TOKEN 설정

4. Claude Code 재시작

설치 완료 후 다시 시도해주세요.
```

---

## CRITICAL RULES (NEVER VIOLATE)

### 1. API Fallback 금지

| 금지 행위 | 이유 |
|-----------|------|
| MCP 없을 때 Linear API 직접 호출 | 이 스킬의 목적을 우회함 |
| curl/fetch로 api.linear.app 요청 | MCP 없이는 작업 불가 |
| @linear/sdk 직접 사용 | MCP 필수 |

**반드시**: MCP 도구가 없으면 설치 안내 출력 후 **작업 중단**. 대안 시도 금지.

### 2. stateId 필수

| 상황 | 결과 |
|------|------|
| stateId 포함 | ✅ Todo로 생성 |
| stateId 생략 | ❌ Triage로 생성 (문제!) |

**반드시**: `linear_createIssue` 호출 시 `stateId` 파라미터 포함.

### 3. 스킬 사용 강제

**이 스킬을 거치지 않고 `linear_createIssue` MCP를 직접 호출하면**:
- stateId 누락으로 Triage 생성
- 템플릿 미적용으로 맥락 없는 이슈 생성
- 확인 단계 생략으로 실수 가능성 증가

---

## 이슈 템플릿

```markdown
## 배경
[왜 해야 하는지 - 문제 상황, 필요성]

## 상세내용
[구체적 맥락, 관련 데이터, 참고 문서, 결정 사항]

## To Do
- [ ] 할 일 1
- [ ] 할 일 2
```

---

## 기본값 (MANDATORY - 모든 이슈에 적용)

| 항목 | 기본값 | 강제 여부 |
|------|--------|----------|
| 담당자 | Step 0에서 조회한 viewer ID | **필수** |
| 상태 | Todo (`6dc4154e-3a35-43d2-ac44-e3d66df85c9b`) | **필수** |
| 팀 | Education (`e108ae14-a354-4c09-86ac-6c1186bc6132`) | **필수** |
| 프로젝트 | 사용자가 선택 | **필수** |

---

## 워크플로우

### Step 0: 초기 데이터 조회 (MANDATORY - 모든 이슈 생성 전 실행)

**반드시 실행**:
```
1. linear_getViewer 호출 → viewer.id 저장 (담당자로 사용)
2. linear_getProjects 호출 → 활성 프로젝트 목록 저장
```

**저장할 값**:
- `VIEWER_ID`: viewer.id (예: "b8ea8eaa-a355-46e2-8e3b-fb15c1f0aae9")
- `ACTIVE_PROJECTS`: state가 "started" 또는 "planned"인 프로젝트들

### Step 1: 정보 수집
- 사용자로부터 이슈 제목, 내용 수집

### Step 2: 프로젝트 선택 (MANDATORY)

**프로젝트는 필수입니다. 반드시 선택받아야 합니다.**

활성 프로젝트 목록을 보여주고 선택받기:
```
프로젝트를 선택해주세요:

1. [프로젝트명 A]
2. [프로젝트명 B]
...

(프로젝트 없이는 이슈를 생성할 수 없습니다)
```

### Step 3: Description 작성
- 위 템플릿 형식으로 description 구성
- 배경 / 상세내용 / To Do 섹션 포함

### Step 4: 생성 전 확인 (MANDATORY)

```
이슈를 생성합니다. 확인해주세요:

- **프로젝트**: [프로젝트명] ← 필수
- **제목**: [이슈 제목]
- **담당자**: 송다혜 (나) ← 자동 설정
- **상태**: Todo ← 자동 설정

**Description 미리보기:**
---
[템플릿 기반 내용]
---

진행할까요?
```

### Step 5: 이슈 생성

**승인 후** `linear_createIssue` 호출:

```
파라미터 (모두 필수):
- title: [제목]
- teamId: "e108ae14-a354-4c09-86ac-6c1186bc6132"  ← Education 팀
- description: [템플릿 기반 내용]
- stateId: "6dc4154e-3a35-43d2-ac44-e3d66df85c9b"  ← Todo 상태 (NEVER OMIT)
- assigneeId: [Step 0에서 조회한 VIEWER_ID]  ← 자동 설정 (NEVER OMIT)
- projectId: [Step 2에서 선택한 프로젝트 ID]  ← 필수 (NEVER OMIT)
- cycleId: [사이클 ID] (선택)
```

**절대 금지**:
- stateId 생략 → Triage로 생성됨
- assigneeId 생략 → 담당자 없음
- projectId 생략 → 프로젝트 미연결

### Step 6: 결과 반환

```
✅ 이슈가 생성되었습니다.

- **ID**: EDU-1234
- **링크**: https://linear.app/geniefy/issue/EDU-1234
- **프로젝트**: [프로젝트명]
- **담당자**: 송다혜
- **상태**: Todo
```
