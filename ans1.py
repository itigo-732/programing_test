
from _datetime import datetime
# 変数の定義
path = "./response.log"
stop: dict[str, datetime] = {}
message = ""

with open(path) as f:
    l_strip = [s.strip() for s in f.readlines()]

for log in l_strip:
    log_split = log.split(",")
    # pingタイムアウト判定
    if log_split[2] == "-":
        # タイムアウト日時の取得
        date = datetime.strptime(log_split[0], "%Y%m%d%H%M%S")
        # すでに、故障状態のipが存在する場合はそのまま
        # 存在しない場合はstopに故障状態のipをkey, dateをvalueとして保存
        if log_split[1] in stop.keys():
            continue
        else:
            stop.setdefault(log_split[1], date)

for log in l_strip:
    log_split = log.split(",")
    date = datetime.strptime(log_split[0], "%Y%m%d%H%M%S")
    if log_split[1] in stop:
        if date.time() < stop[log_split[1]].time() or date.time() == stop[log_split[1]].time():
            continue
        else:
            print(f"{date - stop[log_split[1]]}の間{log_split[1]}は故障していました。")
