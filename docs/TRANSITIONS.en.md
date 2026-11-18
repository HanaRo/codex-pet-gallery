# Animation transitions

[简体中文](TRANSITIONS.md) · **English**

Recorded on 2026-10-22 for desktop client **26.1016.61520, build 21421**. The installed package matched the three previously inspected modules. The repository records observed behavior and provides independent QA tools.

The official Pets guide covers activity states, entry points, and reduced motion. The exact timing, priority, and interruption rules below come from the inspected local build and should be rechecked after client upgrades. Artwork names refer to 1.0.1. The 1.0.0 archive retains its original poses. [Official Pets documentation](https://learn.chatgpt.com/docs/pets)

## Task state, interaction, and displayed frame

1. **Task state.** Activities can select `idle`, `running`, `waiting`, `failed`, or `review`. The initial greeting can select `waving`. A priority or thread change can jump directly between states.
2. **Interaction override.** Drag direction takes priority, then hover (`jumping`), then the task state. In this character, hover shows a standing tail wag and drag shows her being picked up.
3. **Displayed frame.** With `idle`, `running`, or `waving` selected, a supplied `lookFrame` displays one of the 16 direction stills. Otherwise the animation plays and can fall back to slow idle while the underlying task state stays the same.

The task can still be running after the eating animation falls back to idle.

~~~mermaid
flowchart LR
  B[Task state and current notification] --> P{Interaction override}
  D[Horizontal drag] --> P
  H[Hover] --> P
  P --> V[Select drag, jumping, or task state]
  V --> L{Idle, running, or waving with lookFrame?}
  L -->|Yes| K[Show direction still]
  L -->|No| R{Reduced motion?}
  R -->|Yes| F[Show frame 0 of selected state]
  R -->|No| A[Play selected state]
  A -->|Non-idle after three loops| I[Loop slow idle]
  A -->|Idle| I
~~~

## Transitions in the client

| Event | Typical transitions | Behavior and visual checks |
| --- | --- | --- |
| Start, resume, or retry | idle / waiting / failed / review → running | Enters running at frame 0. Align the body, face, bowl, and hands with whichever pose was visible. |
| Task result or input request | running → waiting / review / failed; waiting → running / failed / idle; review / failed → idle | Notifications and thread changes can also trigger these. Check any source frame to the destination's frame 0, including quick successive changes. |
| Greeting ends | waving → idle or current task state | Activity, hover, drag, and gaze can interrupt the greeting. |
| Automatic fallback | any non-idle animation → slow idle | After three loops by default, switches directly to idle frame 0 with the underlying state unchanged. |
| Pointer enters or leaves | task state ↔ jumping | Hover enters the tail wag. Leaving restarts the current task animation from the beginning. |
| Drag starts or reverses | task state / jumping → running-left / running-right; left ↔ right | A horizontal direction change starts the destination row at frame 0. Use a stable grab point for lifted poses. |
| Drag ends or is canceled | running-left / running-right → jumping or task state | Releasing clears the drag override. If the pointer is still hovering, jumping takes over. There is no dedicated set-down row. |
| Gaze appears, changes, or clears | idle / running / waving ↔ look; look → look | A direction still overrides playback. Clearing it restarts the animation at frame 0. Check neighboring angles and the four cardinal directions. |
| System reduced motion | any animation → its frame 0; restart when disabled | Frame 0 must read on its own. A supplied `lookFrame` still displays the direction pose. |
| Content refresh in the same state | running → running and similar | Text updates, same-state activity, and an unchanged drag direction usually leave playback where it is. |

Competing notifications, hover, drag, and gaze can produce cross-state jumps. The 9 × 9 last-to-first-frame matrix from `tools/preview_transitions.py` stress-tests the artwork. Which of its 81 boundaries can actually occur depends on the entry point.

## Exact timing and hard cuts

| Animation | Frame durations in ms | Time before default fallback |
| --- | --- | --- |
| running | 120, 120, 120, 120, 120, 220 | 820 × 3 = 2460 ms |
| waiting | 150, 150, 150, 150, 150, 260 | 1010 × 3 = 3030 ms |
| review | 150, 150, 150, 150, 150, 280 | 1030 × 3 = 3090 ms |
| failed | 140 each for the first 7, then 240 | 1220 × 3 = 3660 ms |
| waving | 140, 140, 140, 280 | 700 × 3 = 2100 ms |
| jumping | 140, 140, 140, 140, 280 | 840 × 3 = 2520 ms |
| running-left / running-right | 120 each for the first 7, then 220 | 1060 × 3 = 3180 ms |
| Slow idle | **1680, 660, 660, 840, 840, 1920** | 6600 ms, loops continuously |

Slow idle multiplies each base duration in `[280, 110, 110, 140, 140, 320]` by six. Use exact timings to evaluate rhythm. The older even-timing GIFs are pose references.

The automatic `running → idle` cut happens after frame 5 of the third running loop, straight into idle frame 0. A task event can instead cut from any running frame to the destination's frame 0. The player sets the sprite cell directly. Its blending, exit states, and interpolation cannot be configured through a sprite sheet. Preview the real cuts when judging transitions.

The inspected entry point leaves the internal continuous-playback option off. A held drag can therefore revert to slow idle after three loops. The local player chooses drag direction based on about four units of horizontal screen movement. Purely vertical drags have no dedicated row.

## Current character transition risks

| Priority | Boundary | What to check |
| --- | --- | --- |
| Regression check | Every running frame → idle frame 0 | 1.0.1 reduced the chopstick lift, narrowed the hair and ear fins, and aligned body scale, feet, and bowl. Chopsticks, rice, and hand poses can still change on the cut. |
| Regression check | idle / running ↔ jumping | The 1.0.1 tail wag retains the bowl and updated face, so the bowl stays visible. Check tail position on an interruption at every frame. |
| P1 | idle / running / waving ↔ look | The inherited gaze stills are empty-handed. Use the current neutral pose and prop when the gaze rows are next revised. |
| P1 | running-left ↔ running-right | Mirroring moves the cowlick grab point and may cause a sideways jump. Unify the anchor while preserving the silhouette and timing. |
| P1 | Lifted drag → jumping / idle | All three use the bowl, but the airborne and standing poses differ. With no set-down row, match scale, limit displacement, and align the destination's frame 0. |
| P2 | waiting / review / waving / failed ↔ bowl-holding states | Decide which props remain visible and where they go before revising the affected rows. |
| P2 | Entry and loop seams | Frame 0 also serves as the reduced-motion pose. The last frame can lead into frame 0 of the same row or idle. Check both boundaries. |

Keep edits scoped to affected rows, preserve the other pixels and a rollback version, and record remaining issues.

## Review checklist for new artwork

1. Set shared body and head proportions, standing foot baseline, lifted grab point, and bowl and tool positions. Prefer a neutral frame 0 that reads by itself.
2. Check the loop seam, natural return to idle, and interruptions from any frame.
3. Cover the three-loop fallback, all six running interruptions, idle → running, running ↔ waiting, running → review or failed, retry, hover entry and exit, drag reversal and release, gaze entry and exit, and reduced motion.
4. Share grab points across lifted poses and foot baselines across grounded poses. Preserve airborne sway and use consistent scale across frames.
5. Generate GIFs from the encoded atlas and record exact durations. Compare versions with the same events and timeline. Use geometry metrics to locate issues and review the motion visually.
6. Artwork can improve poses, scale, expressions, and prop alignment. State priority, interrupt timing, continuous looping, and blending come from the player.

## Export transition previews

~~~bash
python tools/preview_transitions.py \
  --atlas pets/deepseek-chan/versions/1.0.1/spritesheet.png \
  --output dist/transitions

# Compare two atlases on the same transition timeline.
python tools/preview_transitions.py \
  --atlas /path/to/after.png --compare /path/to/before.png \
  --output dist/transition-comparison
~~~

Outputs include the automatic fallback, interruptions from all working frames, common task and interaction GIFs, four sets of key stills, 81 last-to-first-frame boundaries, and geometry metrics. The tool is an offline QA model. Release checks still require asset validation, visual review, and a separate version directory.
