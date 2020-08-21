# -*- coding: utf-8 -*-
"""
Created on Mon Mar 07 09:54:45 2016

@author: Jonatan
"""

class Accumulator:
    'Class for modelling an accumulator'
    
    def __init__(self, max_storage, min_storage, max_transfer, current_storage,
                                                 history = []):
        self.max_storage = max_storage
        self.min_storage = min_storage
        self.max_transfer = max_transfer
        self.current_storage = current_storage
        self.history = history
        
    def get_rel_storage(self):
        """ Returns the ratio between current storage and max storage.
        """
        if self.max_storage == 0:
            # avoid division by zero
            return 0
        else:
            return self.current_storage / self.max_storage
        
    def add(self, q):
        """ Adds as much as possible of the heat q to the accumulator.
            Returns the amount of heat that could be added
        """
        self.history.append(self.current_storage)        
        
        if q < 0:
            raise Exception('Cannot add negative amount of heat')
        else:            
            if self.max_storage - self.current_storage < self.max_transfer:
                # the active limit comes from having an almost full tank
                if q > self.max_storage - self.current_storage:
                    # all heat cannot fit
                    addition = self.max_storage - self.current_storage
                    self.current_storage = self.max_storage
                    return addition
                else:
                    # all heat can fit
                    self.current_storage += q
                    return q
            else:
                # the active limit comes from the transfer capacity                  
                if q > self.max_transfer:
                    # all heat cannot fit
                    self.current_storage += self.max_transfer
                    return self.max_transfer
                else:
                    # all heat can fit
                    self.current_storage += q
                    return q
                    
    def withdraw(self,  q):
        """ Withdraws as much as possible of the heat q from the accumulator.
            Returns the amount of heat withdrawn.
        """
        self.history.append(self.current_storage)        
        
        if q < 0:
            raise Exception('Cannot withdraw negative amount of heat')
            
        else:
            if self.current_storage - self.min_storage < self.max_transfer:
                # the active limit comes from having an almost empty tank
                if q > self.current_storage - self.min_storage:
                    # all desired heat cannot be withdrawn
                    withdrawal = self.current_storage - self.min_storage
                    self.current_storage = self.min_storage
                    return withdrawal
                else:
                    # the full amount of desired heat can be extracted
                    self.current_storage -= q
                    return q
            else:
                # the active limit comes from the transfer capacity
                if q > self.max_transfer:
                    # the full amount of desired heat cannot be extracted
                    self.current_storage -= self.max_transfer
                    return self.max_transfer
                else:
                    # all desired heat can be extracted
                    self.current_storage -= q
                    return q