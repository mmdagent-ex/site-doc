---
title: Timer
slug: timer
---
# Timer

{{< hint info >}}
This feature is part of the Plugin_Variables plugin. Make sure Plugin_Variables is enabled when using it.
{{< /hint >}}

In dialogue you sometimes need to wait a fixed amount of time before acting—for example, "do something if there is no input from the user for a certain time" or "synchronize motion and audio playback." For this purpose, MMDAgent-EX provides a countdown timer for wait handling.

The countdown timer notifies the end of the interval and finishes by outputting the **TIMER_EVENT_STOP** message after the time specified in the arguments has elapsed.

{{< hint warning >}}
Note that the timer resolution is 0.1 seconds. Values smaller than 0.1 s cannot be specified. Counting is done in 0.1-second steps, so differences of a few tens of milliseconds may occur.
{{< /hint >}}

Messages to start or cancel a timer:

- **TIMER_START** Message to start a new timer
- **TIMER_CANCEL** Message to cancel a running timer

Messages emitted when the timer state changes:

- **TIMER_EVENT_START** When a timer is started
- **TIMER_EVENT_STOP** When a timer expires
- **TIMER_EVENT_CANCELLED** When a timer is cancelled or reconfigured

## Basic usage

Start a new timer with the **TIMER_START** message. The argument `(count down alias)` is the name of the timer to start, and `(value)` is the timer duration in seconds.

{{<message>}}
TIMER_START|(count down alias)|(value)
{{</message>}}

If a timer with the same name is already running, the old timer is first cancelled (emitting **TIMER_EVENT_CANCELLED**), and then a new timer with the same name is started (emitting **TIMER_EVENT_START**).

When a timer is started, a **TIMER_EVENT_START** message is emitted.

{{<message>}}
TIMER_EVENT_START|(count down alias)
{{</message>}}

The timer counts down in the background, decreasing its value every 0.1 seconds. When the specified time elapses and the value reaches 0, the timer ends. At that time, a **TIMER_EVENT_STOP** message is emitted and the timer is removed.

{{<message>}}
TIMER_EVENT_STOP|(count down alias)
{{</message>}}

## Cancel

To interrupt a timer before it finishes, use the **TIMER_CANCEL** message.

{{<message>}}
TIMER_CANCEL|(count down alias)|(value)
{{</message>}}

**TIMER_CANCEL** will emit **TIMER_EVENT_CANCELLED** whether or not the specified timer exists.

{{<message>}}
TIMER_EVENT_CANCELLED|(count down alias)
{{</message>}}