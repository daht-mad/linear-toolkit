# Linear Toolkit - 개발 로그

AI 코딩 도구와 함께 진행한 개발 작업 기록입니다.

---

## 목차

### Day 1 (2026-01-30)
1. [devlog-to-linear 스킬 설계 및 생성](#1-devlog-to-linear-스킬-설계-및-생성)
2. [Linear MCP 선택을 위한 비교 조사](#2-linear-mcp-선택을-위한-비교-조사)
3. [MCP 선택 결정](#3-mcp-선택-결정)
4. [Linear 프로젝트 document 추가 시도 (upload-doc 스킬 탄생 배경)](#4-linear-프로젝트-document-추가-시도-upload-doc-스킬-탄생-배경)
5. [proj-update 스킬 테스트, API 자동화 발견, 스킬 개선](#5-proj-update-스킬-테스트-api-자동화-발견-스킬-개선)
   - 5-1. [스킬 최초 실행 및 환경 설정](#5-1-스킬-최초-실행-및-환경-설정)
   - 5-2. [API 자동화 가능성 발견](#5-2-api-자동화-가능성-발견)
   - 5-3. [skill-creator로 proj-update 스킬 개선](#5-3-skill-creator로-proj-update-스킬-개선)
   - 5-4. [MCP vs SDK 토큰 효율성 논의](#5-4-mcp-vs-sdk-토큰-효율성-논의)
   - 5-5. [하이브리드 방식 결정](#5-5-하이브리드-방식-결정)
   - 5-6. [README 작성](#5-6-readme-작성)
6. [MCP vs SDK 방식 결정 및 init-update 스킬 최적화](#6-mcp-vs-sdk-방식-결정-및-init-update-스킬-최적화)
7. [init-update 스킬 기획](#7-init-update-스킬-기획)
8. [init-update 스킬 구현](#8-init-update-스킬-구현)
9. [스킬명 변경 (네이밍 일관성 개선)](#9-스킬명-변경-네이밍-일관성-개선)
10. [Linear MCP 버그 우회](#10-linear-mcp-버그-우회)
11. [MCP 패키지명 수정](#11-mcp-패키지명-수정)
12. [초기 플러그인 생성 (GitHub 배포)](#12-초기-플러그인-생성-github-배포)
13. [플러그인 설치 테스트](#13-플러그인-설치-테스트)

### Day 2 (2026-02-02)
1. [스킬 구조 검토 요청](#1-스킬-구조-검토-요청)
2. [skill-creator 가이드라인 적용](#2-skill-creator-가이드라인-적용)
3. [GitHub 배포](#3-github-배포)

---

## 2026-01-30 (Day 1)

### 1. devlog-to-linear 스킬 설계 및 생성

```
이 기능을 스킬로 만들지 커맨드로 만들지?
```

**배경:**
- gpters-partners 프로젝트에서 DEVLOG.md 작성 후, 이를 Linear 이슈로 변환하는 자동화 필요

**OpenCode 작업:**
- 스킬 vs 커맨드 비교 분석

| 비교 | 스킬 | 커맨드 |
|------|------|--------|
| 호출 | `/devlog-to-linear` | `claude devlog-to-linear --path ...` |
| 실행 방식 | 대화형, 중간중간 확인 | 한 번에 자동 실행 |
| 유연성 | 컨텍스트에 따라 적응 | 입력/출력 고정 |

**결정:** 스킬이 더 적합 (프로젝트 추천 확인, 할 일 조정, 이슈 내용 승인 등 사용자 상호작용 필요)

**skill-creator 프로세스:**
1. `init_skill.py devlog-to-linear` 실행
2. scripts/, assets/ 폴더 삭제 (Linear MCP 사용하므로 불필요)
3. SKILL.md 작성

**스킬 구조:**
- **100% MCP 기반** (스크립트 없음)
- Linear MCP 도구: `linear_getTeams`, `linear_getWorkflowStates`, `linear_getCycles`, `linear_getProjects`, `linear_getViewer`, `linear_getUsers`, `linear_createIssue`, `linear_updateIssue`

**이슈 형식:**
```markdown
## 배경
[왜 해야 하는지]

## 상세내용
[구체적 맥락, 관련 데이터, 참고 문서]

## To Do
- [x] 완료된 항목
- [ ] 미완료 항목
```

**7단계 워크플로우:**
1. DEVLOG 분석
2. 완료된 작업 이슈 생성/업데이트
3. 향후 계획 도출
4. 개별 이슈 내용 작성
5. 메타데이터 정보 수집
6. Linear 이슈 생성
7. 결과 요약

---

### 2. Linear MCP 선택을 위한 비교 조사

```
공식리니어랑 tacticlaunch mcp 비교해줘
```

**OpenCode 작업:**
- 공식 Linear MCP와 @tacticlaunch/mcp-linear 상세 비교 조사
- Librarian 에이전트를 활용해 두 MCP의 전체 도구 목록 수집
- GitHub Issues에서 커뮤니티 피드백 조사

**비교 결과:**

| 항목 | 공식 Linear MCP | @tacticlaunch/mcp-linear |
|------|----------------|--------------------------|
| **도구 수** | 21개 | 42개 |
| **호스팅** | Remote (Linear 관리) | Local (npx) |
| **인증** | OAuth 2.1 | API Key |
| **Initiative 지원** | ❌ | ✅ (10개 도구) |
| **Cycle 지원** | ❌ | ✅ (3개 도구) |
| **이슈 관계 설정** | ❌ | ✅ |

---

### 3. MCP 선택 결정

```
이니셔티브, 사이클 기능이 필요한데 안정성도 중요해. 혹시 방법이 있을까?
```

**OpenCode 작업:**
- 하이브리드 설정(MCP 2개 사용) 방안 제시
- 사용자가 "MCP 2개나 설치하면 토큰 비효율적" 피드백
- 최종 결정: **@tacticlaunch/mcp-linear 단독 사용**

**선택 이유:**
- Initiative, Cycle 관리 기능 필수
- 토큰 효율성을 위해 MCP 하나만 사용
- 알려진 버그는 `getLabels()` 하나뿐 (우회 가능)

---

### 4. Linear 프로젝트 document 추가 시도 (upload-doc 스킬 탄생 배경)

```
/Users/dahye.dyan/Documents/DEV/gpters-partners/docs/지피터스_파트너스_외부용_v2.md 
이 문서를 혹시 커뮤니티 유지 및 관리 프로젝트 하위 document로 넣을 수 있니?
```

**OpenCode 작업:**
- Linear 프로젝트의 Resources 탭에 document 추가 방법 탐색
- Linear MCP의 `linear_getProjects`로 프로젝트 ID 확인
- **결과**: Linear MCP에 `documentCreate` API가 없음 발견

**대안 검토:**
1. 프로젝트 content에 전체 내용 추가 (API로 가능)
2. 이슈로 생성 후 연결
3. Linear UI에서 직접 추가

**추가 탐색:**
- Linear SDK/API 문서 조사 (Context7)
- Linear GraphQL API에서 `documentCreate` mutation 존재 확인
- → **SDK로 직접 API 호출하면 가능**하다는 결론

**핵심 발견:**
- Linear MCP는 document 관련 API를 제공하지 않음
- Linear GraphQL API에는 `documentCreate` mutation이 존재
- → `upload-doc` 스킬에서 직접 API 호출 방식 채택

---

### 5. proj-update 스킬 테스트, API 자동화 발견, 스킬 개선

#### 5-1. 스킬 최초 실행 및 환경 설정

```
/proj-update
```

**OpenCode 작업:**
- proj-update 스킬 실행 시도
- Linear MCP `disabled: true` 상태 발견
- `.env` 파일 토큰 설정 가이드 작성

**해결 과정:**
1. `linear_getViewer()` MCP 호출 실패
2. GraphQL API 직접 호출 시도 → 인증 실패
3. `.env.example` 파일 생성
4. 토큰 형식 문제 발견 및 해결

**.env.example 내용:**
```
# Linear API Token
# https://linear.app/settings/api 에서 발급
LINEAR_API_TOKEN=lin_api_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

---

#### 5-2. API 자동화 가능성 발견

```
혹시 리니어 api 사용하면 프로젝트 업데이트도 자동으로 할 수 있니? ultrathink
```

**OpenCode 작업:**
- Linear GraphQL API 스키마 탐색
- `projectUpdateCreate` mutation 발견!

**핵심 발견:**
```graphql
mutation projectUpdateCreate($input: ProjectUpdateCreateInput!) {
  projectUpdateCreate(input: $input) {
    projectUpdate {
      id
      body
      health
    }
  }
}
```

**input 필드:**
- `projectId` (필수): 프로젝트 ID
- `body` (필수): 업데이트 내용 (Markdown)
- `health`: onTrack | atRisk | offTrack

---

#### 5-3. skill-creator로 proj-update 스킬 개선

**OpenCode 작업:**
- skill-creator 가이드 참고하여 스킬 구조 분석
- `scripts/linear_api.py` 스크립트 생성

**생성된 스크립트 기능:**
```python
# linear_api.py 명령어
python linear_api.py viewer              # 현재 사용자 정보
python linear_api.py my-projects         # 내 프로젝트 목록
python linear_api.py project-issues <id> # 프로젝트 이슈 목록 (상태 포함)
python linear_api.py cycles <teamId>     # 팀 Cycle 목록
python linear_api.py create-update <id> <body> [health]  # 업데이트 생성
```

**테스트 결과:**
```json
// viewer 명령어 성공
{
  "id": "b8ea8eaa-a355-46e2-8e3b-fb15c1f0aae9",
  "name": "송다혜",
  "email": "dahye@gpters.org"
}
```

---

#### 5-4. MCP vs SDK 토큰 효율성 논의

```
그러면 이 스킬은 mcp 아예 안쓰는 게 맞아?
```

```
혹시 mcp를 매번 갖고있는게 토큰 비효율적일 수 있는데 
이걸 다 api로 하는 것에 대해 좋은 방향인지 알려줘
```

**분석 결과:**

| 방식 | 장점 | 단점 |
|------|------|------|
| **MCP 도구** | 타입 안전, 에러 핸들링, 문서화 | 토큰 소비 (도구 목록) |
| **SDK 스크립트** | 토큰 절약, 커스텀 로직 | 직접 구현 필요 |

**필요한 API 5개:**
1. `viewer` - 현재 사용자 정보
2. `projects` - 내가 리드인 프로젝트 목록
3. `project.issues` - 프로젝트 이슈 목록 (상태 포함)
4. `cycles` - 팀 Cycle 목록
5. `projectUpdateCreate` - 프로젝트 업데이트 생성

---

#### 5-5. 하이브리드 방식 결정

```
근데 만약 리니어 mcp를 어차피 가지고 있을거면 그냥 mcp 쓰는 게 더 유리한지 고민해줘
```

**최종 결정: MCP 조회 + SDK mutation 하이브리드**

| 작업 | 방법 | 이유 |
|------|------|------|
| 사용자/프로젝트 조회 | **Linear MCP** | 이미 MCP 설치됨, 타입 안전 |
| 이슈 조회 (상태 필요) | **SDK 스크립트** | MCP `state` 필드 버그 |
| Cycle 조회 | **Linear MCP** | MCP 지원 |
| `projectUpdateCreate` | **SDK 스크립트** | MCP 미지원 |

**SKILL.md 수정:**
- MCP 사용 가능한 부분은 MCP 도구 호출
- MCP에 없거나 버그 있는 부분만 스크립트 사용

---

#### 5-6. README 작성

```
리드미도 작성하자
```

**OpenCode 작업:**
- proj-update 스킬용 README.md 작성
- 사용법, 필요 API, 출력 형식 문서화

---

### 6. MCP vs SDK 방식 결정 및 init-update 스킬 최적화

```
현재 리니어 mcp가 공식 mcp가 아니야. 이걸 설치한 이유는 공식 mcp에는 
이니셔티브 읽는 기능이 없어. 근데 어차피 내가 proj-update, init-update, 
linear-doc 이런 스킬은 mcp가 제공하지 않는 api를 써야해서 별도 sdk 방식을 
붙여서 만들었어. 어차피 이렇게 별도 sdk 방식을 취할거면, 그냥 공식mcp에 
이니셔티브 읽는 기능만 sdk 방식으로 추가하면 되는게 아닐까?
```

**OpenCode 작업:**
- 공식 MCP vs 비공식 MCP 비교 분석
- 하이브리드 방식(공식 MCP + SDK) 가능성 검토
- 현재 스킬들의 API 사용 방식 정리

**분석 결과:**

| 기능 | 공식 MCP | 비공식 MCP | SDK 직접 호출 |
|------|----------|-----------|--------------|
| 이슈 CRUD | ✅ | ✅ | ✅ |
| 프로젝트 조회 | ✅ | ✅ | ✅ |
| 이니셔티브 조회 | ❌ | ✅ | ✅ |
| `projectUpdateCreate` | ❌ | ❌ | ✅ |
| `initiativeUpdateCreate` | ❌ | ❌ | ✅ |
| `documentCreate` | ❌ | ❌ | ✅ |

**결론:**
- 비공식 MCP를 사용하는 이유: 이니셔티브 조회 기능
- 하지만 스킬들이 이미 SDK 방식으로 구현됨
- → **공식 MCP + 이니셔티브 조회 SDK 추가** 방식도 가능
- 현재 구조 유지 결정 (비공식 MCP가 더 많은 도구 제공)

---

```
리니어 SDK 호출하는거랑 graphql api랑 방식 차이가 뭐고, 
지금 내가 이 스킬들을 사용하는데 있어서 뭐가 효율적인지 생각해
```

**OpenCode 작업:**
- API 호출 방식 비교 분석
- 스크립트 조회 → MCP 조회로 전환

**변경 전후 비교:**

| 기능 | 변경 전 | 변경 후 |
|------|---------|---------|
| 이니셔티브 목록 | 스크립트 `my-initiatives` | **MCP** `linear_getInitiatives` |
| 프로젝트 목록 | 스크립트 `initiative-projects` | **MCP** `linear_getInitiativeProjects` |
| 프로젝트 업데이트 조회 | 스크립트 유지 | 스크립트 유지 (MCP에 없음) |
| 이니셔티브 업데이트 생성 | 스크립트 유지 | 스크립트 유지 (MCP에 없음) |

**최종 API 사용 방식:**

| 작업 | 방법 | 이유 |
|------|------|------|
| 이니셔티브 조회 | Linear MCP | `linear_getInitiatives()` |
| 이니셔티브-프로젝트 연결 | Linear MCP | `linear_getInitiativeProjects()` |
| 프로젝트 업데이트 조회 | 스크립트 | MCP에 없음 |
| `initiativeUpdateCreate` | 스크립트 | MCP에 없음 |

---

### 7. init-update 스킬 기획

```
proj-update 스킬 참고해서 init-update 스킬을 만들고 싶어. 
이니셔티브 리드가 하위 프로젝트들의 update 항목을 보고 
팀원 공유하는 요약을 이니셔티브 업데이트로 올리는 걸 하고싶어.
```

**OpenCode 작업:**
- proj-update 스킬 구조 분석 (SKILL.md, scripts/, references/)
- Linear MCP 이니셔티브 관련 도구 조사:
  - `linear_getInitiatives` - 이니셔티브 목록
  - `linear_getInitiativeById` - 상세 조회
  - `linear_getInitiativeProjects` - 하위 프로젝트
  - `linear_updateInitiative` - 속성 변경

**핵심 발견:**
- Linear MCP에 `initiativeUpdateCreate` mutation이 **없음**
- → 스크립트로 GraphQL API 직접 호출 필요

**설계 결정:**

| 항목 | 결정 |
|------|------|
| 업데이트 주기 | Cycle 기준 |
| 요약 방식 | 하이라이트만 (프로젝트별 1줄) |
| Health 결정 | 하위 프로젝트 health 자동 종합 |

---

### 8. init-update 스킬 구현

```
계획대로 구현해줘
```

**OpenCode 작업:**
- 4단계 워크플로우 설계:
  1. 이니셔티브 선택 (my-initiatives)
  2. 하위 프로젝트 업데이트 수집 (initiative-projects, project-updates)
  3. 하이라이트 중심 업데이트 작성
  4. Linear 등록 (create-initiative-update)

- `scripts/linear_api.py` 구현:
  - `my-initiatives` - 내가 owner인 이니셔티브 조회
  - `initiative-projects` - 이니셔티브 하위 프로젝트
  - `project-updates` - 프로젝트 업데이트 조회
  - `create-initiative-update` - 이니셔티브 업데이트 생성

**Health 자동 종합 로직:**
```
모두 onTrack → 🟢 onTrack
1개라도 atRisk → 🟡 atRisk
1개라도 offTrack → 🔴 offTrack
```

---

### 9. 스킬명 변경 (네이밍 일관성 개선)

```
issue 라는 스킬은 create-issue 라고 바꿔줘. 그리고 devlog-to-issue 라고 해줘.
스킬명 바꾸려면 관련된 모든 거 같이 다 바꿔줘
```

**OpenCode 작업:**
- 스킬 이름 변경 작업:
  - `issue` → `create-issue` (동작 명확화)
  - `devlog-to-linear` → `devlog-to-issue` (일관성)

**변경 내역:**

| 이전 | 이후 | 호출 명령어 |
|------|------|------------|
| `issue` | `create-issue` | `/create-issue` |
| `devlog-to-linear` | `devlog-to-issue` | `/devlog-to-issue` |

**변경 파일:**
1. 폴더명: `~/.claude/skills/issue` → `create-issue`
2. 폴더명: `~/.claude/skills/devlog-to-linear` → `devlog-to-issue`
3. SKILL.md의 `name` 필드
4. SKILL.md의 `description` 내 호출 명령어

---

```
혹시 update-proj, update-init 이렇게 바꿔줄 수 있니?
```

**OpenCode 작업:**
- 접두사 패턴 통일 (`update-*`)

**변경 내역:**

| 이전 | 이후 | 호출 명령어 |
|------|------|------------|
| `proj-update` | `update-proj` | `/update-proj` |
| `init-update` | `update-init` | `/update-init` |

**변경 파일:**
1. 폴더명 변경
2. SKILL.md의 `name`, `description` 수정
3. 스크립트 경로 참조 수정

---

### 10. Linear MCP 버그 우회

```
Linear MCP에서 이슈 상태 조회가 안 돼
```

**OpenCode 작업:**
- Linear MCP의 상태 조회 버그 발견
- MCP 대신 직접 API 호출 방식으로 우회
- `scripts/linear_api.py` 스크립트 추가

---

### 11. MCP 패키지명 수정

```
MCP가 연결 안 되는데?
```

**OpenCode 작업:**
- 잘못된 패키지명 발견: `linear-mcp` → `@tacticlaunch/mcp-linear`
- README.md 및 SKILL.md 내 패키지명 수정

---

### 12. 초기 플러그인 생성 (GitHub 배포)

```
Linear 연동 스킬 플러그인 만들어줘
```

**OpenCode 작업:**
- `~/.claude/plugins/linear-toolkit/` 폴더 구조 생성
- 5개 스킬 초기 버전 작성:
  - `create-issue/SKILL.md` - Linear 이슈 생성
  - `devlog-to-issue/SKILL.md` - DEVLOG를 이슈로 변환
  - `linear-doc/SKILL.md` - 문서 업로드
  - `update-proj/SKILL.md` - 프로젝트 업데이트
  - `update-init/SKILL.md` - 이니셔티브 업데이트
- `install.sh` 설치 스크립트 작성
- Git 저장소 초기화 및 GitHub 배포

**생성된 파일:**
- `skills/create-issue/SKILL.md`
- `skills/devlog-to-issue/SKILL.md`
- `skills/linear-doc/SKILL.md`
- `skills/update-proj/SKILL.md`
- `skills/update-init/SKILL.md`
- `install.sh`
- `README.md`

---

### 13. 플러그인 설치 테스트

```
리니어 툴킷 플러그인 배포해서 설치했는데 안 되었나
```

**OpenCode 작업:**
- `/create-issue` 스킬 호출 시 "Unknown skill" 에러 발생
- Linear MCP 정상 작동 확인 (`linear_getTeams` 호출 성공)

**스킬 vs MCP 도구 차이 설명:**
- **스킬** (`/slack`, `/billing` 등): 사용자가 `/명령어`로 직접 호출
- **MCP 도구**: AI가 직접 호출해서 사용

**해결:**
- 스킬 심링크 설정이 제대로 되지 않았을 가능성
- `install.sh` 스크립트 재실행 필요

---

## 2026-02-02 (Day 2)

### 1. 스킬 구조 검토 요청

```
https://github.com/daht-mad/linear-toolkit 이거 내가 배포한 툴킷인데 
여기 각각 skill 한번씩보고 스킬로서 문제될게 없는지 검토해줘. 
특히 스킬 내용 보면 특정 mcp를 호출하거나 api 코드를 실행하는 지침이 있는데 
skill.md 하나면 되는지 궁금해
```

**OpenCode 작업:**
- GitHub 레포지토리에서 5개 스킬 구조 분석
- 각 스킬별 파일 구성 및 API 방식 정리:

| 스킬 | 파일 구조 | API 방식 | SKILL.md만으로? |
|------|----------|----------|-----------------|
| **create-issue** | SKILL.md만 | Linear MCP | ✅ 가능 |
| **devlog-to-issue** | SKILL.md + references | Linear MCP | ✅ 가능 |
| **linear-doc** | SKILL.md + scripts | MCP + 스크립트 | ❌ 스크립트 필수 |
| **update-init** | SKILL.md + scripts + references | MCP + 스크립트 | ❌ 스크립트 필수 |
| **update-proj** | SKILL.md + scripts + references | MCP + 스크립트 | ❌ 스크립트 필수 |

**발견된 문제점:**
1. **스크립트 경로 하드코딩**: `~/.claude/plugins/...` 절대 경로 사용 → 설치 위치 변경 시 동작 안 함
2. **references 로딩 불명확**: Claude가 하이퍼링크를 자동으로 따라가지 않음
3. **불필요한 README.md**: skill-creator 가이드라인 위반

---

### 2. skill-creator 가이드라인 적용

```
skill-creator 스킬을 활용해서 해당 스킬들을 개선해볼까? 
참고로 linear-doc 스킬은 upload-doc으로 변경했어.
```

**OpenCode 작업:**
- skill-creator 가이드라인 로드 및 적용
- 5개 스킬 전체 리팩토링:

| 스킬 | 변경 내용 |
|------|----------|
| **create-issue** | 91줄 → 55줄 간소화 |
| **devlog-to-issue** | 97줄 → 70줄 간소화, references 로딩 지침 명확화 |
| **upload-doc** | 90줄 → 60줄 간소화, 스크립트 경로 상대 경로로 |
| **update-proj** | 110줄 → 75줄 간소화, README.md 삭제, 스크립트 경로 상대 경로 |
| **update-init** | 123줄 → 80줄 간소화, README.md 삭제, 스크립트 경로 상대 경로 |

**주요 개선:**
- `linear-doc` → `upload-doc` 스킬명 변경
- 스크립트 경로: 절대 경로 → 상대 경로 (`scripts/...`)
- README.md 삭제 (skill-creator 가이드라인 준수)
- references 로딩 지침 명확화: "작성 시 [file.md](file.md) 참조"
- SKILL.md 간소화: 중복 설명 제거, 핵심만 남김

---

### 3. GitHub 배포

```
해줘
```

**OpenCode 작업:**
- 변경사항 스테이징 및 커밋
- GitHub push

**결과:**
```
8 files changed, 146 insertions(+), 488 deletions(-)
```

**342줄 감소** - skill-creator 가이드라인대로 간소화 완료

---

## 커밋 히스토리

| 날짜 | 커밋 | 설명 |
|------|------|------|
| 01/30 | `36f1463` | feat: initial linear-toolkit plugin |
| 01/30 | `bda4eb6` | feat: add install script for skill symlinks |
| 02/02 | `5a0d79a` | fix: use direct API calls instead of MCP for issue state queries |
| 02/02 | `fcaf22b` | docs: improve README with MCP setup, usage examples, and troubleshooting |
| 02/02 | `a38410d` | fix: correct Linear MCP package name to @tacticlaunch/mcp-linear |
| 02/02 | `7f56583` | feat: add issue template (배경/상세내용/To Do) to create-issue and devlog-to-issue |
| 02/02 | `98a7170` | refactor: rename linear-doc skill to upload-doc |
| 02/02 | `a9472ac` | refactor: apply skill-creator guidelines to all skills |

---

## 기술 스택

- **AI 도구**: OpenCode (Claude Code)
- **MCP**: @tacticlaunch/mcp-linear
- **스크립트**: Python (Linear API 직접 호출), Node.js (마크다운 처리)
- **배포**: GitHub (https://github.com/daht-mad/linear-toolkit)

---

## 주요 기능

1. **create-issue**
   - Linear 이슈 생성
   - 기본 템플릿 (배경/상세내용/To Do) 적용

2. **devlog-to-issue**
   - DEVLOG.md 파일을 분석하여 Linear 이슈로 변환
   - 완료된 작업과 향후 계획을 이슈로 생성

3. **upload-doc**
   - 마크다운 파일을 Linear 프로젝트 Resources에 문서로 추가
   - Linear MCP에 없는 `documentCreate` API 직접 호출

4. **update-proj**
   - Linear 프로젝트의 Cycle 기반 업데이트 자동 생성
   - "무엇이 달라졌는지" 중심의 결과물 기반 작성

5. **update-init**
   - 이니셔티브의 Cycle 기반 업데이트 자동 생성
   - 하위 프로젝트 업데이트를 종합하여 이니셔티브 관점으로 재해석
