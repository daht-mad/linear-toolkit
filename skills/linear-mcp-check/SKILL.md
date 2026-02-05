---
name: linear-mcp-check
description: "[HOOK - AUTO] Linear MCP 설치 여부 체크 및 자동 설치. create-issue, update-proj, update-init, devlog-to-issue 스킬 실행 전 자동 호출."
hook:
  trigger: before
  skills:
    - create-issue
    - update-proj
    - update-init
    - devlog-to-issue
---

# linear-mcp-check

Linear 스킬 실행 전 MCP 설치 여부를 체크하고, 없으면 자동 설치하는 hook.

---

## 실행 흐름

```
[사용자] /create-issue 테스트
    ↓
[Hook] linear-mcp-check 자동 실행
    ↓
[체크] linear_getViewer 호출 시도
    ├─ 성공 → 원래 스킬 실행 계속
    └─ 실패 → 자동 설치 시도
              ↓
         [설치] claude mcp add linear ...
              ↓
         [확인] 설치 성공 여부 체크
              ├─ 성공 → "MCP 설치 완료" + 원래 스킬 실행
              └─ 실패 → 수동 설치 안내 + 중단
```

---

## Step 1: MCP 설치 여부 체크

`linear_getViewer` MCP 도구 호출 시도:
- **성공** → Step 3 (통과)
- **실패 (도구 없음)** → Step 2 (자동 설치)

---

## Step 2: 자동 설치

### 2-1. 기존 Linear MCP 제거

```bash
# 기존 linear MCP 확인
claude mcp list | grep -i linear

# 있으면 제거
claude mcp remove [발견된-mcp-이름]
```

### 2-2. linear-mcp-plus 설치

```bash
claude mcp add linear -- npx -y @daht-mad/linear-mcp-plus
```

### 2-3. 설치 확인

`linear_getViewer` 다시 호출:
- **성공** → Step 3
- **실패** → 수동 설치 안내 출력 후 **중단**

#### 수동 설치 안내 (자동 설치 실패 시)

```
❌ Linear MCP 자동 설치에 실패했습니다.

수동으로 설치해주세요:

1. 터미널에서 실행:
   claude mcp add linear -- npx -y @daht-mad/linear-mcp-plus

2. Linear API 토큰 설정:
   - https://linear.app/settings/api 에서 토큰 발급
   - 환경변수 LINEAR_API_TOKEN 설정

3. Claude Code 재시작

설치 완료 후 다시 시도해주세요.
```

---

## Step 3: 통과

```
✅ Linear MCP 확인 완료. 스킬을 실행합니다.
```

원래 요청된 스킬 (create-issue 등) 실행 계속.

---

## 주의사항

- 이 hook은 **자동 실행**됩니다. 사용자가 직접 호출할 필요 없음.
- LINEAR_API_TOKEN 환경변수가 없으면 MCP가 설치되어도 인증 실패함.
- Claude Code 재시작이 필요할 수 있음 (MCP 최초 설치 시).
