#!/usr/bin/env python3
"""Export artwork previews from a frozen v2 atlas using the audited row clock.

Each state preview loops one row cycle for inspection. Actual default three-cycle
fallback and interruptions are modeled by preview_transitions.py separately.
MP4 output is optional and requires an ffmpeg executable; Pillow is sufficient
for all PNG/GIF outputs. This tool never modifies the source atlas.
"""
import argparse
from dataclasses import replace
import hashlib
import json
from pathlib import Path
import subprocess

from PIL import Image, ImageDraw
from preview_transitions import (Frame, SNAPSHOT, STATES, cell, load_atlas,
                                 row_frames, save_gif)


def labeled(atlas, frame, label):
    image = Image.new('RGB', (320, 256), '#eef2f8')
    ImageDraw.Draw(image).text((12, 10), label, fill='#182c48')
    sprite = cell(atlas, frame)
    image.paste(sprite, (64, 36), sprite)
    return image


def mp4(path, images, durations, executable):
    width, height = images[0].size
    command = [executable, '-hide_banner', '-loglevel', 'error', '-y',
               '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{width}x{height}',
               '-r', '100', '-i', 'pipe:0', '-an', '-c:v', 'libx264',
               '-pix_fmt', 'yuv420p', '-crf', '18', '-movflags', '+faststart', str(path)]
    with subprocess.Popen(command, stdin=subprocess.PIPE) as process:
        for image, duration in zip(images, durations, strict=True):
            data = image.convert('RGB').tobytes()
            for _ in range(duration // 10):
                process.stdin.write(data)
        process.stdin.close()
        if process.wait():
            raise RuntimeError('ffmpeg failed')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--atlas', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--ffmpeg', help='Optional ffmpeg executable for MP4 copies')
    args = parser.parse_args()
    atlas = load_atlas(args.atlas)
    output = args.output
    (output/'states').mkdir(parents=True, exist_ok=True)
    all_images, all_durations = [], []
    for state in STATES:
        frames = row_frames(state)
        if state == 'idle':
            frames = [replace(frame, ms=frame.ms*6) for frame in frames]
        label = 'tail-wag (jumping slot)' if state == 'jumping' else state
        images = [labeled(atlas, f, f'{label} | {i+1}/{len(frames)}')
                  for i, f in enumerate(frames)]
        durations = [f.ms for f in frames]
        save_gif(output/'states'/f'{state}.gif', images, durations)
        if state == 'jumping':
            save_gif(output/'tail-wag.gif', images, durations)
            contact = Image.new('RGB', (320*5, 256), '#eef2f8')
            for i, image in enumerate(images):
                contact.paste(image, (320*i, 0))
            contact.save(output/'tail-wag-frames.png')
        all_images.extend(images)
        all_durations.extend(durations)
    save_gif(output/'all-states.gif', all_images, all_durations)
    boundary = [Frame(0, 0, 600)] + row_frames('jumping')*3 + [Frame(0, 0, 1680)]
    boundary_images = [labeled(atlas, f, 'idle / tail-wag / idle') for f in boundary]
    boundary_durations = [f.ms for f in boundary]
    save_gif(output/'idle-tail-wag-idle.gif', boundary_images, boundary_durations)
    looks = [Frame(9+i//8, i%8, 180) for i in range(16)]
    save_gif(output/'look-loop.gif',
             [labeled(atlas, f, f'look {i*22.5:g} deg') for i, f in enumerate(looks)],
             [f.ms for f in looks])
    proof = Image.new('RGB', (640, 512), '#eef2f8')
    for i, (state, column) in enumerate([('idle', 0), ('running', 2), ('jumping', 2), ('running-right', 3)]):
        frame = replace(row_frames(state)[column], ms=0)
        proof.paste(labeled(atlas, frame, f'{state} | frame {column}'),
                    ((i%2)*320, (i//2)*256))
    proof.save(output/'four-state-stills.png')
    if args.ffmpeg:
        mp4(output/'all-states.mp4', all_images, all_durations, args.ffmpeg)
        mp4(output/'idle-tail-wag-idle.mp4', boundary_images, boundary_durations, args.ffmpeg)
    manifest = {'atlas_sha256': hashlib.sha256(args.atlas.read_bytes()).hexdigest(),
                'client_snapshot': SNAPSHOT, 'idle_durations_ms': [1680, 660, 660, 840, 840, 1920],
                'state_preview_mode': 'one row cycle looped for artwork inspection',
                'all_states_mode': 'one cycle per row; not a business-state scenario',
                'tail_wag_boundary_mode': 'idle entrance hold, three tail-wag cycles, idle first-frame hold',
                'look_preview_ms_per_direction': 180,
                'timing_does_not_configure_the_client': True,
                'synthetic_tween_or_crossfade': False,
                'mp4_exported': bool(args.ffmpeg)}
    (output/'preview-manifest.json').write_text(json.dumps(manifest, indent=2)+'\n')
    print(json.dumps({'output': str(output), 'states': 9, 'look_frames': 16,
                      'mp4_exported': bool(args.ffmpeg)}))


if __name__ == '__main__':
    main()
