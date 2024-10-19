"""
Helper functions for wind calculations.
# todo add tests
"""

from typing import List
import numpy as np


def calculate_wind_speed(u: float | int, v: float | int) -> float:
    """
    Calculate the wind speed from u and v components.
    Args:
        u (float | int): The u component of the wind vector.
        v (float | int): The v component of the wind vector.
    Returns:
        Wind speed. If both u and v are zero, it returns 0.0.
    """
    if u == 0 and v == 0:
        return 0.0
    return np.sqrt(u ** 2 + v ** 2)


def wind_components_to_speed(ua: float | int | list[float | int], va: float | int | list[float | int]) -> float | list[float]:
    """
    Convert wind components ua and va to wind speed v.
    Args:
        ua (float | int | list[float | int]): The u-component of the wind.
        va (float | int | list[float | int]): The v-component of the wind.
    Returns:
        The calculated wind speed.
    Raises:
        ValueError: If the input types do not match or if they are neither list[float] nor list[int] nor float.
    """
    if isinstance(ua, (float, int)) and isinstance(va, (float, int)):
        if ua == 0 and va == 0:
            return 0.0
        return calculate_wind_speed(ua, va)
    elif isinstance(ua, list) and isinstance(va, list):
        if not all(isinstance(num, (float, int)) for num in ua + va):
            raise ValueError("All elements in both lists must be either float or int.")
        if len(ua) != len(va):
            raise ValueError("Both lists must be of the same length.")
        return [calculate_wind_speed(u, v) for u, v in zip(ua, va)]
    else:
        raise ValueError("Both arguments must be either both float/int or both lists of float/int.")


# todo add tests
def calculate_wind_direction(u: float | int, v: float | int) -> float:
    """
    Args:
        u (float | int): The u component of the wind vector, which can be a float or an int.
        v (float | int): The v component of the wind vector, which can be a float or an int.
    Returns:
        Calculated wind direction in degrees. If both u and v are zero, it returns 0.0.
    """
    if u == 0 and v == 0:
        return 0.0
    return np.mod(180 + np.rad2deg(np.arctan2(u, v)), 360)


def wind_components_to_direction(ua: float | int | List[float | int], va: float | int | List[float | int]) -> float | List[float]:
    """
    Convert wind components ua and va to wind direction phi.
    Args:
        ua (float | int | List[float | int]): The u-component of the wind.
        va (float | int | List[float | int]): The v-component of the wind.
    Returns:
        The calculated wind speed direction.
    Raises:
        ValueError: If the input types and incorrect or do not match or if lists of different lengths are provided.
    """

    if isinstance(ua, (float, int)) and isinstance(va, (float, int)):
        return calculate_wind_direction(ua, va)
    elif isinstance(ua, list) and isinstance(va, list):
        if not all(isinstance(num, (float, int)) for num in ua + va):
            raise ValueError("All elements in both lists must be either float or int.")
        if len(ua) != len(va):
            raise ValueError("Both lists must be of the same length.")
        return [calculate_wind_direction(u, v) for u, v in zip(ua, va)]
    else:
        raise ValueError("Both arguments must be either both float/int or both lists of float/int.")
