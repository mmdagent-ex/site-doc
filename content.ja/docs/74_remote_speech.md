---
title: 音声を再生する
slug: lipsync
---
{{< hint info >}}
外部音声のリップシンクの機能は Plugin_Remote が提供しています。利用時はこのプラグインが有効になっているか確かめてください。
{{< /hint >}}

# 音声を再生する

外部モジュールから音声データを MMDAgent-EX へ渡し、リップシンク付きで再生することができます。実現のための方法がいくつか用意されています。以下、順に説明します。

## 方法１：ファイルで渡す

音声データをファイルに保存し、そのパスを MMDAgent-EX に指定して再生させる方法です。以下の手順で実行します。

- 音声合成（あるいは録音）した内容をオーディオファイルに保存
- そのパスを指定した **SPEAK** コマンドを MMDAgent-EX に送信

**SPEAK** コマンドの詳しい使い方については[「サウンドを再生する」で説明しています。](../sound/#%e9%9f%b3%e5%a3%b0%e5%86%8d%e7%94%9f-with-%e3%83%aa%e3%83%83%e3%83%97%e3%82%b7%e3%83%b3%e3%82%af) 

この方法はシンプルで簡単に実現できますが、外部プロセスとMMDAgent-EXが同じマシンの上で動いている必要があります。また、再生する音声データはファイル単位で、連続した音声ストリームの流し込みには使えません。

## 方法２：ソケットから音声データを流し込んで再生

[ソケット接続](../remote-control) を使って音声データをソケット経由で流し込む方法です。ソケット接続ではテキストメッセージだけでなく、以下に示す特定のヘッダを使うことで音声データを同一ソケット上で送ることができます。[TCPIP接続](../remote-tcpip)と [WebSocket接続](../remote-websocket) のいずれでも動作します。

**この方法で音声データを送る場合、音声データのフォーマットは、エンコード無しの 16kHz, 16bit singed short, モノラル の PCM データである必要があります**。これ以外のサンプリングレートや形式には対応しないので注意してください。

以下、手順を説明します。ソケットからの音声流し込みを使う場合、ソケット接続を確立した後に以下の２つのメッセージをあらかじめ MMDAgent-EX へ送ります。1つ目は操作開始のメッセージで、2つ目はリップシンクさせるモデルのモデルエイリアス名を指定します。それぞれ `__AV_START\n` のように末尾に改行コードを入れて送ることを忘れないでください。

```text
__AV_START
__AV_SETMODEL,モデルエイリアス
```

続けて転送モードを指定するメッセージを同様に送ります。連続した音声ストリームを送り続ける場合は `SNDSTRM\n` を送ります。この場合、終端はMMDAgent-EX側で自動検出されます。ファイルなど、区切られた音声データを送る場合は`SNDFILE\n` を送ります。この場合、終端は送る側が明示的に指定します（後述）。これらのメッセージは省略することもでき、その場合は前者の `SNDSTRM\n` がデフォルトとなります。

```text
(ストリーミングの場合)
SNDSTRM
(ファイル送信の場合)
SNDFILE
```

その後、オーディオデータを短いチャンクごとに区切ってソケットへ送信します。１つのチャンクは、以下のように文字列 "`SND`" に続けて4桁(10進)のチャンク長（バイト数）、それに続けてその指定したチャンク長（バイト数）分のデータ本体を繋げます。改行コードは不要です。これを音声の短いチャンク（1024バイト程度）ごとに連続して送ってください。

```text
SNDxxxxyyyyyyyyyyyyyyyyyyy....
  SND: ヘッダ
  xxxx: データ長（バイト数） 10進数
  yy...　データ長分の音声波形データ
```

ストリーミングの場合（`SNDSTRM\n` 指定時）は、上記のやりかたで短いチャンクごとに音声を送り続けます。`SNDFILE\n` 指定時は、音声終端は MMDAgent-EX 側で自動検出されないので、終端まで送信し終えたら `SNDBRKS\n` を送って入力終了をMMDAgent-EXに伝える必要があります。

この方法は方法１に比べて手間がかかり、音声データ形式に制約がありますが、連続した音声ストリームの流し込みができることと、異なるマシン間でもやりとりできるという利点があります。

### サンプルプログラム

マイクから音声を取り込んでMMDAgent-EXに逐次流し込むサンプルプログラムです。

{{< tabs "sample_remote_speech" >}}
{{< tab "WebSocket" >}}
### WebSocket方式

以下を .mdf に書いて、MMDAgent-EX が WebSocket プロトコルで localhost:9001 へ接続するように設定してください。

{{<mdf>}}
Plugin_Remote_Websocket_Host=localhost
Plugin_Remote_Websocket_Port=9001
Plugin_Remote_Websocket_Directory=/chat
{{</mdf>}}

また PyAudio をインストールしてください

```shell
pip install pyaudio
```

先に以下のサーバスクリプトを実行してから、MMDAgent-EX を起動し、マイクに向かってしゃべると CGエージェントがリップシンクしながら音声を再生するのを確認してください。（うまく動かない場合はオーディオデバイスの設定を確認してください）。

```python
#
# audio streaming example
#
import asyncio
import websockets
import time
import pyaudio

##################################################
# handler for received messages
async def consumer_handler(websocket):
    async for message in websocket:
        print(f"Received message: {message}")

##################################################
# handler to send message: you must append "\n" for each message!
async def producer_handler(websocket):
    # send setup messages.  Example content has model loaded as "0"
    await websocket.send("__AV_START\n")
    await websocket.send("__AV_SETMODEL,0\n")
    # open audio device
    chunk_samples = 480
    chunk_bytes = chunk_samples * 2
    p = pyaudio.PyAudio()
    stream = p.open(
        format=pyaudio.paInt16,
        channels=1,
        rate=16000,
        input=True,
        frames_per_buffer=chunk_samples
        )
    while True:
        # record audio and send to MMDAgent-EX
        input_data = stream.read(chunk_samples)
        header = ("SND" + f"{chunk_bytes:04}").encode('ascii')
        payload = bytearray(header + input_data)
        await websocket.send(payload)
        await asyncio.sleep(0.01)

##################################################
# handler for each connection
async def handle_client(websocket, path):
    # create task to read from the socket
    consumer_task = asyncio.create_task(consumer_handler(websocket))
    # create task to write to the socket
    producer_task = asyncio.create_task(producer_handler(websocket))
    # wait at least one task has been terminated
    done, pending = await asyncio.wait(
        [consumer_task, producer_task],
        return_when=asyncio.FIRST_COMPLETED,
    )
    # cancel other task and close connection
    for task in pending:
        task.cancel()

# main
async def main():
    async with websockets.serve(handle_client, "localhost", 9001):
        await asyncio.Future()  # run forever

if __name__ == '__main__':
    asyncio.run(main())

```

{{< /tab >}}
{{< tab "TCPIP" >}}
### TCPIP方式

MMDAgent-EX を TCP/IP サーバとして起動し、クライアントの Python スクリプトから音声を流し込む例です。

以下を .mdf に書いて、MMDAgent-EX が localhost:60001 を listen するよう設定してください。

{{<mdf>}}
Plugin_Remote_EnableServer=true
Plugin_Remote_ListenPort=60001
{{</mdf>}}

また PyAudio をインストールしてください

```shell
pip install pyaudio
```

MMDAgent-EX を起動したあと、下記のスクリプトを起動してマイクに向かってしゃべり、 CGエージェントがリップシンクしながら音声を再生するのを確認してください。（うまく動かない場合はオーディオデバイスの設定を確認してください）。


```python
import socket
import pyaudio

server = ("127.0.0.1", 60001)
tcp_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp_client.connect(server)

tcp_client.send(bytearray("__AV_START\n".encode('ascii')))
tcp_client.send(bytearray("__AV_SETMODEL,0\n".encode('ascii')))
chunk_samples = 480
chunk_bytes = chunk_samples * 2
p = pyaudio.PyAudio()
stream = p.open(
    format=pyaudio.paInt16,
    channels=1,
    rate=16000,
    input=True,
    frames_per_buffer=chunk_samples
    )
while True:
    input_data = stream.read(chunk_samples)
    header = ("SND" + f"{chunk_bytes:04}").encode('ascii')
    payload = bytearray(header + input_data)
    tcp_client.send(payload)
```

{{< /tab >}}
{{< /tabs >}}

## 方法３：口パクさせる

外部プロセスで完結して音声の再生まで行い、MMDAgent-EX には「口パク」だけさせることもできます。この場合、外部プロセスでリップシンク用のメッセージ **LYPSYNC_START** を作成し、音声を再生するタイミングに合わせて MMDAgent-EX に送ります。

**LIPSYNC_START** メッセージはリップシンクの実行を指示するメッセージです。第1引数は対象とするモデルのエイリアス名、第2引数がリップシンクの内容です。内容は、音素名および持続時間（単位はミリ秒）の列をカンマ区切りで指定します。

{{<message>}}
LIPSYNC_START|gene|sil,187,k,75,o,75,N,75,n,75,i,62,ch,75,i,87,w,100,a,87,sil,212
{{</message>}}

デフォルトで使える音素名は、Open JTalk で用いられている音素セットです。これは「リップシンク定義ファイル」を編集することで容易に変更・拡張可能です。

{{< details "リップシンク定義ファイルについて" close >}}

音素名の定義および各音素名からキャラクターのモーフへの変換規則が、MMDAgent-EX の実行ファイルがあるディレクトリの `AppData` フォルダ以下のファイル `lip.txt` で定義されています。一部を以下に示します。デフォルトでは Open JTalk の音素セットに対して「あ」「い」「う」「お」の4つのモーフの重み付き結合として表現するよう定義されています。これを編集、あるいは音素を追加することで、任意の音素列・モーフに拡張できます。

```text
# number of expressions
4
# expression names
あ
い
う
お
# number of phonemes
69
# phone names and interpolation weight
A   0.2 0.0 0.0 0.0
E   0.1 0.3 0.1 0.0
I   0.0 0.2 0.0 0.0
N   0.0 0.0 0.0 0.0
O   0.0 0.0 0.0 0.2
U   0.0 0.0 0.2 0.0
a   0.5 0.0 0.0 0.0
...
```

{{< /details >}}

MMDAgent-EX は **LIPSYNC_START** で送られた音素列を定義に従ってモーションに変換し、指定モデル上で再生を開始します。リップシンク開始時に **LIPSYNC_EVENT_START** が、終了時に **LIPSYNC_EVENT_STOP** が発行されます。

{{<message>}}
LIPSYNC_EVENT_START|(model alias)
LIPSYNC_EVENT_STOP|(model alias)
{{</message>}}

**LIPSYNC_STOP** で途中で中断もできます。

{{<message>}}
LIPSYNC_STOP|(model alias)
{{</message>}}

この方法の外部プロセスから見たメリット・デメリットです。

メリット：

- 再生が自前なので音声クオリティや再生デバイス等の MMDAgent-EX の仕様に制約されない
- リップシンク内容を制御できる
- 拡張性が高い

デメリット：

- 音素列と持続時間情報からリップシンク情報を自前で作成する必要がある
