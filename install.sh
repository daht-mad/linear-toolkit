#!/bin/bash
# Linear Toolkit 설치 스크립트

set -e

PLUGIN_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
SKILLS_DIR="$HOME/.claude/skills"

echo "🔧 Linear Toolkit 설치 시작..."
echo ""

# ============================================
# Step 1: 기존 Linear MCP 확인 및 제거
# ============================================
echo "📋 Step 1: 기존 Linear MCP 확인..."

# claude mcp list 명령어로 기존 linear MCP 확인
EXISTING_LINEAR=$(claude mcp list 2>/dev/null | grep -i linear || true)

if [ -n "$EXISTING_LINEAR" ]; then
    echo "⚠️  기존 Linear MCP 발견:"
    echo "$EXISTING_LINEAR"
    echo ""
    echo "🗑️  기존 MCP 제거 중..."
    
    # linear 이름이 포함된 모든 MCP 제거
    for mcp_name in $(claude mcp list 2>/dev/null | grep -i linear | awk '{print $1}'); do
        echo "   - $mcp_name 제거..."
        claude mcp remove "$mcp_name" 2>/dev/null || true
    done
    echo "✅ 기존 Linear MCP 제거 완료"
    echo ""
fi

# ============================================
# Step 2: @daht-mad/linear-mcp-plus 설치
# ============================================
echo "📦 Step 2: @daht-mad/linear-mcp-plus 설치..."

# LINEAR_API_TOKEN 환경변수 확인
if [ -z "$LINEAR_API_TOKEN" ]; then
    echo ""
    echo "⚠️  LINEAR_API_TOKEN 환경변수가 설정되지 않았습니다."
    echo ""
    echo "   토큰 발급 방법:"
    echo "   1. https://linear.app/settings/api 접속"
    echo "   2. Personal API Keys > Create key"
    echo "   3. 생성된 토큰을 복사"
    echo ""
    echo "   설정 방법 (택 1):"
    echo "   - export LINEAR_API_TOKEN='lin_api_xxxxx'"
    echo "   - ~/.zshrc 또는 ~/.bashrc에 추가"
    echo ""
    read -p "토큰을 지금 입력하시겠습니까? (y/N): " answer
    if [[ "$answer" =~ ^[Yy]$ ]]; then
        read -p "LINEAR_API_TOKEN: " LINEAR_API_TOKEN
        export LINEAR_API_TOKEN
    fi
fi

# MCP 설치
claude mcp add linear -- npx -y @daht-mad/linear-mcp-plus

echo "✅ linear-mcp-plus 설치 완료"
echo ""

# ============================================
# Step 3: 스킬 심볼릭 링크 생성
# ============================================
echo "🔗 Step 3: 스킬 설치..."

# skills 폴더 생성
mkdir -p "$SKILLS_DIR"

# 심볼릭 링크 생성
SKILLS=("create-issue" "devlog-to-issue" "update-proj" "update-init" "linear-mcp-check")

for skill in "${SKILLS[@]}"; do
    if [ -L "$SKILLS_DIR/$skill" ] || [ -d "$SKILLS_DIR/$skill" ]; then
        echo "   ⚠️  $skill 이미 존재 - 건너뜀"
    else
        ln -s "$PLUGIN_DIR/skills/$skill" "$SKILLS_DIR/$skill"
        echo "   ✅ $skill 설치 완료"
    fi
done

echo ""

# ============================================
# Step 4: 설치 확인
# ============================================
echo "🔍 Step 4: 설치 확인..."

# MCP 설치 확인
if claude mcp list 2>/dev/null | grep -q "linear"; then
    echo "   ✅ Linear MCP: 설치됨"
else
    echo "   ❌ Linear MCP: 설치 실패 - Claude Code 재시작 후 확인 필요"
fi

# 스킬 설치 확인
INSTALLED_COUNT=0
for skill in "${SKILLS[@]}"; do
    if [ -L "$SKILLS_DIR/$skill" ] || [ -d "$SKILLS_DIR/$skill" ]; then
        ((INSTALLED_COUNT++))
    fi
done
echo "   ✅ 스킬: $INSTALLED_COUNT/${#SKILLS[@]}개 설치됨"

echo ""
echo "============================================"
echo "🎉 Linear Toolkit 설치 완료!"
echo "============================================"
echo ""
echo "📌 다음 단계:"
echo "   1. Claude Code 재시작"
echo "   2. '/create-issue 테스트 이슈' 로 테스트"
echo ""
echo "📖 사용 가능한 명령어:"
echo "   /create-issue  - Linear 이슈 생성"
echo "   /update-proj   - 프로젝트 업데이트 작성"
echo "   /update-init   - 이니셔티브 업데이트 작성"
echo "   /devlog-to-issue - DEVLOG를 이슈로 변환"
echo ""
