import pytest
from axolpy.aws import (AWSRegion, ECSCluster, ECSService, RDSDatabase,
                        RDSDatabasePatch)


class TestAWSRegionModel(object):
    def test_aws_region(self):
        """
        Test using AWSRegion.
        """

        region_name = "us-east-1"

        region = AWSRegion(name=region_name)
        pytest.test_aws_region_model_region: AWSRegion = region

        assert region.name == region_name
        assert region.eks_clusters == {}
        assert region.ecs_clusters == {}

        assert str(
            region) == f"{region.__class__.__name__}(name: {region_name}" + \
            f", 0 EKS clusters, 0 ECS clusters, 0 RDS Databases)"

    def test_ecs_cluster(self):
        """
        Test using ECSCluster.
        """

        region: AWSRegion = pytest.test_aws_region_model_region
        cluster_name = "test-cluster"

        cluster = ECSCluster(name=cluster_name, region=region)
        pytest.test_aws_region_model_ecs_cluster: ECSCluster = cluster

        actual_cluster = region.ecs_cluster(name=cluster_name)

        assert actual_cluster.name == cluster_name
        assert actual_cluster.region.name == region.name
        assert actual_cluster.services == {}

        assert str(
            actual_cluster) == f"{actual_cluster.__class__.__name__}(name: {cluster_name}, 0 services)"
        assert str(
            region) == f"{region.__class__.__name__}(name: {region.name}" + \
            f", 0 EKS clusters, 1 ECS clusters, 0 RDS Databases)"

    def test_ecs_service(self):
        """
        Test using ECSService.
        """

        cluster: ECSCluster = pytest.test_aws_region_model_ecs_cluster
        service_name = "test-service"
        desired_count = 5

        service = ECSService(
            name=service_name,
            cluster=cluster,
            desired_count=desired_count,
            foo="bar")
        service.add_property(name="priority", value=2)

        actual_service = cluster.service(name=service_name)

        assert actual_service.name == service_name
        assert actual_service.cluster == cluster
        assert actual_service.desired_count == desired_count
        assert actual_service.property("foo") == "bar"
        assert actual_service.property("priority") == 2

        assert str(
            actual_service) == f"{service.__class__.__name__}(name: {service_name}, desired_count: {desired_count}, 2 properties)"
        assert str(
            cluster) == f"{cluster.__class__.__name__}(name: {cluster.name}, 1 services)"


def test_rds_database():
    """
    Test using RDSDatabase.
    """

    region_name = "us-east-1"
    id = "test-rds"
    db_type = "instance"
    host = "test-host.amazonaws.com"
    port = 5432
    engine_type = "postgresql"
    engine_version = "9.6.3"
    class_type = "db.t2.micro"
    dbname = "test-db"

    region = AWSRegion(name=region_name)
    db = RDSDatabase(id=id,
                     region=region,
                     type=db_type,
                     host=host,
                     port=port,
                     engine_type=engine_type,
                     engine_version=engine_version,
                     class_type=class_type,
                     dbname=dbname)

    assert db.id == id
    assert db.region.name == region_name
    assert db.type == db_type
    assert db.host == host
    assert db.port == port
    assert db.engine_type == engine_type
    assert db.engine_version == engine_version
    assert db.class_type == class_type
    assert db.dbname == dbname
    assert db.is_postgresql() is True
    assert db.is_mysql() is False
    assert str(db) == f"{db.__class__.__name__}(id: {id}, type: {db_type}" + \
        f", host: {host}, port: {port}, engine_type: {engine_type}" + \
        f", engine_version: {engine_version}, class_type: {class_type}, dbname: {dbname})"

    assert len(region.rds_databases) == 1
    assert region.rds_database(id=id) == db


def test_rds_database_patch_model():
    """
    Test rds_database patch model.
    """

    patch_engine_version = "9.6.3"
    patch_class_type = "db.t2.micro"

    patch = RDSDatabasePatch(
        engine_version=patch_engine_version,
        class_type=patch_class_type)

    assert patch.engine_version == patch_engine_version
    assert patch.class_type == patch_class_type
    assert str(patch) == f"{patch.__class__.__name__}" + \
        f"(engine_version: {patch_engine_version}, class_type: {patch_class_type})"

    db = RDSDatabase(id="test-rds",
                     region=AWSRegion(name="us-east-1"),
                     type="instance",
                     host="test-host.amazonaws.com",
                     port=5432,
                     engine_type="postgresql",
                     engine_version="9.6.3",
                     class_type="db.t2.micro",
                     dbname="test-db")

    db.patch = patch

    assert db.patch.engine_version == patch_engine_version
    assert db.patch.class_type == patch_class_type
