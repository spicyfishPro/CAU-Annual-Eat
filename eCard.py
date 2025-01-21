import requests
from datetime import datetime, timedelta
import time
import json

# 配置部分

# 请替换为你的openid
OPENID = "AFCA92137B2431145141919810"
ORGID = "2"  # 通常为固定值，保持不变
COOKIE = ""

# 请求头
HEADERS = {
    "Host": "vcard.cau.edu.cn",
    "Connection": "keep-alive",
    "session-type": "uniapp",
    "x-requested-with": "XMLHttpRequest",
    "content-type": "application/json",
    "Cookie": COOKIE,
    "isWechatApp": "true",
    "orgid": ORGID,
    "Accept-Encoding": "gzip,compress,br,deflate",
    "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 18_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.55(0x18003729) NetType/WIFI Language/zh_CN",
    "Referer": "https://servicewechat.com/wx4f326cc2a5108bc4/30/page-frame.html",
}

# 基础URL
BASE_URL = "https://vcard.cau.edu.cn/wechatApp/selftrade/queryCardSelfTradeList"

TRADE_TYPE = "-1"  # 交易类型，-1表示所有类型


def generate_date_chunks(start_date, end_date, chunk_size=30):
    """生成日期区间的分片，每个分片不超过chunk_size天。"""
    chunks = []
    current_start = start_date
    while current_start <= end_date:
        current_end = current_start + timedelta(days=chunk_size - 1)
        if current_end > end_date:
            current_end = end_date
        chunks.append((current_start, current_end))
        current_start = current_end + timedelta(days=1)
    return chunks


def fetch_consumption_records(begin_date, end_date):
    """发送请求获取指定日期范围内的消费记录。"""
    params = {
        "beginDate": begin_date.strftime("%Y-%m-%d"),
        "endDate": end_date.strftime("%Y-%m-%d"),
        "tradeType": TRADE_TYPE,
        "openid": OPENID,
        "orgid": ORGID,
    }

    try:
        response = requests.get(BASE_URL, headers=HEADERS, params=params, timeout=10)
        response.raise_for_status()  # 检查请求是否成功
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        print(f"请求失败: {e}")
        return None
    except json.JSONDecodeError:
        print("无法解析响应的JSON数据。")
        return None


def main():
    # 设置查询的时间范围（一年内）
    end_date = datetime.today()
    start_date = end_date - timedelta(days=365)

    print(
        f"开始获取从 {start_date.strftime('%Y-%m-%d')} 到 {end_date.strftime('%Y-%m-%d')} 的消费记录。"
    )

    # 生成日期分片
    date_chunks = generate_date_chunks(start_date, end_date, chunk_size=15)
    print(f"总共需要查询 {len(date_chunks)} 次，每次最多查询100条数据。")

    all_records = []

    for idx, (chunk_start, chunk_end) in enumerate(date_chunks, start=1):
        print(
            f"正在查询第 {idx} 个区间: {chunk_start.strftime('%Y-%m-%d')} 至 {chunk_end.strftime('%Y-%m-%d')}"
        )
        data = fetch_consumption_records(chunk_start, chunk_end)

        if data and "data" in data and "data" in data["data"]:
            records = data["data"]["data"]
            print(f"获取到 {len(records)} 条记录。")
            all_records.extend(records)
        else:
            message = data.get("message", "") if data else ""
            print(f"未获取到数据或数据格式不正确。消息: {message}")

        # 为避免请求过于频繁，可以设置延时（例如1秒）
        time.sleep(5)

    print(f"总共获取到 {len(all_records)} 条消费记录。")

    # 将所有记录保存到本地文件（可选）
    with open("consumption_records.json", "w", encoding="utf-8") as f:
        json.dump(all_records, f, ensure_ascii=False, indent=4)

    print("消费记录已保存到 'consumption_records.json'。")


if __name__ == "__main__":
    main()
