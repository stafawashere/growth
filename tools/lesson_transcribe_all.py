"""Transcribe many lesson designs at once, each worker loading the snapshot a single time.

Takes design files or directories (every LSN-*.md directly inside a directory), writes each record
to content/lessons/<id>.json or to --out-dir, prints one line per design and a summary line, and
exits 1 when any design was refused. A refusal is the same one tools/lesson_transcribe.py gives.

Usage: python3 tools/lesson_transcribe_all.py [--workers N] [--out-dir DIR] <design.md | dir> ...
"""
import argparse
import sys
from multiprocessing import Pool
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from app.content.loader import load_snapshot
from tools.lesson_transcribe import CONTENT_LESSONS, DATA_ROOT, TranscriptionError, render, transcribe

DEFAULT_WORKERS = 8

worker_snapshot = None


def load_worker_snapshot(data_root):
   global worker_snapshot
   worker_snapshot = load_snapshot(Path(data_root))


def transcribe_one(job):
   design_path, out_dir = job

   try:
      lesson = transcribe(design_path, worker_snapshot)
   except TranscriptionError as error:
      return (design_path, None, str(error))
   except KeyError as error:
      return (design_path, None, f"the design lacks the field {error}")

   output = Path(out_dir) / f"{lesson['id']}.json"
   output.write_text(render(lesson))

   return (design_path, str(output), None)


def design_paths(arguments):
   paths = []

   for argument in arguments:
      path = Path(argument)

      if path.is_dir():
         paths.extend(sorted(path.glob("LSN-*.md")))
      else:
         paths.append(path)

   return [str(path) for path in paths]


def parse_arguments(argv):
   parser = argparse.ArgumentParser(prog="lesson_transcribe_all.py")
   parser.add_argument("paths", nargs="+")
   parser.add_argument("--workers", type=int, default=DEFAULT_WORKERS)
   parser.add_argument("--out-dir", default=str(CONTENT_LESSONS))

   return parser.parse_args(argv)


def main(argv, data_root=DATA_ROOT):
   arguments = parse_arguments(argv[1:])
   out_dir = Path(arguments.out_dir)
   out_dir.mkdir(parents=True, exist_ok=True)
   jobs = [(path, str(out_dir)) for path in design_paths(arguments.paths)]
   wrote = 0
   refused = 0

   with Pool(arguments.workers, initializer=load_worker_snapshot, initargs=(str(data_root),)) as pool:
      for design_path, output, reason in pool.imap(transcribe_one, jobs):
         if reason is None:
            wrote += 1
            print(f"wrote {output}")
         else:
            refused += 1
            print(f"refused {design_path}: {reason}")

   print(f"designs: {len(jobs)}, wrote: {wrote}, refused: {refused}")

   return 1 if refused else 0


if __name__ == "__main__":
   sys.exit(main(sys.argv))
