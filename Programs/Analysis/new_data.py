
# coding: utf-8

# # Import Libraries

# In[1]:


import pandas
import numpy

import matplotlib.pyplot as plotter
from sklearn.preprocessing import MinMaxScaler
from sklearn.decomposition import PCA


# In[2]:


scaler = MinMaxScaler()


# In[3]:


cpu_data = pandas.read_csv('feb21_cpu.csv')
net_tx_data = pandas.read_csv('feb21_network_tx.csv')
net_rx_data = pandas.read_csv('feb21_network_rx.csv')
disk_io_data = pandas.read_csv('feb21_disk_io.csv')


# In[4]:


data = pandas.concat([cpu_data, net_rx_data, net_tx_data, disk_io_data], join='inner', axis=1)


# In[5]:


data


# In[6]:


data = data.fillna(0)
print(data.columns)


# In[7]:


data.describe()


# In[8]:


not_bb7 = list(filter(lambda x: 'bb7l' not in x, data.columns))
data = data.drop(['Unnamed: 0','Time'], axis=1)


# In[9]:


data = data.clip(lower=0.0, upper=1000.0)


# In[10]:


data.describe()


# In[11]:


def scale_data(data, fit=0):
    
    if fit:
        scaler.fit(data)
    return scaler.transform(data)


# In[12]:


data = scale_data(data,1)


# In[13]:


plotter.imshow(data[:500].T)


# In[14]:


plotter.show()


# In[15]:


plotter.imshow(data[500:1000].T)


# In[16]:


plotter.show()


# In[17]:


plotter.imshow(data[1000:1500].T)


# In[18]:


plotter.show()


# In[19]:


plotter.imshow(data[1500:2000].T)
plotter.show()


# In[20]:


plotter.imshow(data[2000:2500].T)
plotter.show()


# In[21]:


plotter.imshow(data[2500:3000].T)
plotter.show()


# In[22]:


data.shape


# In[23]:


pca = PCA(n_components=2)
pca.fit(data)


# In[35]:


data_app1 = pca.transform(data[:400])
plotter.scatter(data_app1[:,0], data_app1[:,1], c='b', alpha=0.5, label='file IO')

data_app12 = pca.transform(data[500:1000])
plotter.scatter(data_app12[:,0], data_app12[:,1], c='g', alpha=0.5, label='file IO + DFT')

data_anomaly = pca.transform(data[1400:1700])
plotter.scatter(data_anomaly[:,0], data_anomaly[:,1], marker='x', c='r', label='Power failure')

data_everything = pca.transform(data[2000:2400])
plotter.scatter(data_everything[:,0], data_everything[:,1], c='y', label='file IO + DFT + Broadcast')
plotter.legend()
plotter.show()

