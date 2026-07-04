# Antigravity 設定管理 (dot-gemini)

このリポジトリは、Google Antigravity のグローバル設定、ルール、カスタムスキル、および各種スクリプトを Git で一元管理するためのものです。

## ディレクトリ構造と管理対象

実体となるこのリポジトリを `~/.gemini` にシンボリックリンク化して運用します。
`.gitignore` により、一時キャッシュや会話ログ（`brain/` 等）を除外した上で、以下の設定関連ファイルのみをGitの追跡対象にしています。

```
~/_src/dot-gemini
├── .gitignore             # ホワイトリスト形式の除外設定
├── GEMINI.md              # グローバルルール（旧 CLAUDE.md）
├── README.md              # この手順書
├── rules/                 # 共通ワークフローとジャンル別DNA（writing-workflow.md / novel-dna.md / technical-dna.md）
│   └── character_sheet.md # Geminiの性格・口調（任意・非公開）
├── context/
│   └── persona.md         # ユーザーの人となり・好み・価値観（任意・非公開）
├── config/
│   ├── config.json        # アプリのグローバル設定
│   ├── mcp_config.json    # MCPサーバー設定
│   └── skills/            # /draft などのカスタムスキル
└── antigravity/
    ├── scripts/           # 共通スクリプト（export-transcript.py など）
    └── templates/         # プロジェクト開始用テンプレート
```

---

## 環境構築と同期手順

別の環境でこの設定を再現、または再リンクする場合は以下の手順を実行します。

### 1. シンボリックリンクの作成

既存の `~/.gemini` フォルダを退避させ、このリポジトリへのリンクを作成します。

```bash
# 既存フォルダのバックアップ（存在する場合）
mv ~/.gemini ~/.gemini.bak

# シンボリックリンクの作成
ln -s ~/_src/dot-gemini ~/.gemini
```

### 2. コマンドの動作確認

リンク作成後、Antigravity アプリまたは CLI を再起動し、以下のグローバル設定やカスタムスキルが正しく読み込まれるかを確認します。

* `/novel-init` (小説プロジェクトの初期化)
* `/tech-init` (技術書プロジェクトの初期化)
* `/check-text` (テキスト校正)
* `/end` (会話履歴のエクスポート)

---

## 運用上の注意点

* **`.gitignore` による安全な管理**:
  実行時に自動生成される一時フォルダ（`antigravity/scratch/`）や、会話データデータベース（`antigravity/brain/`、`antigravity/conversations/`）は、セキュリティと容量の観点から Git 追跡対象から完全に除外されています。
* **性格・ユーザー情報のカスタマイズ（任意）**:
  `rules/character_sheet.md`（Gemini自身の性格・口調）と `context/persona.md`（ユーザーの人となり）は、このリポジトリでは追跡していない個人用ファイルです。存在する場合のみ `GEMINI.md` から参照されます。公開リポジトリなので、機微な情報を書く場合は非公開のままにしておいてください。
* **シンボリックリンクの維持**:
  設定を追加・変更した際は、直接 `~/.gemini` を編集すれば、自動的にこのリポジトリ内の実ファイルが更新されます。変更後は通常通り Git でコミット＆プッシュしてください。
* **ルールファイルの名称（GEMINI.md と CLAUDE.md の使い分け）**:
  * **グローバル（全体適用）**: `~/.gemini/GEMINI.md` に配置し、Antigravity によって自動で読み込まれます。
  * **プロジェクト個別（ワークスペース適用）**: 本リポジトリ内の各種カスタムスキルやテンプレート（`antigravity/skills/`, `antigravity/templates/`）は、Claude Code との互換性を維持・併用するため、プロジェクト固有のルールファイルとして **`CLAUDE.md`** をそのまま生成・参照する設定になっています（通常 Antigravity のプロジェクト個別ルールで使われる `GEMINI.md` や `AGENTS.md` ではない点にご注意ください）。これにより、同一の原稿・開発フォルダを Claude Code と Antigravity の両方から同じルールで操作できます。
