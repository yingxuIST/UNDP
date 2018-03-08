from __future__ import division  
import pandas
from collections import defaultdict
import matplotlib.pyplot as plot
import networkx as nx


#import csv file
#making sense of the data

matrix_ = pandas.read_csv('data/test.csv',index_col = 0)

print(matrix_)
print(matrix_.values[0])
print(matrix_.index)
print(matrix_.columns[0])
print(len(matrix_.columns))
print(len(matrix_.index))
print(len(matrix_.values))
print(sum(matrix_.values))



#generate a dictionary with tuple(origin, destination) as the key
class CSVDictionary (defaultdict) :

    def __init__(self, matrix_) :

        super(CSVDictionary, self).__init__(tuple)
        
        for i in range(0, len(matrix_.values)) :
            for j in range(0, len(matrix_.values[i])) :
                self[(matrix_.index[i], matrix_.columns[j])] = matrix_.values[i][j]

   
#generate a weighted and directed network
class DirectedNetwork :
    
    def __init__ (self, origin_destination) :
        
        self.network = nx.DiGraph()

        for key in origin_destination.keys() :
            if key[0] != key[1] :
                self.network.add_edge(key[0],key[1], weight = origin_destination[key])

           
    def print_edges (self) :

        print self.network.number_of_edges()


    #draw a province-province movement network
    def draw_graph (self) :
        pos = nx.spring_layout(self.network)
        nx.draw (self.network)
        #plot.show()


dic = CSVDictionary(matrix_)
net = DirectedNetwork(dic)
net.print_edges()
net.draw_graph()
        
        


############## building models ##############

'''
Reasoning:
Tizzoni et. al (2014): human moibily is a key component of
   large-scale spatial-transmission models of infectious disease.
   Riley (2007) reviewed various models for different diseases
   using human mobility data.
   --> human mobiliy data as a proxy to model disease outbreak.

Balcan et al. (2009) found that when modeling infoectious
   diseases, short-scale commuting flows did not exhibit
   significant improvement when adding to the baseline model,
   which long-range traffic data. 
   --> using province-province data can be sufficient.   
'''


def spatial_cluster (matrix_) :

    '''
Eubank et. al (2004) found that people's contact network is
   small-world graph, and location graph is scale free
   --> outbreak is likely to be occur in spatial clusters
   initially.
   
    '''  
#Hypothesis 1: when net flow of a province is signiciantly smaller
#              than average flow, it is likely that the province 
#              currently has a disease outbreak
#Hypothesis 2: when there are more out_flow and in_flow, the province,
#              as a hub, will be likely to have a disease outbreak.


    #get the average flow

    global_flow = 0

    for i in range(0, len(matrix_.values)) :
        for j in range(0, len(matrix_.values[i])) :
            if i != j :
                global_flow += matrix_.values[i][j]

    average_flow = global_flow / len(matrix_.columns)
          
    print ('average flow: %d.' % average_flow)


    #get net flow of each province : in_flow - out_flow
    #get total flow of each province : in_flow + out_flow
    #net_flow = sum(columns) - sum(rows)

    province_net_flow = dict()
    province_total_flow = dict()

    
    for province in range (0, len(matrix_.columns)) :
        out_flow = sum(matrix_.values[province])
        print out_flow
        in_flow = 0
        for row in range (0, len(matrix_.index)) :
            in_flow += matrix_.values[row][province]
        print in_flow
        
        net_flow = in_flow - out_flow
        total_flow = in_flow + out_flow
        
        province_net_flow[matrix_.columns[province]] = net_flow
        province_total_flow[matrix_.columns[province]] = total_flow
        
    print province_net_flow
    print province_total_flow

    
sc = spatial_cluster(matrix_)




def path_model (net) :

#Hypothesis 3: 

    #get province name
    for col in matrix_.columns :
        print col
    
   
pm = path_model(net)
