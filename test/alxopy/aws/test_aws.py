from axolpy.aws import EKSDeployment, EKSStatefulSet


def test_eks_deployment():
    d = EKSDeployment(name="test", replicas=1, foo="bar")
    d.add_property(name="priority", value=2)

    assert d.name == "test"
    assert d.replicas == 1
    assert d.property("foo") == "bar"
    assert d.property("priority") == 2
    assert str(d) == "EKSDeployment(name: test, replicas: 1, 2 properties)"


def test_eks_statefulset():
    d = EKSStatefulSet(name="test", replicas=1, foo="bar")
    d.add_property(name="priority", value=2)

    assert d.name == "test"
    assert d.replicas == 1
    assert d.property("foo") == "bar"
    assert d.property("priority") == 2
    assert str(d) == "EKSStatefulSet(name: test, replicas: 1, 2 properties)"
