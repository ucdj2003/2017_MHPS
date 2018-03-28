# -*- coding: UTF-8 -*-
import random
import os

def check_in_list(order_list,tabu_list):
    result = False
    for i in tabu_list:
        if(order_list == i):
            result = True
    return result

def caluc_max(machine,num_jobs,num_machine):
    #make a copy
    temp = machine

    #init frist row
    for i in range(0,num_jobs):
        if(i==0):
            pass
        else:
            temp[0][i] += temp[0][i-1]

    #update every row
    for i in range(1,num_machine):
        for j in range(0,num_jobs):
            if(j==0):
                temp[i][j] = temp[i][j] + temp[i-1][j]
            else:
                #left is big
                if(temp[i][j-1]>temp[i-1][j]):
                    temp[i][j] += temp[i][j-1]
                #up is big
                else:
                    temp[i][j] = temp[i][j] + temp[i-1][j]
    return temp[num_machine-1][num_jobs-1]

def make_order(machine,order,num_jobs,num_machine):
    #make a copy
    temp = []
    for i in range(0,num_machine):
        temp.append([])

    for i in range(0,num_machine):
        for j in range(0,num_jobs):
            now = order[j]
            temp[i].append(machine[i][now])

    return temp


def do_tabu(file_name):
    #init var
    num_machine = None
    num_jobs = None
    best_score = 9999
    machines = []
    job_order = []
    tabu_list = []
    tabu_count = 0
    iter_count = 0
    iter_max = 10000

    #open file
    print("read: " + file_name)
    f = open(file_name)
    data = []
    lines = f.readlines()
    for i in lines:
        i = i.split()
        data.append(i)
    num_machine = int(data[0][1])
    num_jobs = int(data[0][0])

    print("number of machine: " + str(num_machine))
    print("number of jobs: " + str(num_jobs))

    #trans str to int
    for i in range(1,num_machine+1):
        temp = data[i]
        temp[:] = [int(x) for x in temp]
        machines.append(data[i])

    #make job order
    for i in range(0,num_jobs):
        job_order.append(i)

    random.shuffle(job_order)
    tabu_list.append(job_order)

    #do tabu search 20 times
    while(iter_count<iter_max):
        #if order in tabu list
        if(not check_in_list(job_order,tabu_list)):
            random.shuffle(job_order)
        #if order not in tabu list, do tabu search
        else:
            #if list more then 20, delete oldest order
            if(tabu_count==20):
                del tabu_list[0]
            #add count
            tabu_count += 1
            iter_count += 1
            #add order to tabu list
            tabu_list.append(job_order)
            cc = make_order(machines,job_order,num_jobs,num_machine)
            score = caluc_max(cc,num_jobs,num_machine)
            #update score
            if(score<best_score):
                best_score = score
            #shuffle order
            random.shuffle(job_order)
    return best_score


if __name__=="__main__":
    #load all data
    files = os.listdir("./data/")

    #every data do tabu
    for i in files:
        result = do_tabu("./data/" + i)
        print(i + " best is: " + str(result) + "\n")
