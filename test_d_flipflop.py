#!/usr/bin/env python

import unittest
from myhdl import Simulation, Signal, delay, intbv, bin, traceSignals
from d_flipflop import DFlipFlop
from clock_driver import ClkDriver

class TestClock(unittest.TestCase):

    def test_clock(self):
        """Check that the clock oscillates as expected."""
        def test(clk):
            self.assertEqual(clk, 0)
            yield delay(5)
            for i in range(10):
                self.assertEqual(clk, 0)
                yield delay(10)
                self.assertEqual(clk, 1)
                yield delay(10)
        self.runTests(test)

    def runTests(self, test):
        """Helper method to run the actual tests."""
        clk = Signal(bool(0))
        dut = ClkDriver(clk)
        check = test(clk)
        sim = Simulation(dut, check)
        dut.config_sim(trace=True)
        sim.run(100, quiet=1)
        sim.quit()


class TestDFlipFlop(unittest.TestCase):

    def test_d(self):
        """Check that the synchronous d input is propagated to the output on a rising clock edge."""
        def test(clk, set, rst, d, q):
            # first rising edge is at 10ns
            yield delay(10)
            self.assertEqual(q, 0)
            d.next = 1
            yield delay(1)
            self.assertEqual(q, 1)
            yield delay(4)
            self.assertEqual(q, 1)
            d.next = 0
            yield delay(15)
            self.assertEqual(q, 1)
            yield delay(1)
            self.assertEqual(q, 0)
        self.runTests(test)

    def test_d_opaque(self):
        """Check that the synchronous d input is propagated to the output only on a rising clock edge."""
        def test(clk, set, rst, d, q):
            yield delay(10)
            self.assertEqual(q, 0)
            d.next = 1
            yield delay(1)
            self.assertEqual(q, 1)
            yield delay(4)
            self.assertEqual(q, 1)
            d.next = 0
            self.assertEqual(q, 1)
            yield delay(5)
            d.next = 1
            self.assertEqual(q, 1)
            yield delay(5)
            d.next = 0
            self.assertEqual(q, 1)
            yield delay(5)
            d.next = 1
            self.assertEqual(q, 1)
            yield delay(5)
            self.assertEqual(q, 1)
            yield delay(1)
            self.assertEqual(q, 1)
        self.runTests(test)

    def test_set(self):
        """Check that asynchronous active-low set input sets the flipflop output state to high."""
        def test(clk, set, rst, d, q):
            set.next = 0
            for i in range(20):
                yield delay(5)
                self.assertEqual(q, 1)
        self.runTests(test)

    def test_reset(self):
        """Check that asynchronous active-low reset input resets the flipflop output state to low."""
        def test(clk, set, rst, d, q):
            rst.next = 0
            for i in range(20):
                yield delay(5)
                self.assertEqual(q, 0)
        self.runTests(test)

    def runTests(self, test):
        """Helper method to run the actual tests."""
        clk = Signal(bool(0))
        set = Signal(bool(1))
        rst = Signal(bool(1))
        d = Signal(bool(0))
        q = Signal(bool(0))
        clock_gen = ClkDriver(clk)
        dut = DFlipFlop(clk, set, rst, d, q)
        check = test(clk, set, rst, d, q)
        sim = Simulation(clock_gen, dut, check)
        #sim = Simulation(dut, check)
        dut.config_sim(trace=True)
        sim.run(100, quiet=1)
        sim.quit()


if __name__ == '__main__':
    unittest.main(verbosity=2)
