---
title: Try voice dialogue (fst)
slug: dialog-test-fst
---
# Try voice dialogue (fst)

If speech recognition and speech synthesis are working, you can create voice responses. Let's try a simple voice response using a script (.fst).

{{< hint warning >}}
Please complete the setup for [speech recognition](../asr-setup) and [speech synthesis](../tts-test) first.
{{< /hint >}}

## What is FST

This explains the standard script (.fst) mechanism and how to write it for MMDAgent-EX. An .fst (finite-state transducer) is a state-based scripts with transition condition and actions; for each state you define actions like "when a certain message arrives, output this message". States transition according to actions. Below is a brief overview.

{{< hint info >}}
For the full specification, see the [FST format reference](../fst-format).
{{< /hint >}}

### Basic form

In .fst each action is written on one line as (1) state name, (2) next state name, (3) transition condition, (4) output. For example, the action "in state `Foo`, when a `KEY|1` message arrives, say 'Hello!' and transition to state `Bar`" is written like this:

{{<fst>}}
Foo Bar  KEY|1 SYNTH_START|0|slt_voice_normal|Hello!
{{</fst>}}

### Multiple actions

If you write multiple actions for the same state, they are evaluated concurrently in that state and the one whose condition is satisfied will execute. For example, the following makes state `Foo` wait for either `KEY|1` or `KEY|2`, and perform the corresponding action when one arrives:

{{<fst>}}
Foo Bar  KEY|1 SYNTH_START|0|slt_voice_normal|Hello!
Foo Bar  KEY|2 SYNTH_START|0|slt_voice_normal|How are you?
{{</fst>}}

### Sequential actions

By writing transitions from the target state you can describe sequential actions. The following is part of an .fst that starts speech synthesis for "Hello!", waits for that to finish, then continues with "How are you?":

{{<fst>}}
Foo Bar1  KEY|1 SYNTH_START|0|slt_voice_normal|Hello!
Bar1 Bar2  SYNTH_EVENT_STOP|0 SYNTH_START|0|slt_voice_normal|How are you?
{{</fst>}}

On the first line, in state `Foo` when key `1` is pressed it issues the speech-start message and transitions to state `Bar1`. In state `Bar1` it waits for the speech-finish event `SYNTH_EVENT_STOP|0`, and when that message arrives it issues the next speech message.

Because .fst transitions to the next state immediately after issuing a message without waiting for the result, if you want to wait for some action to complete you should write the awaited message as a transition condition as shown above.

### &lt;eps&gt;

If you use the empty symbol `<eps>` as a condition, that action executes immediately without any condition. For example, you can start speech and play a motion at the same time like this:

{{<fst>}}
Foo Bar1  KEY|1 SYNTH_START|0|slt_voice_normal|Hello!
Bar1 Bar2  <eps> MOTION_ADD|0|greet|motions/action/ojigi.vmd
{{</fst>}}

You can also use `<eps>` in the output to indicate no output.

### Block notation

In .fst scripts you often write a sequence of state transitions to process a series of messages. The following example describes a sequence that, at startup (initial state "0"), sets the stage background, loads a model, adds motions, and sets the camera:

{{<fst>}}
0  s1  <eps> STAGE|images/floor_green.png,images/back_white.png
s1 s2  <eps> MODEL_ADD|0|gene/Gene.pmd
s2 s3  MODEL_EVENT_ADD|0  MOTION_ADD|0|base|motions/wait/01_Wait.vmd|FULL|LOOP|ON|OFF
s3 ss  <eps> CAMERA|0,15.25,0|4.5,0,0|22.4|27.0
{{</fst>}}

In MMDAgent-EX you can write this as a block. Write the first and last state names on the first line of the block, then indent the subsequent lines:

{{<fst>}}
0  ss:
    <eps> STAGE|images/floor_green.png,images/back_white.png
    <eps> MODEL_ADD|0|gene/Gene.pmd
    MODEL_EVENT_ADD|0  MOTION_ADD|0|base|motions/wait/01_Wait.vmd|FULL|LOOP|ON|OFF
    <eps> CAMERA|0,15.25,0|4.5,0,0|22.4|27.0
{{</fst>}}

## Create a simple Q&A

Edit the example's `main.fst` to make a simple Q&A.

