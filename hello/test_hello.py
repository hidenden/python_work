from hello import main, world
from hello import hello
from hello import multi_string

def test_world():
    w1 = world(1)
    assert w1 == "World "
    w3 = world(3)
    assert w3 == "World World World "

def test_hello():
    h1 = hello(1)
    assert h1 == "Hello "
    h3 = hello(3)
    assert h3 == "Hello Hello Hello "

def test_main():
    m1 = main()
    assert m1 == "Hello Hello Hello World World World "

