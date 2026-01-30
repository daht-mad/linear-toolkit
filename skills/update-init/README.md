# init-update

이니셔티브의 Cycle 기반 업데이트를 하위 프로젝트 업데이트를 종합하여 자동 생성하고 Linear에 직접 등록하는 스킬

## 호출 방법

- `/init-update`
- "이니셔티브 업데이트 써줘"
- "이니셔티브 업데이트 작성"

## 워크플로우

```
Step 1: 이니셔티브 선택
    ↓
Step 2: 하위 프로젝트 업데이트 수집
    ↓
Step 3: 업데이트 내용 작성 (하이라이트 중심)
    ↓
Step 4: Linear 등록
```

### Step 1: 이니셔티브 선택
- 내가 owner인 이니셔티브 조회
- Active/Planned 상태만 필터링

### Step 2: 하위 프로젝트 업데이트 수집
- 이니셔티브에 연결된 활성 프로젝트 목록
- 각 프로젝트의 최근 업데이트 및 health 상태

### Step 3: 업데이트 내용 작성
- 프로젝트별 1줄 요약 (핵심 성과만)
- Health 자동 종합:
  - 모든 프로젝트 onTrack → 🟢 onTrack
  - 1개라도 atRisk → 🟡 atRisk
  - 1개라도 offTrack → 🔴 offTrack

### Step 4: Linear 등록
- 내용 확인 후 Linear에 initiativeUpdate 생성
- 등록 완료 시 URL 반환

## 출력 포맷

```markdown
## 📊 이니셔티브 현황

**Health**: 🟢 onTrack

---

### ✅ 이번 Cycle 핵심 성과
- [프로젝트A] 성과 요약
- [프로젝트B] 성과 요약

### ⚠️ 주요 이슈/리스크
- 이슈 내용 → 대응 방안

### 📋 다음 Cycle 중점
- 계획 요약

---

### 프로젝트별 상세
| 프로젝트 | Health | 핵심 진행 |
|----------|--------|-----------|
| 프로젝트A | 🟢 | 한줄 요약 |
```

## 스크립트 명령어

```bash
# 현재 사용자 정보
python scripts/linear_api.py whoami

# 내가 owner인 이니셔티브 목록
python scripts/linear_api.py my-initiatives

# 이니셔티브의 프로젝트 목록
python scripts/linear_api.py initiative-projects <initiative_id>

# 프로젝트의 최근 업데이트
python scripts/linear_api.py project-updates <project_id> [--limit N]

# 이니셔티브 업데이트 생성
python scripts/linear_api.py create-initiative-update <initiative_id> <body_file> [--health onTrack|atRisk|offTrack]
```

## 환경 설정

`.env` 파일에 Linear API 토큰 설정:
```
LINEAR_API_TOKEN=lin_api_xxxxxxxxxxxxx
```

## 파일 구조

```
~/.claude/skills/init-update/
├── SKILL.md                    # 스킬 정의 + 워크플로우
├── README.md                   # 이 파일
├── scripts/
│   └── linear_api.py           # Initiative 관련 GraphQL API
└── references/
    ├── writing-guide.md        # 작성 가이드
    └── output-format.md        # 출력 예시
```

## 핵심 원칙

### DO
- 이니셔티브 전체 관점에서 "무엇이 달라졌는지" 중심
- 프로젝트별 1줄 요약 (핵심 성과만)
- 팀 전체가 이해할 수 있는 비즈니스 언어

### DON'T
- 프로젝트 업데이트 복붙
- 이슈 번호 나열
- 기술 용어만 나열

## 관련 스킬

- [proj-update](../proj-update/) - 프로젝트 단위 업데이트 작성
