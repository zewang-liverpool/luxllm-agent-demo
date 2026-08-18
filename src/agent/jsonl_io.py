"""Small cross-process-safe helpers for append-only JSONL evidence logs."""

from __future__ import annotations

import json
import os
import time
from typing import Dict


def _lock_descriptor(descriptor: int) -> None:
    if os.name == "nt":
        import msvcrt

        os.lseek(descriptor, 0, os.SEEK_SET)
        while True:
            try:
                msvcrt.locking(descriptor, msvcrt.LK_NBLCK, 1)
                return
            except OSError:
                time.sleep(0.005)


def _unlock_descriptor(descriptor: int) -> None:
    if os.name == "nt":
        import msvcrt

        os.lseek(descriptor, 0, os.SEEK_SET)
        msvcrt.locking(descriptor, msvcrt.LK_UNLCK, 1)


def append_jsonl_atomic(path: str, data: Dict) -> None:
    """Append one complete UTF-8 JSON record with a single OS write.

    A Lux match launches one process per player. Experiment runners isolate
    their player log directories on Linux/Barkla, where locks on the shared
    home filesystem are prohibitively slow. Windows retains a short file lock
    for legacy shared-log runs. In both cases a record uses one ``os.write``.
    """
    directory = os.path.dirname(path)
    if directory:
        os.makedirs(directory, exist_ok=True)
    payload = (json.dumps(data, ensure_ascii=False) + "\n").encode("utf-8")
    flags = os.O_APPEND | os.O_CREAT | os.O_WRONLY
    flags |= getattr(os, "O_BINARY", 0)
    descriptor = os.open(path, flags, 0o666)
    try:
        if os.name == "nt":
            _lock_descriptor(descriptor)
        written = os.write(descriptor, payload)
        if written != len(payload):
            raise OSError(
                f"Incomplete JSONL append to {path}: wrote {written} of {len(payload)} bytes"
            )
    finally:
        if os.name == "nt":
            try:
                _unlock_descriptor(descriptor)
            except OSError:
                pass
        os.close(descriptor)
