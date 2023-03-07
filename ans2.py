
"""
設問2
ネットワークの状態によっては、一時的にpingがタイムアウトしても、一定期間するとpingの応答が復活することがあり、
そのような場合はサーバの故障とみなさないようにしたい。
N回以上連続してタイムアウトした場合にのみ故障とみなすように、設問1のプログラムを拡張せよ。
Nはプログラムのパラメータとして与えられるようにすること。
"""
from _datetime import datetime
# 変数の宣言
path = "./response.log"
message = str
stop: dict[str, datetime] = {}
stop_count: dict[str, int] = {}

N = int(input())

with open(path) as f:
    l_strip = [s.strip() for s in f.readlines()]

for log in l_strip:
    log_split = log.split(",")
    # pingタイムアウト判定
    if log_split[2] == "-":
        # タイムアウトした日時とサーバのipの取得
        broken_date = datetime.strptime(log_split[0], "%Y%m%d%H%M%S")

        # すでに、故障状態のipが存在する場合はそのまま
        # 存在しない場合はstopに故障状態のipをkey, dateをvalueとして保存
        if log_split[1] in stop.keys():
            stop_count[log_split[1]] += 1
            continue
        else:
            stop_count.setdefault(log_split[1], 1)
            stop.setdefault(log_split[1], broken_date)



for log in l_strip:
    log_split = log.split(",")
    broken_date = datetime.strptime(log_split[0], "%Y%m%d%H%M%S")

    if log_split[1] in stop:
        broken_ip = stop[log_split[1]]
        if broken_date.time() < broken_ip.time() or broken_date.time() == broken_ip.time():
            continue
        elif stop_count[log_split[1]] >= N and log_split[2] != "-":
            print(f"{broken_date}から{broken_date - stop[log_split[1]]}の間{log_split[1]}は故障していました。")
