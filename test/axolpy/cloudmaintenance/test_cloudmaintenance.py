from axolpy.aws import AWSRegion, ECSCluster, ECSService, RDSDatabase
from axolpy.cloudmaintenance import Operator
from axolpy.kubernetes import Cluster, Deployment, Namespace, StatefulSet


def test_operator() -> None:
    operator = Operator("kobe")
    assert operator.id == "kobe"

    eks_cluster = Cluster(name="allinone")
    namespace = Namespace(name="general", cluster=eks_cluster)
    operator.add_eks_deployment(
        deployment=Deployment(
            name="simple-deployment",
            namespace=namespace,
            replicas=1))
    operator.add_eks_statefulset(
        statefulset=StatefulSet(
            name="simple-stateful-set",
            namespace=namespace,
            replicas=1))

    aws_region = AWSRegion(name="us-east-1")
    ecs_cluster = ECSCluster(name="allinone", region=aws_region)
    operator.add_ecs_service(
        service=ECSService(
            name="simple-service",
            cluster=ecs_cluster,
            desired_count=1))
    operator.add_rds_databases(
        database=RDSDatabase(
            id="simple-database",
            region=aws_region,
            type="instance",
            host="simple-database.us-east-1.rds.amazonaws.com",
            port=5432,
            engine_type="postgresql",
            engine_version="13.6",
            class_type="db.t2.micro"))

    assert len(operator.eks_deployments) == 1
    assert len(operator.eks_statefulsets) == 1
    assert len(operator.ecs_services) == 1
    assert len(operator.rds_databases) == 1
