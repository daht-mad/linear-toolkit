---
name: create-issue
description: Linear 이슈 생성 커맨드. "/create-issue"로 호출하거나 Linear에 이슈를 등록하려 할 때 사용. 기본값으로 상태는 Todo, 담당자는 me(나)로 설정.
---

# Linear 이슈 생성

Linear에 이슈를 생성하는 스킬. 생성 전 사용자 확인을 받는다.

## 워크플로우

1. 사용자로부터 이슈 정보 수집 (제목, 설명 등)
2. 프로젝트 목록 조회 (`list_projects` with `member: me`)
3. **생성 전 확인**: 아래 정보를 사용자에게 표시하고 승인 요청
   - 프로젝트
   - 제목
   - 담당자 (기본값: me)
   - 상태 (기본값: Todo)
4. 승인 후 이슈 생성

## 기본값

| 항목 | 기본값 |
|------|--------|
| 담당자 | `me` |
| 상태 | `Todo` |
| 팀 | `Education` |

## 확인 메시지 형식

```
이슈를 생성합니다. 확인해주세요:

- **프로젝트**: [프로젝트명]
- **제목**: [이슈 제목]
- **담당자**: [담당자명] (기본: 나)
- **상태**: [상태] (기본: Todo)

진행할까요?
```

## 이슈 생성

확인 후 `mcp__linear-server__create_issue` 호출:

```
team: Education
title: [제목]
description: [설명]
project: [프로젝트 ID]
assignee: me
state: Todo
```

## 생성 완료 메시지

생성 후 이슈 ID와 Linear 링크 제공.
