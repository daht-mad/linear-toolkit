#!/bin/bash
# Linear Toolkit 설치 스크립트

PLUGIN_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
SKILLS_DIR="$HOME/.claude/skills"

# skills 폴더 생성
mkdir -p "$SKILLS_DIR"

# 심볼릭 링크 생성
SKILLS=("create-issue" "devlog-to-issue" "update-proj" "update-init")

for skill in "${SKILLS[@]}"; do
  if [ -L "$SKILLS_DIR/$skill" ] || [ -d "$SKILLS_DIR/$skill" ]; then
    echo "⚠️  $skill 이미 존재 - 건너뜀"
  else
    ln -s "$PLUGIN_DIR/skills/$skill" "$SKILLS_DIR/$skill"
    echo "✅ $skill 설치 완료"
  fi
done

echo ""
echo "🎉 Linear Toolkit 설치 완료!"
echo "Claude Code를 재시작하세요."
