from pathlib import Path
from typing import Dict, List

import pytest
from axolpy.cloudmaintenance import Operator, ResourceDataLoader
from axolpy.cloudmaintenance.steps import (UpdateECSTaskCount,
                                           UpdateK8sStatefulSetReplicas)


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


class TestCloudMaintenanceStep(object):
    """
    Test the cloud maintenance steps.
    """

    _dist_path = Path(__file__).parent.joinpath(
        "testdata",
        "maintenance",
        "dist")
    _dist_verify_path = Path(__file__).parent.joinpath(
        "testdata",
        "maintenance",
        "dist-verify")

    def test_update_ecs_task_count_zero(self, operators) -> None:
        """
        Test the update ECS task count step with zeroinfy=True.

        :param operators: A dictionary of Operators.
        :type operators: Dict[:class:`Operator`]
        """

        expect_filenames = ["operator1-0-update-ecs-task-count-ZERO.sh",
                            "operator2-0-update-ecs-task-count-ZERO.sh"]

        self._test_update_ecs_task_count(
            operators=operators,
            zeroinfy=True,
            expect_filenames=expect_filenames)

    def _test_update_ecs_task_count(
            self,
            operators,
            zeroinfy: bool = False,
            expect_filenames: List[str] = list()) -> None:
        """
        Test the update ECS task count step.

        :param operators: A dictionary of Operators.
        :type operators: Dict[:class:`Operator`]
        :param zeroinfy: Whether to zeroinfy the task count.
        :type zeroinfy: bool
        :param expect_filenames: The filenames of the expected files.
        :type expect_filenames: List[str]
        """

        for i in range(3):
            id = f"operator{i+1}"
            operator = operators[id]

            update_ecs_task_count_zero = UpdateECSTaskCount(
                step_no=0,
                operator=operator,
                dist_path=self._dist_path,
                zeroinfy=True)
            update_ecs_task_count_zero.write_file()

        for filename in expect_filenames:
            filepath = Path(self._dist_path, filename)
            assert filepath.exists()
            assert filepath.is_file()

            # Verify that the file content is the same as file in dist-verify
            filepath_verify = Path(self._dist_verify_path, filename)
            with filepath.open() as f:
                with filepath_verify.open() as f_verify:
                    assert f.read() == f_verify.read()

    def test_update_k8s_statefulset_replicas_zero(self, operators) -> None:
        """
        Test the update k8s statefulset replicas step with zeroinfy=True.

        :param operators: A dictionary of Operators.
        :type operators: Dict[:class:`Operator`]
        """

        expect_filenames = ["operator1-0-update-k8s-statefulset-replicas-ZERO.sh",
                            "operator3-0-update-k8s-statefulset-replicas-ZERO.sh"]

        self._test_update_k8s_statefulset_replicas(
            operators=operators,
            zeroinfy=True,
            expect_filenames=expect_filenames)

    def _test_update_k8s_statefulset_replicas(
            self,
            operators,
            zeroinfy: bool = False,
            expect_filenames: List[str] = list()) -> None:
        """
        Test the update k8s statefulset replicas step.

        :param operators: A dictionary of Operators.
        :type operators: Dict[:class:`Operator`]
        :param zeroinfy: Whether to zeroinfy the task count.
        :type zeroinfy: bool
        :param expect_filenames: The filenames of the expected files.
        :type expect_filenames: List[str]
        """

        for i in range(3):
            id = f"operator{i+1}"
            operator = operators[id]

            update_k8s_statefulset_replicas = UpdateK8sStatefulSetReplicas(
                step_no=0,
                operator=operator,
                dist_path=self._dist_path,
                zeroinfy=zeroinfy)
            update_k8s_statefulset_replicas.write_file()

        for filename in expect_filenames:
            filepath = Path(self._dist_path, filename)
            assert filepath.exists()
            assert filepath.is_file()

            # Verify that the file content is the same as file in dist-verify
            filepath_verify = Path(self._dist_verify_path, filename)
            with filepath.open() as f:
                with filepath_verify.open() as f_verify:
                    assert f.read() == f_verify.read()
