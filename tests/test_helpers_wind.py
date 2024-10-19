import pytest

from barra2_dl import helpers_wind


@pytest.mark.parametrize(('u', 'v', 'expected'), [
    (1, 1, 1.4142135623730951),
    (-1, -1, 1.4142135623730951),
    (1., 1., 1.4142135623730951),
    (-1., -1., 1.4142135623730951),
    (0, 0, 0),
    (0., 0., 0.),
])
def test_calculate_wind_speed(u: float, v: float, expected: float) -> None:
    """Example test with parametrization."""
    assert helpers_wind.calculate_wind_speed(u, v) == expected
