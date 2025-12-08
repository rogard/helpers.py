# helpers.py

Collection of helper python scripts.

## [censor.py](../py/censor.py)

Process a file by replacing text between `<censor>` anchors.

Usage:
```
censor --input_path name.unsafe.tex \
  --language tex \
  --comment_symbol "%" \
  --search_begin "<censor>" \
  --search_end "</censor>" \
  --strip-infix ".unsafe"
```

## [ics2json.py](../py/ics2json.py)

Convert an iCalendar (`.ics`) file to JSON; similar to [`ical2json`](https://github.com/philippbosch/ical2json/blob/master/README.md), except it does not rely on a port.

Usage:
```bash
python ics2json.py --url <url/to/ics> --output calendar.json
python ics2json.py --file <path/to/file.ics> --output calendar.json
```

In [Google calendar](https://calendar.google.com), `<ics_url>` is under `Settings>Integrate calendar`.
