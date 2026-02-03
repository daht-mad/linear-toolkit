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
> /upload-doc ./docs/spec.md "프로젝트명"

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
| `upload-doc` | `/upload-doc` | 마크다운 → Linear 프로젝트 문서 |

## 설치

### 1. Linear MCP 설치

Claude Code 설정에서 Linear MCP를 추가합니다.

**방법 A: Claude Code 명령어**
```bash
claude mcp add linear -- npx -y @daht-mad/linear-mcp-plus
```

**방법 B: 수동 설정** (`~/.mcp.json` 또는 `.mcp.json`)
```json
{
  "mcpServers": {
    "linear": {
      "command": "npx",
      "args": ["-y", "@daht-mad/linear-mcp-plus"],
      "env": {
        "LINEAR_API_TOKEN": "${LINEAR_API_TOKEN}"
      }
    }
  }
}
```

**토큰 발급**: [Linear Settings > API](https://linear.app/settings/api) > Personal API keys > Create key

> `@daht-mad/linear-mcp-plus`는 기존 `@tacticlaunch/mcp-linear`의 버그를 수정하고, 프로젝트/이니셔티브 업데이트, 문서 생성 등 추가 도구를 포함합니다.

### 2. 플러그인 설치

```bash
# Git clone
git clone https://github.com/daht-mad/linear-toolkit.git ~/.claude/plugins/linear-toolkit

# 설치 스크립트 실행
~/.claude/plugins/linear-toolkit/install.sh

# Claude Code 재시작
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

### `/upload-doc` - 문서 추가

마크다운 파일을 Linear 프로젝트의 Resources에 추가합니다.

```
> /upload-doc ./docs/spec.md "커뮤니티 유지"

# 다음 문서를 Linear에 추가합니다:
# - 제목: 파트너스 운영 스펙
# - 프로젝트: 지피터스 커뮤니티 유지 및 관리
#
# 진행할까요?
```

## 라이선스

MIT
