import argparse


def RR(jobs: list, q_t: int):
    start_time = jobs[0][1]
    sum_turnover, sum_weight_turnover, end_time = 0, 0, 0
    print('时间片轮转算法：')
    s_list = [x[2] for x in jobs]
    while jobs:
        if jobs[0][2] > q_t:
            print('时刻{}：进程{}开始运行'.format(start_time, jobs[0][0]))
            jobs[0][2] -= q_t
            start_time += q_t
            jobs.append(jobs[0])
            jobs.pop(0)
        else:
            end_time = start_time + jobs[0][2]
            turnover = end_time - jobs[0][1]
            weight_turnover = turnover / s_list[jobs[0][0]]
            sum_turnover += turnover
            sum_weight_turnover += weight_turnover
            print('时刻{}：进程{}开始运行'.format(start_time, jobs[0][0]))
            print('进程%s :开始时间 %.4f\t,结束时间 %.4f\t,周转时间 %.4f\t,带权周转时间 %.4f\n' % (
                jobs[0][0], start_time, end_time, turnover, weight_turnover))
            start_time = end_time
            jobs.pop(0)
    print('RR平均周转时间 %.4f\t,平均带权周转时间 %.4f' % (sum_turnover / len(s_list), sum_weight_turnover / len(s_list)))


if __name__ == '__main__':
    parse = argparse.ArgumentParser(description='模拟RR算法')
    parse.add_argument('-t', '-T', required=True, nargs='+', type=float, help='每个进程到达时间T')
    parse.add_argument('-s', '-S', required=True, nargs='+', type=float, help='服务时间S')
    parse.add_argument('-q', required=True, type=int, help='切片时间q')
    args = parse.parse_args()
    print(args.q)

    if len(args.t) != len(args.s):
        raise Exception('进程缺少到达时间T或服务时间S')
    job_list = list()
    for i, (t, s) in enumerate(zip(args.t, args.s)):
        job_list.append([i, t, s])
    RR(job_list, args.q)
