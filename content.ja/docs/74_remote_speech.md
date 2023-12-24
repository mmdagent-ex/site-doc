---
title: 音声データを流し込む
slug: remote-speech
---
{{< hint info >}}
外部音声のリップシンクの機能は Plugin_Remote が提供しています。利用時はこのプラグインが有効になっているか確かめてください。
{{< /hint >}}

# 音声データを流し込む

外部モジュールから音声データを MMDAgent-EX へ渡し、リップシンク付きで再生することができます。実現のための方法がいくつか用意されています。以下、順に説明します。

## 方法１：ファイルで渡す

音声データをファイルに保存し、そのパスを MMDAgent-EX に指定して再生させる方法です。以下の手順で実行します。

- 音声合成（あるいは録音）した内容をオーディオファイルに保存
- そのパスを指定した **SPEAK** コマンドを MMDAgent-EX にソケット等で送信

**SPEAK** コマンドの詳しい使い方については[「サウンドを再生する」](../sound/#%e9%9f%b3%e5%a3%b0%e5%86%8d%e7%94%9f-with-%e3%83%aa%e3%83%83%e3%83%97%e3%82%b7%e3%83%b3%e3%82%af)をご覧ください。

この方法はシンプルで簡単ですが、ファイル名の受け渡しになるので、送信元のプロセスとMMDAgent-EXが同じファイルシステムを共有するマシン上で動いている必要があります。また、再生する音声データはファイル単位のみで、連続した音声ストリームには使えません。

## 方法２：ソケットから音声データを流し込む

[ソケット接続](../remote-control) を使ってソケット経由で音声データを外部から流し込むことができます。ソケット接続ではテキストメッセージのやりとりができますが、以下に示す特定のヘッダを使うことで音声データを同一のソケット上で送ることができます。[TCPIP接続](../remote-tcpip)と [WebSocket接続](../remote-websocket) のいずれでも動作します。

**この方法で音声データを送る場合、音声データのフォーマットは、エンコード無しの 16kHz, 16bit singed short, モノラル の PCM データである必要があります**。これ以外のサンプリングレートや形式には対応しないので注意してください。また、リップシンクするモデルは[.shapemap にリップシンク情報を記述する](../sound/#準備-1)必要があります。

### 通信手順の解説

以下、通信手順を説明します。ソケットからの音声流し込みを使う場合、ソケット接続を確立した後に以下の２つのメッセージをあらかじめ MMDAgent-EX へ送ります。1つ目は操作開始のメッセージで、2つ目は**リップシンクさせるモデルのモデルエイリアス名**の指定です。それぞれ `__AV_START\n` のように末尾に改行コードを入れて送ることを忘れないでください。

```text
__AV_START
__AV_SETMODEL,モデルエイリアス
```

続けて転送モードを指定するメッセージを送ります。連続した音声ストリームを送り続ける場合は `SNDSTRM\n` を送ります。指定しない場合のデフォルトはこちらです。この場合、MMDAgent-EX側で無音区間の除去と音声区間検出が自動的に行われます。ファイルなどあらかじめ区切られた音声データを送る場合は`SNDFILE\n` を送っておきます。この場合、MMDAgent-EX側で無音区間の検出・除去は行われません。音声データの終端は、送る側が明示的に指定する必要があります（後述）。

```text
(ストリーミングの場合)
SNDSTRM
(ファイル送信の場合)
SNDFILE
```

その後、オーディオデータを短いチャンクごとに区切って送信します。１つのチャンクは、以下のように文字列 "`SND`" に続けて4桁(10進)のチャンク長（バイト数）、それに続けてその指定したチャンク長（バイト数）分の音声波形データを繋げます。改行コードは不要です。これを音声の短いチャンク（1024バイト程度）ごとに連続して送ります。チャンクのサイズは 4K Bytes を越えないようにしてください。

```text
SNDxxxxyyyyyyyyyyyyyyyyyyy....
  SND: ヘッダ
  xxxx: データ長（バイト数） 10進数
  yy...　データ長分の音声波形データ
```

`SNDFILE\n` 指定時は、音声終端は MMDAgent-EX 側で自動検出されないので、終端まで送信し終えたら `SNDBRKS\n` を送って入力終了をMMDAgent-EXに伝えます。

### サンプル

以下、「マイクデバイスから音声を録音しながらMMDAgent-EXにリアルタイムに流し込む」サンプルスクリプトを示します。WebSocket と TCPIP の両方のサンプルを示します。マイクデバイスを準備してから実行してください。

{{< tabs "sample_remote_speech" >}}
{{< tab "WebSocket" >}}
### WebSocket方式

MMDAgent-EX が WebSocket プロトコルで localhost:9001 へ接続するよう、以下を Example の .mdf に書いてください。（TCP/IP方式とは同時に使えないので、TCP/IP のサーバあるいはクライアントの設定があれば消すかコメントアウトしてください）

{{<mdf>}}
Plugin_Remote_Websocket_Host=localhost
Plugin_Remote_Websocket_Port=9001
Plugin_Remote_Websocket_Directory=/chat
{{</mdf>}}

以下は WebSocket サーバのサンプルスクリプトです。

```python
#
# audio streaming example: websocket server
#
#!pip install asyncio
#!pip install websockets
#!pip install pyaudio
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

まず上記のサーバスクリプトを実行し、次に MMDAgent-EX を Example で起動してください。起動したら、マイクに向かってしゃべると CGエージェントがリップシンクしながらその音声を再生します。うまく動かない場合はオーディオデバイスの設定を確認してください。

{{< /tab >}}
{{< tab "TCP/IP" >}}
### TCPIP方式

MMDAgent-EX が TCP/IP サーバとして起動し、クライアントが接続して音声を流し込む場合のサンプルです。まず以下を Example の .mdf に書いてください。（WebSocketと同時には使えないので、WebSocketの設定があれば消すかコメントアウトしてください）

{{<mdf>}}
Plugin_Remote_EnableServer=true
Plugin_Remote_ListenPort=50001
{{</mdf>}}

MMDAgent-EX を起動したあと、下記のスクリプトを起動することで接続され、音声のストリーミングが始まります。マイクに向かってしゃべり、 CGエージェントがリップシンクしながら音声を再生するのを確認してください。（うまく動かない場合はオーディオデバイスの設定を確認してください）。

```python
#
# audio streaming example: tcp/ip client
#
#!pip install pyaudio
import socket
import pyaudio

# connect to localhost:50001
server = ("localhost", 50001)
tcp_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp_client.connect(server)

# send initial setup message: example script starts a model with "0", so specify it
tcp_client.send(bytearray("__AV_START\n".encode('ascii')))
tcp_client.send(bytearray("__AV_SETMODEL,0\n".encode('ascii')))

# open audio for recording
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

# main loop to capture audio and send it to MMDAgent-EX
while True:
    input_data = stream.read(chunk_samples)
    header = ("SND" + f"{chunk_bytes:04}").encode('ascii')
    payload = bytearray(header + input_data)
    tcp_client.send(payload)
```

ファイル等のバッファされたオーディオデータを送る場合は以下の点に注意してください。

1. 1回あたり送信できるチャンクのサイズは1000バイト未満です。長いオーディオデータは小さなチャンク（1000バイト未満）に細切れにして送ってください。
2. 送信されたオーディオデータは再生を待たずに即座に受け取られ、MMDAgent-EX内の別スレッドでバッファリングされつつ順次再生されます。このとき、ソケット接続を close したら、音声再生も含めて終了するため、データ送信終了後すぐに接続を close するとオーディオが最後まで再生されずに止まってしまいます。送信後すぐに接続をクローズしたい場合は、再生秒数分だけ待ってから close するようにしてください。

{{< /tab >}}
{{< /tabs >}}

この方法は、方法１に比べてコーディングが必要で、音声データの形式にも制約がありますが、連続した音声ストリームの流し込みができることと、送信プロセスと MMDAgent-EX が異なるマシン間でもやりとりできるという利点があります。

## 方法３：口パクさせる

外部プロセスだけで音声の再生までを自前で行い、MMDAgent-EX には「口パク」だけさせることもできます。この場合、外部プロセスでリップシンク用のメッセージ **LYPSYNC_START** を作成し、音声を再生するタイミングに合わせてソケット等で MMDAgent-EX に送ります。

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
