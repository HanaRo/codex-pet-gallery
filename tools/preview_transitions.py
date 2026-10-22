#!/usr/bin/env python3
"""Render hard-cut QA from an encoded atlas; model the audited desktop snapshot.

This is an offline inspection model, not a configuration for the Codex player.
No interpolation, crossfade, synthetic character pixels, or extra runtime rows.
"""
from __future__ import annotations

import argparse
import csv
from dataclasses import dataclass, replace
import hashlib
import json
import math
from pathlib import Path

from PIL import Image, ImageDraw

SNAPSHOT = '26.1016.61520 (21421), audited 2026-10-22'
STATES = ('idle', 'running-right', 'running-left', 'waving', 'jumping',
          'failed', 'waiting', 'running', 'review')
COUNTS = (6, 8, 8, 4, 5, 8, 6, 6, 6)
DURATIONS = ((280, 110, 110, 140, 140, 320),
             (120,) * 7 + (220,), (120,) * 7 + (220,),
             (140, 140, 140, 280), (140,) * 4 + (280,),
             (140,) * 7 + (240,), (150,) * 5 + (260,),
             (120,) * 5 + (220,), (150,) * 5 + (280,))
LOOK_ELIGIBLE = {'idle', 'running', 'waving'}
DRAG_STATES = {'running-left', 'running-right'}


@dataclass(frozen=True)
class Frame:
    row: int
    column: int
    ms: int


def row_frames(state):
    row = STATES.index(state)
    return [Frame(row, column, ms) for column, ms in enumerate(DURATIONS[row])]


def animation_plan(state, *, reduced_motion=False, loop=False):
    action = row_frames(state)
    if reduced_motion:
        return action[:1], None
    idle = [replace(frame, ms=frame.ms * 6) for frame in row_frames('idle')]
    if state == 'idle':
        return idle, 0
    if loop:
        return action, 0
    repeated = action * 3
    return repeated + idle, len(repeated)


def frame_at(state, elapsed_ms, *, reduced_motion=False, loop=False):
    frames, start = animation_plan(state, reduced_motion=reduced_motion, loop=loop)
    if reduced_motion:
        return frames[0]
    elapsed = max(0, elapsed_ms)
    total = sum(frame.ms for frame in frames)
    if elapsed >= total:
        prefix = sum(frame.ms for frame in frames[:start])
        elapsed = prefix + (elapsed - prefix) % (total - prefix)
    for frame in frames:
        if elapsed < frame.ms:
            return frame
        elapsed -= frame.ms
    raise AssertionError('unreachable timeline position')


def selected_state(base, *, hover=False, drag=None):
    if base not in STATES:
        raise ValueError(f'Unknown state: {base}')
    if drag is not None and drag not in DRAG_STATES:
        raise ValueError(f'Unknown drag override: {drag}')
    return drag or ('jumping' if hover else base)


