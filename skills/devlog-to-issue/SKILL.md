---
name: devlog-to-issue
description: DEVLOG.md 파일을 분석하여 Linear 이슈로 변환. 완료된 작업 기록 및 향후 계획을 맥락까지 포함한 이슈로 생성. "/devlog-to-issue", "데브로그 이슈로", "DEVLOG Linear 변환" 등으로 호출.
---

# devlog-to-issue

DEVLOG.md를 분석하여 **맥락이 포함된 Linear 이슈** 생성/업데이트

## 핵심 기능

DEVLOG에서 추출한 정보를 완전한 이슈로 변환:
- **배경**: 왜 이 작업이 필요한지
- **상세내용**: 구체적 맥락, 결정 사항
- **To Do**: 완료([x]) + 미완료([ ]) 항목

## 이슈 템플릿

```markdown
## 배경
[DEVLOG의 문제 인식에서 추출]

## 상세내용
[구체적 맥락, 관련 데이터, 결정 사항]

## To Do
- [x] 완료된 항목
- [ ] 미완료 항목
```

## 기본값

| 항목 | 기본값 |
|------|--------|
| 담당자 | `me` |
| 상태 | `Todo` |
| 사이클 | 오늘 기준 현재 사이클 |
| 프로젝트 | active 중 추천 → 사용자 확인 |

## 워크플로우

### 1. DEVLOG 분석

파일 읽고 추출:
- 배경/문제 인식 → 이슈 "배경" 섹션
- 진행한 작업 → To Do `[x]` 항목
- 주요 결정 사항 → "상세내용" 섹션
- 미완료/후속 작업 → 별도 이슈

### 2. 완료된 작업 처리

| 케이스 | 동작 |
|--------|------|
| 기존 이슈 URL 있음 | `linear_updateIssue`로 업데이트 |
| URL 없음 | `linear_createIssue`로 새 이슈 |

### 3. 향후 계획 → 개별 이슈

각 후속 작업에 맥락 포함한 이슈 작성 → 사용자 확인

### 4. 메타데이터 수집 (병렬)

- `linear_getTeams` → 팀 ID
- `linear_getWorkflowStates` → Todo 상태 ID
- `linear_getCycles` → 현재 사이클
- `linear_getProjects` → active 프로젝트
- `linear_getViewer` → 담당자 ID

### 5. 결과 요약

| 이슈 | 제목 | 담당자 | 프로젝트 | 사이클 |
|------|------|--------|----------|--------|
| [EDU-1234](링크) | 제목 | 담당자 | 프로젝트 | Cycle N |

## 참고

Linear MCP 도구 상세: [references/linear-mcp-tools.md](references/linear-mcp-tools.md) (사이클 매핑, 이슈 ID 추출 등)
