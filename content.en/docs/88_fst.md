

---
title: FST Format
slug: fst-format
---

# FST Format

## Introduction

The operation scripts of MMDAgent-EX are described using a state transition model, with conditions and actions. The file extension is .fst.

At runtime, MMDAgent-EX is always in a certain state. The module monitors messages flowing within MMDAgent (input messages) and if an input message matches any of the conditions waiting in the current state, it outputs the corresponding message to MMDAgent and transitions to the next state. This process is repeated to execute the dialogue scenario.

In MMDAgent-EX, the .fst specification has been expanded from the original MMDAgent, but compatibility is maintained, and old .fst files for the original can still be used.

In MMDAgent, you can display the .fst debug window internally with the `Shift+f` key. Also, you can open the running fst file in an editor with the `e` key. Please utilize this for operation checks.

How to use Sub-FST.

## VSCode Extension

We have released a VS Code extension for .fst files, please give it a try.

https://marketplace.visualstudio.com/items?itemName=MMDAgent-EX.dialogue-fst-editing-support

The extension includes the following features:

- Input assistance that tells you about message specifications and arguments
- Detection of states to be aware of, such as states with no transitions or states that are not transitioned from anywhere
- The ability to move to the definition by specifying the state name
- Display a list of references that jump to the state name

## Overview

.fst files are text files. Lines starting with `#` are ignored as comments.

The following is an example. In this example, it first sets the background image, loads the model file and plays the motion, and sets the camera parameters. Then, it transitions to a state named `MAINLOOP`. In the `MAINLOOP` state, it sends corresponding messages for each key input and returns to the `MAINLOOP` state.

`<eps>` represents an empty word in FST. That is, if there is an `<eps>` in the condition field, it is always TRUE and the line proceeds to the next without waiting for input. Also, if there is an `<eps>` in the output field, it proceeds without outputting anything.

{{<fst>}}

# initial values
${agentPMD}="Agents/mai/mai.pmd"
${camera_default}="1.7,12.7,0.0|0.0,0.0,0.0|44|16|1"

# Begins with state "0"
0 MAINLOOP:
  <eps>                    STAGE|floor.png,back.jpg
  <eps>                    CAMERA|${camera_default}
  <eps>                    MODEL_ADD|0|${agentPMD}
  MODEL_EVENT_ADD|0        MOTION_ADD|0|base|waiting.vmd|FULL|ONCE|OFF|OFF
  MOTION_EVENT_ADD|0|base  <eps>

MAINLOOP MAINLOOP:
  KEY|1 MOTION_ADD|0|ojigi|mei_greeting.vmd|FULL|ONCE|ON|OFF

MAINLOOP MAINLOOP:
  KEY|2 SYNTH_START|0|mei_voice_normal|Hello.

MAINLOOP MAINLOOP:
  KEY|9 AVATAR_LOGSAVE_START|log.txt

MAINLOOP MAINLOOP:
  KEY|0 AVATAR_LOGSAVE_STOP
{{</fst>}}

## Basic Format

Indentation is critical. The state name line should have no indent, and the transition description line should be indented. This is mandatory.

The state name can be any string. In older versions of MMDAgent, it was just a number, but in the latest version, you can use any string. The state ID representing the initial state is fixed at "`0`" (zero).

Each field is separated by a space or tab. If you want to specify a value that includes a space, such as a path name, use `""` or `''`.

{{<fst>}}
name1 name2:
    input_message1 output_message2
    input_message2 output_message2
    ...

name2 name3:
    ...
{{</fst>}}

## Details of Transition Description

`name1`, `name2`, ... are state names. The first one represents the current state, the second one represents the transition destination state. The lines indented from the next line represent the behavior definition sequence between the two states. Each `input_message` is the field for the transition condition, and `output_message` is the field for the message to be output at runtime.

The behavior definition can be written over several lines. If it is described in multiple lines, it will be processed sequentially as a sub-state from top to bottom. In other words, in the above example, when the current state becomes `name1`, first wait for `input_message1`. When it arrives, output `output_message2` and wait for the next line's `input_message2`. When a message corresponding to `input_message2` arrives, issue `output_message2`... and so on, connecting in order. When the last line of that block ends, transition to the state name specified by `name2`.

If you define multiple blocks that start with the same state name, they are evaluated from the one defined earlier in the .fst file. That is, in the following example, if the input matches both `input_message1` and `input_message1`, the top one is prioritized.

{{<fst>}}
name1 name2:
    input_message1 output_message1

name1 name3:
    input_message2 output_message2
    ...
{{</fst>}}

## Local Variables

