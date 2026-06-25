import requests
import time

# ====== 配置区 ======
MID = "3706959876327428"   # 注意：这里只填数字UID（mid）
WEBHOOK = "https://oapi.dingtalk.com/robot/send?access_token=6cd1045d96588c4b00f28a1e28fb2819748a93800163683733b47eecf71f7165"

headers = {
    "User-Agent": "Mozilla/5.0"
}

last_id = None


def get_data():
    url = f"https://api.bilibili.com/x/polymer/web-dynamic/v1/feed/space?host_mid={MID}"
    try:
        r = requests.get(url, headers=headers, timeout=10)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        print("请求失败:", e)
        return None


def extract_text(item):
    try:
        modules = item.get("modules", {})
        module_dynamic = modules.get("module_dynamic", {})
        desc = module_dynamic.get("desc", {})
        return desc.get("text", "（无文本内容）")
    except:
        return "（解析失败）"


while True:
    try:
        data = get_data()
        if not data:
            time.sleep(10)
            continue

        items = data.get("data", {}).get("items", [])
        if not items:
            print("暂无动态")
            time.sleep(10)
            continue

        item = items[0]
        dynamic_id = item.get("id_str")

        text = extract_text(item)

        if dynamic_id and dynamic_id != last_id:
            last_id = dynamic_id

            msg = {
                "msgtype": "text",
                "text": {
                    "content": f"通知\n【B站更新】\n{text}"
                }
            }

            res = requests.post(WEBHOOK, json=msg)
            print("已推送:", res.text)

        else:
            print("无更新")

        time.sleep(10)  # 防止刷接口

    except Exception as e:
        print("错误:", e)
        time.sleep(5)
