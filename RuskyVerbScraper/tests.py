import unittest
from RusKeyDataScrape import *

class TestPadThousandsFunction(unittest.TestCase):
    
    def test_pad_Thousands_with_one_character(self):
        result = padThousands("F")
        self.assertEqual(result, "000F")
        
    def test_pad_Thousands_with_two_characters(self):
        result = padThousands("FF")
        self.assertEqual(result, "00FF")
        
    def test_pad_Thousands_with_three_characters(self):
        result = padThousands("FFF")
        self.assertEqual(result, "0FFF")
        
    def test_pad_Thousands_with_four_character(self):
        result = padThousands("FFFF")
        self.assertEqual(result, "FFFF")
        
class TestCountVowels(unittest.TestCase):
    
    def test_vowel_count_zero(self):
        result = countVowels('JjKk')
        self.assertEqual(result, 0)
    
    def test_vowel_count_one(self):
        result = countVowels('JjяKk')
        self.assertEqual(result, 1)
    
    def test_vowel_count_two(self):
        result = countVowels('JjKяяk')
        self.assertEqual(result, 2)
    
    def test_vowel_count_three(self):
        result = countVowels('JЁИОjKk')
        self.assertEqual(result, 3)
    
class TestCheckWordForStress(unittest.TestCase):
    
    def test_check_one_syllable_word_without_stress_returns_false(self):
        result = checkWordForStress('чтобы')
        self.assertFalse(result)
        
    def test_check_word_with_stress_returns_true(self):
        result = checkWordForStress('HellóWorld')
        self.assertTrue(result)
        
    # def test_check_word_for_stress_returns_false_with_no_stress(self):
    #     result = checkWordForStress('FjkL')

if __name__ == '__main__':
    unittest.main()