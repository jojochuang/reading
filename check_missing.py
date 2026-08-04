#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
檢查哪些字有 SVG 檔案但沒有在 strokeMap.js 中
"""

import re
import json
from pathlib import Path

SVG_DIR = Path.home() / "Documents" / "word writing" / "svg"
STROKEMAP_FILE = Path(__file__).parent / "strokeMap.js"

def extract_unicode_from_filename(filename):
    """從檔名提取 Unicode（前4碼）"""
    match = re.match(r'^([0-9a-fA-F]{4})_', filename)
    if match:
        return match.group(1).lower()
    return None

def load_strokeMap():
    """從 strokeMap.js 載入已有的字"""
    if not STROKEMAP_FILE.exists():
        return set()
    
    content = STROKEMAP_FILE.read_text(encoding='utf-8')
    # 提取所有中文字
    chars = re.findall(r'"([\u4e00-\u9fff])"', content)
    return set(chars)

def scan_svg_folders():
    """掃描所有 SVG 資料夾"""
    svg_chars = {}
    missing_svg = []
    invalid_filename = []
    
    if not SVG_DIR.exists():
        print(f"❌ SVG 資料夾不存在: {SVG_DIR}")
        return svg_chars, missing_svg, invalid_filename
    
    for folder in sorted(SVG_DIR.iterdir()):
        if not folder.is_dir() or folder.name.startswith('.'):
            continue
        
        char = folder.name
        svg_files = list(folder.glob("*.svg"))
        
        if not svg_files:
            missing_svg.append(char)
            continue
        
        unicode_hex = extract_unicode_from_filename(svg_files[0].name)
        if not unicode_hex:
            invalid_filename.append((char, svg_files[0].name))
            continue
        
        svg_chars[char] = unicode_hex
    
    return svg_chars, missing_svg, invalid_filename

def main():
    print("🔍 檢查遺漏的字...\n")
    
    # 載入 strokeMap.js 中已有的字
    strokeMap_chars = load_strokeMap()
    print(f"📝 strokeMap.js 中有 {len(strokeMap_chars)} 個字\n")
    
    # 掃描 SVG 資料夾
    svg_chars, missing_svg, invalid_filename = scan_svg_folders()
    print(f"📂 SVG 資料夾中有 {len(svg_chars)} 個字\n")
    
    # 找出有 SVG 但沒有在 strokeMap 中的字
    missing_in_strokeMap = []
    for char in svg_chars:
        if char not in strokeMap_chars:
            missing_in_strokeMap.append((char, svg_chars[char]))
    
    # 找出在 strokeMap 中但沒有 SVG 的字
    missing_in_svg = []
    for char in strokeMap_chars:
        if char not in svg_chars:
            missing_in_svg.append(char)
    
    # 顯示結果
    if missing_in_strokeMap:
        print(f"⚠️  發現 {len(missing_in_strokeMap)} 個字有 SVG 但沒有在 strokeMap.js 中:")
        for char, unicode_hex in missing_in_strokeMap[:30]:
            print(f"   - {char} (Unicode: {unicode_hex})")
        if len(missing_in_strokeMap) > 30:
            print(f"   ... 還有 {len(missing_in_strokeMap) - 30} 個")
        print("\n   這些字需要重新執行 update_strokeMap.py 來加入")
    else:
        print("✅ 所有有 SVG 的字都在 strokeMap.js 中")
    
    if missing_in_svg:
        print(f"\n⚠️  發現 {len(missing_in_svg)} 個字在 strokeMap.js 中但沒有 SVG 檔案:")
        for char in missing_in_svg[:30]:
            print(f"   - {char}")
        if len(missing_in_svg) > 30:
            print(f"   ... 還有 {len(missing_in_svg) - 30} 個")
    
    if invalid_filename:
        print(f"\n⚠️  發現 {len(invalid_filename)} 個資料夾的 SVG 檔名格式不正確:")
        for char, filename in invalid_filename[:20]:
            print(f"   - {char}: {filename}")
        if len(invalid_filename) > 20:
            print(f"   ... 還有 {len(invalid_filename) - 20} 個")
        print("\n   提示: SVG 檔名格式應為 {unicode}_{序號}.svg，例如: 4e95_01.svg")
    
    if missing_svg:
        print(f"\n⚠️  發現 {len(missing_svg)} 個資料夾沒有 SVG 檔案:")
        for char in missing_svg[:20]:
            print(f"   - {char}")
        if len(missing_svg) > 20:
            print(f"   ... 還有 {len(missing_svg) - 20} 個")

if __name__ == "__main__":
    main()
