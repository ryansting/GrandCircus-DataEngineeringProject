# -*- coding: utf-8 -*-
"""Remote Jobs by Site

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/14Gp_WjEl-4HUTwoijHkNnFLJBGiuDKiy
"""

#Remote Jobs vs Local

import pandas as pd
from collections import Counter
import plotly.graph_objs as go
import plotly.express as px

filename = 'Combined_Version_2.csv'
data = pd.read_csv(filename)


df = pd.DataFrame(data)



df = df.query("`Location` == 'Remote'")
df2 = df.groupby('Job Website').count()


print(df2)

fig = px.bar(df2, y='Job Title', labels={}, title ="Indeed Top Skills")



fig.show()