import matplotlib.pyplot as plt
import numpy as np
import random
import pandas

results = pandas.DataFrame()
for p in range(0,11):
    temp = pandas.DataFrame.from_records({'Index':p, 'Percent':  "{0}/{1}".format(p*10, (10-p)*10), 'Result': random.randint(0, 1)}, index=['Percent'])
    results=pandas.concat([results,temp])
#//print(results)


plt.plot('Percent', 'Result', data=results, marker='x')
plt.show()
