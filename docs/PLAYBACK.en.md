# Client playback and animation states

[简体中文](PLAYBACK.md) · **English**

These observations come from a static inspection of desktop client 26.1016.61520 on October 22, 2026. They describe that build. The project distributes its own assets and tools.

## State selection and playback

The floating pet uses the first displayed activity or notification. An executing task selects `running`, an input request selects `waiting`, a failure or blocker selects `failed`, and a completed task awaiting review selects `review`. General information or no activity selects `idle`. The first wake-up greeting can select `waving`.

A drag direction takes priority over hover. Hover temporarily selects `jumping`, which this pet uses for a standing tail wag.

| State | DeepSeek-chan 1.0.1 animation | Frames | One loop | Time before slow idle |
| --- | --- | ---: | ---: | ---: |
| idle | Waits with an empty bowl, blinks and breathes | 6 | About 6.6 s at slow speed | Loops continuously |
| running-right | Kicks and wags when picked up and dragged right | 8 | 1.06 s | 3.18 s |
| running-left | Kicks and wags when picked up and dragged left | 8 | 1.06 s | 3.18 s |
| waving | Waves hello | 4 | 0.70 s | 2.10 s |
| jumping | Stands with the bowl and wags her tail | 5 | 0.84 s | 2.52 s |
| failed | Looks upset, then recovers | 8 | 1.22 s | 3.66 s |
| waiting | Holds the bowl and waits | 6 | 1.01 s | 3.03 s |
| running | Eats rice | 6 | 0.82 s | 2.46 s |
| review | Rests her chin on her hand and inspects | 6 | 1.03 s | 3.09 s |

Scholar Disguise uses the same layout. She looks at the rice behind her book at idle, holds the book during the hover tail wag, raises it to hide her mouth while eating, and straightens her slipping wig during either drag animation. [Scholar Disguise manifest](../pets/deepseek-gpt-scholar/versions/1.0.0/manifest.json)

By default, a non-idle animation plays three loops, then switches to slow idle even if the task is still running. Updating command text alone leaves the current animation state unchanged. Interactions and state changes can interrupt these timings.

The six slow idle frames last 1680, 660, 660, 840, 840, and 1920 ms, for a total of 6.6 seconds. A state change or the end of a hover, drag, or gaze override restarts the applicable animation. The player switches directly between cells. [State transitions](TRANSITIONS.en.md)

The player supports an internal `loop=true` setting for continuous non-idle animation. The inspected floating pet and the pet next to a Work response leave it off. Another avatar container enables it, so behavior can vary by entry point.

## Gaze directions and still frames

The last two v2 rows contain 16 single-frame gaze directions clockwise in 22.5° steps. 000 points up, 090 right, 180 down, and 270 left. The direction loop preview steps through all poses for inspection.

In `idle`, `running`, and `waving`, a client-supplied look target can replace the animation with a direction still. Targets can come from the text cursor or computer-use context. Ordinary mouse movement alone may produce no look target.

With system reduced motion enabled, a regular animation displays the first frame of the current state.

## What the sprite sheet controls

The sheet controls the artwork, what each pose depicts, clarity, and alignment. The Pets upload accepts an image. Loop counts, timing, and triggers come from the client. The 1.0.1 GIF and MP4 previews use the inspected client's precise timing. Individual state GIFs repeat one cycle for inspection. The automatic fallback after three loops has its own transition preview. Some historical 1.0.0 GIFs use even timing. Other client builds may play differently.

[Pets documentation](https://learn.chatgpt.com/docs/pets)
