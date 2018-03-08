from __future__ import division  
import pandas
from collections import defaultdict
import matplotlib.pyplot as plot
import networkx as nx
import operator


#import csv file
#making sense of the data

matrix_ = pandas.read_csv('data/data.csv',header = None) 

#generate a dictionary with tuple(origin, destination) as the key
class CSVDictionary (defaultdict) :

    def __init__(self, matrix_) :

        super(CSVDictionary, self).__init__(tuple)
        
        for i in range(0, len(matrix_.index)) :
            self[(int(matrix_.values[i][0]), int(matrix_.values[i][1]))] \
              = int(matrix_.values[i][6])


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
        nx.draw (self.network)
        plot.show()

      

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

class DiseaseOutbreak :
#Assumptions: 1. Destinations do not include intermediary destinations.
#             2. Distance does not matter, because the lenghth of the infection
#                is longer than the travel length time regardless of distance.
#                Secondly, distance does not matter if we assue health and infected
#                people have the same ability to travel to every location.
#             3. Every time step, that mobility value stays the same regardless of
#                outbreak status.
#             4. Assuming a certain percentage of population rather than a quantity of
#                people get infected during outbreak.
#             5. Outbreaks happens because an overwhelming population get infected at once (threshold)
#             6. All outbreaks are equally bad (did not quantify outbreak beyond population size)

    def __init__ (self, outbreak_province, t, i) :
        self.outbreak_provinces = set()
        self.outbreak_provinces.add(outbreak_province)

        #given a infected person move to a province without outbreak, the percentage cause outbreak.
        self.transmission_rate = t

        #given a person in an outbreak province, the chance to get infected.
        self.infection_rate = i

        # the percentage of the population that can cause an outbreak
        self.default_threshold = 0.0002

    def step (self, dic) :
        #theorectically, the mobility can change each step
        #mobility happens, probability of provinces having an outbreak changes
        new_infected_province = set()
        for outbreak_province in self.outbreak_provinces :
            new_infected_province.update(self.disease_spread(dic, outbreak_province))
        self.outbreak_provinces.update(new_infected_province)   
                    

    def print_outbreak_prov (self) :
        print self.outbreak_provinces

    def run(self, num_step, dic) :
        self.print_outbreak_prov()
        for num in range(0,num_step) :
            self.step(dic) 
            self.print_outbreak_prov()


    def disease_spread (self, dic, outbreak_province) :
        new_outbreak_prov = set()
        for origin_destination in dic.keys() :
            if origin_destination[0] == outbreak_province and \
                origin_destination[1] != outbreak_province :
                mobile_population = dic[origin_destination]
                infected_population = self.get_infected_population(mobile_population)
                dest = origin_destination[1]
                pop_threshold = self.default_threshold * dic[(dest, dest)] #encodes population
                outbreak = self.has_outbreak(infected_population, pop_threshold)
                if outbreak :
                    new_outbreak_prov.add(origin_destination[1])
        return new_outbreak_prov
    
                

    def get_infected_population(self, population) :
        return self.infection_rate * population
    
    
    def has_outbreak(self, in_infected_population, threshold_outbreak) :
        #threshold_outbreak could vary from province to province

        return self.transmission_rate * in_infected_population >= threshold_outbreak

    
dic = CSVDictionary(matrix_)
net = DirectedNetwork(dic)
net.print_edges()
net.draw_graph()

# original outbreak province: 1
# transmission rate: 0.2
# infection rate: 0.1
# number of time steps: 10
outbreak = DiseaseOutbreak(1,0.2,0.1)
outbreak.run(10,dic)




