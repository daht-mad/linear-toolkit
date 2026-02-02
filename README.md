# Linear Toolkit

Linear 업무 자동화를 위한 Claude Code 플러그인.

프로젝트 업데이트, 이슈 생성, 문서 추가 등을 자연어로 처리합니다.

## 사용 예시

```
# 프로젝트 업데이트 작성
> /update-proj
> 프로젝트 업데이트 써줘

# 이슈 생성
> /create-issue 파트너스 자격 검토 기준 정리
> 이거 Linear 이슈로 만들어줘

# DEVLOG를 이슈로 변환
> /devlog-to-issue ./DEVLOG.md
> 이 데브로그 이슈로 등록해줘

# 마크다운을 Linear 문서로
> /linear-doc ./docs/spec.md "프로젝트명"

# 이니셔티브 업데이트
> /update-init
```

## 포함된 스킬

| 스킬 | 호출 | 설명 |
|------|------|------|
| `create-issue` | `/create-issue` | Linear 이슈 생성 (기본: 담당자=me, 상태=Todo) |
| `devlog-to-issue` | `/devlog-to-issue` | DEVLOG.md → Linear 이슈 변환 |
| `update-proj` | `/update-proj` | 프로젝트 Cycle 업데이트 (결과물 중심) |
| `update-init` | `/update-init` | 이니셔티브 업데이트 (프로젝트 종합) |
| `linear-doc` | `/linear-doc` | 마크다운 → Linear 프로젝트 문서 |

## 설치

### 1. Linear MCP 설치

Claude Code 설정에서 Linear MCP를 추가합니다.

**방법 A: Claude Code 명령어**
```bash
claude mcp add linear -- npx -y @linear/mcp-server
```

**방법 B: 수동 설정** (`~/.mcp.json` 또는 `.mcp.json`)
```json
{
  "mcpServers": {
    "linear": {
      "command": "npx",
      "args": ["-y", "@linear/mcp-server"]
    }
  }
}
```

> Linear MCP 첫 실행 시 브라우저에서 OAuth 인증이 진행됩니다.

### 2. 플러그인 설치

```bash
# Git clone
git clone https://github.com/daht-mad/linear-toolkit.git ~/.claude/plugins/linear-toolkit

# 설치 스크립트 실행
~/.claude/plugins/linear-toolkit/install.sh

# Claude Code 재시작
```

### 3. API 토큰 설정

일부 스킬(`update-proj`, `update-init`, `linear-doc`)은 MCP에 없는 API를 사용하므로 토큰이 필요합니다.

**토큰 발급**: [Linear Settings > API](https://linear.app/settings/api) > Personal API keys > Create key

**설정 위치** (둘 중 하나):
```bash
# 프로젝트별
echo "LINEAR_API_TOKEN=lin_api_xxxxx" >> ./.env

# 전역
echo "LINEAR_API_TOKEN=lin_api_xxxxx" >> ~/.env
```

## 스킬별 상세

### `/update-proj` - 프로젝트 업데이트

Cycle 기반으로 "만든 결과 / 만들 결과"를 자동 생성합니다.

```
> /update-proj

# 출력 예시:
# 1. 지피터스 커뮤니티 유지 및 관리 (Lead)
# 2. AI스터디 20기 준비 및 운영 (Member)
#
# 번호를 입력해주세요: 1
#
# --- 만든 결과 (1/24~1/30) ---
# ## [파트너스 시스템] 자격 관리 체계 전면 개편
# ...
#
# Linear에 바로 올릴까요?
```

### `/create-issue` - 이슈 생성

자연어로 이슈를 생성합니다. 프로젝트, Cycle 자동 추천.

```
> /create-issue 파트너스 자격 검토 로직 개선

# 이슈를 생성합니다. 확인해주세요:
# - 프로젝트: 지피터스 커뮤니티 유지 및 관리
# - 제목: 파트너스 자격 검토 로직 개선
# - 담당자: 송다혜 (기본: 나)
# - 상태: Todo
#
# 진행할까요?
```

### `/devlog-to-issue` - DEVLOG 변환

개발 로그를 분석해서 완료된 작업과 후속 이슈를 자동 생성합니다.

```
> /devlog-to-issue ./DEVLOG.md

# DEVLOG 분석 결과:
# - 완료: 파트너스 초대이력 파싱 (68명)
# - 후속: 기여활동 대시보드 구축
#
# 이슈를 생성할까요?
```

### `/linear-doc` - 문서 추가

마크다운 파일을 Linear 프로젝트의 Resources에 추가합니다.

```
> /linear-doc ./docs/spec.md "커뮤니티 유지"

# 다음 문서를 Linear에 추가합니다:
# - 제목: 파트너스 운영 스펙
# - 프로젝트: 지피터스 커뮤니티 유지 및 관리
#
# 진행할까요?
```

## 알려진 이슈

### Linear MCP state 필드 버그

Linear MCP의 이슈 조회 시 `state` 필드가 `{}`로 반환되는 버그가 있습니다.

```json
// MCP 응답
{ "state": {} }  // 비어있음

// 정상 응답
{ "state": { "name": "Done", "type": "completed" } }
```

**영향받는 스킬**: `update-proj` (이슈 상태 필요)

**해결**: 스크립트로 직접 GraphQL API 호출 (자동 적용됨)

## API 사용 방식

| 기능 | 방법 | 이유 |
|------|------|------|
| 이슈 조회 (state 필요) | 스크립트 | MCP 버그 |
| 이슈 조회 (state 불필요) | Linear MCP | |
| 이니셔티브/프로젝트 조회 | Linear MCP | |
| 이슈 CRUD | Linear MCP | |
| `projectUpdateCreate` | 스크립트 | MCP 미지원 |
| `initiativeUpdateCreate` | 스크립트 | MCP 미지원 |
| `documentCreate` | 스크립트 | MCP 미지원 |

## 라이선스

MIT
