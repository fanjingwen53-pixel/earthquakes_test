import requests
import json   # 导入 json 模块，用来解析数据

def get_data():
    # 从 USGS 服务器请求地震数据
    response = requests.get(
        "https://earthquake.usgs.gov/fdsnws/event/1/query.geojson",
        params={
            'starttime': "2000-01-01",
            "maxlatitude": "58.723",
            "minlatitude": "50.008",
            "maxlongitude": "1.67",
            "minlongitude": "-9.756",
            "minmagnitude": "1",
            "endtime": "2018-10-11",
            "orderby": "time-asc"
        }
    )

    # 获取返回的文本内容（JSON 格式）
    text = response.text

    # 把 JSON 字符串解析成 Python 字典
    data = json.loads(text)

    # 返回数据
    return data


def count_earthquakes(data):
    """返回总地震数量"""
    return len(data["features"])   # 所有地震都在 "features" 列表里


def get_magnitude(earthquake):
    """获取某个地震的震级"""
    return earthquake["properties"]["mag"]


def get_location(earthquake):
    """获取某个地震的位置（经纬度）"""
    # "geometry" -> "coordinates" 是一个 [lon, lat, depth] 列表
    lon, lat, _ = earthquake["geometry"]["coordinates"]
    return (lat, lon)


def get_maximum(data):
    """找到最大震级及其位置"""
    max_mag = None
    max_loc = None

    for eq in data["features"]:
        mag = get_magnitude(eq)
        if mag is None:
            continue  # 有些记录没有震级
        if (max_mag is None) or (mag > max_mag):
            max_mag = mag
            max_loc = get_location(eq)

    return max_mag, max_loc


# 主程序入口
if __name__ == "__main__":
    data = get_data()
    print(f"Loaded {count_earthquakes(data)} earthquakes")

    max_magnitude, max_location = get_maximum(data)
    print(f"The strongest earthquake was at {max_location} with magnitude {max_magnitude}")
