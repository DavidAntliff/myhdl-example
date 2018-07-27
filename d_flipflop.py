#!/usr/bin/env python
from myhdl import block, always, Signal

@block
def DFlipFlop(clk, set, rst, d, q):

    @always(clk.posedge, set.negedge, rst.negedge)
    def logic():
        if set == 0:
            q.next = 1
        elif rst == 0:
            q.next = 0
        else:
            q.next = d

    return logic
