from typing import List, Tuple

from ...utils import Severity, validation_node


@validation_node(severity=Severity.ERROR)
def vardims_validator(
    key: str, actual: Tuple[str, ...], expected: List[str]
) -> List[str]:
    """
    Verify dimensions are as expected (correct names, correct number, correct sequence) as
    compared to the configuration for this variable. This is opposed to the dimvar check which
    simply checks if the dims constitute valid dimensions. An admin user can then choose whether"
    " to change the configuration if the dims are otherwise valid. Note that this entails going through all
    other datasets and adjusting those dimensions, so it is recommended to proceed with caution in that case
    """
    actual_dims = str(list(actual))
    expected_dims = str(expected)
    result = []
    if actual_dims != expected_dims:
        result += [
            f"{key}:Dimensions for variable do not "
            "match expected dimensions from configuration"
            f" {actual_dims}!={expected_dims}"
        ]
    return result
