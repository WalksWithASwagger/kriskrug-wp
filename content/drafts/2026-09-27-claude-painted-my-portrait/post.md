---
title: "I Made Claude Paint My Portrait in MS Paint. No Scripts."
slug: claude-painted-my-portrait-ms-paint
status: draft
date: 2026-09-27
categories: [AI for Creatives, Creative Technology & Making]
tags: [Claude, JSPaint, portraiture, AI collaboration, process, Isaiah Odhner]
excerpt: "Four sessions, a hand mixed palette, and one rule: brushes and clicking only. No scripting the canvas. The failures taught me more than the finished picture did."
---

# I Made Claude Paint My Portrait in MS Paint. No Scripts.

I handed [Claude](https://claude.com/claude-code) my profile photo, pointed it at [JSPaint](https://jspaint.app), and gave it one rule. Use brushes and clicking. Do not use the javascript tool. Do not cheat.

That rule is the entire experiment. A model that writes code could render my face in about four seconds by pushing pixels through a script. Ban the script and a code problem turns into a painting problem. Now it has to pick a color, put the stroke somewhere, and live with it.

JSPaint is [Isaiah Odhner's](https://isaiahodhner.io) browser resurrection of MS Paint, faithful down to the Edit Colors dialog. That dialog turns out to matter.

>>> A model that writes code could render my face in four seconds. Banning the shortcut turns a code problem into a painting problem.

[[VIDEO]]

## It had to mix paint before it could paint

MS Paint gives you twenty eight color slots and not one of them is skin.

So the first real work was mixing. Open Edit Colors, type RGB values, overwrite a slot, repeat. By the end there was a seven step auburn ramp for the beard, five skin tones, two background glows, and a near black for the cap.

Nobody tells you that the constraint in 1995 software is the palette, not the brush.

## Every failure was the same failure

It made a shape where a form should be. Every single time.

- Sheen on the black beanie, attempt one: overshot the hat and left a teal arc floating in the background.
- Sheen on the beanie, attempt two: filled correctly, read as two hard slabs pasted onto wool. Painted out.
- Highlight on the forehead: three parallel bars.
- Shadow under the cap brim: a grey slab.
- Glow falloff in the background: concentric contour lines, like a topographic map.

The fix never changed. Break the edge. Jitter the spacing. Let the boundary go ragged and irregular until it stops announcing itself.

>>> A form is not a shape with a clean border. It is a gradient that never quite resolves.

## Rim light is the moment it became a head

For three sessions the picture stayed flat. Face, beard, hat, all more or less accurate, all sitting on the background like a sticker.

Rim light fixed it. Warm orange down the left silhouette where the background glow sits. Cool cyan down the right edge of the cap, the beard, the shoulder. One light on each side, hugging the outline.

That is the oldest move in portrait painting and it works identically on a 600 pixel canvas in a browser toy.

## The record turned out to be more fragile than the painting

Here is the part I did not see coming.

The timelapse up top is not a screen recording. JSPaint keeps your full undo history and will render that history out as an animated GIF. 834 frames, every one of them a real brush stroke that actually happened.

Then a browser tab closed between sessions and took the history with it.

The painting survived by luck. JSPaint autosaves to browser storage, and File then Manage Storage still had it sitting there. The undo history was gone. Two entire sessions of work now exist only as a before and an after.

[[GALLERY-BEFORE-AFTER]]

So the video has a seam in it. It runs 834 honest frames, then dissolves straight into the finished portrait. Everything between those two states happened, and there is no footage of it.

>>> The painting survived. The record of making it did not.

## What I take from this

The constraint did the work. Not the model, not the prompt, the fence.

"Use brushes" is a short sentence that deletes every fast path and leaves only the slow one. What came back is not a better picture than a script would have produced. It is a different sort of object, with four sessions of decisions baked into it, and most of those decisions were wrong before they were right.

I keep landing in the same place on this stuff. The interesting question is not what these tools do when you let them run. It is what they do when you put a fence around them and make them work inside your constraints instead of their own.

I was circling this two years ago with [Autolume and post photographic portraiture](https://kriskrug.co/2024/12/02/autolume-post-photographic-cybernetic-portraiture/), and again last week in [Montreal, staring at a robot mirror](https://kriskrug.co/2026/09/16/all-in-montreal-robot-mirror/). Same question, different tools. Who is holding the brush, and what did they give up to hold it?
