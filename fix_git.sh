#!/bin/bash
# 修復 Git 倉庫，移除圖片檔案追蹤，確保重要檔案可被追蹤

cd "$(dirname "$0")"

echo "🔧 開始修復 Git 倉庫..."

# 1. 確保 .gitignore 存在
if [ ! -f .gitignore ]; then
    echo "創建 .gitignore 檔案..."
    cat > .gitignore << 'EOF'
# 忽略圖片檔案（檔案太大，不需要上傳到 GitHub）
*.JPEG
*.jpeg
*.JPG
*.jpg
*.PNG
*.png
*.GIF
*.gif

# 忽略系統檔案
.DS_Store
.DS_Store?
._*
.Spotlight-V100
.Trashes
ehthumbs.db
Thumbs.db

# 忽略編輯器檔案
*.swp
*.swo
*~
.vscode/
.idea/

# 忽略臨時檔案
*.tmp
*.log
EOF
fi

# 2. 從 Git 中移除圖片檔案（但保留本地檔案）
echo "從 Git 中移除圖片檔案追蹤..."
git rm --cached *.JPEG 2>/dev/null || true
git rm --cached *.JPG 2>/dev/null || true
git rm --cached *.jpeg 2>/dev/null || true
git rm --cached *.jpg 2>/dev/null || true

# 3. 移除系統檔案
echo "移除系統檔案追蹤..."
git rm --cached .DS_Store 2>/dev/null || true

# 4. 添加重要檔案
echo "添加重要檔案到 Git..."
git add -f .gitignore
git add -f index.html
git add -f strokeMap.js
git add -f update_strokeMap.py
git add -f check_missing.py
git add -f update.sh
git add -f debug_strokeMap.html

echo ""
echo "✅ 完成！"
echo ""
echo "現在你可以在 GitHub Desktop 中："
echo "1. 查看變更（應該會看到圖片檔案被移除）"
echo "2. 提交變更"
echo "3. 推送到 GitHub"
echo ""
echo "重要檔案已準備好上傳："
echo "  - index.html"
echo "  - strokeMap.js"
echo "  - update_strokeMap.py"
echo "  - check_missing.py"
echo "  - update.sh"
echo "  - debug_strokeMap.html"
