import h5py
import numpy as np
import pytest

from ..external_reference_guard import (
    ExternalReferenceError,
    assert_no_external_references,
)


def _write_units(dataset: h5py.Dataset) -> None:
    dataset.attrs["units"] = "microseconds since 1900-01-01"


def test_clean_file_passes(tmp_path):
    path = tmp_path / "clean.nc"
    with h5py.File(path, "w") as file:
        _write_units(file.create_dataset("Time", data=np.arange(10, dtype="int64")))

    assert_no_external_references([str(path)])


def test_external_storage_is_rejected(tmp_path):
    secret = tmp_path / "secret.bin"
    np.arange(10, dtype="int64").tofile(secret)
    path = tmp_path / "ext_storage.nc"
    with h5py.File(path, "w") as file:
        _write_units(
            file.create_dataset(
                "Time",
                shape=(10,),
                dtype="int64",
                external=[(str(secret), 0, h5py.h5f.UNLIMITED)],
            )
        )

    with pytest.raises(ExternalReferenceError, match="external storage"):
        assert_no_external_references([str(path)])


def test_external_link_is_rejected(tmp_path):
    target = tmp_path / "target.nc"
    with h5py.File(target, "w") as file:
        _write_units(file.create_dataset("Time", data=np.arange(10, dtype="int64")))
    path = tmp_path / "with_extlink.nc"
    with h5py.File(path, "w") as file:
        file["Time"] = h5py.ExternalLink(str(target), "Time")

    with pytest.raises(ExternalReferenceError, match="external link"):
        assert_no_external_references([str(path)])


def test_virtual_dataset_is_rejected(tmp_path):
    source = tmp_path / "source.nc"
    with h5py.File(source, "w") as file:
        file.create_dataset("Time", data=np.arange(10, dtype="int64"))
    path = tmp_path / "vds.nc"
    layout = h5py.VirtualLayout(shape=(10,), dtype="int64")
    layout[:] = h5py.VirtualSource(str(source), "Time", shape=(10,))
    with h5py.File(path, "w") as file:
        _write_units(file.create_virtual_dataset("Time", layout))

    with pytest.raises(ExternalReferenceError, match="virtual dataset"):
        assert_no_external_references([str(path)])
