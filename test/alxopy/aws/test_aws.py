from axolpy.aws import EKSDeployment


def test_eksdeployment():
    d = EKSDeployment(name="test", replicas=1, foo="bar")
    d.add_property(name="priority", value=2)

    assert d.name == "test"
    assert d.replicas == 1
    assert d.property("foo") == "bar"
    assert d.property("priority") == 2
    assert str(d) == "EKSDeployment(name: test, replicas: 1, 2 properties)"
