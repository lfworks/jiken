#!/bin/bash

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE}  Python Project Template - セットアップウィザード${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

# ====================================
# Step 1: リモートURLの変更
# ====================================
echo -e "${GREEN}[ステップ 1/3] リモートURLの変更${NC}"
echo "----------------------------------------"

CURRENT_REMOTE=$(git remote get-url origin 2>/dev/null || echo "未設定")
echo -e "現在のリモートURL: ${YELLOW}${CURRENT_REMOTE}${NC}"
echo ""

read -p "新しいリモートURLを設定しますか? (y/N): " CHANGE_REMOTE
if [[ "$CHANGE_REMOTE" =~ ^[Yy]$ ]]; then
    read -p "新しいリモートURLを入力してください: " NEW_REMOTE_URL

    if [ -n "$NEW_REMOTE_URL" ]; then
        git remote set-url origin "$NEW_REMOTE_URL" 2>/dev/null || git remote add origin "$NEW_REMOTE_URL"
        echo -e "${GREEN}✓ リモートURLを更新しました: ${NEW_REMOTE_URL}${NC}"
    else
        echo -e "${YELLOW}⚠ リモートURLの変更をスキップしました${NC}"
    fi
else
    echo -e "${YELLOW}⚠ リモートURLの変更をスキップしました${NC}"
fi

echo ""

# ====================================
# Step 2: プロジェクト名の変更
# ====================================
echo -e "${GREEN}[ステップ 2/3] プロジェクト名の変更${NC}"
echo "----------------------------------------"

CURRENT_PROJECT="python-project-template"
CURRENT_MODULE="python_project_template"

echo -e "現在のプロジェクト名: ${YELLOW}${CURRENT_PROJECT}${NC}"
echo -e "現在のモジュール名: ${YELLOW}${CURRENT_MODULE}${NC}"
echo ""

read -p "新しいプロジェクト名を入力してください (例: my-awesome-project) [Enter でスキップ]: " NEW_PROJECT_NAME

if [ -n "$NEW_PROJECT_NAME" ]; then
    # プロジェクト名をケバブケースに正規化
    NEW_PROJECT_KEBAB=$(echo "$NEW_PROJECT_NAME" | tr '[:upper:]' '[:lower:]' | sed 's/_/-/g')
    # モジュール名をスネークケースに変換
    NEW_MODULE_SNAKE=$(echo "$NEW_PROJECT_NAME" | tr '[:upper:]' '[:lower:]' | sed 's/-/_/g')

    echo ""
    echo -e "以下の名前で更新します:"
    echo -e "  プロジェクト名 (ケバブケース): ${GREEN}${NEW_PROJECT_KEBAB}${NC}"
    echo -e "  モジュール名 (スネークケース): ${GREEN}${NEW_MODULE_SNAKE}${NC}"
    echo ""

    read -p "この名前で更新しますか? (y/N): " CONFIRM_NAME

    if [[ "$CONFIRM_NAME" =~ ^[Yy]$ ]]; then
        echo -e "${BLUE}ファイルを更新中...${NC}"

        # pyproject.toml の更新
        if [ -f "pyproject.toml" ]; then
            sed -i.bak "s/name = \"${CURRENT_PROJECT}\"/name = \"${NEW_PROJECT_KEBAB}\"/" pyproject.toml
            sed -i.bak "s|Homepage = \"https://github.com/lfworks/${CURRENT_PROJECT}\"|Homepage = \"https://github.com/YOUR_USERNAME/${NEW_PROJECT_KEBAB}\"|" pyproject.toml
            sed -i.bak "s|Repository = \"https://github.com/lfworks/${CURRENT_PROJECT}\"|Repository = \"https://github.com/YOUR_USERNAME/${NEW_PROJECT_KEBAB}\"|" pyproject.toml
            sed -i.bak "s|Issues = \"https://github.com/lfworks/${CURRENT_PROJECT}/issues\"|Issues = \"https://github.com/YOUR_USERNAME/${NEW_PROJECT_KEBAB}/issues\"|" pyproject.toml
            sed -i.bak "s|packages = \[\"src/${CURRENT_MODULE}\"\]|packages = [\"src/${NEW_MODULE_SNAKE}\"]|" pyproject.toml
            sed -i.bak "s|--cov=src/${CURRENT_MODULE}|--cov=src/${NEW_MODULE_SNAKE}|" pyproject.toml
            rm -f pyproject.toml.bak
            echo -e "  ${GREEN}✓${NC} pyproject.toml"
        fi

        # README.md の更新
        if [ -f "README.md" ]; then
            sed -i.bak "s/${CURRENT_PROJECT}/${NEW_PROJECT_KEBAB}/g" README.md
            sed -i.bak "s/${CURRENT_MODULE}/${NEW_MODULE_SNAKE}/g" README.md
            rm -f README.md.bak
            echo -e "  ${GREEN}✓${NC} README.md"
        fi

        # ディレクトリ名の変更
        if [ -d "src/${CURRENT_MODULE}" ]; then
            mv "src/${CURRENT_MODULE}" "src/${NEW_MODULE_SNAKE}"
            echo -e "  ${GREEN}✓${NC} src/${NEW_MODULE_SNAKE}/"
        fi

        # テストファイルのインポート文を更新
        if [ -d "tests" ]; then
            find tests -name "*.py" -type f -exec sed -i.bak "s/from ${CURRENT_MODULE}/from ${NEW_MODULE_SNAKE}/g" {} \;
            find tests -name "*.py" -type f -exec sed -i.bak "s/import ${CURRENT_MODULE}/import ${NEW_MODULE_SNAKE}/g" {} \;
            find tests -name "*.py.bak" -delete
            echo -e "  ${GREEN}✓${NC} tests/"
        fi

        echo -e "${GREEN}✓ プロジェクト名の更新が完了しました${NC}"
    else
        echo -e "${YELLOW}⚠ プロジェクト名の変更をスキップしました${NC}"
    fi
else
    echo -e "${YELLOW}⚠ プロジェクト名の変更をスキップしました${NC}"
fi

echo ""

# ====================================
# Step 3: カスタマイズオプション
# ====================================
echo -e "${GREEN}[ステップ 3/3] カスタマイズオプション${NC}"
echo "----------------------------------------"

# GitHub Actions ワークフローの削除
read -p "GitHub Actions ワークフローを削除しますか? (y/N): " DELETE_WORKFLOWS
if [[ "$DELETE_WORKFLOWS" =~ ^[Yy]$ ]]; then
    if [ -d ".github/workflows" ]; then
        rm -rf .github/workflows
        echo -e "${GREEN}✓ .github/workflows を削除しました${NC}"
    fi
else
    echo -e "${YELLOW}⚠ GitHub Actions ワークフローの削除をスキップしました${NC}"
fi

# CODEOWNERS の削除
read -p "CODEOWNERS ファイルを削除しますか? (y/N): " DELETE_CODEOWNERS
if [[ "$DELETE_CODEOWNERS" =~ ^[Yy]$ ]]; then
    if [ -f ".github/CODEOWNERS" ]; then
        rm -f .github/CODEOWNERS
        echo -e "${GREEN}✓ .github/CODEOWNERS を削除しました${NC}"
    fi
else
    echo -e "${YELLOW}⚠ CODEOWNERS の削除をスキップしました${NC}"
fi

# CONTRIBUTING.md の削除
read -p "CONTRIBUTING.md を削除しますか? (y/N): " DELETE_CONTRIBUTING
if [[ "$DELETE_CONTRIBUTING" =~ ^[Yy]$ ]]; then
    if [ -f "CONTRIBUTING.md" ]; then
        rm -f CONTRIBUTING.md
        echo -e "${GREEN}✓ CONTRIBUTING.md を削除しました${NC}"
    fi
else
    echo -e "${YELLOW}⚠ CONTRIBUTING.md の削除をスキップしました${NC}"
fi

# セットアップスクリプト自体の削除
echo ""
read -p "このセットアップスクリプトを削除しますか? (y/N): " DELETE_SETUP
if [[ "$DELETE_SETUP" =~ ^[Yy]$ ]]; then
    DELETE_SETUP_FLAG=true
    echo -e "${YELLOW}⚠ セットアップスクリプトは最後に削除されます${NC}"
else
    DELETE_SETUP_FLAG=false
    echo -e "${YELLOW}⚠ セットアップスクリプトの削除をスキップしました${NC}"
fi

echo ""

# ====================================
# 変更のコミット
# ====================================
echo -e "${GREEN}[完了] セットアップ完了${NC}"
echo "----------------------------------------"

# Gitの変更があるか確認
if [ -n "$(git status --porcelain)" ]; then
    echo ""
    read -p "変更をコミットしますか? (y/N): " COMMIT_CHANGES

    if [[ "$COMMIT_CHANGES" =~ ^[Yy]$ ]]; then
        git add -A
        git commit -m "chore: 初期セットアップ完了

- リモートURLを更新
- プロジェクト名を変更
- 不要なファイルを削除"
        echo -e "${GREEN}✓ 変更をコミットしました${NC}"
    else
        echo -e "${YELLOW}⚠ コミットをスキップしました（手動でコミットしてください）${NC}"
    fi
fi

# セットアップスクリプトの削除
if [ "$DELETE_SETUP_FLAG" = true ]; then
    SCRIPT_PATH="${BASH_SOURCE[0]}"
    rm -f "$SCRIPT_PATH"
    echo -e "${GREEN}✓ セットアップスクリプトを削除しました${NC}"
fi

echo ""
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}セットアップが完了しました！ 🎉${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
echo -e "次のステップ:"
echo -e "  1. ${YELLOW}uv sync --all-extras${NC} で依存関係をインストール"
echo -e "  2. ${YELLOW}make check${NC} ですべてのチェックを実行"
echo -e "  3. コーディングを開始！"
echo ""
