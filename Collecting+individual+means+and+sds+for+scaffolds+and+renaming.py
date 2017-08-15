
# coding: utf-8

# In[354]:

import pandas as pd


# In[388]:

import re


# In[355]:

def load_names(x, y):   ###x should be the current drive and y the file of names
    name_list = pd.read_csv(current_drive + file_of_names, header=None)   ##just reads in the name file
    return name_list


# In[356]:

def load_file(current_drive, id_name, suffix_to_use):   
    loaded_id_file = pd.read_csv(current_drive + id_name + suffix_to_use)
    return loaded_id_file


# In[496]:

def loop_plus_cat(current_drive, file_of_names, suffix_to_use):
    fish_name_list = load_names(current_drive, file_of_names)
    fish_name_list = fish_name_list.values.flatten()
    current_file = pd.read_csv(current_drive+fish_name_list[0]+suffix_to_use)
    for i in fish_name_list[1:]:
        new_file = pd.read_csv(current_drive+i+suffix_to_use)
        current_file = current_file.merge(new_file, left_on="Scaff", right_on="Scaff", how="outer")
    return current_file


# In[443]:

def make_names_whole(current_drive, file_of_names):
    fish_name_list = load_names(current_drive, file_of_names)
    fish_name_list = fish_name_list.values.flatten()
    col_names = []
    for i in fish_name_list:
        col_names.append([i,i])
    return col_names


# In[ ]:

def indexing_by_scaff(x):
    to_be_index = x['Scaff']
    x.set_index(to_be_index,inplace=True)
    x.index.names = ["Scaffolds"]
    x = x.iloc[:,1:]
    return(x)


# In[444]:

def comb_names(x,y):   ###Combines the ID name and the column name X is the list of names to add to the beginning of each column name, y is the data frame with the columns
    new_name = []
    for i in range(0,len(x)):
        new_name.append([x[i] + "_" + y.columns[i]])
    return new_name


# In[500]:

def collect_fns():  ###Collects and runs all other functions
    collected_data = loop_plus_cat("C://Users/Owner/OneDrive/School/Data, analyses/ChicaPopGen/Samtools indexing for depth/","fish_name_list.txt","_scaff_coverage_means.csv")
    collected_data_ind = indexing_by_scaff(collected_data)
    dat = make_names_whole("C://Users/Owner/OneDrive/School/Data, analyses/ChicaPopGen/Samtools indexing for depth/","fish_name_list.txt")
    dat = sum(dat,[])   ###Flattens out a list of lists
    new_cols = comb_names(dat,collected_data_ind)
    collected_data_ind.columns = sum(new_cols,[])
    collected_data_ind.rename(columns = lambda x: str(x)[:-2],inplace=True)
    return collected_data_ind


# In[501]:

fin_collected_data = collect_fns()


# In[363]:

fin_collected_data.to_csv("C://Users/Owner/OneDrive/School/Data, analyses/ChicaPopGen/Samtools indexing for depth/mean_and_sd_coverage_combined.csv")

