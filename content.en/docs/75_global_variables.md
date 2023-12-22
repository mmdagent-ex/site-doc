

---
title: Collaboration Using Global Variables
slug: global-variables
---

# Collaboration Using Global Variables

MMDAgent-EX has an internal storage area for global variables, and you can assign, change, and reference values using .fst scripts, .mdf configuration files, or messages.

Global variables are a collection of key-value pairs. Below, we will explain how to assign and reference values.

## Assigning with .mdf

All pairs written in the following form are assigned and held in the global variable as key-value values at startup.

{{<mdf>}}
KeyName=String
{{</mdf>}}

You can retrieve the setting value later, and you can also define arbitrary key-value values unrelated to the settings in the .mdf.

## Referencing & Assigning with .fst

In .fst, you can reference the value of a global variable anywhere in the form of `${%KeyName}`. 
The value is evaluated not at the time of .fst load, but at the time the line is executed.

The following is an example of assigning the value of the key "`ModelName`" of the global variable as the model alias name, which is the first argument of the **MODEL_ADD** message. (See the [explanation page](../fst-format) for handling variables in .fst)

{{<fst>}}
0 LOOP:
    <eps> MODEL_ADD|${%ModelName}|...
{{</fst>}}

You can also use the value itself as a condition, as shown below.

{{<fst>}}
LOOP LOOP:
    ${%KeyName}==string SYNTH_START|mei|...
{{</fst>}}

You can also assign values using the [additional field at the end of the line](../fst-format/#%e3%83%ad%e3%83%bc%e3%82%ab%e3%83%ab%e5%a4%89%e6%95%b0).

{{<fst>}}
0 LOOP:
  ...
  <eps>  MODEL_ADD|mei|... ${%KeyName}=string
{{</fst>}}

## Assigning with Messages

You can assign values by issuing a `KEYVALUE_SET` message.

{{<message>}}
KEYVALUE_SET|(key name)|(value)
{{</message>}}

## Binding with MODEL_BINDFACE

Another use for the [`MODEL_BINDFACE` message](../motion-bind/#model_bindface) is to bind a morph not to a static value, but to a global variable. Morphs with a specified bind will then be controlled by the value of the bound global variable, with the morph changing in real time each time the variable's value changes.

You can use this to provide a specific morph value from a .mdf setting, or to control a specific morph in real time from the outside by streaming in values with the **KEYVALUE_SET** message.

{{<message>}}
MODEL_BINDFACE|(key name)|(min)|(max)|(model alias)|(morph name)|rate1|rate2
{{</message>}}

`min`, `max` are the minimum and maximum values of the global variable, and `rate1`, `rate2` are the corresponding minimum and maximum values of the morph. Values below `min` are capped at `rate1`, and values above `max` are capped at `rate2`. The range in between is interpolated linearly. This is represented in the diagram below (where the horizontal axis represents the global variable's value, and 1 on the vertical axis corresponds to `rate1` and 2 to `rate2`).

![BindBone](/images/bindbone.png)

You can unbind with the `MODEL_UNBINDFACE` command.

{{<message>}}
MODEL_UNBINDFACE|(model alias)|(morph name)
{{</message>}}