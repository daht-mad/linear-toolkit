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

## 기본값

| 항목 | 기본값 | ID |
|------|--------|-----|
| 담당자 | `me` (linear_getViewer로 조회) | - |
| 상태 | `Todo` | `6dc4154e-3a35-43d2-ac44-e3d66df85c9b` |
| 팀 | `Education` | - |

---

## 워크플로우

### Step 1: 정보 수집
- 사용자로부터 이슈 제목, 내용 수집
- 프로젝트 지정 여부 확인

### Step 2: 프로젝트 조회
- `linear_getProjects` 호출
- 활성 프로젝트 목록 표시 (state: "started" 또는 "planned")

### Step 3: Description 작성
- 위 템플릿 형식으로 description 구성
- 배경 / 상세내용 / To Do 섹션 포함

### Step 4: 생성 전 확인 (MANDATORY)

```
이슈를 생성합니다. 확인해주세요:

- **프로젝트**: [프로젝트명]
- **제목**: [이슈 제목]
- **담당자**: [담당자명] (기본: 나)
- **상태**: Todo

**Description 미리보기:**
---
[템플릿 기반 내용]
---

진행할까요?
```

### Step 5: 이슈 생성

**승인 후** `linear_createIssue` 호출:

```
파라미터:
- title: [제목]
- teamId: [팀 ID]
- description: [템플릿 기반 내용]
- stateId: "6dc4154e-3a35-43d2-ac44-e3d66df85c9b"  ← MANDATORY
- assigneeId: [담당자 ID 또는 me]
- projectId: [프로젝트 ID] (선택)
- cycleId: [사이클 ID] (선택)
```

### Step 6: 결과 반환

```
✅ 이슈가 생성되었습니다.

- **ID**: EDU-1234
- **링크**: https://linear.app/geniefy/issue/EDU-1234
```
