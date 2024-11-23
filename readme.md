# 「AITuberを作ってみたらプロンプトエンジニアリングがよくわかった件」 サンプルソースコード
## 概要
このリポジトリは[「AITuberを作ってみたらプロンプトエンジニアリングがよくわかった件」](https://amzn.to/3OoGSdI)のサンプルソースコードです。  
[「AITuberを作ってみたら生成AIプログラミングがよくわかった件」](https://amzn.to/4fYlA29)の続本になります。[前書のリポジトリ](https://github.com/sr2mg/aituber_python_programing_example)  

本リポジトリでは、本に出てきたコードを公開しています。
なお、本で発生していたコード不備やバグに関しては発見次第リポジトリで修正しているため、本のコードとリポジトリのコードが若干異なる場合があります。
その場合はこちらのリポジトリのコードを正としてください。

## 訂正について
本書にはいくつかの誤りがあります。
日経BP社のページ・著者のnoteを参照してください。
- https://bookplus.nikkei.com/atcl/catalog/update/24/11/19/00230/
- https://note.com/sr2mg/n/n04248868443d


## 動作環境
- python 3.11.9
- poetry 

## Get Started
### Poetryを持っている人
以下のコマンドでインストールしてください。
```
poetry install
```

### Poetryを持っていない人
以下の順番でインストールしてください。

#### venvの作成
```
python -m venv .venv
```
#### venvの有効化
(WindowsPowerShell)
```
.venv\Scripts\Activate.ps1
```
(WindowsComandPrompt)
```
.venv\Scripts\activate.bat
```
(macOS/Linux)
```
source .venv/bin/activate
```
#### requirements.txtのインストール
```
pip install -r requirements.txt
```
#### .envファイルの作成
.env.templateをコピーして.envファイルを作成してください。
```
cp .env.template .env
```
このファイルに環境変数を記述してください。