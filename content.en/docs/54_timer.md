

---
title: Timer
slug: timer
---

# Timer

{{< hint info >}}
This feature is part of the Plugin_Variables plugin. Please make sure that Plugin_Variables is enabled when using it.
{{< /hint >}}

There are scenarios where certain timing or reactions are necessary in dialogue, such as "doing something when there is no input from the user for a certain period of time" or "matching the timing of motion and voice playback". To accommodate this, MMDAgent-EX provides a "countdown timer" for performing wait processing.

The countdown timer notifies the passage of time by outputting a **TIMER_EVENT_STOP** message after the time specified in the argument has passed, and then ends.

{{< hint warning >}}
Please note that the resolution of the timer is 0.1 seconds. You cannot set a value smaller than 0.1 seconds. Also, because the count is in units of 0.1 seconds, there will be a margin of error of several tens of milliseconds.
{{< /hint >}}

The messages to start and interrupt the timer are as follows:

- **TIMER_START** Message to start a new timer
- **TIMER_CANCEL** Message to cancel a timer in operation

The messages output when the timer state changes are as follows:

- **TIMER_EVENT_START** When the timer starts
- **TIMER_EVENT_STOP** When the timer ends
- **TIMER_EVENT_CANCELLED** When the timer is cancelled or reset

## Basic Usage

Start a new timer with the **TIMER_START** message. The argument `(count down alias)` is the name of the new timer to start, and `(value)` is the timer time (in seconds).

{{<message>}}
TIMER_START|(count down alias)|(value)
{{</message>}}

If a timer with the same name is already running, the old timer will be cancelled first (issuing a **TIMER_EVENT_CANCELLED** message), and then a timer with the same name will start anew (issuing a **TIMER_EVENT_START** message).

A **TIMER_EVENT_START** message is issued when the timer starts.

{{<message>}}
TIMER_EVENT_START|(count down alias)
{{</message>}}

The timer decreases by 0.1 second in the background. When the specified time has passed and the value has decreased to 0, it's the end of the timer. At the end, a **TIMER_EVENT_STOP** message is output and the timer is deleted.

{{<message>}}
TIMER_EVENT_STOP|(count down alias)
{{</message>}}

## Cancel

When you want to interrupt a timer in the middle, use the **TIMER_CANCEL** message.

{{<message>}}
TIMER_CANCEL|(count down alias)|(value)
{{</message>}}

**TIMER_CANCEL** will issue a **TIMER_EVENT_CANCELLED** regardless of whether the specified timer exists or not.

{{<message>}}
TIMER_EVENT_CANCELLED|(count down alias)
{{</message>}}