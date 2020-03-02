# mmgmail

Gmail 操作ライブラリ。

## 必要な環境変数

特になし。

## インストール

```(sh)
pip install git+https://github.com/yukkun007/mmgmail
```

## アップグレード

```(sh)
pip install -U git+https://github.com/yukkun007/mmgmail
```

## 使い方 (コードからモジュールを利用)

[参照](#モジュールを利用)

## 使い方 (コマンドラインアプリ)

```(sh)
mmgmail --help
```

## アンインストール

```(sh)
pip uninstall mmgmail
```

## 開発フロー

### 環境構築

1. プロジェクトディレクトリに仮想環境を作成するために下記環境変数を追加

   - Linux

     ```(sh)
     export PIPENV_VENV_IN_PROJECT=true
     ```

   - Windows

     ```(sh)
     set PIPENV_VENV_IN_PROJECT=true
     ```

1. `pip install pipenv`
1. `git clone git@github.com:yukkun007/mmgmail.git`
1. `pipenv install --dev`

### install package

下記は編集可能モードでインストールされる。

```(sh)
pip install -e .
```

通常のインストールは下記だがソース編集の都度`upgrade package`が必要なので基本は`-e`をつける。

```(sh)
pip install .
```

### upgrade package

```(sh)
pip install --upgrade . (もしくは-U)
```

## 開発行為

### モジュールを利用

```(python)
$ python
>>> import mmgmail
>>> mmgmail.do_something("Foo")
```

### コマンドラインアプリを実行

```(sh)
pipenv run start (もしくはmmgmail)
```

### unit test

```(sh)
pipenv run ut
```

### lint

```(sh)
pipenv run lint
```

### create api document (sphinx)

```(sh)
pipenv run doc
```
