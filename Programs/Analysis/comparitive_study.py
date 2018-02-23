
# coding: utf-8

# ##### Imports

# In[1]:


import pandas
import numpy
import matplotlib.pyplot as plotter

from sklearn.preprocessing import MinMaxScaler


# Define scaling function

# In[2]:


scaler = MinMaxScaler()

def scale_df(dataframe, fit=0):

    if fit:
        scaler.fit(dataframe)

    return scaler.transform(dataframe)


# Get Broadcast data

# In[3]:


bcast_cpu_df = pandas.read_csv('cpu.csv')
bcast_network_tx_df = pandas.read_csv('network_tx.csv')
bcast_network_rx_df = pandas.read_csv('network_rx.csv')
bcast_disk_io_df = pandas.read_csv('disk_io.csv')


# In[4]:


bcast_df = pandas.concat([bcast_cpu_df, bcast_network_tx_df, bcast_network_rx_df, bcast_disk_io_df], join='inner', axis=1)


# In[5]:


bcast_df.head(5)


# In[6]:


bcast_df.shape


# Get No App data

# In[7]:


noapp_cpu_df = pandas.read_csv('no_app_cpu.csv')
noapp_network_tx_df = pandas.read_csv('no_app_network_tx.csv')
noapp_network_rx_df = pandas.read_csv('no_app_network_rx.csv')
noapp_disk_io_df = pandas.read_csv('no_app_disk_io.csv')


# In[8]:


noapp_df = pandas.concat([noapp_cpu_df, noapp_network_tx_df, noapp_network_rx_df, noapp_disk_io_df], join='inner', axis=1)


# In[9]:


noapp_df.head(5)


# In[10]:


noapp_df.shape


# In[11]:


data = pandas.concat([noapp_df, bcast_df], axis=0)


# In[12]:


data.shape


# In[13]:


not_bb1_columns = list(filter(lambda x: 'bb1l' not in x, data.columns))
data = data.drop(['Unnamed: 0','Time'] + not_bb1_columns,1)


# In[14]:


data = data.fillna(0)


# In[15]:


data = scale_df(data,1)


# In[16]:


del data


# #### Only consider BB1 for example plots

# In[17]:


bcast_df = bcast_df.drop(['Unnamed: 0','Time']+ not_bb1_columns,1).fillna(0)
bcast_df.shape
noapp_df = noapp_df.drop(['Unnamed: 0','Time']+ not_bb1_columns,1).fillna(0)
bcast_df = scale_df(bcast_df,0)
noapp_df = scale_df(noapp_df,0)


# ## Write visualisation functions

# ###### Line Plot function

# In[18]:


def line_plot(matrix, start=0, end=100):

    for series in range(matrix.shape[0]):
        plotter.plot(matrix[series,start:end])

    plotter.legend()
    plotter.show()


# ###### Patch display function

# In[19]:


def patch_show(matrix, start=0, end=100):
    plotter.imshow(matrix[:,start:end])
    plotter.show()


# ### Get numpy arrays

# In[20]:


bcast_arr = bcast_df.T
noapp_arr = noapp_df.T
print(bcast_arr.shape)
print(noapp_arr.shape)


# ### Early Plots

# In[21]:


line_plot(bcast_arr)


# In[22]:


line_plot(noapp_arr)


# ### Early middle

# In[23]:


line_plot(bcast_arr,10000,10010)


# In[24]:


line_plot(noapp_arr,10000,10010)


# ### Late plots

# In[25]:


line_plot(bcast_arr,40000,40100)


# In[26]:


line_plot(noapp_arr,40000,40100)


# ### Early Patch

# In[27]:


patch_show(bcast_arr,0,300)


# In[28]:


patch_show(noapp_arr,0,300)


# ### Early Middle

# In[29]:


patch_show(bcast_arr,1000,1300)


# In[30]:


patch_show(noapp_arr,1000,1300)


# ### Late Patch

# In[31]:


patch_show(bcast_arr,40000,40300)


# In[32]:


patch_show(noapp_arr,40000,40300)


# ### Save arrays

# In[37]:


#numpy.save("bcast_arr.npy",bcast_arr)
#numpy.save("noapp_arr.npy",noapp_arr)
