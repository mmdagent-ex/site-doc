---
title: FST Format
slug: fst-format
---
# FST Format

## Introduction

MMDAgent-EX behavior scripts describe conditions and actions as a state-transition model. File extension is .fst.

At runtime, MMDAgent-EX is always in a single state. Modules monitor messages flowing inside MMDAgent (input messages). If an input message matches one of the conditions waiting in the current state, the module outputs the corresponding message to MMDAgent and transitions to the specified next state. Repeating this executes the interaction scenario.

MMDAgent-EX extends the original MMDAgent .fst specification, but compatibility is preserved: older .fst files for the original MMDAgent can be used as-is.

In MMDAgent, pressing Shift+f opens an internal debug window for .fst files. Pressing e opens the running .fst file in an editor. Use these for checking behavior.

Using subFSTs.

## VS Code Extension

A VS Code extension for .fst files is available — please try it:

https://marketplace.visualstudio.com/items?itemName=MMDAgent-EX.dialogue-fst-editing-support

Features include:

- Input assist that shows message specifications and arguments
- Detection of problematic states such as states with no outgoing transitions or states never transitioned to
- Jump to a state's definition by specifying its name
- Show a list of references that jump to a given state name

## Overview

.fst files are plain text. Lines beginning with `#` are comments and ignored.

The following is an example. In this example, the script first sets background images, loads a model file and plays a motion, and once camera parameters are set it transitions to the state named `MAINLOOP`. In the `MAINLOOP` state, it sends the corresponding messages for various key inputs and returns to the `MAINLOOP` state.

`<eps>` denotes the empty symbol in FST. That is, if the condition field is `<eps>` it is always TRUE and the line proceeds without waiting for input. If the output field is `<eps>` nothing is output and it proceeds.

{{<fst>}}
# initial values
${agentPMD}="Agents/mai/mai.pmd"
${camera_default}="1.7,12.7,0.0|0.0,0.0,0.0|44|16|1"

# begins with state "0"
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

## Basic Syntax

Indentation is important. State-name lines must have no indentation; transition lines must be indented. This is mandatory.

State names may be any string. In older MMDAgent versions they were numeric only, but the latest version accepts arbitrary strings. The initial state ID is fixed to "0" (the numeral zero).

Fields are separated by spaces or tabs. When specifying values that include spaces (e.g., paths), use double or single quotes.

{{<fst>}}
name1 name2:
    input_message1 output_message2
    input_message2 output_message2
    ...

name2 name3:
    ...
{{</fst>}}

## Transition Details

`name1`, `name2`, ... are state names: the first is the current state and the second is the next state. The indented lines following them define a sequence of action definitions between those two states. Each line's `input_message` is the transition condition field, and `output_message` is the message emitted at runtime.

An action definition can span multiple lines. When multiple lines are provided, they are processed in order as sub-states. That is, if the current state is `name1`, it first waits for `input_message1`. When that arrives, it emits `output_message1` and then waits for `input_message2` on the next line. When `input_message2` arrives, it emits `output_message2`, and so on. After the last line of that block is completed, the FST transitions to the state named by `name2`.

If you define multiple blocks starting with the same state name, they are evaluated in the order they appear in the .fst file. Therefore, if both `input_message1` and `input_message2` match, the earlier (upper) block takes precedence.

{{<fst>}}
name1 name2:
    input_message1 output_message1

name1 name3:
    input_message2 output_message2
    ...
{{</fst>}}

## Local Variables

Each .fst can define, assign, and reference local variables. Local variables are scoped to each .fst and are not shared with other sub .fst files or plugins.

You can set initial values at the start of the .fst file (before the first state definition).

{{<fst>}}
${agentPMD}="Agents/mai/mai.pmd"
${camera_default}="1.7,12.7,0.0|0.0,0.0,0.0|44|16|1"
{{</fst>}}

You can reference local variables in both condition and output fields. Writing `${variable_name}` replaces that portion at runtime (when evaluated) with the current value of the local variable for evaluation or execution.

{{<fst>}}
XXX YYY:
    <eps> MODEL_ADD|mei|${agentPMD}
{{</fst>}}

Local variable values can be used as transition conditions. These conditions do not rely on input messages and trigger when the given expression evaluates to TRUE. Only the `==` and `!=` comparison operators are supported.

{{<fst>}}
XXX YYY:
    ${flag}==xxx  MODEL_ADD|mei|...

WWW ZZZ:
    ${flag}!=yyy  MODEL_ADD|mei|...
{{</fst>}}

Note that expression evaluation occurs only once immediately after the state is entered. The expression is evaluated right after the transition into the state; if it becomes true later during the state's residence, it will not trigger.

Runtime value changes and assignments are written as additional fields at the end of each transition line. You can reference other variables in assignments.

{{<fst>}}
XXX YYY:
  <eps>            <eps>  ${place}=Nagoya

ZZZ QQQ:
  MODEL_ADD|mei|.. <eps>  ${value}=${src}/${dst}
{{</fst>}}

You can assign multiple values at once.

{{<fst>}}
XXX YYY:
  <eps>  <eps>  ${src}=Nara,${dst}=Tokyo,${pref}=nozomi
{{</fst>}}

## Global Variables

By prefixing the variable name with `%` like `${%globalVarName}` you can reference and write to [global variables](./75_global_variables.md). Global variables’ initial values are set in the .mdf and their values are shared across FSTs and plugins.

{{<fst>}}
XXX YYY:
  <eps>            <eps>  ${place}=${%KeyName}
{{</fst>}}

