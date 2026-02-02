---
name: upload-doc
description: 마크다운 파일을 Linear 프로젝트 Resources에 문서로 추가. "/upload-doc", "리니어에 문서 추가", "프로젝트에 md 파일 올려줘" 등으로 호출. Linear MCP에서 지원하지 않는 documentCreate API를 직접 호출.
---

# Upload Document

마크다운 파일을 Linear 프로젝트의 Resources에 문서로 추가한다.

## 사용법

```
/upload-doc <파일경로> [프로젝트명]
```

**예시:**
- `/upload-doc ./docs/spec.md "커뮤니티 유지"`
- `/upload-doc ~/plan.md` (대화형 프로젝트 선택)

## 워크플로우

### Step 1: 인자 확인

`$ARGUMENTS`에서 파싱:
- 첫 번째 인자: 파일 경로 (필수)
- 나머지: 프로젝트 지정자 (선택)

인자 없으면 사용법 안내 후 중단.

### Step 2: 파일 검증

1. 파일 존재 확인
2. `.md` 확장자 확인
3. 파일 내용 읽기
4. 제목 추출: 첫 `# ` 헤딩 또는 파일명

### Step 3: 프로젝트 조회

`linear_getProjects` MCP로 프로젝트 목록 조회.

**프로젝트 지정자 있음:**
1. ID 정확 매칭 (UUID 형식)
2. 이름 부분 매칭 (대소문자 무시)
3. 여러 개 매칭 시 선택 요청

**프로젝트 지정자 없음:**
프로젝트 목록 표시 후 선택 요청.

### Step 4: 확인 및 생성

사용자에게 확인:
```
다음 문서를 Linear에 추가합니다:
- 제목: {title}
- 프로젝트: {projectName}
- 미리보기: {첫 200자...}

진행할까요? (제목 변경 시 새 제목 입력)
```

### Step 5: API 호출

스크립트 실행:
```bash
node ~/.claude/plugins/linear-toolkit/skills/upload-doc/scripts/create-doc.mjs "<파일경로>" "<프로젝트ID>" "<제목>"
```

환경변수 `LINEAR_API_TOKEN` 필요.

### Step 6: 결과 리포트

**성공:**
```
문서 생성 완료
- 제목: {title}
- 프로젝트: {projectName}
- Document ID: {id}
```

**실패:** 에러 메시지 및 해결 방법 안내.

## 에러 처리

| 상황 | 대응 |
|------|------|
| 파일 없음 | 경로 확인 안내 |
| 프로젝트 매칭 없음 | 유사 목록 표시 |
| 토큰 없음 | LINEAR_API_TOKEN 설정 안내 |
| API 오류 | 에러 메시지 표시 |