Open the example `main.fst` in a text editor and add the following at the end. This is the simplest Q&A: when a `RECOG_EVENT_STOP` message containing the recognition result is issued, issue a `SYNTH_START` message to trigger speech synthesis.

{{<fst>}}
LOOP LOOP:
    RECOG_EVENT_STOP|hello SYNTH_START|0|slt_voice_normal|"Hello! Nice to meet you!"
{{</fst>}}

{{< hint info >}}
Indentation matters in .fst. The first line of a block must be unindented; subsequent lines must be indented. The indent width is flexible.
{{< /hint >}}

After editing, start the content.  Say "Hello", and the agent replies "Hello! Nice to meet you!".

<img width="480" alt="snapshot" src="/images/example_2.png"/>

## Add facial expressions

Let's add an expression to the utterance. Start an expression motion at speech start. Add the following line to the end of the section you added earlier:

{{<fst>}}
LOOP LOOP:
    RECOG_EVENT_STOP|hello SYNTH_START|0|slt_voice_normal|"Hello! Nice to meet you!"
    <eps> MOTION_ADD|0|emote|gene/motion/03_smile.vmd|PART|ONCE
{{</fst>}}

Save the `.fst` and try it. Close MMDAgent-EX and start it again, or reload with Shift+r. Say "Hello" again and confirm the agent smiles while responding.

## Run expressions and motions concurrently

Make the agent perform a motion along with the expression. Insert the following bolded line above the previously added line.

{{<fst>}}
LOOP LOOP:
    RECOG_EVENT_STOP|hello SYNTH_START|0|slt_voice_normal|"Hello! Nice to meet you!"
    <eps> MOTION_ADD|0|action|motions/action/ojigi.vmd|FULL|ONCE
    <eps> MOTION_ADD|0|emote|gene/motion/03_smile.vmd|PART|ONCE
{{</fst>}}

Save and reload, then say something to confirm the agent bows while smiling.

Because `<eps>` causes unconditional immediate execution, the first `MOTION_ADD` and the second `MOTION_ADD` are both sent to MMDAgent-EX with no time gap. MMDAgent-EX can blend multiple motions and play them simultaneously.

## Overview of .fst

Here is a brief summary of .fst. An .fst is a finite-state automaton (more precisely a finite-state transducer) used to describe behavior. Simply put, it lists "what to do when something happens."

The current .fst looks like the following. For example, the block up to the fifth line defines a sequence that:

- sets the floor and background images on startup,
- loads the model,
- when loading finishes starts a looping wait motion,
- sets the camera position,
- then moves to the state named "LOOP".

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

In MMDAgent-EX all commands and event notifications are handled via messaging. In .fst you block until a message matching the condition arrives; when it does, you emit the corresponding message and move to the next line. If multiple blocks start with the same state name, the block whose condition is satisfied first will execute. The token "`<eps>`" means "no specification": as a condition it issues its message immediately without waiting.

.fst lets you describe various interactions based on automata. This overview ends here; for details see [FST format](../fst-format).

