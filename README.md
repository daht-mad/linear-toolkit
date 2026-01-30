# Linear Toolkit

Linear 업무 자동화를 위한 Claude Code 플러그인.

## 포함된 스킬

| 스킬 | 호출 | 설명 |
|------|------|------|
| `create-issue` | `/create-issue` | Linear 이슈 생성 |
| `devlog-to-issue` | `/devlog-to-issue` | DEVLOG.md → Linear 이슈 변환 |
| `update-proj` | `/update-proj` | 프로젝트 Cycle 업데이트 작성 |
| `update-init` | `/update-init` | 이니셔티브 업데이트 작성 |
| `linear-doc` | `/linear-doc` | 마크다운 → Linear 문서 추가 |

## 설치

```bash
# 1. Git clone
git clone https://github.com/daht-mad/linear-toolkit.git ~/.claude/plugins/linear-toolkit

# 2. 설치 스크립트 실행
~/.claude/plugins/linear-toolkit/install.sh

# 3. Claude Code 재시작
```

## 요구사항

### 1. Linear MCP
Linear MCP가 설정되어 있어야 합니다.

### 2. 환경변수
`.env` 파일에 토큰 설정 (스크립트용):
```
LINEAR_API_TOKEN=lin_api_xxxxxxxxxxxxx
```

> MCP는 자체 인증을 사용하지만, `update-proj`, `update-init`, `linear-doc` 스킬의
> 일부 기능(MCP에 없는 API)은 스크립트를 사용하므로 토큰이 필요합니다.

## API 사용 방식

| 기능 | 방법 |
|------|------|
| 조회 (이슈, 프로젝트, 이니셔티브 등) | Linear MCP |
| 이슈 CRUD | Linear MCP |
| `projectUpdateCreate` | 스크립트 |
| `initiativeUpdateCreate` | 스크립트 |
| `documentCreate` | 스크립트 |

## 라이선스

MIT