## Environment Variables

You can reference environment variables with `${%ENV{ENV_NAME}}`. (Available in versions from 2025.7.9 onward)

{{<fst>}}
XXX YYY:
  <eps>            <eps>  ${place}=${%ENV{PLACE_NAME}}
{{</fst>}}

## Condition Field Syntax

### Plain Text

If the condition field contains a string that does not match any of the special forms below, it matches input messages that are exactly equal to that string.

### Variable Values

You can use local variable values as transition conditions. These conditions do not depend on input messages; the transition occurs when the expression evaluates to TRUE. Only `==` and `!=` are supported.

{{<fst>}}
XXX YYY:
    ${flag}==xxx  MODEL_ADD|mei|...

WWW ZZZ:
    ${flag}!=yyy  MODEL_ADD|mei|...
{{</fst>}}

Remember that expressions are evaluated only once right after the state is entered.

### Regular Expressions

You can match text using regular expressions by enclosing the entire condition field with `@`. The following example matches when the recognition result (`RECOG_EVENT_STOP`) contains `Station` or `station`.

{{<fst>}}
XXX YYY:
    @RECOG_EVENT_STOP\|.*[Ss]tation.*@  <eps>
{{</fst>}}

The content between `@` is passed directly to the regex engine, so characters like `|` must be escaped as `\|` as in the example. The regex library used is Google RE2. Refer to Google’s documentation (e.g., https://support.google.com/a/answer/1371417?hl=ja) for syntax details.

Note that matching is full-match, not substring match. A regex that only matches part of the message will not match; write the regex so the entire message matches.

{{<fst>}}
# Bad example
XXX YYY:
    @[Ss]tation@  <eps>
{{</fst>}}

After evaluating a regex, captured groups are automatically assigned to local variables `${1}`, `${2}`, etc. You can use these to extract matched parts into local variables. For example, the following extracts model alias and motion alias from a `MOTION_EVENT_ADD` message into `${model}` and `${motion}`.

{{<fst>}}
XXX YYY:
    @MOTION_EVENT_ADD\|(.*)\|(.*)@ <eps> ${model}=${1},${motion}=${2}
{{</fst>}}

## %INCLUDE

Inside an .fst you can include another file with:

{{<fst>}}
%INCLUDE("filename.fst")
{{</fst>}}

Includes are expanded when reading the .fst; the included content is inserted as-is at that location and interpreted. There is no special scoping for state names or variables. Be careful to avoid name collisions and ensure consistency when including files.

## Parallel FST Execution (SubFSTs)

MMDAgent-EX can run multiple subFSTs in parallel alongside the main FST. SubFSTs connect to the main queue in the same way as the main FST; their outputs are sent to the main queue.

SubFSTs run in parallel with the main FST. Inputs are cascaded to subFSTs, and subFST outputs flow into the message queue. SubFSTs operate independently of the main FST. You can start any number of subFSTs.

Local variables are independent per FST. Note that KeyValue values are stored in MMDAgent-EX's memory and can be shared across FSTs.

### Startup Method 1: Static

If the main FST file is:

```text
foobar.fst
```

place files with names like:

```text
foobar.fst.xxx.fst
```

MMDAgent-EX checks, at startup, whether any files with names like that exist next to the main FST file and automatically starts all those found as subFSTs when launching the main FST.

### Startup Method 2: Dynamic

You can start a subFST at runtime by issuing the message **SUBFST_START**. This allows starting a subFST from an external trigger or from an existing running FST in response to events. `alias` specifies an arbitrary alias name for the subFST being started.

{{<message>}}
SUBFST_START|alias|file.fst
{{</message>}}

If the specified file `file.fst` cannot be opened, the above triggers an error. To check whether the file exists and only start when present, use **SUBFST_START_IF**.

{{<message>}}
SUBFST_START_IF|alias|file.fst
{{</message>}}

When a subFST starts running, the event **SUBFST_EVENT_START** is issued.

{{<message>}}
SUBFST_EVENT_START|alias
{{</message>}}

A started subFST begins execution from state `0`. All subFSTs run in parallel with the main FST.

### SubFST Termination

A subFST immediately stops when it reaches a state that has no defined next transitions (a terminal state). When it stops, the message **SUBFST_EVENT_STOP** is issued so other modules can detect that the subFST has terminated.

{{<message>}}
SUBFST_EVENT_STOP|alias
{{</message>}}

If an FST is waiting for messages or looping and never reaches a terminal state, that subFST will keep running. To stop it, use the following **SUBFST_STOP**.

### Forcible SubFST Stop

A running subFST can be forcibly stopped by sending the **SUBFST_STOP** message. In this case, the **SUBFST_EVENT_STOP** message is also issued on termination.

{{<message>}}
SUBFST_STOP|alias
{{</message>}}

### AT_EXIT State

When a subFST receives a stop command via **SUBFST_STOP**, if the subFST defines a state named `AT_EXIT` it will not stop immediately. Instead, it is forcibly transitioned to the `AT_EXIT` state and then executes the subsequent instructions. Using `AT_EXIT` allows you to define cleanup actions that always run on termination, for example removing models displayed by the subFST before finishing.

After transitioning to `AT_EXIT`, the subFST continues to operate from the `AT_EXIT` state as usual. Therefore, if you wait for messages or write loops in `AT_EXIT`, the subFST may not terminate. If you use `AT_EXIT`, the script author is responsible for ensuring that `AT_EXIT` eventually reaches a terminal state so the subFST can finish.