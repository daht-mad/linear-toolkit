# proj-update

Linear 프로젝트의 Cycle 기반 업데이트를 **결과물 중심**으로 자동 생성하고 Linear에 직접 등록하는 Claude Code 스킬

## 특징

- 이슈 나열이 아닌 **"뭐가 달라졌는지"** 중심 작성
- 현재 Cycle → 만든 결과, 다음 Cycle → 만들 결과
- 말머리 + 이모지로 영역 구분
- AS-IS / TO-BE 표로 변경사항 명확화
- Linear에 Project Update로 직접 등록

## 사용법

```
/proj-update
```

또는

```
프로젝트 업데이트 써줘
프로젝트 업데이트 작성
```

## 워크플로우

1. **프로젝트 선택** - 내가 리드인 프로젝트 목록에서 선택
2. **Cycle/이슈 수집** - Linear MCP로 현재/다음 Cycle 이슈 가져오기
3. **업데이트 작성** - 결과물 중심으로 그룹핑하여 작성
4. **Linear 등록** - 확인 후 Project Update로 등록

## 환경 설정

`.env` 파일에 Linear API 토큰 필요:

```
LINEAR_API_TOKEN=lin_api_xxxxxxxxxxxxx
```

## 파일 구조

```
proj-update/
├── README.md                 # 이 파일
├── SKILL.md                  # 스킬 정의 및 워크플로우
├── scripts/
│   └── linear_api.py         # Linear API 직접 호출 (projectUpdateCreate)
└── references/
    ├── output-format.md      # 출력 포맷 예시
    └── writing-guide.md      # 말머리/이모지 가이드
```

## 의존성

- **Linear MCP** - 프로젝트, Cycle, 이슈 조회
- **Python 3** - Linear API 스크립트 실행
- **requests** - API 호출

```bash
pip install requests python-dotenv
```

## 출력 예시

```markdown
# 만든 결과 (1/24~1/30)

## [파트너스 시스템] 🔧 자격 관리 체계 전면 개편

**한 줄 요약**: 복잡하고 흩어져 있던 파트너 자격 기준을 단순화하고, 관리 시스템을 에어테이블로 일원화

**기존 문제**
- 누가 언제 파트너가 됐는지 카톡 대화 뒤져야 알 수 있었음

**변경 사항**

| 구분 | AS-IS | TO-BE |
|------|-------|-------|
| 자격 검토 | 1월·7월 일괄 | 초대일 기준 6개월마다 개별 |
| 기여 기준 | 기존 3회↑ / 신규 2회↑ | **모두 2회↑** |

**완료된 작업**
- 카톡 20,000줄에서 초대이력 파싱 → 68명 에어테이블 입력

---

# 만들 결과 (1/31~2/6)

## [파트너스 시스템] 📢 자격 기준 변경 공지

**목표**: 바뀐 기준을 파트너들에게 공식 안내

- [ ] 팀 내부 문서 리뷰
- [ ] 파트너스방 카톡 공지
```

## 관련 스킬

- [init-update](../init-update/) - 이니셔티브 업데이트 (프로젝트 업데이트 종합)
- [issue](../issue/) - Linear 이슈 생성
- [devlog-to-linear](../devlog-to-linear/) - DEVLOG → Linear 이슈 변환
