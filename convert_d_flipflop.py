#!/usr/bin/env python
from myhdl import Signal, ResetSignal, modbv

from d_flipflop import DFlipFlop

def convert_d_flipflop(hdl):
    """Convert d_flipflop block to Verilog or VHDL"""
    clock = Signal(bool(0))
    set = Signal(bool(1))
    reset = Signal(bool(1))
    d = Signal(bool(0))
    q = Signal(bool(0))
    inst = DFlipFlop(clock, set, reset, d, q)
    inst.convert(hdl=hdl)