{{< hint info >}}
We provide a [VS Code extension for .fst file editing](https://marketplace.visualstudio.com/items?itemName=MMDAgent-EX.dialogue-fst-editing-support) to help editing .fst in VS Code. Please consider using it.
{{< /hint >}}

## Additional: Extend the script

Here are a few ways to write more flexible dialogues using .fst features.

### OR conditions

Let's make the same response for both "Konnichiwa" and "Hello". To match multiple conditions, add parallel nodes using "`+`".

{{<fst>}}
LOOP LOOP:
    RECOG_EVENT_STOP|Konnichiwa. SYNTH_START|0|slt_voice_normal|"Nice to meet you!"
    +RECOG_EVENT_STOP|hello
    <eps> MOTION_ADD|0|action|motions/action/ojigi.vmd|FULL|ONCE
    <eps> MOTION_ADD|0|emote|gene/motion/03_smile.vmd|PART|ONCE
{{< / fst>}}

By writing a "`+`" line with only a condition, you add that condition as an OR to the previous line. If either matches, the message item on the first line (here `SYNTH_START`) is executed and then the script moves to the next line.

If you include output messages on the "`+`" line as well, they will also be emitted in parallel. The following example returns "Nice to meet you!" for "Konnichiwa" and "Hello, thank you!" for "hello", and plays the same motion.

{{<fst>}}
LOOP LOOP:
    RECOG_EVENT_STOP|Konnichiwa. SYNTH_START|0|slt_voice_normal|"Nice to meet you!"
    +RECOG_EVENT_STOP|hello SYNTH_START|0|slt_voice_normal|"Hello, thank you!"
    <eps> MOTION_ADD|0|action|motions/action/ojigi.vmd|FULL|ONCE
    <eps> MOTION_ADD|0|emote|gene/motion/03_smile.vmd|PART|ONCE
{{< / fst>}}

You can write multiple "`+`" lines. The example below extends the previous case to also match "Bonjour" and give the same response:

{{<fst>}}
LOOP LOOP:
    RECOG_EVENT_STOP|Konnichiwa SYNTH_START|0|slt_voice_normal|"Nice to meet you!"
    +RECOG_EVENT_STOP|hello
    +RECOG_EVENT_STOP|Bonjour
    <eps> MOTION_ADD|0|action|motions/action/ojigi.vmd|FULL|ONCE
    <eps> MOTION_ADD|0|emote|gene/motion/03_smile.vmd|PART|ONCE
{{< / fst>}}

If you want completely different processing, split them into separate blocks. The example below keeps the "Konnichiwa" behavior, and makes "Hello" produce "Hello, thank you!" while waving.

{{<fst>}}
LOOP LOOP:
    RECOG_EVENT_STOP|Konnichiwa SYNTH_START|0|slt_voice_normal|"Nice to meet you!"
    <eps> MOTION_ADD|0|action|motions/action/ojigi.vmd|FULL|ONCE
    <eps> MOTION_ADD|0|emote|gene/motion/03_smile.vmd|PART|ONCE

LOOP LOOP:
    RECOG_EVENT_STOP|hello SYNTH_START|0|slt_voice_normal|"Hello, thank you!"
    <eps> MOTION_ADD|0|action|motions/action/wavehands.vmd|FULL|ONCE
    <eps> MOTION_ADD|0|emote|gene/motion/10_impressed.vmd|PART|ONCE
{{< / fst>}}

### Sequential actions

Here is an example describing a two-stage response to "Hello":

1. Reply "Hello!" while bowing.
2. After the bow finishes, say "Nice to meet you" in a happy voice while smiling.

{{<fst>}}
LOOP LOOP:
    RECOG_EVENT_STOP|hello SYNTH_START|0|slt_voice_normal|Hello!
    <eps> MOTION_ADD|0|action|motions/action/ojigi.vmd|FULL|ONCE
    MOTION_EVENT_STOP|0|action SYNTH_START|0|slt_voice_happy|"Nice to meet you!"
    <eps> MOTION_ADD|0|emote|gene/motion/03_smile.vmd|PART|ONCE
{{< / fst>}}

The key is waiting for the bow motion to finish. MMDAgent-EX issues `MOTION_EVENT_STOP|0|action` when the action motion ends, so this .fst waits for `MOTION_EVENT_STOP|0|action` before proceeding.

In general, you describe interactions by chaining waits for events and outputting messages as needed.

## Using regular expressions

Conditions are matched by exact text by default, but you can use regular expressions for more flexible matching. To use a regex, surround the condition with "`@`". For example, the earlier

{{<fst>}}
LOOP LOOP:
    RECOG_EVENT_STOP|hello SYNTH_START|0|slt_voice_normal|"Hello! Nice to meet you!"
    +RECOG_EVENT_STOP|hello
{{< / fst>}}

can be written with a regular expression like this. When the condition is a regex, it matches if the message text satisfies the regex.

{{<fst>}}
LOOP LOOP:
    @RECOG_EVENT_STOP\|(Hello|Hello)@</b>  SYNTH_START|0|slt_voice_normal|"Hello! Nice to meet you!"
{{< / fst>}}

For a special use, you can echo back the recognition result. In the output message, "${1}" is replaced with the text matched by the first capture group in the regex.

{{<fst>}}
LOOP LOOP:
    @RECOG_EVENT_STOP\|(.*)@</b>  SYNTH_START|0|mei_voice_normal|${1}
{{< / fst>}}

Regular expressions perform a full-match.

### Handling overlaps

If multiple conditions match, the one defined earlier takes priority.