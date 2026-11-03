from app import addition

def test_addition():
    assert addition(2, 3) == 5

def test_addition_negatifs():
    assert addition(-1, -1) == -2
