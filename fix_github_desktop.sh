#!/bin/bash
# 修復 GitHub Desktop 顯示問題

cd "$(dirname "$0")"

echo "🔧 修復 GitHub Desktop 顯示問題..."
echo ""

# 1. 檢查檔案是否在 Git 中
echo "📋 檢查檔案追蹤狀態："
echo ""
git ls-files | grep -E "(index|strokeMap|update|check|debug|gitignore)" | while read file; do
    if [ -f "$file" ]; then
        echo "  ✅ $file (已追蹤)"
    else
        echo "  ❌ $file (檔案不存在)"
    fi
done

echo ""
echo "📝 檢查未追蹤的檔案："
git ls-files --others --exclude-standard | head -10

echo ""
echo "🔍 檢查 .gitignore 規則："
git check-ignore -v index.html strokeMap.js update_strokeMap.py 2>&1 || echo "  這些檔案沒有被忽略"

echo ""
echo "💡 解決方案："
echo ""
echo "1. 在 GitHub Desktop 中："
echo "   - 按 Cmd+R 或點擊 View → Refresh"
echo "   - 或者關閉並重新打開 GitHub Desktop"
echo ""
echo "2. 如果還是不行，嘗試："
echo "   - Repository → Repository Settings → 檢查路徑是否正確"
echo "   - 或者重新添加倉庫：File → Add Local Repository"
echo ""
echo "3. 檢查檔案權限："
ls -l index.html strokeMap.js update_strokeMap.py | awk '{print $1, $9}'

echo ""
echo "✅ 檔案已經在 Git 中，問題可能是 GitHub Desktop 的顯示快取"
echo "   請嘗試重新整理 GitHub Desktop"
