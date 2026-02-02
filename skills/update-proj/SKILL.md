---
name: update-proj
description: Linear 프로젝트의 Cycle 기반 업데이트를 결과물 중심으로 자동 생성하고 Linear에 직접 등록. "/update-proj", "프로젝트 업데이트 써줘", "프로젝트 업데이트 작성" 등으로 호출. 이슈 나열이 아닌 '무엇이 달라졌는지' 중심으로 작성.
---

# update-proj

프로젝트 주간 업데이트를 **결과물 중심**으로 자동 생성 → Linear 등록

## 핵심 원칙

- 이슈 나열 ❌ → 뭐가 달라졌는지/달라질지 중심
- 맥락 포함 (기존 문제 → 변경 사항 → 완료 작업)
- 이슈 번호 생략, ~요/~합니다 말투 금지

## 스크립트 (Linear MCP 버그 우회)

Linear MCP의 state 필드 버그로 스크립트 사용:

```bash
# 내 프로젝트 목록 (started 상태, 리드/멤버)
python scripts/linear_api.py my-projects

# 프로젝트 이슈 (state, cycle 포함)
python scripts/linear_api.py project-issues <project_id>

# Cycle 정보
python scripts/linear_api.py active-cycle <team_id>
python scripts/linear_api.py cycles <team_id>

# 업데이트 등록 (MCP에 없음)
python scripts/linear_api.py create-update <project_id> /tmp/update.md --health onTrack
```

## 워크플로우

### 1. 프로젝트 선택

`my-projects` 스크립트로 내가 리드/멤버인 started 프로젝트 조회 → 사용자 선택

### 2. Cycle/이슈 수집

- 현재 Cycle 이슈 = **만든 결과**
- 다음 Cycle 이슈 = **만들 결과**

### 3. 업데이트 작성

이슈를 그룹핑하여 결과물 중심으로 작성. 작성법:

- **말머리/이모지 가이드**: 작성 시 [references/writing-guide.md](references/writing-guide.md) 참조
- **출력 포맷 예시**: 작성 시 [references/output-format.md](references/output-format.md) 참조

**만든 결과 포맷:**
```markdown
## 🔧 [말머리] 결과물 제목

**한 줄 요약**: X를 Y로 개선

**기존 문제**
- 문제점

**변경 사항**
| 구분 | AS-IS | TO-BE |
|------|-------|-------|
| 항목 | 기존 | **변경** |

**완료된 작업**
- 작업 내용
```

**만들 결과 포맷:**
```markdown
## 🔧 [말머리] 결과물 제목

**목표**: 한 줄 설명

- [ ] 할 일
```

### 4. Linear 등록

1. 사용자 확인: "Linear에 바로 올릴까요?"
2. health 선택: 🟢 onTrack / 🟡 atRisk / 🔴 offTrack
3. `create-update` 스크립트 실행
4. 등록된 URL 반환

## 환경변수

```
LINEAR_API_TOKEN=lin_api_xxxxxxxxxxxxx
```

.env 파일 위치: 프로젝트 루트 또는 `~/.env`
