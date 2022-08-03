from pathlib import Path

import pytest
from axolpy.cloudmaintenance import Operator, ResourceDataLoader
from axolpy.cloudmaintenance.steps import UpdateECSTaskCount


@pytest.fixture
def aws_regions():
    """
    Fixture for some AWS regions.

    :return: A dictionary of AWSRegions.
    :rtype: Dict[str, :class:`AWSRegion`]
    """

    return ResourceDataLoader.load_from_file(
        data_path=Path(__file__).parent.joinpath("testdata"),
        maintenance_id="maintenance")


@pytest.fixture
def operators(aws_regions):
    """
    Generate some Operators by reading from the test data.

    :param aws_regions: Data of all regions.
    :type aws_regions: Dict[str, :class:`AWSRegion`]

    :return: A dictionary of Operators.
    :rtype: Dict[:class:`Operator`]
    """

    operators = dict()
    for i in range(3):
        id = f"operator{i+1}"
        operator = Operator(id=id)
        operator.data_loader.load_from_file(
            data_path=Path(__file__).parent.joinpath("testdata"),
            maintenance_id="maintenance",
            aws_regions=aws_regions)
        operators[id] = operator

    return operators


def test_update_ecs_task_count(operators) -> None:
    dist_path = Path(__file__).parent.joinpath(
        "testdata",
        "maintenance",
        "dist")
    dist_verify_path = Path(__file__).parent.joinpath(
        "testdata",
        "maintenance",
        "dist-verify")

    for i in range(3):
        id = f"operator{i+1}"
        operator = operators[id]

        update_ecs_task_count_zero = UpdateECSTaskCount(
            step_no=0,
            operator=operator,
            dist_path=dist_path,
            zeroinfy=True)
        update_ecs_task_count_zero.write_file()

    expect_filenames = ["operator1-0-update-ecs-task-count-ZERO.sh",
                        "operator2-0-update-ecs-task-count-ZERO.sh"]

    for filename in expect_filenames:
        filepath = Path(dist_path, filename)
        assert filepath.exists()
        assert filepath.is_file()

        # Verify that the file content is the same as file in dist-verify
        filepath_verify = Path(dist_verify_path, filename)
        with filepath.open() as f:
            with filepath_verify.open() as f_verify:
                assert f.read() == f_verify.read()
