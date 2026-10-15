# -*- coding: utf-8 -*-
"""강의 HTML(티스토리 게시용으로 만든 05 HTML)을 이 사이트의 글 파일로 바꾼다.

실행: python tools/lecture_to_post.py "강의.html" --date 2026-10-07 --main lectures --sub claude-github-pages [--slug c1-github-pages] [--title "제목"] [--cover "C-1강"]
출력: _posts/<날짜>-<slug>.html

하는 일: front matter에 제목·카테고리·요약·표지 글자를 붙이고, 본문 전체를 {% raw %}로 감싸
표지 글자는 --cover가 없으면 파일 이름 앞의 'C-1강' 같은 강의 번호를 쓴다.
코드 예시의 {{ }}·{% %}가 사이트 빌드를 깨지 않게 한다. 맨 앞의 [대표 이미지] 자리표시자 문단은 뺀다.
본문의 글자는 바꾸지 않는다(본문에 든 endraw 태그 글자만 같은 모양의 문자 참조로 바꾼다).
"""
import argparse, os, re, sys, html as htmlmod

sys.stdout.reconfigure(encoding='utf-8')
ap = argparse.ArgumentParser()
ap.add_argument('src')
ap.add_argument('--date', required=True)
ap.add_argument('--main', required=True)
ap.add_argument('--sub', required=True)
ap.add_argument('--slug')
ap.add_argument('--title')
ap.add_argument('--cover')
ap.add_argument('--out', default='_posts')
a = ap.parse_args()

body = open(a.src, encoding='utf-8').read()
body = re.sub(r'^\s*<p[^>]*>\[대표 이미지\]</p>\s*(<p[^>]*>&nbsp;</p>\s*)?', '', body, count=1)
name = os.path.splitext(os.path.basename(a.src))[0]
title = a.title or name
mc = re.match(r'([A-Z]-\d+강|\d+강)', name)
cover = a.cover or (mc.group(1) if mc else '')
slug = a.slug or re.sub(r'[^a-z0-9]+', '-', title.lower()).strip('-') or 'lecture'
m = re.search(r'<p[^>]*data-ke-size="size14"[^>]*>(.*?)</p>', body, re.S)
summary = htmlmod.unescape(re.sub(r'<[^>]+>', '', m.group(1))).strip().lstrip('→').strip() if m else ''
q = lambda s: '"' + s.replace('\\', '\\\\').replace('"', '\\"') + '"'
front = '---\ntitle: %s\ndate: %s 09:00:00 +0900\ncategory_main: %s\ncategory_sub: %s\n' % (q(title), a.date, a.main, a.sub)
if summary:
    front += 'summary: %s\n' % q(summary[:180])
if cover:
    front += 'cover_text: %s\n' % q(cover)
front += '---\n'
# 본문에 글자로 든 endraw 태그는 감싼 구역을 일찍 끝내므로 첫 중괄호를 문자 참조(&#123;)로 바꾼다. 화면에는 같은 글자로 보인다
body = re.sub(r'\{(%-?\s*endraw\s*-?%\})', r'&#123;\1', body)
os.makedirs(a.out, exist_ok=True)
out = os.path.join(a.out, '%s-%s.html' % (a.date, slug))
open(out, 'w', encoding='utf-8', newline='\n').write(front + '{% raw %}\n' + body.rstrip('\n') + '\n{% endraw %}\n')
print('만듦:', out)
