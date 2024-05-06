# raspi-cam

Raspberry Piとカメラを使用した実習教材です。
本レポジトリは[デジらくだ](https://digirakuda.org/)の取り組みの一環で使用されます。

# 使い方

## Raspberry Pi本体のセットアップ

次の機材を接続してRaspberry Piを立ち上げてください。

- Raspberry Pi 4
- ACアダプタ
- ディスプレイ
- HDMIケーブル
- マウス
- キーボード
- USBカメラ

## リポジトリをダウンロードする

このWebページは、リポジトリと呼ばれる単位のプログラムの配布場所です。
まずはこのリポジトリをダウンロードして、リポジトリ内のプログラムを手元のRaspberry Piで使用できるようにしてください。
ターミナルから次のコマンドを実行することでダウンロードできます。

```bash
git clone https://github.com/siida36/raspi-cam
```

## 実行環境のセットアップ

リポジトリをダウンロードしたら、次はプログラムを実行するための準備を行います。

### ローカルリポジトリへ移動する

ダウンロードするコマンドを実行したディレクトリの下には `raspi-cam` というディレクトリが追加されています。
そのディレクトリの中へと移動してください。

```bash
cd raspi-cam
```

### Raspberry Piで利用するソフトウェアの更新

ターミナルから次のコマンドを実行してください。
`apt update`　でアップグレード可能なソフトウェアのリストを更新し `apt upgrade` でアップグレードを実施します。
時間がないときは `apt upgrade` を省略しても構いません。

```bash
sudo apt update
sudo apt upgrade
```

### エディタのインストール

プログラムを編集するためのソフトウェアであるエディタをインストールします。
Windowsにおけるメモ帳やVS　Codeと同様の役割があります。

```bash
sudo apt install -y vim
```

### 仮想環境の作成

プログラムを実行するためには、さまざまな他のソフトウェアをインストールする必要があります。
そしてこのリポジトリでは、インストール先を仮想環境と呼ばれる場所に指定します。
仮想環境を使用することで、インストールしたソフトウェアを管理しやすくなります。

ターミナルから次のコマンドで仮想環境 `raspi-cam` を作成してください。
なお、すでに作成済みの場合は実行する必要はありません。

```bash
python -m venv raspi-cam
```

### 仮想環境の起動

作成した仮想環境を起動します。

```bash
source raspi-cam/bin/activate
```

---

（注) もし起動に失敗する場合は、仮想環境を作成したディレクトリではない可能性があります。
次のコマンドを実行してディレクトリ内のファイルとディレクトリを確認し、 `raspi-cam` というディレクトリが存在するか確認してください。

```bash
ls -lha
```

### 仮想環境内にOpenCVをインストール

OpenCVは、画像処理を行うためのライブラリ（ソフトウェア）です。
カメラで撮影した画像を元に様々なプログラミングを行う際に使用します。

```bash
pip install opencv-python
```

### カメラ撮影用ソフトウェアのインストール

```bash
sudo apt install -y fswebcam
```

以上で、仮想環境の作成は完了です。

## 実習1

### 画像を１枚撮影する

次のコマンドを実行することで、カメラを使って撮影することができます。
撮影された画像は `output` ディレクトリの中に保存されます。

```bash
python src/raspi_cam.py
```

### 画像を定期的に撮影する

Raspberry PiのようなLinuxのOSでは、cronと呼ばれる定期的にコマンドを実行するソフトウェアを利用できます。
次のコマンドでcronの編集画面を開いてください。

```bash
crontab -e
```

また、初回実行時にはどのエディタでcronを編集するか質問されます。 `/usr/bin/vim.basic` と指定されている選択肢の番号を指定してください。

編集画面では末尾へ次のように記載してください。

```crontab
* * * * * python /home/pi/raspi-cam/src/raspi_cam.py
```

記載後、エディタを保存して閉じると、１分ごとに画像が撮影されるようになります。

### 撮影した画像をネットワークから確認する

まずはRaspberry Piでローカルサーバを立ち上げます。
これにより、実行したディレクトリをネットワーク上からアクセスできるようになります。

```bash
python -m http.server 8080
```

次にRaspberry Piではない別のPCで、Webブラウザを立ち上げてください。
そしてURL欄に次のように打ち込むと、Raspberry Piのディレクトリにアクセスできます。

`http://localhost:8080`

公開されているディレクトリに `output` があることを確認したら、その中にある写真を覗いてみましょう。
