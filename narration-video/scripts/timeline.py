"""Validate final-video timing and export SRT; standard library only."""
import argparse
import json
import math
from pathlib import Path


def number(value):
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
        raise ValueError("Time must be finite numeric seconds")
    return value


def millis(value):
    return int(number(value) * 1000 + 0.5)


def validate(data):
    if data.get("version") != 1:
        raise ValueError("Unsupported version")
    duration = number(data["duration"])
    if duration <= 0:
        raise ValueError("Duration must be positive")
    cues = data["cues"]
    if not cues or number(cues[0]["time"]) != 0:
        raise ValueError("First cue must start at zero")
    previous = -1
    for cue in cues:
        t = number(cue["time"])
        if not previous < t < duration:
            raise ValueError("Cues must increase strictly within duration")
        if not isinstance(cue.get("page"), str) or not cue["page"]:
            raise ValueError("Cue needs page ID")
        visible = cue.get("visible")
        if not isinstance(visible, list) or any(not isinstance(x, str) or not x for x in visible):
            raise ValueError("Cue needs full visible-ID list")
        if len(set(visible)) != len(visible):
            raise ValueError("Duplicate visible IDs")
        previous = t
    previous = 0
    for sub in data["subtitles"]:
        start, end = number(sub["start"]), number(sub["end"])
        if not 0 <= previous <= start < end <= duration:
            raise ValueError("Subtitles overlap or exceed duration")
        if millis(start) >= millis(end):
            raise ValueError("Subtitle collapses at millisecond precision")
        text = sub.get("text")
        if not isinstance(text, str) or not text.strip() or any(not line.strip() for line in text.split("\n")) or "\r" in text:
            raise ValueError("Subtitle text is empty or has blank lines")
        previous = end
    return data


def stamp(seconds):
    hours, total = divmod(millis(seconds), 3600000)
    minutes, total = divmod(total, 60000)
    seconds, ms = divmod(total, 1000)
    return f"{hours:02}:{minutes:02}:{seconds:02},{ms:03}"


def srt(data):
    validate(data)
    return "".join(f"{i}\n{stamp(s['start'])} --> {stamp(s['end'])}\n{s['text']}\n\n"
                   for i, s in enumerate(data["subtitles"], 1))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("timeline", type=Path)
    parser.add_argument("--srt", type=Path)
    args = parser.parse_args()
    data = validate(json.loads(args.timeline.read_text(encoding="utf-8")))
    if args.srt:
        if args.srt.resolve() == args.timeline.resolve():
            parser.error("Output must not overwrite input")
        with args.srt.open("x", encoding="utf-8", newline="\n") as output:
            output.write(srt(data))
    print(f"Validated {len(data['cues'])} cues and {len(data['subtitles'])} subtitles")


if __name__ == "__main__":
    main()