def rendered_frame(base, elapsed_ms, *, hover=False, drag=None,
                   look=None, reduced_motion=False, loop=False):
    state = selected_state(base, hover=hover, drag=drag)
    if look is not None:
        if not isinstance(look, int) or not 0 <= look < 16:
            raise ValueError('look must be an index from 0 through 15')
        if state in LOOK_ELIGIBLE:
            return Frame(9 + look // 8, look % 8, 0)
    return frame_at(state, elapsed_ms, reduced_motion=reduced_motion, loop=loop)


def first(state, ms=500):
    return replace(row_frames(state)[0], ms=ms)


def cut(source, target):
    return [replace(row_frames(source)[-1], ms=300), first(target)]


def scenarios():
    cases = {'running-auto-idle': animation_plan('running')[0]}
    cases['running-interrupt-idle'] = [frame for i in range(6) for frame in
        (Frame(7, i, 240), first('idle', 600))]
    for source, target in [('idle', 'running'), ('running', 'waiting'),
                           ('waiting', 'running'), ('running', 'review'),
                           ('running', 'failed'), ('review', 'idle'),
                           ('failed', 'running'), ('waiting', 'idle')]:
        cases[f'{source}-to-{target}'] = cut(source, target)
    cases['hover-enter-exit'] = [first('idle')] + row_frames('jumping') + [first('idle')]
    for direction in ('running-right', 'running-left'):
        for target in ('idle', 'jumping'):
            cases[f'{direction}-release-{target}'] = row_frames(direction) + [first(target)]
    cases['drag-direction-reversal'] = row_frames('running-right') + row_frames('running-left')
    cases['idle-look-return'] = [first('idle')] + [Frame(9+i//8, i%8, 400)
                                                for i in (0, 4, 8, 12)] + [first('idle')]
    cases['look-return-restarts-running'] = [Frame(7, 2, 400), Frame(9, 4, 500)] + row_frames('running')
    return cases


def load_atlas(path):
    with Image.open(path) as im:
        if im.size != (1536, 2288) or im.mode != 'RGBA':
            raise ValueError('Expected a v2 1536x2288 RGBA atlas')
        return im.copy()


def cell(atlas, frame):
    return atlas.crop((frame.column*192, frame.row*208,
                       (frame.column+1)*192, (frame.row+1)*208))


def scene(atlases, frame):
    canvas = Image.new('RGB', (208*len(atlases), 244), '#eef2f8')
    draw = ImageDraw.Draw(canvas)
    for index, (label, atlas) in enumerate(atlases):
        draw.text((index*208+8, 8), f'{label}  r{frame.row}c{frame.column}', fill='#182c48')
        sprite = cell(atlas, frame)
        canvas.paste(sprite, (index*208+8, 30), sprite)
    return canvas.resize((canvas.width*2, canvas.height*2), Image.Resampling.LANCZOS)


def save_gif(path, frames, durations):
    frames[0].save(path, save_all=True, append_images=frames[1:],
                   duration=durations, loop=0, disposal=2, optimize=False)


def edge_metrics(source, target):
    a = source.getchannel('A').tobytes()
    b = target.getchannel('A').tobytes()
    intersection = sum(x > 16 and y > 16 for x, y in zip(a, b))
    union = sum(x > 16 or y > 16 for x, y in zip(a, b))
    bounds = [im.getchannel('A').point(lambda value: 255 if value > 16 else 0).getbbox()
              for im in (source, target)]
    if None in bounds:
        return {'alpha_iou': 0, 'bbox_center_delta_px': None, 'baseline_delta_px': None}
    centers = [((r[0]+r[2])/2, (r[1]+r[3])/2) for r in bounds]
    return {'alpha_iou': round(intersection/max(1, union), 4),
            'bbox_center_delta_px': round(math.dist(*centers), 3),
            'baseline_delta_px': bounds[1][3]-bounds[0][3]}


def stress_matrix(atlas, output):
    # All 81 last-to-first boundaries are art stress tests, not reachability claims.
    sheet = Image.new('RGB', (9*400, 9*240), '#eef2f8')
    draw = ImageDraw.Draw(sheet)
    records = []
    for row, source in enumerate(STATES):
        for column, target in enumerate(STATES):
            a = cell(atlas, row_frames(source)[-1]);b = cell(atlas, row_frames(target)[0])
            x = column*400;y = row*240
            draw.text((x+5, y+5), f'{source} -> {target}', fill='#182c48')
            sheet.paste(a, (x+4, y+28), a);sheet.paste(b, (x+204, y+28), b)
            records.append({'source':source, 'target':target, **edge_metrics(a,b)})
    sheet.save(output/'last-to-first-stress-matrix.png')
    with (output/'last-to-first-stress-metrics.csv').open('w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=list(records[0]));writer.writeheader();writer.writerows(records)
    return records


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--atlas', type=Path, required=True)
    parser.add_argument('--compare', type=Path, help='Optional previous atlas; both receive identical frame/timing sequences')
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    atlas = load_atlas(args.atlas);args.output.mkdir(parents=True, exist_ok=True)
    atlases = [('AFTER' if args.compare else 'CURRENT', atlas)]
    if args.compare:atlases.insert(0, ('BEFORE', load_atlas(args.compare)))
    manifest = {'client_snapshot':SNAPSHOT, 'atlas_sha256':hashlib.sha256(args.atlas.read_bytes()).hexdigest(),
                'timing_is_snapshot_specific':True, 'synthetic_crossfade_or_tween':False,
                'cases':[], 'metrics_are_review_aids_not_acceptance':True}
    for name, frames in scenarios().items():
        save_gif(args.output/f'{name}.gif', [scene(atlases, f) for f in frames], [f.ms for f in frames])
        manifest['cases'].append({'name':name, 'frames':len(frames), 'duration_ms':sum(f.ms for f in frames)})
    # Concrete proof of the natural boundary, suitable for a still-only viewer.
    key = [Frame(7,5,220), Frame(0,0,1680), Frame(0,1,660), Frame(0,3,840)]
    examples = [scene(atlases, f) for f in key]
    stills = Image.new('RGB', (examples[0].width*2, examples[0].height*2), '#eef2f8')
    for index, im in enumerate(examples):stills.paste(im, ((index%2)*im.width, (index//2)*im.height))
    stills.save(args.output/'running-idle-key-stills.png')
    manifest['stress_boundaries'] = stress_matrix(atlas,args.output)
    target = cell(atlas,first('idle'))
    manifest['running_interrupt_metrics'] = [edge_metrics(cell(atlas,f),target) for f in row_frames('running')]
    if args.compare:
        previous = atlases[0][1];old_idle=cell(previous,first('idle'))
        manifest['previous_running_interrupt_metrics'] = [edge_metrics(cell(previous,f),old_idle) for f in row_frames('running')]
    (args.output/'transition-report.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'scenarios':len(manifest['cases']), 'stress_boundaries':81,
                      'output':str(args.output), 'client_snapshot':SNAPSHOT},ensure_ascii=False))


if __name__ == '__main__':
    main()
