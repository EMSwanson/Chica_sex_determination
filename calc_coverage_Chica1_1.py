import pandas as pd
import numpy as np

Chica1_1 = pd.read_table('depth_Chica1_1.dep',header=None)
Chica1_1.columns = ["Scaff","Count","Coverage"]

means = Chica1_1.groupby('Scaff').mean()
means1 = means.ix[:,["Coverage"]]
means1.columns = ["meanCoverage"]

sds = Chica1_1.groupby('Scaff').std()
sds1 = sds.ix[:,["Coverage"]]
sds1.columns = ["sdCoverage"]

mean_and_sd = pd.concat([means1,sds1],axis=1)
mean_and_sd.to_csv('Chica1_1_scaff_coverage_means.csv')

