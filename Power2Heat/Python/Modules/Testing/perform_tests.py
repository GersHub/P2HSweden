# -*- coding: utf-8 -*-
"""
Created on Wed Mar 30 09:03:25 2016

@author: Jonatan

Perform test suite
"""

from __future__ import division
from test_ac_constraints import test_add, test_withdraw
from test_dist_accumulators import test_dist_ac
from test_accumulation_strategy import test_acs_priority
from test_accumulation_regional_constraint import test_regional_constraint
from test_zero_ac import test_zero_ac

print 'Test add:', test_add()
print 'Test withdraw:', test_withdraw()
print 'Test dist ac:', test_dist_ac()
print 'Test priority filling:', test_acs_priority()
print 'Test regional constraint:', test_regional_constraint()
print 'Test zero accumulation:', test_zero_ac()

