# -*- coding: utf-8 -*-
"""
Created on Wed Mar 30 08:38:48 2016

@author: Jonatan

Automatic test for accumulator constraints: max storage, min storage,
max_transfer
"""

from __future__ import division
from Modules.Accumulation.Accumulator import Accumulator

def test_add():

    my_ac = Accumulator(9, 0, 2, 5)
    
    # test max transfer limit
    q_added = my_ac.add(3)    

    if q_added != 2 or my_ac.current_storage != 7:
        return False
    
    # test mass balance
    q_added = my_ac.add(1)
    
    if q_added != 1 or my_ac.current_storage != 8:
        return False
    
    # test max storage limit    
    q_added = my_ac.add(3)
    
    if q_added != 1 or my_ac.current_storage != 9:
        return False
    
    return True

def test_withdraw():
    
    my_ac = Accumulator(9, 1, 2, 5)
    
    # test max transfer limit
    q_ext = my_ac.withdraw(3)
    
    if q_ext != 2 or my_ac.current_storage != 3:
        return False
    
    # test mass balance
    q_ext = my_ac.withdraw(1)
    
    if q_ext != 1 or my_ac.current_storage != 2:
        return False
        
    # test min storage limit
        
    q_ext = my_ac.withdraw(3)
    
    if my_ac.current_storage != 1:
        return False
    
    return True
