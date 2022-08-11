from pathlib import Path
from typing import List, Type, TypeVar

import pytest
from axolpy.cloudmaintenance import Operator, ResourceDataLoader
from axolpy.cloudmaintenance.steps import (CloudMaintenanceStep,
                                           DumpMysqlTableStatus, DumpPgstats,
                                           ModifyDatabaseClassType,
                                           ModifyDatabaseEngineVersion,
                                           QueryDatabaseStatus,
                                           QueryECSTaskStatus,
                                           QueryK8sDeploymentStatus,
                                           RestartK8sDeployment,
                                           UpdateECSTaskCount,
                                           UpdateK8sDeploymentReplicas,
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


S = TypeVar('S', bound=CloudMaintenanceStep)


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

    def _test_cloud_maintenance_step(self,
                                     step_no: int,
                                     cloud_maintenance_step_class: Type[S],
                                     operators,
                                     zeroinfy: bool = False,
                                     expect_filenames: List[str] = list()) -> None:
        """
        Test the cloud maintenance step.

        :param step_no: The step number.
        :type step_no: int
        :param cloud_maintenance_step_class: The class of the cloud maintenance step.
        :type cloud_maintenance_step_class: :class:`Type[S]`
        :param operators: A dictionary of Operators.
        :type operators: Dict[:class:`Operator`]
        :param zeroinfy: Whether to zeroinfy the count/replicas.
        :type zeroinfy: bool
        :param expect_filenames: The filenames of the expected files.
        :type expect_filenames: List[str]
        """

        for i in range(3):
            id = f"operator{i+1}"
            operator = operators[id]

            args = {"step_no": step_no,
                    "operator": operator,
                    "dist_path": self._dist_path}
            if zeroinfy:
                args["zeroinfy"] = True
            cloud_maintenance_step = cloud_maintenance_step_class(**args)
            cloud_maintenance_step.write_file()

        for filename in expect_filenames:
            filepath = Path(self._dist_path, filename)
            assert filepath.exists()
            assert filepath.is_file()

            # Verify that the file content is the same as file in dist-verify
            filepath_verify = Path(self._dist_verify_path, filename)
            with filepath.open() as f:
                with filepath_verify.open() as f_verify:
                    assert f.read() == f_verify.read()

    def test_update_ecs_task_count_zero(self, operators) -> None:
        """
        Test the update ECS task count step with zeroinfy=True.

        :param operators: A dictionary of Operators.
        :type operators: Dict[:class:`Operator`]
        """

        expect_filenames = ["operator1-0-update-ecs-task-count-ZERO.sh",
                            "operator2-0-update-ecs-task-count-ZERO.sh"]

        self._test_cloud_maintenance_step(
            step_no=0,
            cloud_maintenance_step_class=UpdateECSTaskCount,
            operators=operators,
            zeroinfy=True,
            expect_filenames=expect_filenames)

    def test_update_ecs_task_count_resume(self, operators) -> None:
        """
        Test the update ECS task count step with zeroinfy=False.

        :param operators: A dictionary of Operators.
        :type operators: Dict[:class:`Operator`]
        """

        expect_filenames = ["operator1-1-update-ecs-task-count-RESUME.sh",
                            "operator2-1-update-ecs-task-count-RESUME.sh"]

        self._test_cloud_maintenance_step(
            step_no=1,
            cloud_maintenance_step_class=UpdateECSTaskCount,
            operators=operators,
            expect_filenames=expect_filenames)

    def test_update_k8s_statefulset_replicas_zero(self, operators) -> None:
        """
        Test the update k8s statefulset replicas step with zeroinfy=True.

        :param operators: A dictionary of Operators.
        :type operators: Dict[:class:`Operator`]
        """

        expect_filenames = ["operator1-0-update-k8s-statefulset-replicas-ZERO.sh",
                            "operator3-0-update-k8s-statefulset-replicas-ZERO.sh"]

        self._test_cloud_maintenance_step(
            step_no=0,
            cloud_maintenance_step_class=UpdateK8sStatefulSetReplicas,
            operators=operators,
            zeroinfy=True,
            expect_filenames=expect_filenames)

    def test_update_k8s_statefulset_replicas_resume(self, operators) -> None:
        """
        Test the update k8s statefulset replicas step with zeroinfy=False.

        :param operators: A dictionary of Operators.
        :type operators: Dict[:class:`Operator`]
        """

        expect_filenames = ["operator1-1-update-k8s-statefulset-replicas-RESUME.sh",
                            "operator3-1-update-k8s-statefulset-replicas-RESUME.sh"]

        self._test_cloud_maintenance_step(
            step_no=1,
            cloud_maintenance_step_class=UpdateK8sStatefulSetReplicas,
            operators=operators,
            expect_filenames=expect_filenames)

    def test_update_k8s_deployment_replicas_zero(self, operators) -> None:
        """
        Test the update k8s deployment replicas step with zeroinfy=True.

        :param operators: A dictionary of Operators.
        :type operators: Dict[:class:`Operator`]
        """

        expect_filenames = ["operator1-0-change-k8s-deployment-replicas-ZERO.sh",
                            "operator3-0-change-k8s-deployment-replicas-ZERO.sh"]

        self._test_cloud_maintenance_step(
            step_no=0,
            cloud_maintenance_step_class=UpdateK8sDeploymentReplicas,
            operators=operators,
            zeroinfy=True,
            expect_filenames=expect_filenames)

    def test_update_k8s_deployment_replicas_resume(self, operators) -> None:
        """
        Test the update k8s deployment replicas step with zeroinfy=False.

        :param operators: A dictionary of Operators.
        :type operators: Dict[:class:`Operator`]
        """

        expect_filenames = ["operator1-1-change-k8s-deployment-replicas-RESUME.sh",
                            "operator3-1-change-k8s-deployment-replicas-RESUME.sh"]

        self._test_cloud_maintenance_step(
            step_no=1,
            cloud_maintenance_step_class=UpdateK8sDeploymentReplicas,
            operators=operators,
            expect_filenames=expect_filenames)

    def test_dump_pg_stats(self, operators) -> None:
        """
        Test the dump pg stats step.

        :param operators: A dictionary of Operators.
        :type operators: Dict[:class:`Operator`]
        """

        expect_filenames = ["operator1-0-dump-pgstats.sh",
                            "operator2-0-dump-pgstats.sh"]

        self._test_cloud_maintenance_step(
            step_no=0,
            cloud_maintenance_step_class=DumpPgstats,
            operators=operators,
            expect_filenames=expect_filenames)

    def test_dump_mysql_table_status(self, operators) -> None:
        """
        Test the dump mysql table status step.

        :param operators: A dictionary of Operators.
        :type operators: Dict[:class:`Operator`]
        """

        expect_filenames = ["operator1-0-dump-mysqltablestatus.sh"]

        self._test_cloud_maintenance_step(
            step_no=0,
            cloud_maintenance_step_class=DumpMysqlTableStatus,
            operators=operators,
            expect_filenames=expect_filenames)

    def test_modify_database_engine_version(self, operators) -> None:
        """
        Test the modify database engine version step.

        :param operators: A dictionary of Operators.
        :type operators: Dict[:class:`Operator`]
        """

        expect_filenames = ["operator1-0-modify-database-engineversion.sh",
                            "operator2-0-modify-database-engineversion.sh"]

        self._test_cloud_maintenance_step(
            step_no=0,
            cloud_maintenance_step_class=ModifyDatabaseEngineVersion,
            operators=operators,
            expect_filenames=expect_filenames)

    def test_modify_database_class_type(self, operators) -> None:
        """
        Test the modify database class type step.

        :param operators: A dictionary of Operators.
        :type operators: Dict[:class:`Operator`]
        """

        expect_filenames = ["operator1-0-modify-database-classtype.sh",
                            "operator2-0-modify-database-classtype.sh"]

        self._test_cloud_maintenance_step(
            step_no=0,
            cloud_maintenance_step_class=ModifyDatabaseClassType,
            operators=operators,
            expect_filenames=expect_filenames)

    def test_query_database_status(self, operators) -> None:
        """
        Test the query database status step.

        :param operators: A dictionary of Operators.
        :type operators: Dict[:class:`Operator`]
        """

        expect_filenames = ["operator1-0-query-database-status.sh",
                            "operator2-0-query-database-status.sh"]

        self._test_cloud_maintenance_step(
            step_no=0,
            cloud_maintenance_step_class=QueryDatabaseStatus,
            operators=operators,
            expect_filenames=expect_filenames)

    def test_restart_k8s_deployment(self, operators) -> None:
        """
        Test the restart k8s deployment step.

        :param operators: A dictionary of Operators.
        :type operators: Dict[:class:`Operator`]
        """

        expect_filenames = ["operator2-0-restart-k8s-deployment.sh",
                            "operator3-0-restart-k8s-deployment.sh"]

        self._test_cloud_maintenance_step(
            step_no=0,
            cloud_maintenance_step_class=RestartK8sDeployment,
            operators=operators,
            expect_filenames=expect_filenames)

    def test_query_k8s_deployment_status(self, operators) -> None:
        """
        Test the query k8s deployment status step.

        :param operators: A dictionary of Operators.
        :type operators: Dict[:class:`Operator`]
        """

        expect_filenames = ["operator1-0-query-k8s-deployment-status.sh",
                            "operator2-0-query-k8s-deployment-status.sh",
                            "operator3-0-query-k8s-deployment-status.sh"]

        self._test_cloud_maintenance_step(
            step_no=0,
            cloud_maintenance_step_class=QueryK8sDeploymentStatus,
            operators=operators,
            expect_filenames=expect_filenames)

    def test_query_ecs_task_status(self, operators) -> None:
        """
        Test the query ecs task status step.

        :param operators: A dictionary of Operators.
        :type operators: Dict[:class:`Operator`]
        """

        expect_filenames = ["operator1-0-query-ecs-task-status.sh",
                            "operator2-0-query-ecs-task-status.sh"]

        self._test_cloud_maintenance_step(
            step_no=0,
            cloud_maintenance_step_class=QueryECSTaskStatus,
            operators=operators,
            expect_filenames=expect_filenames)
