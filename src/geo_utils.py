# !/usr/bin/python3
# -*- coding: utf-8 -*-
# @Project : practice
# @FileName : geo_utils.py
# @Author : convexwf@gmail.com
# @CreateDate : 2023-10-17 15:04
# @UpdateTime : TODO

from typing import Tuple
import math

# Length of the semi-major axis of the ellipsoid(earth), measured in meters.
EARTH_SEMI_MAJOR_AXIS = 6378245.0

# Flattening of the ellipsoid(earth), a dimensionless quantity.
EARTH_ECCENTRICITY_SQUARE = 0.00669342162296594323

def _transformlat(lng, lat):
    ret = -100.0 + 2.0 * lng + 3.0 * lat + 0.2 * lat * lat + \
          0.1 * lng * lat + 0.2 * math.sqrt(math.fabs(lng))
    ret += (20.0 * math.sin(6.0 * lng * math.pi) + 20.0 *
            math.sin(2.0 * lng * math.pi)) * 2.0 / 3.0
    ret += (20.0 * math.sin(lat * math.pi) + 40.0 *
            math.sin(lat / 3.0 * math.pi)) * 2.0 / 3.0
    ret += (160.0 * math.sin(lat / 12.0 * math.pi) + 320 *
            math.sin(lat * math.pi / 30.0)) * 2.0 / 3.0
    return ret


def _transformlng(lng, lat):
    ret = 300.0 + lng + 2.0 * lat + 0.1 * lng * lng + \
          0.1 * lng * lat + 0.1 * math.sqrt(math.fabs(lng))
    ret += (20.0 * math.sin(6.0 * lng * math.pi) + 20.0 *
            math.sin(2.0 * lng * math.pi)) * 2.0 / 3.0
    ret += (20.0 * math.sin(lng * math.pi) + 40.0 *
            math.sin(lng / 3.0 * math.pi)) * 2.0 / 3.0
    ret += (150.0 * math.sin(lng / 12.0 * math.pi) + 300.0 *
            math.sin(lng / 30.0 * math.pi)) * 2.0 / 3.0
    return ret

def is_out_of_china(latitude: float, longitude: float) -> bool:
    """Check if the coordinate is out of China. WGS-84 coordinate is used.

    Args:
        latitude (float)
        longitude (float)

    Returns:
        bool: True if the coordinate is out of China, False otherwise.
    """
    return not (73.66 < longitude < 135.05 and 3.86 < latitude < 53.55)

def GCJ02_to_WGS84(latitude: float, longitude:float) -> Tuple[float, float]:
    """Convert GCJ-02 coordinate to WGS-84 coordinate.

    Args:
        latitude (float)
        longitude (float)

    Returns:
        Tuple[float, float]: WGS-84 coordinate as (latitude, longitude)
    """

    dlat = _transformlat(longitude - 105.0, latitude - 35.0)
    dlng = _transformlng(longitude - 105.0, latitude - 35.0)
    radlat = latitude / 180.0 * math.pi
    magic = math.sin(radlat)
    magic = 1 - EARTH_ECCENTRICITY_SQUARE * magic * magic
    sqrtmagic = math.sqrt(magic)
    dlat = (dlat * 180.0) / ((EARTH_SEMI_MAJOR_AXIS * (1 - EARTH_ECCENTRICITY_SQUARE)) / (magic * sqrtmagic) * math.pi)
    dlng = (dlng * 180.0) / (EARTH_SEMI_MAJOR_AXIS / sqrtmagic * math.cos(radlat) * math.pi)
    mglat = latitude + dlat
    mglng = longitude + dlng
    return [latitude * 2 - mglat, longitude * 2 - mglng]

def WGS84_to_GCJ02(latitude: float, longitude:float) -> Tuple[float, float]:
    """Convert WGS-84 coordinate to GCJ-02 coordinate.

    Args:
        latitude (float)
        longitude (float)

    Returns:
        Tuple[float, float]: GCJ-02 coordinate as (latitude, longitude)
    """
    dlat = _transformlat(longitude - 105.0, latitude - 35.0)
    dlng = _transformlng(longitude - 105.0, latitude - 35.0)
    radlat = latitude / 180.0 * math.pi
    magic = math.sin(radlat)
    magic = 1 - EARTH_ECCENTRICITY_SQUARE * magic * magic
    sqrtmagic = math.sqrt(magic)
    dlat = (dlat * 180.0) / ((EARTH_SEMI_MAJOR_AXIS * (1 - EARTH_ECCENTRICITY_SQUARE)) / (magic * sqrtmagic) * math.pi)
    dlng = (dlng * 180.0) / (EARTH_SEMI_MAJOR_AXIS / sqrtmagic * math.cos(radlat) * math.pi)
    mglat = latitude + dlat
    mglng = longitude + dlng
    return [mglat, mglng]
