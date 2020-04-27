"""
Routines to work with dump files generated by OCaml core.
"""
import os
import logging
from dataclasses import dataclass
from typing import List
import ijson

from .ast import Scheme


log = logging.getLogger('plugins')
log.setLevel(logging.DEBUG)


@dataclass
class PluginWarning:
    """Inspection message generated by Python plugin."""
    msg: str


def run_all_inspections(scheme: Scheme) -> List[PluginWarning]:
    """Run all inspections implemented as Python plugins."""
    return []


def process_dump(dump_path: str) -> List[PluginWarning]:
    warnings = []

    scheme = None
    with open(dump_path, 'rb') as f:
        for item in ijson.items(f, ""):
            scheme = Scheme.from_dict(item)

    if not scheme:
        log.error(f'Can\'t extract dump scheme from {dump_path}!')
        return []

    warnings = run_all_inspections(scheme)

    return warnings


def remove_dump(dump_path: str):
    """Remove processed dump file."""
    try:
        os.remove(dump_path)
    except OSError as e:
        log.error(f'Can\'t remove {dump_path}: {str(e)}')
