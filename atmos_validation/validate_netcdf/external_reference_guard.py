"""Reject HDF5/NetCDF files that reference storage outside themselves.

HDF5 external storage, external links and virtual datasets make a variable's
bytes resolve from a separate, file-embedded path only when the data is *read*.
Inspecting metadata does not dereference them, so untrusted files can be
screened and rejected before anything is opened through xarray/h5py.
"""

from typing import List, Set

import h5py
import h5py.h5o as h5o


class ExternalReferenceError(Exception):
    """Raised when a file points at storage outside itself."""


def assert_no_external_references(paths: List[str]) -> None:
    """Raise ExternalReferenceError if any file uses external storage, an
    external link or a virtual dataset. Only metadata is read, never data."""
    for path in paths:
        with h5py.File(path, "r") as file:
            findings: List[str] = []
            _scan_group(file, findings, set())
            if findings:
                raise ExternalReferenceError(
                    f"Refusing to open {path}: it references storage outside the file "
                    f"({'; '.join(findings)}). External storage, external links and "
                    "virtual datasets are not permitted."
                )


def _scan_group(group: h5py.Group, findings: List[str], visited: Set[int]) -> None:
    for key in group.keys():
        # Inspect the link itself first so external links are never dereferenced.
        link = group.get(key, getlink=True)
        if isinstance(link, h5py.ExternalLink):
            parent = (group.name or "").rstrip("/")
            findings.append(f"external link '{parent}/{key}' -> {link.filename}")
            continue
        if isinstance(link, h5py.SoftLink):
            # Stays within the file; its hard-linked target is scanned on its own.
            continue

        item = group[key]
        addr = h5o.get_info(item.id).addr
        if addr in visited:  # guard against cyclic hard links
            continue
        visited.add(addr)

        if isinstance(item, h5py.Group):
            _scan_group(item, findings, visited)
        elif isinstance(item, h5py.Dataset):
            _scan_dataset(item, findings)


def _scan_dataset(dataset: h5py.Dataset, findings: List[str]) -> None:
    if dataset.is_virtual:
        findings.append(f"virtual dataset '{dataset.name}'")
    if dataset.id.get_create_plist().get_external_count() > 0:
        findings.append(f"external storage '{dataset.name}'")
