---
title: Dialogue Control by FST
slug: dialog-test-fst
---
# Try Dialogue Control by FST

Upon working voice recognition and speech synthesis, you can start creating a voice responses. Let's try writing a simple voice response scenario using FST script (.fst).

{{< hint warning >}}
Please complete the setup for [voice recognition](../asr-setup) and [speech synthesis](../tts-test) before start.
{{< /hint >}}

## What is FST?

MMDAgent-EX offers a finite-state machine based interaction management.  It defines how to act with the messages sent by the modules.  The definision file is ".fst", which defines sequencial input-to-output message translation as a form of FST (finite state transducer).

It consists of a set of states and transitions, in which each transition defines input-output actions to define a course of dialogue.  In this page we provide a simple overview and example as follows.

{{< hint info >}}
To know all the specifications and format of FST, please see the [reference format explanation](../fst-format).
{{< /hint >}}

### Basic Form

In .fst, each line defines one transition from state to state, which consists of space-separated fields: (1) source state name, (2) destination state name, (3) input message matching pattern, and (4) output message. The following example shows an action that "at state `Hoge`, If the `KEY|1` message comes, issue a message `SYNTH_START|0|...`, and move to the state `Foo`".  All .fst files have the initial state '0' and starts with the state.

{{<fst>}}
Hoge Foo  KEY|1 SYNTH_START|0|slt_voice_normal|Hello!
{{</fst>}}

### Multiple Actions

You can define everal actions for different conditions in the same source state.  When specified, they are evaluated in the state at run time and the one whose condition is met is executed. For example, if you define actions as follows, it waits for the input of `KEY|1` and `KEY|2` on state `Hoge`, and performs corresponding action when either comes.

{{<fst>}}
Hoge Foo  KEY|1 SYNTH_START|0|slt_voice_normal|Hello!
Hoge Foo  KEY|2 SYNTH_START|0|slt_voice_normal|How are you?
{{</fst>}}

### Sequential Actions

Sequential actions can be defined as a sequence of state transitions. The following is a part of a .fst script that starts a speech synthesis of "Hello" and then continues to say "How are you?" after waiting for the previous synthesis to finish.

{{<fst>}}
Hoge foo1  KEY|1 SYNTH_START|0|slt_voice_normal|Hello!
foo1 foo2  SYNTH_EVENT_STOP|0 SYNTH_START|0|slt_voice_normal|How are you?
{{</fst>}}

When the `1` key was pressed at state `Hoge`, the message to trigger the start message for speech synthesis is issued, and then it moves to state `foo1`.  In state `foo1`, it waits for the speech synthesis end event `SYTH_EVENT_STOP|0`, and when that message comes, it issues the next speech synthesis message.

Note that transition will not block. it move to the next state just after issuing the output message, without waiting for the result of the message issued. So, if you want to wait for some action to occur, you write the message as a transition condition like above.

### &lt;eps&gt;

When you use the empty string `<eps>` at the third field (input), the action is executed immediately. For instance, you can start both speech synthesis and motion at the same time as shown below.

{{<fst>}}
Hoge foo1  KEY|1 SYNTH_START|0|slt_voice_normal|Hello!
foo1 foo2  <eps> MOTION_ADD|0|greet|motions/action/ojigi.vmd
{{</fst>}}

You can also use `<eps>` in the output to have no output.

### Block style

In .fst scripts, you often describe sequential state transitions to process a series of messages. For example, the following is a set of commands in .fst that successively sets the background, loads the model, sets the motion, and configures the camera from the boot time (initial state is "`0`").

{{<fst>}}
0  s1  <eps> STAGE|images/floor_green.png,images/back_white.png
s1 s2  <eps> MODEL_ADD|0|gene/Gene.pmd
s2 s3  MODEL_EVENT_ADD|0  MOTION_ADD|0|base|motions/wait/01_Wait.vmd|FULL|LOOP|ON|OFF
s3 ss  <eps> CAMERA|0,15.25,0|4.5,0,0|22.4|27.0
{{</fst>}}

As seen above the format is redundant since the middle states are straight forward and no need to have their specific names.

In MMDAgent-EX, you can describe the set of single transition sequence as a block as follows. In this example, only the names of the first state and last state of this block should be written in the first line, and then follows the sequential processes with head indentation.

{{<fst>}}
0  ss:
    <eps> STAGE|images/floor_green.png,images/back_white.png
    <eps> MODEL_ADD|0|gene/Gene.pmd
    MODEL_EVENT_ADD|0  MOTION_ADD|0|base|motions/wait/01_Wait.vmd|FULL|LOOP|ON|OFF
    <eps> CAMERA|0,15.25,0|4.5,0,0|22.4|27.0
{{</fst>}}

## Example of a Simple QA

Let's edit the `main.fst` in the Example to create a simple Q&A session.

Open `main.fst` of the Example in a text editor, and append the following part at the end. This is the simplest form of Q&A session, which says, "When a `RECOG_EVENT_STOP` message containing a voice recognition result is issued, issue a `SYNTH_START` message to instruct voice synthesis."

