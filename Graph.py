# -*- coding: utf-8 -*-
"""
Created on Wed Feb 15 05:22:16 2017

@author: sachin
"""
from collections import defaultdict ##Dictionary to store the Edge Details


def find_path(graph, start, end, path=[]):
    path = path + [start]
    if start == end:
        return path
    if not graph.has_key(start):
        return None
    for node in graph[start]:
        if node not in path:
            newpath = find_path(graph, node, end, path)
            if newpath: return newpath
    return None
        
#######find_path function------> referenced from: https://www.python.org/doc/essays/graphs/#######

def load(MST):
    ##Store the Edges in the Graph dictionary
    graph = defaultdict(list)
    for src,dest  in MST:
            ##symmetric Property: as it is Undirected Graph
            graph[src].append(dest)
            graph[dest].append(src)
    
    trafficlist = []
    #######################LOAD TRAFFIC FROM THE FILE GIVEN################################
    with open("C:\\Users\\sachi\\Desktop\\KB\\assignment\\traffictableW17.txt") as f:
        for line in f:
            trafficlist.append([int(n) for n in line.strip().split()]) ##split each line(src,dest,load) and add it into the list
    
    path = [];path_list = [];load_list = [];load_path_list = []
    ##find path for each src-dest given in Traffic list 
    for pair in trafficlist:
        load_list.append(pair[2])
        src,dest,load = pair
        path.append(find_path(graph,src,dest,path_list)) ##calculates path for given Source and Destination 
        
    load_path_list.append(zip(path,load_list)) #final path and its corresponding load to be assigned on each link
    
    #printing path and corresponding transit traffic to be applied on each link
    pairs=[]
    ##Print out the PATH and the associated Load to be applied on each link 
    print "PATH FROM SRC-DEST LOAD(Kbps)\tHops"
    for i in load_path_list:
        for pair in i:
            pairs.append(pair[0])
            print pair[0],pair[1],"Kbps ----",len(pair[0])-1,"hops"
    print 
    
    ##find out the Indivdual load on each link
    individual_edgeload_cost = []
    for j in load_path_list:
        for i in j:
            path , cost = i
            k = 0
            for l in path:
                while k < (len(path)-1):
                    b = path[k],path[k+1],cost
                    individual_edgeload_cost.append(b)
                    k+=1
    src = [];dest = [];load = []
    ##Sort the individual load link on edge
    individual_edgeload_cost = sorted(individual_edgeload_cost)
    ## split the list and add to source,destination, and load to find out the total load on each link (contains transit traffic)
    for pair in sorted(individual_edgeload_cost):
        src.append(pair[0])
        dest.append(pair[1])
        load.append(pair[2])
    i = 0
    ##contains list of src-dest pair with the added load value(Transit Traffic)
    already_there=[] 
    while i<(len(src)-1):
        if (src[i]==src[i+1] and dest[i]==dest[i+1]):
            lo=load[i+1]=load[i]+load[i+1]
            a=(src[i],dest[i],lo)
        else:
            b=(src[i],dest[i],load[i]) 
            already_there.append(b)   
        if(i==(len(src)-2)):
            already_there.append(a)
        i+=1            
    
    s=[];d=[];l=[]
    MST_Load=[]
    for pair in already_there:
        s.append(pair[0])
        d.append(pair[1])
        l.append(pair[2])
    print
    i=0
    ##Add the load from the Same links which involves the Transit Traffic
    while i<=(len(s)-1): 
        j=0
        while j<(len(d)-1):
            if s[i]==d[j] and d[i]==s[j]:
                lo=l[i]+l[j]
                a = (s[i],d[i],lo)
                if a not in MST_Load:
                    MST_Load.append(a)
            j+=1
        i+=1
    
    source = []; destination = [];finalLoad = []
    for pair in sorted(MST_Load):
        source.append(pair[0])
        destination.append(pair[1])
        finalLoad.append(pair[2])
    i=0
    ##Remove the Parallel Property from the List
    while i<len(finalLoad)-1:
        j=1
        while j<len(finalLoad)-1:
            if i!=j and finalLoad[i]== finalLoad[j]:
                del source[j]
                del destination[j]
                del finalLoad[j]
            j+=1
        i+=1
    ll = zip(source,destination,finalLoad)
    ##Remove the symmetric Property from the List
    i=0
    while i<len(s):
        j=0
        while j<len(source):
            if (s[i]==source[j] and d[i]==destination[j]) or (s[i]==destination[j] and d[i]==source[j]):
                del s[i]
                del d[i]
                del l[i]
            j+=1
        i+=1
            
    i=0
    while i<len(s):
        j=0
        while j<len(source)-2:
            if (s[i]==source[j] and d[i]==destination[j]) or (s[i]==destination[j] and d[i]==source[j]):
                del s[i]
                del d[i]
                del l[i]
            j+=1
        i+=1
    final_list = zip(s[:-1],d[:-1],l[:-1])
    ##MST_Load final contains the final load in the MST    
    mst_src = [];mst_dest=[];mst_load=[];mst_utilization=[];sumUtilization=0.0
    MST_Load=ll+final_list
    print "Utilization of the Links"
    ##Print out the Source,Destination and associated load and utilization of each link
    print "SOURCE\tDESTINATION\tLOAD\t\tUTILIZATION"
    for pair in sorted(MST_Load):
        mst_src.append(pair[0]) ##contains source values of MST
        mst_dest.append(pair[1]) ##contains destination values of MST
        mst_load.append(pair[2]) ##contains traffic(including transit traffic) of MSt
        utilization=format((float(pair[2])/1544)*100,'.3f')   #1.544Mbps T1 Link used so it will be 1544Kbps after converting
        mst_utilization.append(utilization)
        sumUtilization=sumUtilization+float(utilization) ##Sum of all utilization in MST
        print pair[0],"\t",pair[1],"\t\t",pair[2],"Kbps\t",format((float(pair[2])/1544)*100,'.3f'),"%"
    average = (sumUtilization/len(mst_utilization)) ##Average Utilization
    max_utilization=max(mst_utilization, key=float) ##Maximum Utilization in MST
    print "Max Utilization = ",max_utilization,"%"
    print "Average Utilization = ",format(average,'.3f'),"%"
    print

    ##Print Path lenth with number of hops between given source and destination also traffic generated between them
    print "Path Length"
    sum_traffic_hops=0;total_traffic=0
    print "SOURCE\tDESTINATION\tLOAD\t\tHOPS"
    for v,lv in zip(pairs,load_list):
        total_traffic=total_traffic+lv    ##total traffic
        sum_traffic_hops=sum_traffic_hops+(lv*(len(v)-1)) ##sum of (traffic * Hops between A to B)
        print v[0],"------>",v[-1],"\t\t",lv,"Kbps         ",len(v)-1,"hops"
        
    ##averahe hops=sum of (traffic between A to B * Hops between A to B)/sum of(traffic between A to B)
    Average_hops=sum_traffic_hops/total_traffic
    print "Average Hops = ",Average_hops,"Hops"     

    T_bar=float((1024*8))/1544000 #1.544Mbps = 1544000 bytes
    Average_delay = (float(T_bar)*float(Average_hops))/(1-float(max_utilization)/100) ##(TBar*avg_hops)/(1-maxutilization)
    print
    print
    print "TBar = ",format(T_bar,'.5f'),"seconds"
    print "Average Hops = ",format(float(sum_traffic_hops)/total_traffic,'.3f'),"Hops"
    print "Max Utilization = ",max_utilization,"%"
    print "Average Delay = ",format(Average_delay,'.5f'),"seconds"    