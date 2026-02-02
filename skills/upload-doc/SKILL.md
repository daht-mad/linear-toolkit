---
name: upload-doc
description: 마크다운 파일을 Linear 프로젝트 Resources에 문서로 추가. "/upload-doc", "리니어에 문서 추가", "프로젝트에 md 파일 올려줘" 등으로 호출. Linear MCP에서 지원하지 않는 documentCreate API를 직접 호출.
---

# upload-doc

마크다운 파일을 Linear 프로젝트 Resources에 문서로 추가

## 사용법

```
/upload-doc <파일경로> [프로젝트명]
```

**예시:**
- `/upload-doc ./docs/spec.md "커뮤니티 유지"`
- `/upload-doc ~/plan.md` (대화형 프로젝트 선택)

## 스크립트

```bash
# 문서 생성 (MCP에 없음)
node scripts/create-doc.mjs "<파일경로>" "<프로젝트ID>" "<제목>"
```

## 워크플로우

### 1. 인자 확인

`$ARGUMENTS`에서 파싱:
- 첫 번째: 파일 경로 (필수)
- 나머지: 프로젝트 지정자 (선택)

### 2. 파일 검증

- 파일 존재/확장자(.md) 확인
- 제목 추출: 첫 `# ` 헤딩 또는 파일명

### 3. 프로젝트 조회

`linear_getProjects` MCP로 프로젝트 목록 조회

- 지정자 있음: ID/이름 매칭 → 여러 개면 선택 요청
- 지정자 없음: 목록 표시 후 선택 요청

### 4. 확인 및 생성

```
다음 문서를 Linear에 추가합니다:
- 제목: {title}
- 프로젝트: {projectName}
- 미리보기: {첫 200자...}

진행할까요? (제목 변경 시 새 제목 입력)
```

### 5. 결과

**성공:** Document ID 반환
**실패:** 에러 메시지 및 해결 방법

## 환경변수

```
LINEAR_API_TOKEN=lin_api_xxxxxxxxxxxxx
```

.env 파일 위치: 프로젝트 루트 또는 `~/.env`
