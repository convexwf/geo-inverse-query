# !/usr/bin/python3
# -*- coding: utf-8 -*-
# @Project : geo-inverse-query
# @FileName : extract_ok_geo.py
# @Author : convexwf@gmail.com
# @CreateDate : 2024-05-08 18:33
# @UpdateTime : 2024-10-18 22:40

import csv
import json
import os
from enum import Enum

from geo_utils import GCJ02_to_WGS84, WGS84_to_GCJ02

csv.field_size_limit(2048576)

OUTPUT_JSON_DIR = os.environ.get("OUTPUT_JSON_DIR", "/tmp/city_info")
OK_GEO_CSV_PATH = os.path.join(OUTPUT_JSON_DIR, "ok_geo.csv")

CITY_JSON_DIR = os.path.join(OUTPUT_JSON_DIR, "output_city_info")

CHOOSE_CITY = {
    "beijing": "北京市",
    "shanghai": "上海市",
    "guangdong": "广东省",
    "zhejiang": "浙江省",
    "jiangsu": "江苏省",
    "sichuan": "四川省",
    "hubei": "湖北省",
    "henan": "河南省",
    "hebei": "河北省",
    "shanxi": "山西省",
    "shandong": "山东省",
    "liaoning": "辽宁省",
    "jilin": "吉林省",
    "heilongjiang": "黑龙江省",
    "anhui": "安徽省",
    "fujian": "福建省",
    "jiangxi": "江西省",
    "hunan": "湖南省",
    "guizhou": "贵州省",
    "yunnan": "云南省",
    "hainan": "海南省",
    "guangxi": "广西壮族自治区",
    "neimenggu": "内蒙古自治区",
    "xinjiang": "新疆维吾尔自治区",
    "xizang": "西藏自治区",
    "qinghai": "青海省",
    "gansu": "甘肃省",
    "ningxia": "宁夏回族自治区",
    "shannxi": "陕西省",
    "chongqing": "重庆市",
    "tianjin": "天津市",
}


class CityType(Enum):
    NONE = "CITY_TYPE_NONE"
    PROVINCE = "CITY_TYPE_PROVINCE"  # 省
    MUNICIPALITY = "CITY_TYPE_MUNICIPALITY"  # 直辖市
    PREFECTURE = "CITY_TYPE_PREFECTURE"  # 地级市
    COUNTY = "CITY_TYPE_COUNTY"  # 县区
    TOWN = "CITY_TYPE_TOWN"  # 镇


def read_ok_geo_csv():
    lines = []
    with open(OK_GEO_CSV_PATH, "r", encoding="utf-8") as f:
        csv_reader = csv.reader(f)
        next(csv_reader)
        # header: (id-行政区划ID, pid-父级行政区划ID, deep-行政级别, name-名称, ext_path-完整名称, geo-中心经纬度, polygon-边界)
        for row in csv_reader:
            xzqh_id = row[0]  # 行政区划ID
            deep = row[2]  # 0: 省 1: 市 2: 区 3：镇
            ext_path = row[4]  # 完整行政区划名称，以空格分隔 e.g 北京市 北京市 东城区
            geo = row[5]  # 中心经纬度，以空格分隔 GCJ-02坐标系
            polygon = row[
                6
            ]  # 边界集合，以;分隔，每个边界以,分隔，每个点以空格分隔经纬度 GCJ-02坐标系
            lines.append([xzqh_id, deep, ext_path, geo, polygon])
    return lines


def extract_geo(geo: str, ext_path: str):
    """extract wgs84 geo from gcj02 geo from ok_geo.csv

    Args:
        geo (str): center geo in gcj02 format, e.g 116.405285 39.904989
        ext_path (str): _description_

    Returns:
        extracted wgs84 geo, e.g [116.405285, 39.904989]
    """
    if geo == "EMPTY":
        print(f"Error: geo is empty, {ext_path}")
        return [0, 0]
    gcj02_lon, gcj02_lat = geo.split(" ")
    wgs84_lat, wgs84_lon = GCJ02_to_WGS84(float(gcj02_lat), float(gcj02_lon))
    return [wgs84_lon, wgs84_lat]


def extract_mongo_polygon(polygons: str) -> dict:
    """extract mongodb supported polygon format from text.

    Args:
        polygons (str): polygon text.

    Returns:
        A multi-polygon dict object as mongodb supported format.
    """
    if polygons == "EMPTY":
        return {"type": "MultiPolygon", "coordinates": []}
    boundary_list = []
    for it in polygons.split(";"):
        points = it.split(",")
        boundary = []
        for point in points:
            point = point.strip().split(" ")
            gcj02_lon, gcj02_lat = float(point[0]), float(point[1])
            wgs84_lat, wgs84_lon = GCJ02_to_WGS84(gcj02_lat, gcj02_lon)
            boundary.append([wgs84_lon, wgs84_lat])
        boundary.append(boundary[0])
        boundary_list.append([boundary])
    return {"type": "MultiPolygon", "coordinates": boundary_list}


def extract_city_type(deep: str) -> CityType:
    """Get city type by deep

    Args:
        deep (str): 0: 省 1: 市 2: 区 3：镇

    Returns:
        CityType, e.g CityType.PROVINCE
    """
    if deep == "0":
        return CityType.PROVINCE
    if deep == "1":
        return CityType.MUNICIPALITY
    if deep == "2":
        return CityType.COUNTY
    if deep == "3":
        return CityType.TOWN
    return CityType.NONE


def extract_ext_path(ext_path: str):
    """extract primary_name, secondary_name, city_name from ext_path

    Args:
        ext_path (str): e.g 北京市 北京市 东城区

    Returns:
        (str, str, str): (primary_name, secondary_name, city_name)
    """
    ext_params = ext_path.split(" ")
    primary_name = ext_params[0]
    secondary_name = ext_params[1] if len(ext_params) > 1 else primary_name
    city_name = ext_params[2] if len(ext_params) > 2 else secondary_name
    return primary_name, secondary_name, city_name


def generate_city_json(lines: list, choose_city: str) -> list:
    """generate city json data from ok_geo.csv

    Args:
        lines (list): text lines from ok_geo.csv
        choose_city (str): city name to choose. Only the city contains this name will be extracted.

    Returns:
        extracted city info list.
    """
    city_list = []
    for line in lines:
        xzqh_id, deep, ext_path, geo, polygon = line
        primary_name, secondary_name, city_name = extract_ext_path(ext_path)
        if choose_city not in ext_path:
            continue
        city = {
            "city_id": f"{xzqh_id:0<6}",
            "city_name": city_name,
            "city_type": extract_city_type(deep).value,
            "country_name": "中国",
            "primary_name": primary_name,
            "secondary_name": secondary_name,
            "timezone": "Asia/Shanghai",
            "city_center": extract_geo(geo, ext_path),
            "city_boundary": extract_mongo_polygon(polygon),
        }
        city_list.append(city)
    return city_list


def main():
    os.makedirs(CITY_JSON_DIR, exist_ok=True)
    lines = read_ok_geo_csv()
    for city_en, city_cn in CHOOSE_CITY.items():
        print(f"extracting {city_cn} geo data from ok_geo.csv...")
        city_list = generate_city_json(lines, city_cn)
        with open(
            os.path.join(CITY_JSON_DIR, f"{city_en}.json"), "w+", encoding="utf-8"
        ) as f:
            f.write(json.dumps(city_list, ensure_ascii=False, indent=4))


if __name__ == "__main__":
    main()
