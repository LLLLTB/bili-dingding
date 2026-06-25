import requests

UID = "123456"  # 改成你的B站UID
WEBHOOK = "你的钉钉Webhook"

def get_dynamic():
    url = f"https://api.bilibili.com/x/polymer/web-dynamic/v1/feed/space?host_mid={UID}"
    return requests.get(url, timeout=10).json()

last_id = None

while True:
    try:
        data = get_dynamic()
        item = data["data"]["items"][0]

        dynamic_id = item["id_str"]
        text = item["modules"]["module_dynamic"]["desc"]["text"]

        if dynamic_id != last_id:
            last_id = dynamic_id

            msg = {
                "msgtype": "text",
                "text": {
                    "content": f"通知\n【B站更新】\n{text}"
                }
            }

            requests.post(WEBHOOK, json=msg)
            print("已推送")

        else:
            print("无更新")

    except Exception as e:
        print("错误:", e)
