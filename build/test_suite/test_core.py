def test_core_startup():
    from core import main
    assert callable(main.main)