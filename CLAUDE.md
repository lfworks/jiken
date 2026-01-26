# CLAUDE.md

このドキュメントは、Claudeがこのプロジェクトのコードを生成する際に従うべきガイドラインを記載しています。

## プロジェクト哲学

- **効率の良いライブラリ**: シンプルで小さな責務を果たすために必要な最小限の機能を提供すること
- **依存関係の最小化**: 依存するthird partyライブラリを最小限にすること
  - 依存するライブラリが増えれば増えるほどソフトウェアの品質を落とすため

## コーディング規約

### 命名規則
- **クラス名**: CamelCase
- **関数/メソッド名**: snake_case
- **プライベートメンバ**: アンダーバー（_）開始
- **型ヒント**: 可能な限り使用
- **docstring**: Googleスタイル、英語で簡潔に記述
- **エラーメッセージ**: 英語で記述

### 例外処理ガイドライン
- **例外チェイン**: `raise NewException(msg) from original_exception` 形式を使用
  - 元の例外情報を保持して、デバッグ時に根本原因を追跡可能にする
  - 参考: [Python例外処理ドキュメント](https://docs.python.org/ja/3/library/exceptions.html#exception-context)
- **不要な変数代入の回避**: エラーメッセージは直接記述し、`error_msg`等の中間変数は避ける

### 設計原則
- **SRP（単一責任原則）**: 各クラスは一つの責任のみを持つ
- **クラス化**: 将来の拡張や依存注入を見据えて基本的にクラス化
- **テスト容易性**: 外部I/Oは抽象化してMock/patchしやすく設計
- **継承より移譲**: 継承階層は浅く、compositionを優先
  - Pythonの`typing.Protocol`を活用してインターフェースを定義

## テスト時のベストプラクティス

### テストの配置と構造
- **単体テスト**: `test/`ディレクトリ配下に配置
- **外部依存の排除**: DB接続、HTTP通信は行わない
- **テストデータ**: `test/test_data/`配下に配置

### Mock/Patchの活用
- **Mock/Patchの活用**: 外部サービスは適切にMock化
- **create_autospecの使用**: `unittest.mock.create_autospec(Class, instance=True)`でモックを作成し、実際のクラスのインターフェースを保証
- **雑なsetUp避ける**: 各テストメソッドで必要な依存関係のみをセットアップ
- **Loggerのmockは避ける**: log出力の確認は不要

### テーブル駆動テスト
複数のパラメータやシナリオをテストする場合は、`@parameterized.expand`を使用してテーブル駆動テストを実装する：

```python
from parameterized import parameterized

class ExampleTestCase(unittest.TestCase):
    @parameterized.expand(
        [
            # テストケース1: 正常系
            (
                # 入力データ
                {"input": "valid_data", "flag": True},
                # 期待値
                ("expected_output", 200),
            ),
            # テストケース2: 異常系
            (
                {"input": None, "flag": False},
                (None, None),
            ),
        ]
    )
    def test_example_function(self, input_data, expected):
        result = example_function(input_data)
        self.assertEqual(expected, result)
```

## 実装時のガイドライン

### 1. 新しいコードを書く前に
- 既存の類似機能がないかを確認
- 共通ユーティリティの活用を検討
- 設定ファイルの適切な利用

### 2. 外部データソースを扱う際
- レート制限の考慮
- 適切なエラーハンドリング
- リトライ機構の実装

### 3. 大量データの処理時
- メモリ使用量の監視
- バッチ処理の実装
- 進捗状況の適切な報告

### 4. テストの記述
- 正常系・異常系の両方をテスト
- Mockを活用した外部依存の排除
- エッジケースの考慮
