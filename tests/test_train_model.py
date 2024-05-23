import unittest
from unittest.mock import patch, MagicMock

from src.train import temp_pred_model,humid_pred_model,co2_pred_model,voc_pred_model,pm25_pred_model

class TestTempTrainModel(unittest.TestCase):
    