You can define, assign, and reference local variables for each .fst. They are enclosed for each .fst. (Do not confuse with MMDAgent-EX's global variables)

The initial value can be specified in the first part of the .fst file (before the first state definition).

{{<fst>}}
${agentPMD}="Agents/mai/mai.pmd"
${camera_default}="1.7,12.7,0.0|0.0,0.0,0.0|44|16|1"
{{</fst>}}

Local variables can be referenced in the condition field and output field. By writing `${variable name}`, it will replace that part at runtime (the moment it is evaluated) with the value of that local variable at that time, and evaluation and execution will be performed.

{{<fst>}}
XXX YYY:
    <eps> MODEL_ADD|mei|${agentPMD}
{{</fst>}}

In the condition field, you can use the value of a local variable as a transition condition. Only matches as a string are possible. The comparison operators are `==` and `!=` only.

{{<fst>}}
XXX YYY:
    ${flag}==xxx  MODEL_ADD|mei|...

WWW ZZZ:
    ${flag}!=yyy  MODEL_ADD|mei|...
{{</fst>}}

Changes in runtime values and assignments are described as additional fields at the end of each transition. It is also possible to reference between variables.

{{<fst>}}
XXX YYY:
  <eps>            <eps>  ${place}=Nagoya

ZZZ QQQ:
  MODEL_ADD|mei|.. <eps>  ${value}=${src}/${dst}
{{</fst>}}

It is also possible to assign multiple values at once.

{{<fst>}}
XXX YYY:
  <eps>  <eps>  ${src}=Nara,${dst}=Tokyo,${pref}=nozomi
{{</fst>}}

By writing `${%global variable name}`, you can handle and retrieve global variables as local variables.

{{<fst>}}
XXX YYY:
  <eps>            <eps>  ${place}=${%KeyName}
{{</fst>}}

## How to Write Condition Fields

### Plain Text

If you write a string that does not match any of the following in the condition field, it will match an input message that exactly matches it.

### Variable Value

The value of a local variable can be a transition condition. This condition does not depend on the input message, and the transition occurs when the evaluation of the given expression is TRUE. The comparison operators are `==` and `!=` only.

{{<fst>}}
XXX YYY:
    ${flag}==xxx  MODEL_ADD|mei|...

WWW ZZZ:
    ${flag}!=yyy  MODEL_ADD|mei|...
{{</fst>}}

Please note that the evaluation of the expression is only once immediately after transitioning to that state. Whether the expression holds true or not is only evaluated immediately after the transition to the state, and it does not respond even if the expression holds true during the state stay.

### Regular Expressions

You can use regular expressions for text matching. To write it, enclose the entire condition field with `@`. The following is an example of a transition description that conditionally matches when a message containing `Station` or `station` arrives in the recognition result (`RECOG_EVENT_STOP`).

{{<fst>}}
XXX YYY:
    @RECOG_EVENT_STOP\|.*[Ss]tation.*@  <eps>
{{</fst>}}

The range enclosed by `@` is thrown directly to the regular grammar engine, so be careful, for example, `|` needs to be written as `\|` as in the example. The regular expression library uses [Google RE2](https://github.com/google/re2). Refer to [Google's document](https://support.google.com/a/answer/1371417?hl=ja) etc. for the format.

Note that it is a full match, not a partial match. Regular expressions that only catch part of it will not match. Write the regular expression so that the entire message matches.

{{<fst>}}

# Bad example
XXX YYY:
    @[Ss]tation@  <eps>
{{</fst>}}

After evaluating the regular expression, the sub-match range enclosed in parentheses is automatically assigned to local variables `${1}`, `${2}`, etc. This allows you to extract the matched part into a local variable. For example, the following is an example of extracting the model alias name and motion alias name from the `MOTION_EVENT_ADD` message into `${model}` and `${motion}`.

{{<fst>}}
XXX YYY:
    @MOTION_EVENT_ADD\|(.*)\|(.*)@ <eps> ${model}=${1},${motion}=${2}
{{</fst>}}

## %INCLUDE

Inside .fst,

{{<fst>}}
%INCLUDE("filename.fst")
{{</fst>}}

By doing so, you can include the specified file at that location.

Includes are expanded when reading .fst, and the contents are interpreted as if they were expanded right there. No particular scope processing is done for state names or variables. Be very careful about state name conflicts and processing consistency.

## Parallel FST Launch (Sub FST)

You can run multiple FSTs in parallel. When the main FST file is

```text
foobar.fst
```

if there are .fst files with names like the following, MMDAgent-EX will also open them at the same time. (`xxx` is any character)

```text
foobar.fst.xxx.fst
```

All launched sub FSTs will start in parallel with the main FST. Input is cascaded to the sub FST and the output of the sub FST is streamed into the message queue. Sub FSTs operate independently of the main FST.

Typical uses include, for example,

- Playing motions at regular intervals
- Launching corresponding messages when certain messages arrive

These allow you to write operations that run independently from the state in dialogue management.

{{< hint ms >}}

## launching Sub FST by message

You can start a FST as sub-fst by **SUBFST_START** message.

{{< message >}}
SUBFST_START|(new_alias)|fst_filename
{{< / message >}}

**SUBFST_START** will produce error when the specified fst file does not exist.  You can instead use **SUBFST_START_IF** to start the sub-fst only when the file exists (no error when the file foes not exist, just do nothing)

{{< message >}}
SUBFST_START_IF|(new_alias)|fst_filename
{{< / message >}}

Upon success, they issue **SUBFST_EVENT_START|alias**.

{{< message >}}
SUBFST_EVENT_START|(alias)
{{< / message >}}

The started sub-FST will disappear when **it reaches a state with no arc**.  Or you can explicitly terminate a sub-fst by **SUBFST_STOP** message.

{{< message >}}
SUBFST_STOP|(alias)
{{< / message >}}

When a sub-FST has been stopped by either reached no-arc state or terminated by **SUBFST_STOP**, it issues **SUBFST_EVENT_STOP**.

{{< message >}}
SUBFST_EVENT_STOP|(alias)
{{< / message >}}

{{< hint info >}}
A special state **AT_EXIT**: In case a running sub-fst is told to stop immediately by **SUBFST_STOP**, if it has a state label **AT_EXIT** in it, it immediately jumps to the **AT_EXIT** state instead of termination.  You can use this feature to define end-of-fst processing.  Note the the processing after **AT_EXIT** should not have any incomplete wait or loop, since it prevents the sub-fst to terminate forever.
{{< /hint >}}

{{< /hint >}}
