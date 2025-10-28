---
title: Format of PACKAGE_DESC.txt
slug: package-desc-format
---
# Format of PACKAGE_DESC.txt

## Basic

```text
# Specify the MDF file to launch.
# If not specified, search the content folder and launch from the .mdf
# file located in the deepest folder hierarchy.
execMDFFile=some/where/foobar.mdf

# Text to display in bookmarks and history.
# If not specified, the file name is used.
# If only "label=" is specified, no text label will be shown.
#label=string

# Image file to display in bookmarks and history.
# Displayed together with the label above (if label= is empty, only the image will be shown).
# It is stretched to 7:1, so creating it with a 7:1 aspect ratio is best.
# If not specified, a file named banner.png will be searched for.
# If banner.png does not exist either, no image is used.
#image=hoge.png

# Specify a README file to be shown to the content user.
# If specified, it is displayed full-screen on the content's first launch.
# Must be a text file (UTF-8).
#readme=readme.txt

# Specify whether to force user agreement after showing the README file.
# If set to true, two buttons, Accept and Decline, will appear at the bottom of the README,
# and pressing Decline can prevent playback.
# If set to true, be sure to also specify the readme above.
#readmeForceAgreement=true
```

## Security

```text
# Disable browsing in the built-in browser
nonBrowse=true

# Disallow launching on desktop OS (Win/Mac/Linux)
nonDesktop=true
```

## Auto-update

Automatically update specific files while content is playing. At the specified interval, query the content's source server for updates to the specified files, and if the server reports an update, download only those files in the background.

Normally, web content updates and new diffs are checked and downloaded at content startup. In addition to that, using this option allows specified files to be updated in the background while the content is running, without stopping playback.

```text
# Specify filenames to auto-check and attempt background updates for.
autoUpdateFiles=xxx.mdf[,xxx.fst,…]

# Specify the auto-check interval in seconds
autoUpdatePeriod=20
```

## Data collection

Settings to upload logs recorded by `LOG_START` and `LOG_FINISH` to a server. When using this, ensure proper operational safeguards (for example, obtain user consent) to avoid covert data collection.

```text
# Enable server upload for logs.
# Specify the destination server URL.
#logUploadURL=url_string

# Use to specify the HTTP version string.
# Default is "HTTP/1.1"
#logUploadHTTPVersion=STRING

# Specify a log identifier string
# Use when you want to embed content name or version into logs
#logIdentifier=string
```

## Plugin_Kafka

```text
# Broker address for Apache Kafka logging.
kafkaBroker=host:port

# Partition number of the broker to connect.
kafkaPartition=partition_number

# Producer name to connect. When this option is specified, the app will
# connect to the Kafka server as “producer” at startup, and start
# sending all  #logs to the topic channel at real time.
#
# The app can be either producer or consumer, but not both.
# Do not specify both KafkaProducerTopic and KafkaConsumerTopic.
kafkaProducerTopic=topic_string

# Consumer name to connect. When this option is specified, the app will
# connect to the Kafka server as “consumer” at content startup, and start
# receiving feeded messages from the topic channel and processing them
# at real time.
#
# The app can act either producer or consumer, but not both.
# Do not specify both KafkaProducerTopic and KafkaConsumerTopic.
kafkaConsumerTopic=topic_string

# Compression codec.
kafkaCodec=codec_string
```