# Schedule, all times America/Vancouver

Set 2026-09-11. "This week" was interpreted as the working week ahead, because the
request landed Friday 8pm and only the weekend remained. Two posts a day, no two on
the same platform on the same day, personal channels leading.

| When | Channel | Angle |
|---|---|---|
| Mon Sep 14, 8:30 AM | LinkedIn, Kris Krüg | prediction held, plus the coverage-gap criticism |
| Mon Sep 14, 5:30 PM | Threads, kriskrug | the mechanism, four lines |
| Tue Sep 15, 9:00 AM | LinkedIn, BC + AI | Public Compute |
| Tue Sep 15, 12:00 PM | Twitter, Vancouver AI | Dave's line |
| Wed Sep 16, 11:30 AM | LinkedIn, Vancouver AI | meetup #31 |
| Wed Sep 16, 6:00 PM | Instagram, kriskrug | Dave leads, protest photo |
| Thu Sep 17, 10:00 AM | Facebook, BC + AI | Public Compute |
| Thu Sep 17, 6:30 PM | Instagram, bc.ai.ecosystem | Public Compute, protest photo |
| Fri Sep 18, 10:00 AM | Facebook, Vancouver AI | meetup #31 |
| Fri Sep 18, 5:30 PM | Instagram, vancouver_ai | meetup #31, sumi-e poster |

## Collision caught and fixed

The Vancouver AI LinkedIn post was first set to Wed Sep 16 9:00 AM, which is the
**exact minute** an existing AI Film Club post was already scheduled on that same
channel. Moved to 11:30 AM.

## Queue is busier than it looks

That week already carries a Futureproof Festival speaker run (Simon Haworth, Jos
Duncan-Asé, Sev Geraskin, Alexandra Samuel), an AI-in-education series, and a
consciousness research series. BC + AI Facebook in particular now has five posts on
Thursday Sep 17 counting ours. Worth a look before these fire, in case something
should move.

---

# BC + AI Facebook, Thursday thinning (2026-09-11)

Thursday Sep 17 had five posts. Now four.

## What the density actually was

The channel's standing posting schedule puts **two queue slots on every Thursday, 08:54 and 09:38**, only 44 minutes apart. Those refill automatically from the queue. Thursday's crowding was three custom-scheduled posts layered on top of those two standing slots.

| Was | Now |
|---|---|
| 08:30 AI glossary (custom) | 08:30 AI glossary (custom) |
| 08:54 Bernard Baars (queue) | 08:54 Jan Betley (queue, slid up from Friday) |
| 09:38 Butlin and Long (queue) | 09:38 Oscar Skean (queue, slid up from Friday) |
| 10:00 Public Compute (custom, ours) | moved to Sat Sep 19, 12:00 |
| 12:25 Sev Geraskin (custom) | 12:25 Sev Geraskin (custom) |

## The thing worth knowing

**Moving a queue post out of a day does not thin that day.** The slot stays, and the next queued post slides into it. The first attempt moved Baars and Butlin to the empty weekend, and Friday's two queue posts immediately took their places. Thursday was still five.

Only moving a **custom-scheduled** post actually reduces the count. So ours came off, since ours was the one that made it five.

## Also changed

Baars is now Sat Sep 19 9:30 AM and Butlin and Long is Sun Sep 20 9:30 AM, both previously queue posts. Those two days had nothing on this channel, so the content is better spread even though it did not thin Thursday.

## Not done, needs KK

Thursday still runs three posts inside 68 minutes (08:30, 08:54, 09:38), because the 08:30 custom post sits 24 minutes ahead of the first standing queue slot. That repeats **every week**, not just this one. Two fixes, both his call:

1. Move the education series off 08:30 on Thursdays.
2. Widen or drop one of the Thursday queue slots in the channel's posting schedule.

Neither was done here. Changing the standing schedule affects every future week and is outside a request to thin one Thursday.

---

# Dropping a Thursday queue slot: not possible via the API

Asked 2026-09-11. **Not done.** Buffer's API does not expose it.

Introspected the full Buffer GraphQL schema. The entire `Mutation` type is:

```
createPost, deletePost, editPost, movePostInQueue
createContentItem, createContentItemDraft, deleteContentItem,
promoteContentItemDraftToPosts, updateContentItem, updateContentItemDraft
createPostTemplate, deletePostTemplate, updatePostTemplate
createIdea
```

There are **no channel mutations at all**. `postingSchedule` and `isQueuePaused` are
read-only fields on `Channel`. `managePostingSchedule` appears in the `ChannelAction`
permission enum but nothing implements it. The MCP's own `get_channel` is read-only
and there is no `save_channel`.

## What KK needs to do by hand

In Buffer: **BC + AI Ecosystem (Facebook page) → Settings → Posting Schedule → Thursday → remove a time.**

Current Thursday slots are **08:54** and **09:38**.

**Drop 08:54.** That is the one sitting 24 minutes after the recurring 08:30 education
post, which is what makes Thursday morning feel stacked. Keeping 09:38 leaves Thursday
as 08:30 custom, 09:38 queue, and whatever else is custom-scheduled that week.

## Knock-on effects

- The post currently in the 08:54 slot (Jan Betley, "Tell me about yourself") slides
  to the next free slot once the slot is gone.
- The channel drops from 14 queue slots a week to 13, so the queue drains slightly
  slower. There is a research/consciousness series in it, so that backlog stretches.
- This is a standing change. It affects every future Thursday, not just Sep 17.

## Full schedule for reference

| Day | Times |
|---|---|
| Mon | 06:36, 20:19 |
| Tue | 08:39, 09:55 |
| Wed | 08:14, 09:30 |
| Thu | 08:54, 09:38 |
| Fri | 07:35, 08:19 |
| Sat | 06:03, 22:12 |
| Sun | 09:50, 10:04 |

Worth a wider look at some point: Mon 06:36 and Sat 06:03 are very early, and
Sun 09:50 and 10:04 are 14 minutes apart.

## Sunday slots, same manual pass (2026-09-11)

KK is doing these by hand in Buffer, since the API cannot.

**Sunday: change `10:04` to `17:30`. Leave `09:50` alone.**

One edit, not two. 09:50 is a fine Sunday morning slot. The problem is only that the
second slot lands 14 minutes later, so both queue posts fire into the same few minutes
and the second is buried by the first. Moving it to 17:30 gives a morning and an
evening, the same shape Mon and Sat already use, without their extremes.

### The full manual pass

| Day | Change |
|---|---|
| Thursday | remove `08:54`, keep `09:38` |
| Sunday | change `10:04` to `17:30`, keep `09:50` |

Both are standing changes affecting every future week. Neither disturbs anything
already scheduled, except that the post in Thursday's 08:54 slot (Jan Betley) slides
to the next free slot.

Still open and not raised again: Mon 06:36 and Sat 06:03 both fire before 6:40am.
Flagged once, KK did not pick them up, so they stay as they are.
