---
title: Integration Using Global Variables
slug: global-variables
---
# Integration Using Global Variables

MMDAgent-EX has an internal storage area for global variables. .fst scripts, .mdf configuration files, or messages can assign, modify, and read those values.

Global variables are a collection of key-value pairs. Below we explain how to assign and reference values.

## Assignment in .mdf

All pairs written in the following form are assigned to and retained as key-value entries in the global variables at startup.

{{<mdf>}}
KeyName=String
{{</mdf>}}

You can retrieve these settings later, and you can also define arbitrary key-value entries in the .mdf that are unrelated to built-in settings.

## Referencing and assigning in .fst

In .fst files you can reference a global variable anywhere using `${%KeyName}`.
The value is evaluated not at .fst load time but at the moment that line is executed.

The example below assigns the value of the global variable with key "ModelName" as the first argument (model alias) of the **MODEL_ADD** message. (See the FST format documentation for details on variable handling in .fst.)

{{<fst>}}
0 LOOP:
    <eps> MODEL_ADD|${%ModelName}|...
{{</fst>}}

You can also use the value itself as a condition, like this:

{{<fst>}}
LOOP LOOP:
    ${%KeyName}==string SYNTH_START|mei|...
{{</fst>}}

You can also assign values using the [end-of-line additional fields](../fst-format/).

{{<fst>}}
0 LOOP:
  ...
  <eps>  MODEL_ADD|mei|... ${%KeyName}=string
{{</fst>}}


## Assigning via messages

You can assign values by sending the `KEYVALUE_SET` message.

{{<message>}}
KEYVALUE_SET|(key name)|(value)
{{</message>}}

## Binding with MODEL_BINDFACE

As an alternative use of the [`MODEL_BINDFACE` message](../motion-bind/#model_bindface), you can bind a morph to a global variable instead of a fixed value. A bound morph is controlled by the value of the bound global variable, and the morph will follow and update in real time whenever the variable changes.

This lets you, for example, provide a specific morph's value from a setting in the .mdf, or stream values from an external source via `KEYVALUE_SET` messages to control a morph in real time.

{{<message>}}
MODEL_BINDFACE|(key name)|(min)|(max)|(model alias)|(morph name)|rate1|rate2
{{</message>}}

`min` and `max` are the minimum and maximum of the global variable's value; `rate1` and `rate2` are the corresponding morph minimum and maximum values. Values below `min` are capped to `rate1`; values above `max` are capped to `rate2`. Values in between are linearly interpolated. The graph below illustrates this (horizontal axis = global variable value; vertical: 1 corresponds to `rate1`, 2 corresponds to `rate2`).

![BindBone](/images/bindbone.png)

You can unbind with `MODEL_UNBINDFACE`.

{{<message>}}
MODEL_UNBINDFACE|(model alias)|(morph name)
{{</message>}}