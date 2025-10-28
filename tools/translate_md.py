#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
JA原稿 (content.ja) を正として EN原稿 (content.en) を GPT で再翻訳し、
content.en 内のセクション内リンク（他ページ・同一ページ）を
旧アンカー→新アンカーへ一括更新するスクリプト。

- Front-Matter は保持し、title/description 等の英語訳は置換
- Markdown 構造は維持（見出しレベル・コードブロック・箇条書き等）
- 旧→新の見出しアンカー対応表を作り、全 .md を横断してリンク再書換え
- ドライラン (--dry-run) あり
"""

import os
import re
import sys
import json
import yaml
import argparse
import hashlib
from pathlib import Path
from typing import Dict, List, Tuple

# ====== OpenAI API (Responses) ======
# pip install openai pyyaml
from openai import OpenAI

with open("key.txt", "r", encoding="utf-8") as f:
    OPENAI_API_KEY = f.read().strip()

# --------- ユーティリティ ---------
HEADING_RE = re.compile(r'^(#{1,6})\s+(.*)\s*$', re.MULTILINE)
LINK_RE = re.compile(r'\[([^\]]+)\]\(([^)]+)\)')

def sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()

def load_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")

def save_text(path: Path, text: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")

def split_front_matter(md: str) -> Tuple[str, str, str]:
    """--- YAML --- を抽出して (fm, body, kind) を返す。fmはYAML文字列（---含む）。"""
    if md.startswith('---'):
        parts = md.split('---', 2)
        if len(parts) >= 3:
            # parts: ['', YAML, rest]
            return '---' + parts[1] + '---', parts[2].lstrip('\n'), 'yaml'
    if md.startswith('+++'):
        parts = md.split('+++', 2)
        if len(parts) >= 3:
            return '+++' + parts[1] + '+++', parts[2].lstrip('\n'), 'toml'
    return '', md, ''

def parse_yaml_block(fm: str) -> dict:
    if not fm:
        return {}
    raw = fm.strip()
    if raw.startswith('---'):
        raw = raw.strip('-').strip()
        return yaml.safe_load(raw) or {}
    return {}

def rebuild_front_matter(fm_dict: dict) -> str:
    if not fm_dict:
        return ''
    return '---\n' + yaml.safe_dump(fm_dict, allow_unicode=True, sort_keys=False) + '---\n'

def slugify_hugo_like(text: str) -> str:
    """
    Hugo(Goldmark) っぽい簡易アンカー化：
    - 小文字化
    - アルファベット・数字・スペース・ハイフン以外を削除
    - スペースを '-' に
    - 連続 '-' を 1 個に
    - 先頭末尾の '-' を除去
    """
    t = text.strip().lower()
    # 括弧や記号をざっくり削除（英語向け）
    t = re.sub(r'[^a-z0-9\-\s]', '', t)
    t = re.sub(r'\s+', '-', t)
    t = re.sub(r'-{2,}', '-', t)
    return t.strip('-')

def extract_headings(md: str) -> List[Tuple[int, str, str]]:
    """
    [(level, heading_text, slug)] を上から順に返す
    """
    out = []
    for m in HEADING_RE.finditer(md):
        level = len(m.group(1))
        text = m.group(2).strip()
        out.append((level, text, slugify_hugo_like(text)))
    return out

def replace_links(md: str, slug_map_for_files: Dict[str, Dict[str, str]], current_file: Path) -> str:
    """
    md 内の [text](target#anchor) を、slug_map_for_files に基づき置換。
    - target: 相対 md ファイル（.md / ディレクトリindex.md等にも対応簡易）
    - anchor: 旧slug -> 新slug 置換
    - text: 見出しテキストが完全一致する場合は新見出しに置換
    """
    def normalize_target_path(target: str) -> Tuple[str, str]:
        # 分離: path + #fragment
        if '#' in target:
            path, frag = target.split('#', 1)
        else:
            path, frag = target, ''
        return path, frag

    def canonical_md_path(base: Path, link_path: str) -> str:
        # ../log/ や ../log/#anchor, ../log/index.md などを content.en 相対の仮想キーに
        p = (base.parent / link_path).resolve()
        # 標準化：拡張子 .md を付ける/落とす問題に緩く対処
        if p.suffix.lower() != '.md':
            # ディレクトリや拡張子無しは index.md を想定（Hugoの典型構成）
            if p.is_dir():
                p = p / 'index.md'
            else:
                # 拡張子無しのときは .md を仮定
                p = p.with_suffix('.md')
        try:
            return str(p.relative_to(EN_ROOT.resolve()))
        except Exception:
            return str(p)

    def _repl(m):
        text = m.group(1)
        target_raw = m.group(2)
        path_part, frag = normalize_target_path(target_raw)

        # 同一ページ内 #anchor ショートカット
        if path_part in ('', '#', '.'):
            file_key = str(current_file.resolve().relative_to(EN_ROOT.resolve()))
        else:
            file_key = canonical_md_path(current_file, path_part)

        new_text = text
        new_target = target_raw

        file_map = slug_map_for_files.get(file_key)
        if file_map and frag:
            old_slug = frag.strip().lower()
            new_slug = file_map.get(old_slug)
            if new_slug:
                # slug 差替え
                new_path = path_part if path_part else ''
                new_target = f"{new_path}#{new_slug}"

                # テキストが旧見出しと完全一致するなら、新見出しに差替え
                # 逆引き（旧slug -> 新見出しテキスト）を用意
                # file_map は old_slug -> new_slug しか持たないので、別に old_slug -> new_heading も持たせる
                # このために、slug_map_for_files_extra を併用する設計に変更
                pass

        return f"[{new_text}]({new_target})"

    return LINK_RE.sub(_repl, md)

# 旧→新 見出しテキストも置き換えたいので、追加マップを持つ:
# files_map: file_key -> {
#   "slug_map": {old_slug: new_slug},
#   "title_map": {old_heading: new_heading}  # 文字列一致用
# }
def replace_links_with_titles(md: str, files_map: Dict[str, Dict[str, Dict[str, str]]], current_file: Path) -> str:
    def normalize_target_path(target: str) -> Tuple[str, str]:
        if '#' in target:
            path, frag = target.split('#', 1)
        else:
            path, frag = target, ''
        return path, frag

    def canonical_md_path(base: Path, link_path: str) -> str:
        p = (base.parent / link_path).resolve()
        if p.suffix.lower() != '.md':
            if p.is_dir():
                p = p / 'index.md'
            else:
                p = p.with_suffix('.md')
        try:
            return str(p.relative_to(EN_ROOT.resolve()))
        except Exception:
            return str(p)

    def _repl(m):
        text = m.group(1)
        target_raw = m.group(2)
        path_part, frag = normalize_target_path(target_raw)

        if path_part in ('', '#', '.'):
            file_key = str(current_file.resolve().relative_to(EN_ROOT.resolve()))
        else:
            file_key = canonical_md_path(current_file, path_part)

        out_text = text
        out_target = target_raw

        info = files_map.get(file_key)
        if info and frag:
            old_slug = frag.strip().lower()
            new_slug = info["slug_map"].get(old_slug)
            if new_slug:
                new_path = path_part if path_part else ''
                out_target = f"{new_path}#{new_slug}"
                # テキスト一致ならタイトルも置換
                new_title = info["title_from_slug"].get(old_slug)
                if new_title and text.strip() == info["old_title_from_slug"].get(old_slug, ''):
                    out_text = new_title

        return f"[{out_text}]({out_target})"

    return LINK_RE.sub(_repl, md)

# ====== OpenAI 翻訳 ======
TRANSLATION_SYSTEM_PROMPT = """\
You are a professional technical/localization translator (JA -> EN) for a Hugo website.
**Keep Markdown structure and front matter intact.**
- Preserve heading levels (#, ##, ###), lists, code fences, tables, links, image tags.
- Translate only human-readable text (including headings and link texts), not URLs, code, or file paths.
- If front matter (YAML) has 'title' or 'description', translate their values to English.
- Keep internal anchors consistent with the translated headings (we will regenerate slugs programmatically).
- Keep relative links and image paths unchanged.
- Use concise, natural, globally understandable technical English; avoid overly literal JP phrasing.
"""

def translate_markdown(client: OpenAI, model: str, ja_md: str) -> str:
    """
    入力全体を翻訳（構造保持）。結果は Markdown のまま返す。
    簡易キャッシュ付き（内容ハッシュ）。
    """
    cache_dir = Path(".cache_translation")
    cache_dir.mkdir(exist_ok=True)
    key = f"{model}:{sha256(ja_md)}"
    cache_path = cache_dir / f"{key}.md"
    if cache_path.exists():
        return cache_path.read_text(encoding="utf-8")

    resp = client.responses.create(
        model=model,
        input=[
            {"role": "system", "content": TRANSLATION_SYSTEM_PROMPT},
            {"role": "user", "content": ja_md},
        ],
    )
    out = resp.output_text
    cache_path.write_text(out, encoding="utf-8")
    return out

# ====== メイン処理 ======
def main(args):
    global EN_ROOT
    JA_ROOT = Path(args.ja_root).resolve()
    EN_ROOT = Path(args.en_root).resolve()
    model = args.model
    dry_run = args.dry_run

    # OpenAI client
    if not OPENAI_API_KEY:
        print("ERROR: OPENAI_API_KEY is not set.", file=sys.stderr)
        sys.exit(1)
    client = OpenAI(api_key=OPENAI_API_KEY)

    # 1) content.en の旧見出しマップ収集
    print("Scanning old EN headings...")
    old_map = {}  # file_key -> { slug_map: {old_slug: old_slug}, title_from_slug, old_title_from_slug }
    en_files = [p for p in EN_ROOT.rglob("*.md") if p.is_file()]
    for en in en_files:
        rel = str(en.resolve().relative_to(EN_ROOT))
        md = load_text(en)
        headings = extract_headings(md)
        slug_map = {}
        title_from_slug = {}
        old_title_from_slug = {}
        for _, text, slug in headings:
            slug_map[slug] = slug
            title_from_slug[slug] = text  # 初期は旧=新
            old_title_from_slug[slug] = text
        old_map[rel] = {
            "slug_map": slug_map,
            "title_from_slug": title_from_slug,
            "old_title_from_slug": old_title_from_slug,
        }

    # 2) JA を翻訳して EN を上書き（ただし dry-run なら書かない）
    print("Translating JA -> EN and preparing new EN...")
    new_en_texts: Dict[str, str] = {}
    files_processed = 0
    ja_files = [p for p in JA_ROOT.rglob("*.md") if p.is_file()]

    for ja in ja_files:
        rel_from_ja = str(ja.resolve().relative_to(JA_ROOT))
        en_path = EN_ROOT / rel_from_ja  # mirror構造
        if not en_path.exists():
            # EN が存在しない場合はスキップ（必要なら作る仕様に変えてOK）
            continue

        ja_md = load_text(ja)

        # Front-Matter を先に分解し、本文とまとめて翻訳 → 後で fm を差し直す
        fm, body, _ = split_front_matter(ja_md)
        # fmの中の title/description は翻訳してよいので、まとめて投入
        translated = translate_markdown(client, model, ja_md)

        # 念のため再分解して fm と body を復元
        tfm, tbody, _ = split_front_matter(translated)
        if not tfm:
            # FM 無し or 翻訳時に外れた → 元fmを残し、tbodyはtranslated全体扱い
            tfm = fm
            tbody = translated if not fm else translated.replace(fm, '', 1).lstrip()

        new_text = (tfm + '\n' if tfm else '') + tbody
        new_en_texts[str(en_path.resolve())] = new_text
        files_processed += 1

    print(f"Prepared {files_processed} EN files.")

    # 3) 新ENの見出しを解析し、old->new の slug/title 対応を構築
    print("Building slug/title replacement maps...")
    files_map = {}
    for abs_en_path, new_text in new_en_texts.items():
        enp = Path(abs_en_path)
        rel = str(enp.resolve().relative_to(EN_ROOT))
        new_headings = extract_headings(new_text)
        old_info = old_map.get(rel, {"slug_map": {}, "title_from_slug": {}, "old_title_from_slug": {}})

        # 旧見出しの slug の集合（順序で対応付け：見出し数が一致しない場合は best-effort）
        old_slugs = list(old_info["slug_map"].keys())
        new_slugs = [h[2] for h in new_headings]
        old_titles = list(old_info["title_from_slug"].values())
        new_titles = [h[1] for h in new_headings]

        slug_map = {}
        title_from_slug = {}
        old_title_from_slug = {}

        for i, old_slug in enumerate(old_slugs):
            if i < len(new_slugs):
                slug_map[old_slug] = new_slugs[i]
                title_from_slug[old_slug] = new_titles[i] if i < len(new_titles) else new_titles[-1] if new_titles else ''
                old_title_from_slug[old_slug] = old_titles[i] if i < len(old_titles) else ''
            else:
                # 余った旧slugは自己写像のまま
                slug_map[old_slug] = old_slug
                title_from_slug[old_slug] = old_info["title_from_slug"].get(old_slug, '')
                old_title_from_slug[old_slug] = old_info["old_title_from_slug"].get(old_slug, '')

        files_map[rel] = {
            "slug_map": slug_map,
            "title_from_slug": title_from_slug,
            "old_title_from_slug": old_title_from_slug,
        }

    # 4) リンク置換（全 EN ファイル横断）
    print("Rewriting links across content.en ...")
    updated_texts: Dict[str, str] = {}

    # 4-1. まずは翻訳後テキストに対してリンク置換
    for abs_en_path, new_text in new_en_texts.items():
        enp = Path(abs_en_path)
        replaced = replace_links_with_titles(new_text, files_map, enp)
        updated_texts[abs_en_path] = replaced

    # 4-2. 翻訳対象外（JAに対応が無く今回未更新）の EN にも、他ページのリンク変更を反映
    untouched_en = [p for p in EN_ROOT.rglob("*.md") if str(p.resolve()) not in updated_texts]
    for p in untouched_en:
        md = load_text(p)
        replaced = replace_links_with_titles(md, files_map, p)
        updated_texts[str(p.resolve())] = replaced

    # 5) 書き込み or ドライラン表示
    if dry_run:
        print("---- DRY RUN (no files written) ----")
        show = 0
        for abs_path, txt in updated_texts.items():
            orig = load_text(Path(abs_path)) if Path(abs_path).exists() else ""
            if orig != txt:
                show += 1
                rel = str(Path(abs_path).resolve().relative_to(Path.cwd().resolve()))
                print(f"[would update] {rel}")
                if show >= 20:
                    print("... (more files omitted)")
                    break
    else:
        print("Writing files...")
        for abs_path, txt in updated_texts.items():
            save_text(Path(abs_path), txt)
        print("Done.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="JA->EN retranslation for Hugo + anchor-safe link rewrite")
    parser.add_argument("--ja-root", required=True, help="Path to content.ja")
    parser.add_argument("--en-root", required=True, help="Path to content.en")
    parser.add_argument("--model", default="gpt-5-mini", help="OpenAI model (e.g., gpt-5, gpt-5-mini, gpt-4.1-mini)")
    parser.add_argument("--dry-run", action="store_true", help="Do not write files; just report")
    args = parser.parse_args()
    main(args)
