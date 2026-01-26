# Python Project Template

[![CI](https://github.com/lfworks/pyreinfolib/actions/workflows/ci.yml/badge.svg)](https://github.com/lfworks/pyreinfolib/actions/workflows/ci.yml)
[![Python Version](https://img.shields.io/badge/python-3.11%2B-blue)](https://www.python.org/downloads/)

モダンなPythonプロジェクトテンプレート。PyPI公開を想定した構造になっています。

## 特徴

このテンプレートには以下のツールが設定済みです：

- **[uv](https://github.com/astral-sh/uv)**: 高速なPythonパッケージマネージャー
- **[ruff](https://github.com/astral-sh/ruff)**: 高速なlinter/formatter
- **[ty](https://github.com/astral-sh/ty)**: Astral製の型チェッカー
- **[vulture](https://github.com/jendrikseipp/vulture)**: デッドコード検出ツール
- **pytest**: テストフレームワーク（カバレッジ測定付き）
- **GitHub Actions**: CI/CD（format, lint, type check, test, dead code detection）

## クイックスタート

### 前提条件

- Python 3.11以上
- [uv](https://github.com/astral-sh/uv)のインストール

```bash
# uvのインストール（まだの場合）
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### セットアップ

```bash
# リポジトリをクローン
git clone https://github.com/lfworks/pyreinfolib.git
cd pyreinfolib

# 依存関係をインストール
uv sync --all-extras
```

### 開発

```bash
# フォーマット
make format

# Lint
make lint

# 型チェック
make type-check

# テスト実行
make test

# デッドコード検出
make deadcode

# YAML Lint
make yamllint

# すべてのチェックを実行
make check

# クリーンアップ
make clean
```

## プロジェクト構造

```
.
├── .github/
│   └── workflows/
│       └── ci.yml          # CI/CD設定
├── scripts/
│   └── setup.sh            # セットアップスクリプト
├── src/
│   └── pyreinfolib/
│       ├── __init__.py
│       ├── core.py         # メインコード
│       └── py.typed        # 型情報マーカー
├── tests/
│   ├── __init__.py
│   └── test_core.py        # テストコード
├── .gitignore
├── .python-version         # Pythonバージョン指定
├── .yamllint               # yamllint設定
├── Makefile                # 開発用コマンド
├── README.md
└── pyproject.toml          # プロジェクト設定
```

## このテンプレートの使い方

### 方法1: セットアップコマンドを使用（推奨）

最も簡単な方法は、インタラクティブなセットアップコマンドを使用することです：

```bash
# テンプレートをクローン
git clone https://github.com/lfworks/pyreinfolib.git my-new-project
cd my-new-project

# セットアップウィザードを実行
make setup
```

セットアップウィザードでは以下を対話形式で設定できます：

1. **リモートURLの変更**: 新しいリポジトリのURLに変更
2. **プロジェクト名の変更**: プロジェクト名とモジュール名を一括変更
   - `pyproject.toml`
   - `src/` ディレクトリ名
   - `README.md`
   - テストファイル内のimport文
3. **カスタマイズ**: 不要なファイルの削除
   - GitHub Actions ワークフロー
   - CODEOWNERS
   - CONTRIBUTING.md
   - セットアップスクリプト自体

セットアップ完了後、以下のコマンドで開発を開始できます：

```bash
# 依存関係をインストール
uv sync --all-extras

# コードを書く
# テストを書く
# CI/CDが自動的に動作します
```

### 方法2: 手動でセットアップ

GitHubで「Use this template」ボタンを使用するか、手動でクローン＆変更：

#### 1. テンプレートから新規プロジェクトを作成

```bash
# 新しいプロジェクトとしてクローン
git clone https://github.com/lfworks/pyreinfolib.git my-new-project
cd my-new-project

# リモートURLを変更
git remote set-url origin https://github.com/your-username/my-new-project.git
```

#### 2. プロジェクト名を変更

以下のファイル内の `pyreinfolib` と `pyreinfolib` を自分のプロジェクト名に置換：

- `pyproject.toml`
- `src/pyreinfolib/` ディレクトリ名
- `README.md`
- テストファイル内のimport文

#### 3. カスタマイズ

- `pyproject.toml`の`authors`、`description`などを更新
- `README.md`をプロジェクトに合わせて更新

#### 4. 開発を開始

```bash
# 依存関係をインストール
uv sync --all-extras

# コードを書く
# テストを書く
# CI/CDが自動的に動作します
```

## CI/CD

GitHub Actionsで以下のチェックが自動実行されます：

- **Format Check**: コードフォーマットの確認
- **Lint**: コード品質チェック
- **Type Check**: 型チェック（ty）
- **Test**: テスト実行（Python 3.9-3.12）
- **Dead Code Detection**: デッドコード検出

## リポジトリセキュリティ設定

### ブランチ保護ルール（Branch Protection Rules）

**mainブランチに以下の保護ルールを設定することを強く推奨します：**

#### 必須設定

1. **Require a pull request before merging（マージ前にPRを必須にする）**
   - ✅ 有効化
   - ✅ Require approvals: 最低1人の承認が必要
   - ✅ Dismiss stale pull request approvals when new commits are pushed

2. **Require status checks to pass before merging（マージ前にステータスチェックを必須にする）**
   - ✅ 有効化
   - ✅ Require branches to be up to date before merging
   - 必須チェック項目：
     - `format` (CI)
     - `lint` (CI)
     - `type-check` (CI)
     - `test` (CI)
     - `deadcode` (CI)

3. **Require conversation resolution before merging（マージ前にコメント解決を必須にする）**
   - ✅ 有効化

4. **Do not allow bypassing the above settings（上記設定のバイパスを許可しない）**
   - ✅ 有効化（管理者であってもルールを守る）

#### 推奨設定

5. **Restrict who can push to matching branches（プッシュできるユーザーを制限）**
   - mainブランチへの直接プッシュを禁止
   - 特定のユーザー/チームのみ許可（必要に応じて）

6. **Require linear history（リニアな履歴を必須にする）**
   - マージコミットを防ぐ（Squash or Rebaseのみ許可）

### CODEOWNERS設定

`.github/CODEOWNERS`ファイルでコードレビューの承認者を設定できます。このテンプレートでは、すべてのファイルの変更に対してオーナーの承認が必要になるように設定されています。

設定を有効化するには、ブランチ保護ルールで「Require review from Code Owners」を有効にしてください。

## PyPIへの公開

このテンプレートはPyPI公開を想定した構造になっています：

```bash
# ビルド
uv build

# PyPIへアップロード（testpypiで先にテスト推奨）
uv publish --token <your-pypi-token>
```

## 貢献

1. このリポジトリをフォーク
2. フィーチャーブランチを作成 (`git checkout -b feature/amazing-feature`)
3. 変更をコミット (`git commit -m 'Add some amazing feature'`)
4. ブランチにプッシュ (`git push origin feature/amazing-feature`)
5. プルリクエストを作成

## 参考リンク

- [uv documentation](https://github.com/astral-sh/uv)
- [ruff documentation](https://docs.astral.sh/ruff/)
- [ty documentation](https://github.com/astral-sh/ty)
- [vulture documentation](https://github.com/jendrikseipp/vulture)
- [pytest documentation](https://docs.pytest.org/)
