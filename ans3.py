

from _datetime import datetime

# 変数の宣言
path = "./response.log"
message = str
stop: dict[str, datetime] = dict()
stop_count: dict[str, int] = dict()
response_time: dict[str, int] = dict()
response_date: dict[str, datetime] = dict()
N = int(input())
m, t = map(int, input().split(" "))

with open(path) as f:
    l_strip = [s.strip() for s in f.readlines()]

for log in l_strip:
    log_split = log.split(",")
    # タイムアウトした日時とサーバのipの取得
    broken_date = datetime.strptime(log_split[0], "%Y%m%d%H%M%S")
    # pingタイムアウト判定
    if log_split[2] == "-":

        # すでに、故障状態のipが存在する場合はそのまま
        # 存在しない場合はstopに故障状態のipをkey, dateをvalueとして保存
        if log_split[1] in stop.keys():
            stop_count[log_split[1]] += 1
        else:
            stop_count.setdefault(log_split[1], 1)
            stop.setdefault(log_split[1], broken_date)
    else:
        if log_split[1] in response_time.keys():
            response_time[log_split[1]] = response_time[log_split[1]] + int(log_split[2])
            if response_time[log_split[1]] / m >= t　* m:
                response_date.setdefault(log_split[1], broken_date)
        else:
            response_time.setdefault(log_split[1], int(log_split[2]))

print(response_date)

for log in l_strip:
    log_split = log.split(",")
    broken_date = datetime.strptime(log_split[0], "%Y%m%d%H%M%S")

    if log_split[1] in stop:
        broken_ip = stop[log_split[1]]
        if broken_date.time() < broken_ip.time() or broken_date.time() == broken_ip.time():
            continue
        elif stop_count[log_split[1]] >= N and log_split[2] != "-":
            print(f"{broken_date}から{broken_date - stop[log_split[1]]}の間{log_split[1]}は故障していました。")

for ip, time in response_time.items():
    ave_time = time / m
    if ave_time >= t:
        print(f"{response_date[ip]}から{ip}においての直近{m}回の平均応答時間が{ave_time: .2f}ミリ秒を超えました。")