{{<fst>}}
LOOP LOOP:
    RECOG_EVENT_STOP|hello SYNTH_START|0|slt_voice_normal|"Hello! Nice to meet you!"
{{</fst>}}

{{< hint info >}}
In .fst files, indentation matters. The first line of a block should have no indentation, and the following lines should be indented. The width of the indentation is up to you.
{{< /hint >}}

After editing, launch the content and try saying "Hello". The agent will respond "Hello, nice to meet you!"

<img width="480" alt="snapshot" src="/images/example_2.png"/>

## Adding Facial Expression

Let's try to add expression to your speech. Start the facial motion at the same time as the speech. Add a new line at the end of the part you just added, as shown below.

{{<fst>}}
LOOP LOOP:
    RECOG_EVENT_STOP|hello SYNTH_START|0|slt_voice_normal|"Hello! Nice to meet you!"
    <eps> MOTION_ADD|0|emote|gene/motion/03_smile.vmd|PART|ONCE
{{</fst>}}

Save the .fst and give it a try. Close MMDAgent-EX and relaunch it, or reload it with the `Shift+r` key. Say "Hello" again and confirm that it responds with a smile.

## Performing Facial Expressions and Actions Concurrently

Let's also perform actions along with the facial expressions. Add the bold line below above the line you just added.

{{<fst>}}
LOOP LOOP:
    RECOG_EVENT_STOP|hello SYNTH_START|0|slt_voice_normal|"Hello! Nice to meet you!"
    <eps> MOTION_ADD|0|action|motions/action/ojigi.vmd|FULL|ONCE
    <eps> MOTION_ADD|0|emote|gene/motion/03_smile.vmd|PART|ONCE
{{</fst>}}

After saving and reloading, say "Hello" and confirm that it bows while smiling.

By using `<eps>` for unconditional execution, the first `MOTION_ADD` and the second `MOTION_ADD` are passed to MMDAgent-EX in succession without any time gap. In MMDAgent-EX, multiple motions can be overlaid and played at the same time.

## Overview of .fst

Here, we'll briefly introduce .fst. .fst is a script that describes operations as a finite state automaton (more precisely, a finite state transducer). In simple terms, it sequentially describes "what to do when something happens".

The current .fst looks as follows. For example, the block up to the 5th line after startup defines a series of processes such as:

- Setting the floor and background images
- Loading the model
- Once loading is complete, looping the standby motion
- Setting the camera position
- After the above is done, moving to a state named "LOOP"

{{<fst>}}
0 LOOP:
    <eps> STAGE|images/floor_green.png,images/back_white.png
    <eps> MODEL_ADD|0|gene/Gene.pmd
    MODEL_EVENT_ADD|0  MOTION_ADD|0|base|motions/wait/01_Wait.vmd|FULL|LOOP|ON|OFF
    <eps> CAMERA|0,15.25,0|4.5,0,0|22.4|27.0

LOOP LOOP:
    KEY|1 SYNTH_START|0|slt_voice_normal|"Hello! Nice to meet you!"

LOOP LOOP:
    RECOG_EVENT_STOP|hello SYNTH_START|0|slt_voice_normal|"Hello! Nice to meet you!"
    <eps> MOTION_ADD|0|action|motions/action/ojigi.vmd|FULL|ONCE
    <eps> MOTION_ADD|0|emote|gene/motion/03_smile.vmd|PART|ONCE
{{< / fst>}}

In MMDAgent-EX, all command instructions and event notifications are done via messaging. In .fst, the basic mechanism is to wait (block) until a message that meets the conditions arrives, and when a message that meets the conditions arrives, issue a corresponding message and move to the next line. If there are multiple blocks starting from the same state name, the block that meets the conditions first is executed. Also, "`<eps>`" represents "no specification", and in the condition part, it indicates to issue a message immediately without waiting and move on.

.fst allows you to describe various interactions based on an automaton. This is the end of the explanation here, but for more details about .fst, please refer to [FST Format](../fst-format).

