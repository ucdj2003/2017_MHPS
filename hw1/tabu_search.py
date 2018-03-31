# -*- coding: UTF-8 -*-
import random
import os
import operator
import time

def check_in_list(order_list,check_list):
    for i in check_list:
        if(operator.eq(order_list,i)):
            return True
    return False

def swap_order(orignal_order,swap_num):
    #swap order[num0] and order[num1]
    temp_order = None
    temp_order = orignal_order
    temp = temp_order[swap_num[0]]
    temp_order[swap_num[0]] = temp_order[swap_num[1]]
    temp_order[swap_num[1]] = temp
    return temp_order

def make_new_order(orignal_order,jobs):
    #create two random number to swap
    random_number = random.sample(range(jobs), 2)
    return swap_order(orignal_order,random_number)

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
    #fellow order list adjust job list
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
    best_order = None
    worst_score = 0
    avg_score = 0
    machines = []
    tabu_list = []
    iter_count = 0
    iter_max = 10000
    tabu_list_max = 200

    #open file
    f = open(file_name)
    data = []
    lines = f.readlines()
    for i in lines:
        i = i.split()
        data.append(i)
    num_machine = int(data[0][1])
    num_jobs = int(data[0][0])

    #print details
    print("read: " + file_name)
    print("number of machines: " + str(num_machine))
    print("number of jobs: " + str(num_jobs))
    print("iterations: " + str(iter_max))
    print("tabu list length: " + str(tabu_list_max))

    #trans str to int
    for i in range(1,num_machine+1):
        temp = data[i]
        temp[:] = [int(x) for x in temp]
        machines.append(data[i])

    #create a temp order save current job order
    temp_order = []
    for i in range(0,num_jobs):
            temp_order.append(i) 

    #do tabu search iter_max times
    while(iter_count<iter_max):
        #make a job order
        job_order = []
        #load previous order to job order
        for i in temp_order:
            job_order.append(i)
        #use previous job order to create new order
        job_order = make_new_order(job_order,num_jobs)
        #update temp order
        temp_order = job_order

        #if order in tabu list, pass this order
        if(check_in_list(job_order,tabu_list)):
            pass
        #if order not in tabu list, do tabu search
        else:
            #if list more then max, delete oldest order
            if(len(tabu_list)==tabu_list_max):
                del tabu_list[0]
            #add iter count
            iter_count += 1
            #add order to tabu list
            tabu_list.append(job_order)
            #use job order adjust machine's job list
            machine_list = make_order(machines,job_order,num_jobs,num_machine)
            #calculation score
            score = caluc_max(machine_list,num_jobs,num_machine)
            #update score
            if(score<best_score):
                best_score = score
                best_order = job_order
            if(score>worst_score):
                worst_score = score
            avg_score += score
    avg_score = avg_score/iter_count
    return best_score,worst_score,avg_score,best_order

if __name__=="__main__":
    #load all data
    files = os.listdir("./data/")
    #every file do tabu search
    for i in files:
        start_time = time.time()
        best,worst,avg,order = do_tabu("./data/" + i)
        execute_time = time.time() - start_time

        print("best score is: " + str(best))
        print("worst score is: " + str(worst))
        print("avg score is: " + str(avg))
        print("best order is: ")
        print(order)
        print("execute time: %.4fs\n" % (execute_time))