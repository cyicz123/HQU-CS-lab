import argparse


def FCFS(jobs: list):
    start_time = jobs[0][1]
    sum_turnover, sum_weight_turnover, end_time = 0, 0, 0
    print('FCFS算法：')
    for job in jobs:
        print('时刻{}：进程{}开始运行'.format(job[1], job[0]))
        end_time = start_time + job[2]
        turnover = end_time - job[1]
        weight_turnover = turnover / job[2]
        sum_turnover += turnover
        sum_weight_turnover += weight_turnover
        print('进程%s :开始时间 %.4f\t,结束时间 %.4f\t,周转时间 %.4f\t,带权周转时间 %.4f\n' % (
            job[0], start_time, end_time, turnover, weight_turnover))
        start_time = end_time
    print('FCFS平均周转时间 %.4f\t,平均带权周转时间 %.4f' % (sum_turnover / len(jobs), sum_weight_turnover / len(jobs)))


def SJF(jobs: list):
    jobs_num = len(jobs)
    start_time = jobs[0][1]
    sum_turnover, sum_weight_turnover, end_time = 0, 0, 0
    jobs_q = list()
    jobs_q.append(jobs.pop(0))
    print('SJF算法：')
    while jobs_q:
        job = jobs_q[0]
        print('时刻{}：进程{}开始运行'.format(job[1], job[0]))
        end_time = start_time + job[2]
        turnover = end_time - job[1]
        weight_turnover = turnover / job[2]
        sum_turnover += turnover
        sum_weight_turnover += weight_turnover
        print('进程%s :开始时间 %.4f\t,结束时间 %.4f\t,周转时间 %.4f\t,带权周转时间 %.4f\n' % (
            job[0], start_time, end_time, turnover, weight_turnover))
        start_time = end_time
        jobs_q.pop(0)
        while jobs and end_time > jobs[0][1]:
            if not jobs_q:
                jobs_q.append(jobs.pop(0))
            for index, (_, _, S) in enumerate(jobs_q):
                if jobs[0][2] < S:
                    jobs_q.insert(index, jobs.pop(0))
                    break
    print('SJF平均周转时间 %.4f\t,平均带权周转时间 %.4f' % (sum_turnover / jobs_num, sum_weight_turnover / jobs_num))


if __name__ == '__main__':
    parse = argparse.ArgumentParser(description='模拟FCFS和SJF算法')
    parse.add_argument('-t', '-T', required=True, nargs='+', type=float, help='每个进程到达时间T')
    parse.add_argument('-s', '-S', required=True, nargs='+', type=float, help='服务时间S')
    parse.add_argument('--FCFS', dest='fcfs', action='store_true', help='使用FCFS算法，缺省为SJF算法')
    args = parse.parse_args()
    switch_fcfs = args.fcfs

    if len(args.t) != len(args.s):
        raise Exception('进程缺少到达时间T或服务时间S')
    job_list = list()
    for i, (t, s) in enumerate(zip(args.t, args.s)):
        job_list.append((i, t, s))
    if switch_fcfs:
        FCFS(job_list)
    else:
        SJF(job_list)
