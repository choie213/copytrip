# 여행 동선 앱 작업 규칙 (Claude, ChatGPT/Codex 공통)

이 저장소는 **개인 비공개** 여행 일정 앱(정적 사이트 + PWA)입니다. 주인은 한 명이고, 일정 수정은 Claude와 ChatGPT(Codex) 둘 다 합니다. 같은 규칙을 지켜 주세요.

## 구조
- `index.html`: 여행 목록(대시보드). `data/trips.json`을 읽음
- `<슬러그>/index.html`: 여행 화면(껍데기). 실제 내용은 `app.js`, `app.css`가 그림
- `data/<슬러그>/plan.json`: 일정 원본. 여기만 고치면 화면이 바뀜
- `data/<슬러그>/i18n.json`: 영어, 일본어 번역 (비어 있어도 됨)
- `data/<슬러그>/weather.json`: GitHub Actions가 만드는 파일. **직접 수정 금지**
- 여행: `2026-11-fukuoka`(내 일정), `2026-10-hiroshima`(원작자 예시 데이터)

## plan.json 작성법 (요약)
- `items`에 카드를 한 번만 쓰고, `days[].plans.base.sun`/`rain`에 **번호(인덱스)** 로 참조함. 항목을 중간에 끼우면 번호가 밀리니 가능하면 끝에 추가하고 `sun`/`rain` 순서로 위치를 정함
- 장소 카드: `name`, `q`(구글 지도 검색어), 선택 `time`("HH:MM"), `note`, `tip`
- 선택지: `{"type":"choice","title":..., "options":[{name,q,note}], "multi":false}`
- 시간을 모르면 `time`을 생략 (빈 칸으로 표시됨)
- 자세한 필드는 README.md의 "데이터 구조" 참고

## 작업 전후 필수
1. 수정 후 `python3 scripts/check_plan.py` 실행. 오류가 있으면 고친 뒤에만 커밋
2. **main에 바로 푸시하지 말고** `claude/...` 또는 `codex/...` 브랜치에서 작업하고 PR을 엽니다. 병합은 주인이 합니다
3. 확인되지 않은 정보(영업시간, 요금, 예약 시각)는 지어내지 말고 `확인 필요`로 적기
4. 사용자가 정한 조건(숙소, 항공편, 순서)은 임의로 바꾸지 말고 바꾸자고 제안만 하기

## 보안 규칙 (중요)
- 저장소는 **비공개 유지**. 공개로 바꾸지 말 것
- 커밋 금지: API 키, 토큰, 비밀번호, 예약번호, 여권/신분증 번호, 카드 번호, 주민/전화번호
- 구글 지도 키는 `config.js`의 `window.MAPS_KEY`에 **주인이 직접** 넣음. 대신 넣어 주지 말고, 키는 도메인(HTTP 리퍼러) 제한과 Maps Embed API 한정으로 만들도록 안내
- 외부 주소를 코드에 하드코딩하지 말 것 (날씨 파일도 같은 사이트의 상대 경로를 씀)
- `robots.txt`, `_headers`, 각 `index.html`의 `noindex`는 지우지 말 것
- `.github/workflows`를 바꿀 때는 먼저 주인에게 설명하고 확인받기

## 라이선스
원본 코드는 MIT입니다. `LICENSE` 파일(원작자 저작권 표시)은 유지하세요.
