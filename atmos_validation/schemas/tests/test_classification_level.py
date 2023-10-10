from .. import ClassificationLevel


def test_ordered_enum():
    assert ClassificationLevel.OPEN >= ClassificationLevel.OPEN
    assert ClassificationLevel.INTERNAL > ClassificationLevel.OPEN
    assert ClassificationLevel.RESTRICTED >= ClassificationLevel.INTERNAL
    assert ClassificationLevel.INTERNAL < ClassificationLevel.RESTRICTED
    assert ClassificationLevel.RESTRICTED <= ClassificationLevel.RESTRICTED
