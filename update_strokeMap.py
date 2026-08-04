#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
自動更新 strokeMap.js 腳本
從 SVG 資料夾掃描中文字和 Unicode，自動生成筆順網動圖網址
"""

import os
import re
import json
from pathlib import Path

# 設定路徑
SVG_DIR = Path.home() / "Documents" / "word writing" / "svg"
OUTPUT_FILE = Path(__file__).parent / "strokeMap.js"
BASE_URL = "https://www.twpen.com/bishun-animation"

def extract_unicode_from_filename(filename):
    """從檔名提取 Unicode（前4碼）"""
    # 匹配格式：4e95_01.svg 或 4e95_01_xxx.svg
    match = re.match(r'^([0-9a-fA-F]{4})_', filename)
    if match:
        return match.group(1).lower()
    return None

def scan_svg_folders():
    """掃描 SVG 資料夾，收集中文字和 Unicode 對應"""
    char_map = {}
    missing_svg = []
    invalid_filename = []
    
    if not SVG_DIR.exists():
        print(f"❌ SVG 資料夾不存在: {SVG_DIR}")
        return char_map, missing_svg, invalid_filename
    
    print(f"📂 掃描 SVG 資料夾: {SVG_DIR}\n")
    
    # 遍歷所有資料夾
    for folder in sorted(SVG_DIR.iterdir()):
        if not folder.is_dir() or folder.name.startswith('.'):
            continue
        
        char = folder.name  # 中文字（資料夾名稱）
        
        # 在資料夾內找第一個 SVG 檔案來提取 Unicode
        svg_files = list(folder.glob("*.svg"))
        if not svg_files:
            missing_svg.append(char)
            continue
        
        # 從第一個檔案提取 Unicode
        unicode_hex = extract_unicode_from_filename(svg_files[0].name)
        if not unicode_hex:
            invalid_filename.append((char, svg_files[0].name))
            continue
        
        char_map[char] = unicode_hex
        # 只在詳細模式下顯示每個字
        # print(f"  ✓ {char} -> {unicode_hex}")
    
    return char_map, missing_svg, invalid_filename

def generate_strokeMap_js(char_map):
    """生成 strokeMap.js 檔案內容"""
    import time
    
    lines = ['const strokeMap = {']
    
    # 按中文字排序
    sorted_chars = sorted(char_map.items(), key=lambda x: x[0])
    
    for char, unicode_hex in sorted_chars:
        url = f"{BASE_URL}/{unicode_hex}-stroke-order.gif"
        # 轉義特殊字符
        char_escaped = json.dumps(char, ensure_ascii=False)
        lines.append(f'  {char_escaped}: "{url}",')
    
    lines.append('};')
    
    # 添加版本資訊（用於快取清除）
    timestamp = int(time.time())
    lines.append(f'// strokeMap 版本: {timestamp}')
    lines.append(f'// 總字數: {len(char_map)}')
    
    content = '\n'.join(lines)
    
    return content, timestamp

def main():
    print("🚀 開始自動更新 strokeMap.js...\n")
    
    # 掃描 SVG 資料夾
    char_map, missing_svg, invalid_filename = scan_svg_folders()
    
    if not char_map:
        print("\n❌ 沒有找到任何中文字和 Unicode 對應")
        return
    
    print(f"✅ 成功處理 {len(char_map)} 個中文字")
    
    # 生成 strokeMap.js
    content, timestamp = generate_strokeMap_js(char_map)
    
    # 寫入檔案
    try:
        OUTPUT_FILE.write_text(content, encoding='utf-8')
        print(f"\n✅ 成功更新 {OUTPUT_FILE}")
        print(f"   共 {len(char_map)} 個字")
        print(f"   版本時間戳: {timestamp}")
        print(f"\n💡 提示: 如果網頁仍顯示舊資料，請清除瀏覽器快取或強制重新載入")
    except Exception as e:
        print(f"\n❌ 寫入檔案失敗: {e}")
        return
    
    # 顯示警告
    if missing_svg:
        print(f"\n⚠️  發現 {len(missing_svg)} 個資料夾沒有 SVG 檔案:")
        for char in missing_svg[:20]:  # 只顯示前20個
            print(f"   - {char}")
        if len(missing_svg) > 20:
            print(f"   ... 還有 {len(missing_svg) - 20} 個")
    
    if invalid_filename:
        print(f"\n⚠️  發現 {len(invalid_filename)} 個資料夾的 SVG 檔名格式不正確:")
        for char, filename in invalid_filename[:20]:  # 只顯示前20個
            print(f"   - {char}: {filename}")
        if len(invalid_filename) > 20:
            print(f"   ... 還有 {len(invalid_filename) - 20} 個")
        print("\n   提示: SVG 檔名格式應為 {unicode}_{序號}.svg，例如: 4e95_01.svg")
    
    # 顯示統計
    print("\n📊 統計資訊:")
    print(f"   - 成功處理: {len(char_map)} 個字")
    if missing_svg:
        print(f"   - 缺少 SVG: {len(missing_svg)} 個資料夾")
    if invalid_filename:
        print(f"   - 檔名格式錯誤: {len(invalid_filename)} 個資料夾")
    
    # 檢查是否有重複的 Unicode
    unicode_counts = {}
    for char, unicode_hex in char_map.items():
        if unicode_hex not in unicode_counts:
            unicode_counts[unicode_hex] = []
        unicode_counts[unicode_hex].append(char)
    
    duplicates = {k: v for k, v in unicode_counts.items() if len(v) > 1}
    if duplicates:
        print(f"   - ⚠️  發現 {len(duplicates)} 個重複的 Unicode:")
        for unicode_hex, chars in duplicates.items():
            print(f"     {unicode_hex}: {', '.join(chars)}")
    else:
        print("   - ✓ 沒有重複的 Unicode")

if __name__ == "__main__":
    main()
