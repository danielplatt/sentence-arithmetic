import unittest
from web_visualisation.activify import activify


def test_activify():
    assert activify('The car is chased by the dog.') == 'the dog chases The car . '
    testcase = unittest.TestCase()
    testcase.assertRaises(ValueError, activify, 'The dog chases the car.')