{{< hint info >}}
We have released a [VS Code extension for .fst files](https://marketplace.visualstudio.com/items?itemName=MMDAgent-EX.dialogue-fst-editing-support) to assist with .fst editing in VS Code. Please use it together.
{{< /hint >}}

## Advanced Usage Cases

We'll introduce a way to describe the dialogue a bit more effectively within the range that can be realized using the .fst script function.

### OR Conditions

Let's set it up so that the same response is returned when you say not only "Konnichiwa" but also "Hello". If you want to match multiple conditions, you can add parallel nodes using "`+`".

{{<fst>}}
LOOP LOOP:
    RECOG_EVENT_STOP|hello. SYNTH_START|0|slt_voice_normal|"Nice to meet you!"
    +RECOG_EVENT_STOP|hello</b>
    <eps> MOTION_ADD|0|action|motions/action/ojigi.vmd|FULL|ONCE
    <eps> MOTION_ADD|0|emote|gene/motion/03_smile.vmd|PART|ONCE
{{< / fst>}}

By writing the condition term following "`+`", you can add conditions to the condition of the line immediately above with OR. Regardless of which matches, the message item of the first line (for example `SYNTH_START`) is executed and it moves to the next line.

If you write the issued message in the "`+`" line as well as the condition, you can parallelize the issued messages as well. The following is an example of returning "Nice to meet you!" for "Konnichiwa" and "Hello, thank you!" for "Hello". After executing either, it moves to the next line of motion playback.

{{<fst>}}
LOOP LOOP:
    RECOG_EVENT_STOP|hello. SYNTH_START|0|slt_voice_normal|"Nice to meet you!"
    +RECOG_EVENT_STOP|hello SYNTH_START|0|slt_voice_normal|"Hello, thank you!"
    <eps> MOTION_ADD|0|action|motions/action/ojigi.vmd|FULL|ONCE
    <eps> MOTION_ADD|0|emote|gene/motion/03_smile.vmd|PART|ONCE
{{< / fst>}}

You can write multiple "`+`" lines. Below is an example of extending the same response to "Konnichiwa", "Hello", and also "Bonjour".

{{<fst>}}
LOOP LOOP:
    RECOG_EVENT_STOP|hello. SYNTH_START|0|slt_voice_normal|"Nice to meet you!"
    +RECOG_EVENT_STOP|hello
    +RECOG_EVENT_STOP|Bonjour.
    <eps> MOTION_ADD|0|action|motions/action/ojigi.vmd|FULL|ONCE
    <eps> MOTION_ADD|0|emote|gene/motion/03_smile.vmd|PART|ONCE
{{< / fst>}}

If you want to perform completely different processes, it may be a good idea to divide them into individual blocks. The following is an example where "Konnichiwa" remains the same, and when you say "Hello", it responds with "Hello, thank you!" while waving its hand. By defining blocks that start from the same state, you can determine which block operates based on the condition of the first line of each block.

{{<fst>}}
LOOP LOOP:
    RECOG_EVENT_STOP|hello. SYNTH_START|0|slt_voice_normal|"Nice to meet you!"
    <eps> MOTION_ADD|0|action|motions/action/ojigi.vmd|FULL|ONCE
    <eps> MOTION_ADD|0|emote|gene/motion/03_smile.vmd|PART|ONCE

LOOP LOOP:
    RECOG_EVENT_STOP|hello SYNTH_START|0|slt_voice_normal|"Hello, thank you!"
    <eps> MOTION_ADD|0|action|motions/action/wavehands.vmd|FULL|ONCE
    <eps> MOTION_ADD|0|emote|gene/motion/10_impressed.vmd|PART|ONCE
{{< / fst>}}

### Sequential Actions

Here's an example of how to describe a sequence of actions using .fst. The following shows a two-step response to "Hello".

1. Respond with "Hello" while bowing.
2. After the bow, respond with a happy voice saying, "Nice to meet you" with a smile.

{{<fst>}}
LOOP LOOP:
    RECOG_EVENT_STOP|hello SYNTH_START|0|slt_voice_normal|Hello!
    <eps> MOTION_ADD|0|action|motions/action/ojigi.vmd|FULL|ONCE
    MOTION_EVENT_STOP|0|action SYNTH_START|0|slt_voice_happy|"Nice to meet you!"
    <eps> MOTION_ADD|0|emote|gene/motion/03_smile.vmd|PART|ONCE
{{< / fst>}}

The key point is the part where it waits for the bowing motion to finish. When the bowing motion ends, MMDAgent-EX issues `MOTION_EVENT_STOP|0|action`. In this .fst, it is designed to perform the next action after waiting for `MOTION_EVENT_STOP|0|action`.

Thus, the basic idea of .fst is to describe interactions by stacking procedures that wait for any event and output any event.

## Using Regular Expressions

The condition judgment is an exact match, and it only matches if the text of the description and the message match exactly. However, by using regular expressions, you can describe more flexible matching. When using regular expressions, enclose the condition term with "`@`". For instance,

{{<fst>}}
LOOP LOOP:
    RECOG_EVENT_STOP|hello SYNTH_START|0|slt_voice_normal|"Hello! Nice to meet you!"
    +RECOG_EVENT_STOP|hello
{{< / fst>}}

The part written like above can also be written with regular expressions as follows. When the condition term is a regular expression, it is determined whether the message matches that regular expression.

{{<fst>}}
LOOP LOOP:
    @RECOG_EVENT_STOP¥|(Hello|Hello)。@</b>  SYNTH_START|0|slt_voice_normal|"Hello! Nice to meet you!"
{{< / fst>}}

For special purposes, you can also describe mimicry of recognition results by writing as follows. The "`${1}`" in the issued message item is replaced by the character corresponding to the first character in the parentheses that matches in the regular expression.

{{<fst>}}
LOOP LOOP:
    @RECOG_EVENT_STOP¥|(.*)@</b>  SYNTH_START|0|slt_voice_normal|${1}
{{< / fst>}}

The regular expression is a total match.

### Non-detereministic arcs

If multiple conditions match, the one defined earlier takes precedence.
