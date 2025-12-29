import unittest

from idsf import compute_inclusivity
from fuzzy_system_clarity import compute_clarity
from fuzzy_system_accessibility import compute_accessibility
from fuzzy_system_navigation import compute_navigation
from fuzzy_system_fairness import compute_fairness

class TestInclusivityFuzzySystem(unittest.TestCase):

    ## =========================================================================
    ## Part 1: BLACK BOX TESTS (End-to-End functional szenarios)
    ## Test whole system with inputs (0-5) till output (0-100)
    ## =========================================================================

    def test_bb_ideal_scenario(self):
        """Black Box: all inputs are perfect (5.0). Expecting: > 80 (Really inclusive)."""
        c = compute_clarity(5, 5, 5, 5)
        a = compute_accessibility(5, 5, 5, 5)
        n = compute_navigation(5, 5, 5, 5)
        f = compute_fairness(5, 5, 5, 5)
        
        result = compute_inclusivity(c, a, n, f)
        self.assertGreaterEqual(result, 80, f"Expecting really inclusive with point higher then 80, we got: {result}")

    def test_bb_worst_scenario(self):
        """Black Box: all inputs are 0. Expecting: < 50 (Not inclusive enough)."""
        c = compute_clarity(0, 0, 0, 0)
        a = compute_accessibility(0, 0, 0, 0)
        n = compute_navigation(0, 0, 0, 0)
        f = compute_fairness(0, 0, 0, 0)
        
        result = compute_inclusivity(c, a, n, f)
        self.assertLessEqual(result, 50, f"Expecting not inclusive enough and therefore score under 50, we got: {result}")

    def test_bb_average_scenario(self):
        """Black Box: all average iputs (2.5). Expecting: Point in field 30-70."""
        val = 2.5
        c = compute_clarity(val, val, val, val)
        a = compute_accessibility(val, val, val, val)
        n = compute_navigation(val, val, val, val)
        f = compute_fairness(val, val, val, val)
        
        result = compute_inclusivity(c, a, n, f)
        self.assertTrue(30 <= result <= 100, f"Expecting point in average field, got: {result}")

    def test_bb_mixed_realistic(self):
        """Black Box: Mix (Good, Average, Poor)."""
        # Ein System ist gut, eines schlecht, zwei mittel
        c = compute_clarity(5, 5, 5, 5)       # Good
        a = compute_accessibility(1, 1, 1, 4) # Poor
        n = compute_navigation(5, 5, 5, 5)    # Average
        f = compute_fairness(5, 5, 5, 5)      # Average

        result = compute_inclusivity(c, a, n, f)
        # accessibility is poor and there the overall score should be poor
        self.assertLess(result, 70, f"if accessibility is poor then public service is not inclusive enough with {result}.")

    def test_bb_slightly_below_perfect(self):
        """Black Box: Nearly perfect"""
        val = 4.0 # Gut, aber nicht maximal
        c = compute_clarity(val, val, val, val)
        a = compute_accessibility(val, val, val, val)
        n = compute_navigation(val, val, val, val)
        f = compute_fairness(val, val, val, val)
        
        result = compute_inclusivity(c, a, n, f)
        self.assertGreater(result, 50, "Should still be inclusive enough")


    ## =========================================================================
    ## Part 2: WHITE BOX TESTS - IDSF Master System (idsf.py)
    ## Test the rules from  compute_inclusivity (Input 0-100)
    ## =========================================================================

    
    def test_wb_fairness_rule1_really_fair(self):
        """White Box Fairness:  All are 'good' or high 'average'."""
        # Rule 1 triggers 'Really fair' (High output)
        res = compute_inclusivity(50, 50, 50, 50)
        self.assertGreaterEqual(res, 80, "Fairness Rule 1 should yield Really Fair with  > 80.")

    def test_wb_fairness_rule2_fair_enough_mixed(self):
        """White Box Fairness:- Mix from 'good' and 'average'."""
        res = compute_inclusivity(50, 25, 25, 25)
        self.assertTrue(50 <= res <= 100, f"Fairness Rule 2 should yield Far enough with 50 <= res <= 80, it is  {res}")

    def test_wb_fairness_rule3_polarized(self):
        """White Box Fairness: - Strong Polarisation ('good' and 'poor')."""
        res = compute_inclusivity(50, 0, 50, 0)
        self.assertTrue(50 <= res <= 100, f"Fairness Rule 3 (Polarisiert) should be Vale 25 <= res <= 75 it is: {res}")

    def test_wb_fairness_rule4_low_average(self):
        """White Box Fairness:  - Mix aus 'poor' und 'average'."""
        res = compute_inclusivity(25, 0, 25, 0)
        self.assertTrue(50 <= res <= 100, f"Fairness Regel 4 should be fair enough with  value: {res}")

    def test_wb_fairness_rule5_fail(self):
        """White Box Fairness:  - Mehrheit 'poor' -> 'Not fair enough'."""
        res = compute_inclusivity(0, 0, 0, 50)
        self.assertLess(res, 50, "Should not be fair enough with  < 50")


    ## =========================================================================
    ## Part 3: WHITE BOX TESTS - Fairness Subsystem (fuzzy_system_fairness.py)
    ## Substitute for all principles accessibility, clarity, fainress and navigation since all have the five rules.
    ## Inputs are from scala 0-5.
    ## =========================================================================

    def test_wb_fairness_rule1_really_fair(self):
        """White Box Fairness: Regel 1 - All are 'good' or high 'average'."""
        # Rule 1 triggers 'Really fair' (High output)
        res = compute_fairness(5, 5, 5, 5)
        self.assertGreaterEqual(res, 80, "Fairness Rule 1 should yield Really Fair with  > 80.")

    def test_wb_fairness_rule2_fair_enough_mixed(self):
        """White Box Fairness: Regel 2 - Mix from 'good' and 'average'."""
        res = compute_fairness(5, 2.5, 2.5, 2.5)
        self.assertTrue(50 <= res <= 100, f"Fairness Rule 2 should yield Far enough with 50 <= res <= 80, it is  {res}")

    def test_wb_fairness_rule3_polarized(self):
        """White Box Fairness: Regel 3 - Strong Polarisation ('good' and 'poor')."""
        res = compute_fairness(5, 0, 5, 0)
        self.assertTrue(50 <= res <= 100, f"Fairness Rule 3 (Polarisiert) should be Vale 25 <= res <= 75 it is: {res}")

    def test_wb_fairness_rule4_low_average(self):
        """White Box Fairness: Regel 4 - Mix aus 'poor' und 'average'."""
        res = compute_fairness(2.5, 0, 2.5, 0)
        self.assertTrue(50 <= res <= 100, f"Fairness Regel 4 should be fair enough with  value: {res}")

    def test_wb_fairness_rule5_fail(self):
        """White Box Fairness: Regel 5 - Mehrheit 'poor' -> 'Not fair enough'."""
        # Rule 5: (poor & poor & poor) triggert 'Not fair enough'
        res = compute_fairness(0, 0, 0, 5)
        self.assertLess(res, 50, "Should not be fair enough with  < 50")

if __name__ == '__main__':
    unittest.main()