from joblib import dump, load
import Services
import pandas as pd
import Models
import json

import os
PATH = os.getcwd() + "\\"
print(Services.define_topic(PATH, 'message.txt', False))
