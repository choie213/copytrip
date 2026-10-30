#!/usr/bin/env python3
"""일정 데이터 검증. 커밋 전에 실행: python3 scripts/check_plan.py"""
import json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
errors = []

def err(msg): errors.append(msg)

def load(p):
    try:
        return json.loads(p.read_text(encoding='utf-8'))
    except Exception as e:
        err(f'{p.relative_to(ROOT)}: JSON 오류 {e}')
        return None

trips = load(ROOT / 'data/trips.json') or []
for t in trips:
    slug = t.get('slug', '?')
    for k in ('slug', 'name', 'start', 'end'):
        if k not in t: err(f'trips.json {slug}: {k} 없음')
    if not (ROOT / slug / 'index.html').exists(): err(f'{slug}/index.html 없음')
    if not (ROOT / slug / 'manifest.webmanifest').exists(): err(f'{slug}/manifest.webmanifest 없음')
    plan = load(ROOT / 'data' / slug / 'plan.json')
    load(ROOT / 'data' / slug / 'i18n.json')
    if not plan: continue
    for k in ('trip', 'locations', 'rainThreshold', 'days', 'items'):
        if k not in plan: err(f'{slug}/plan.json: {k} 없음')
    n = len(plan.get('items', []))
    for d in plan.get('days', []):
        if not re.fullmatch(r'\d{4}-\d{2}-\d{2}', d.get('date', '')): err(f'{slug}: 날짜 형식 오류 {d.get("date")}')
        if d.get('default') not in d.get('plans', {}): err(f'{slug} {d.get("date")}: default 일정 키가 plans에 없음')
        for key, pl in d.get('plans', {}).items():
            if pl.get('weather') not in plan.get('locations', {}): err(f'{slug} {d["date"]}/{key}: weather 지점이 locations에 없음')
            for i in pl.get('sun', []) + pl.get('rain', []):
                if not isinstance(i, int) or not 0 <= i < n: err(f'{slug} {d["date"]}/{key}: 항목 번호 {i} 범위 밖 (items {n}개)')
    for i, it in enumerate(plan.get('items', [])):
        t_ = it.get('time')
        if t_ and not re.fullmatch(r'\d{1,2}:\d{2}', t_): err(f'{slug} items[{i}] {it.get("name")}: time 형식 오류 {t_}')

# 비밀값이 올라가지 않았는지 간단 검사 (구글 지도 키는 config.js 에 주인이 넣는 값이라 별도 안내)
pat = re.compile(r'AIza[0-9A-Za-z_\-]{30,}|gh[pousr]_[0-9A-Za-z]{30,}|sk-[0-9A-Za-z]{30,}|AKIA[0-9A-Z]{16}')
for p in ROOT.rglob('*'):
    if p.is_file() and '.git' not in p.parts and p.suffix in ('.js', '.json', '.html', '.md', '.py', '.yml', '.txt', '.css', '.csv'):
        for m in pat.finditer(p.read_text(encoding='utf-8', errors='ignore')):
            err(f'{p.relative_to(ROOT)}: 비밀값처럼 보이는 문자열 발견 ({m.group(0)[:8]}...)')

if errors:
    print('검증 실패:'); [print(' -', e) for e in errors]; sys.exit(1)
print('검증 통과: 여행 %d개' % len(trips))
