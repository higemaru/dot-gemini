# Antigravity 移行用フォルダ

このフォルダは、`~/.claude/` のカスタムスキル、テンプレート、ルール設定、各種スクリプトを Antigravity 用にコンバートしたものです。

## 使い方

内容を確認して問題がなければ、以下のコマンドを実行して Antigravity のグローバル設定ディレクトリにコピーしてください。

```bash
# ディレクトリの作成
mkdir -p ~/.gemini/antigravity/skills
mkdir -p ~/.gemini/antigravity/templates
mkdir -p ~/.gemini/antigravity/scripts
mkdir -p ~/.gemini/rules

# グローバルルールのコピー
cp ~/Downloads/dot-gemini/GEMINI.md ~/.gemini/GEMINI.md

# 個別ルールのコピー
cp -R ~/Downloads/dot-gemini/rules/ ~/.gemini/rules/

# スキルとテンプレート、スクリプトのコピー
cp -R ~/Downloads/dot-gemini/skills/ ~/.gemini/antigravity/skills/
cp -R ~/Downloads/dot-gemini/templates/ ~/.gemini/antigravity/templates/
cp -R ~/Downloads/dot-gemini/scripts/ ~/.gemini/antigravity/scripts/
```

コピー完了後、Antigravity でこれらのグローバルルール、スキル、スクリプトが利用可能になります。
