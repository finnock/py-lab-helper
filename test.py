import numpy as np
import pandas
from scipy import interpolate
import matplotlib.pyplot as plt
import pandas as pd

df = pandas.DataFrame({
    'pot': [1,2,3,4,5,6,7,8,9],
    'cur': [1,2,3,4,5,6,7,8,9],
    'cycle': 1
})