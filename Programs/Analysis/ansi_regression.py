
# coding: utf-8

# # ANSI Application analysis

# In[ ]:


import numpy
import pandas
import matplotlib.pyplot as plotter
from scipy.stats import pearsonr
from sklearn.metrics import mean_squared_error, mean_absolute_error


# In[ ]:


def view_boxplot(df):
    get_ipython().magic('matplotlib')
    df.boxplot()
    plotter.show()


# ## CPU data

# In[ ]:


cpu_df = pandas.read_csv('data/ansi_fake_data/ansi_fake_data_cpu.csv', index_col='Time').drop('Unnamed: 0', axis=1)


# In[ ]:


#cpu_df.columns


# In[ ]:


#view_boxplot(cpu_df)


# ## Network TX

# In[ ]:


txnet_df = pandas.read_csv('data/ansi_fake_data/ansi_fake_data_network_tx.csv', index_col='Time').drop('Unnamed: 0', axis=1)


# In[ ]:


#txnet_df.columns


# In[ ]:


#view_boxplot(txnet_df)


# ## Network RX

# In[ ]:


rxnet_df = pandas.read_csv('data/ansi_fake_data/ansi_fake_data_network_rx.csv', index_col='Time').drop('Unnamed: 0', axis=1)


# In[ ]:


#rxnet_df.columns


# In[ ]:


rxnet_df = rxnet_df.clip(lower=0, upper=15000)
#view_boxplot(rxnet_df)


# ## Disk IO data

# In[ ]:


disk_df = pandas.read_csv('data/ansi_fake_data/ansi_fake_data_disk_io.csv', index_col='Time').drop('Unnamed: 0', axis=1)


# In[ ]:


#disk_df.columns


# In[ ]:


disk_df = disk_df.clip(lower=0, upper=4000)
#view_boxplot(disk_df)


# ## Context switching

# In[ ]:


context_df = pandas.read_csv('data/ansi_fake_data/ansi_fake_data_context.csv', index_col='Time').drop('Unnamed: 0', axis=1)


# In[ ]:


#context_df.columns


# In[ ]:


context_df = context_df.clip(lower=0, upper=5000)
#view_boxplot(context_df)


# ## Seperate into proper dataframes for each node

# In[ ]:


dframes = [cpu_df, txnet_df, rxnet_df, context_df, disk_df]
node = {}

for i in range(1,5):
    frames = []
    
    for dframe in dframes:
        columns = list(filter(lambda x: f'bb{i}l' in x, dframe.columns))
        frames.append(dframe[columns])

    node[i] = pandas.concat(frames, join='inner', axis=1).fillna(0)[:38200]


# In[ ]:


for i in range(1,5):
    print(node[i].shape)
    for column in node[i].columns:
        #node[i][column].hist()
        #plotter.ylabel("Number of data samples")
        #plotter.xlabel("value")
        #plotter.savefig(f"node{i}_{column}_hist.png")
        #plotter.show()
        pass


# ## Get data

# In[ ]:


data_matrices = []

for i in range(1,5):
    data_matrices.append(node[i].as_matrix())
    
data = numpy.vstack(data_matrices)


# In[ ]:


data.shape


# In[ ]:


tdata = data[:,24]
plotter.plot(tdata.T[:100])
plotter.show()
print(data.shape)


# In[ ]:


#data = data[:,24]


# ## Prepare scaler

# In[ ]:


from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import RobustScaler
scaler = MinMaxScaler()


# In[ ]:


scaler.fit(data)
del data


# ---

# ## Correrlation measurement

# ---

# ------

# -----

# # Prediction

# In[ ]:


for i in range(len(data_matrices)):
    
    transformed = scaler.transform(data_matrices[i])
    data_matrices[i] = transformed

X = numpy.stack(data_matrices[:-1], axis=1)
print(data_matrices[3].shape)


# In[ ]:


print(X.shape)
LEN = X.shape[0]
SPLIT = int(0.9*LEN)

train_X = X[:SPLIT,:,:]
val_X = X[SPLIT:SPLIT+1000,:,:]
test_X = X[SPLIT+1000:,:,:]
diff_app_X = data_matrices[3][SPLIT+1000:,:]


# In[ ]:


X = train_X
X = numpy.transpose(X, (1, 0, 2))
val_X = numpy.transpose(val_X, (1, 0, 2))
test_X = numpy.transpose(test_X, (1, 0, 2))


ano_test = test_X[0]
norm_test = test_X[2]
diff_app_test = diff_app_X

print(f"Validation shape is {val_X.shape}")
print(f"Anomaly test shape is {ano_test.shape}")
print(f"Normal test shape is {norm_test.shape}")
print(f"Different app test shape is {diff_app_test.shape}")


# In[ ]:


def flat_generator(X, tsteps = 5, ravel=1):
    i = 0
    
    while True:
        batch_X = X[:,i:i+tsteps,:]
        batch_y = X[:,i+tsteps,:]
            
        if ravel:
            batch_X = batch_X.reshape((batch_X.shape[0], -1))
        #print(batch_X.shape)
        #print(batch_y.shape)
        
        yield batch_X, batch_y
        
        i += 1
        if i > (X.shape[1] - tsteps - 1):
            i = 0
            continue


# ## Flat models

# In[ ]:


from keras.models import Model
from keras.layers import Dense, Input, Dropout, GRU
from keras.callbacks import EarlyStopping


# In[ ]:


def train(model, tgen, vgen, name="none"):
    estopper = EarlyStopping(patience=15, min_delta=0.0001)
    history = model.fit_generator(tgen, steps_per_epoch=1000, epochs=10000, callbacks=[estopper], shuffle=False, validation_data=vgen, validation_steps=1000, verbose=1)
    plotter.plot(history.history['loss'],label='train')
    plotter.plot(history.history['val_loss'],label='validation')
    plotter.legend()
    plotter.xlim(0,150)
    plotter.xlabel("Epochs")
    plotter.ylabel("Error")
    plotter.savefig(f"{name}_train.png", dpi=10000)
    plotter.show()
    print(f"Training loss for final epoch is {history.history['loss'][-1]}")
    print(f"Validation loss for final epoch is {history.history['val_loss'][-1]}")


# In[ ]:


def plot_running_stats(error, window_size=5):
    error = numpy.array(error)
    window = numpy.ones(window_size)/window_size
    running_mean = numpy.convolve(error, window, mode="same")
    
    plotter.plot(error, 'g-', alpha=0.3, label="Error")
    plotter.plot(running_mean, 'r-', alpha=0.9, label="Running mean")
    plotter.ylim(0,0.2)
    plotter.xlabel("time")
    plotter.ylabel("Error")
    plotter.savefig(f"{name}_truetestloss.png", dpi=10000)
    plotter.show()
    error = numpy.array(error)
    print(f"The mean error for {name} is {numpy.mean(error)}")


# In[ ]:


def data_test(model, dataset=test_X[0], ravel=1, write=0, name="none", window=5):
    test_gen = flat_generator(numpy.array([dataset]), TIMESTEPS,0)
    error = []
    targets = []
    preds = []
    for i in range(2000):
        _input,target = next(test_gen)
        targets.append(target.squeeze())
        if ravel:
            _input = _input.ravel()[:,numpy.newaxis].T
            
        pred = model.predict(_input)
        #print(target.shape)
        #print(pred.shape)
        preds.append(pred.squeeze())
        error.append(mean_absolute_error(y_pred=pred, y_true=target))

    targets = numpy.vstack(targets)
    preds = numpy.vstack(preds)
    plot_running_stats(error, window_size=window)
    
    #print(error)


# In[ ]:


def gen_test(model, dataset=test_X[0], ravel=1, write=0, name="none"):
    test_gen = flat_generator(numpy.array([dataset]), TIMESTEPS,0)
    error = []
    targets = []
    preds = []
    for i in range(2000):
        _input,target = next(test_gen)
    
        if i != 0:
            #print(_input.shape)
            _input = _input.squeeze()[1:,:]
            #print(_input.shape)
            _input = numpy.append(pred,_input, axis=0)[numpy.newaxis,:,:]
            #print(_input.shape)
        
        targets.append(target.squeeze())
        if ravel:
            _input = _input.ravel()[:,numpy.newaxis].T
            
        pred = model.predict(_input)
        #print(target.shape)
        #print(pred.shape)
        preds.append(pred.squeeze())
        error.append(mean_absolute_error(y_pred=pred, y_true=target))

    targets = numpy.vstack(targets)
    preds = numpy.vstack(preds)

    plotter.plot(error, 'g-', alpha=0.5)
    plotter.ylim(0,0.2)
    plotter.xlabel("time")
    plotter.ylabel("Error")
    plotter.savefig(f"{name}_testloss.png")
    plotter.show()
    error = numpy.array(error)
    print(numpy.mean(error))
    plotter.boxplot(error)
    plotter.ylim(0,0.2)
    plotter.xlabel("time")
    plotter.ylabel("Error")
    plotter.savefig(f"{name}_boxplot.png")
    plotter.show()
    if write:
        numpy.savetxt('loss.txt', numpy.array(error))
    true_test(model,dataset,ravel=ravel,name=name)
    #print(error)


# In[ ]:


def test(model, ravel=1, name="none", window=2):
    print(f"---------- Beginning tests for {name} ----------")
    print(f"Testing on anomaly data.")
    data_test(model, dataset=ano_test, ravel=ravel, name=(name+"_anomaly_"), window=window)
    print(f"Testing on normal data.")
    data_test(model, dataset=norm_test, ravel=ravel, name=(name+"_normal_"), window=window)
    print(f"Testing on different app data.")
    data_test(model, dataset=diff_app_test, ravel=ravel, name=(name+"_diff_app_"), window=window)
    print("="*20)
    print("\r\n\r\n")


# ### Linear Regression

# #### 2 steps

# In[ ]:


TIMESTEPS = 2
DIM = 29
tgen = flat_generator(X, TIMESTEPS)
vgen = flat_generator(val_X, TIMESTEPS)
name = "lin2"


# In[ ]:


input_layer = Input(shape=(TIMESTEPS*DIM,))
output = Dense(DIM, activation='sigmoid')(input_layer)


# In[ ]:


model = Model(input_layer, output)
model.compile(loss='mean_absolute_error', optimizer='adam', metrics=['mae'])


# In[ ]:


train(model, tgen, vgen, name=name)
test(model, name=name, window=TIMESTEPS)


# #### 5 steps

# In[ ]:


TIMESTEPS = 5
DIM = 29
tgen = flat_generator(X, TIMESTEPS)
vgen = flat_generator(val_X, TIMESTEPS)
name = "lin5"


# In[ ]:


input_layer = Input(shape=(TIMESTEPS*DIM,))
output = Dense(DIM, activation='sigmoid')(input_layer)


# In[ ]:


model = Model(input_layer, output)
model.compile(loss='mean_absolute_error', optimizer='adam', metrics=['mae'])


# In[ ]:


train(model, tgen, vgen, name=name)
test(model, name=name)


# #### 10 steps

# In[ ]:


TIMESTEPS = 10
DIM = 29
tgen = flat_generator(X, TIMESTEPS)
vgen = flat_generator(val_X, TIMESTEPS)
name = "lin10"


# In[ ]:


input_layer = Input(shape=(TIMESTEPS*DIM,))
output = Dense(DIM, activation='sigmoid')(input_layer)


# In[ ]:


model = Model(input_layer, output)
model.compile(loss='mean_absolute_error', optimizer='adam', metrics=['mae'])


# In[ ]:


train(model, tgen, vgen, name=name)
test(model, name=name)


# #### 20 steps

# In[ ]:


TIMESTEPS = 20
DIM = 29
tgen = flat_generator(X, TIMESTEPS)
vgen = flat_generator(val_X, TIMESTEPS)
name = "lin20"


# In[ ]:


input_layer = Input(shape=(TIMESTEPS*DIM,))
output = Dense(DIM, activation='sigmoid')(input_layer)


# In[ ]:


model = Model(input_layer, output)
model.compile(loss='mean_absolute_error', optimizer='adam', metrics=['mae'])


# In[ ]:


train(model, tgen, vgen, name=name)
test(model, name=name)


# #### 50 steps

# In[ ]:


TIMESTEPS = 50
DIM = 29
tgen = flat_generator(X, TIMESTEPS)
vgen = flat_generator(val_X, TIMESTEPS)
name = "lin50"


# In[ ]:


input_layer = Input(shape=(TIMESTEPS*DIM,))
output = Dense(DIM, activation='sigmoid')(input_layer)


# In[ ]:


model = Model(input_layer, output)
model.compile(loss='mean_absolute_error', optimizer='adam', metrics=['mae'])


# In[ ]:


train(model, tgen, vgen, name=name)
test(model, name=name)


# ### NN with 1 hidden layer

# #### 2 steps

# In[ ]:


TIMESTEPS = 2
DIM = 29
tgen = flat_generator(X, TIMESTEPS)
vgen = flat_generator(val_X, TIMESTEPS)
name = "nn1_2"


# In[ ]:


input_layer = Input(shape=(TIMESTEPS*DIM,))
hidden = Dense(100, activation='relu')(input_layer)
output = Dense(DIM, activation='sigmoid')(hidden)


# In[ ]:


model = Model(input_layer, output)
model.compile(loss='mean_absolute_error', optimizer='adam', metrics=['mae'])


# In[ ]:


train(model, tgen, vgen, name=name)
test(model, name=name)


# #### 5 steps

# In[ ]:


TIMESTEPS = 5
DIM = 29
tgen = flat_generator(X, TIMESTEPS)
vgen = flat_generator(val_X, TIMESTEPS)
name = "nn1_5"


# In[ ]:


input_layer = Input(shape=(TIMESTEPS*DIM,))
hidden = Dense(100, activation='relu')(input_layer)
output = Dense(DIM, activation='sigmoid')(hidden)


# In[ ]:


model = Model(input_layer, output)
model.compile(loss='mean_absolute_error', optimizer='adam', metrics=['mae'])


# In[ ]:


train(model, tgen, vgen, name=name)
test(model, name=name)


# #### 10 steps

# In[ ]:


TIMESTEPS = 10
DIM = 29
tgen = flat_generator(X, TIMESTEPS)
vgen = flat_generator(val_X, TIMESTEPS)
name = "nn1_10"


# In[ ]:


input_layer = Input(shape=(TIMESTEPS*DIM,))
hidden = Dense(100, activation='relu')(input_layer)
output = Dense(DIM, activation='sigmoid')(hidden)


# In[ ]:


model = Model(input_layer, output)
model.compile(loss='mean_absolute_error', optimizer='adam', metrics=['mae'])


# In[ ]:


train(model, tgen, vgen, name=name)
test(model, name=name)


# #### 20 steps

# In[ ]:


TIMESTEPS = 20
DIM = 29
tgen = flat_generator(X, TIMESTEPS)
vgen = flat_generator(val_X, TIMESTEPS)
name = "nn1_20"


# In[ ]:


input_layer = Input(shape=(TIMESTEPS*DIM,))
hidden = Dense(100,activation='relu')(input_layer)
output = Dense(DIM, activation='sigmoid')(hidden)


# In[ ]:


model = Model(input_layer, output)
model.compile(loss='mean_absolute_error', optimizer='adam', metrics=['mae'])


# In[ ]:


train(model, tgen, vgen, name=name)
test(model, name=name)


# #### 50 steps

# In[ ]:


TIMESTEPS = 50
DIM = 29
tgen = flat_generator(X, TIMESTEPS)
vgen = flat_generator(val_X, TIMESTEPS)
name = "nn1_50"


# In[ ]:


input_layer = Input(shape=(TIMESTEPS*DIM,))
hidden = Dense(100,activation='relu')(input_layer)
output = Dense(DIM, activation='sigmoid')(hidden)


# In[ ]:


model = Model(input_layer, output)
model.compile(loss='mean_absolute_error', optimizer='adam', metrics=['mae'])


# In[ ]:


train(model, tgen, vgen, name=name)
test(model, name=name)


# ### NN with 2 hidden layers

# #### 2 steps

# In[ ]:


TIMESTEPS = 2
DIM = 29
tgen = flat_generator(X, TIMESTEPS)
vgen = flat_generator(val_X, TIMESTEPS)
name = "nn2_2"


# In[ ]:


input_layer = Input(shape=(TIMESTEPS*DIM,))
hidden = Dense(500, activation='relu')(input_layer)
hidden = Dense(100, activation='relu')(hidden)
output = Dense(DIM, activation='sigmoid')(hidden)


# In[ ]:


model = Model(input_layer, output)
model.compile(loss='mean_absolute_error', optimizer='adam', metrics=['mae'])


# In[ ]:


train(model, tgen, vgen, name=name)
test(model, name=name)


# #### 5 steps

# In[ ]:


TIMESTEPS = 5
DIM = 29
tgen = flat_generator(X, TIMESTEPS)
vgen = flat_generator(val_X, TIMESTEPS)
name = "nn2_5"


# In[ ]:


input_layer = Input(shape=(TIMESTEPS*DIM,))
hidden = Dense(500, activation='relu')(input_layer)
hidden = Dense(100, activation='relu')(hidden)
output = Dense(DIM, activation='sigmoid')(hidden)


# In[ ]:


model = Model(input_layer, output)
model.compile(loss='mean_absolute_error', optimizer='adam', metrics=['mae'])


# In[ ]:


train(model, tgen, vgen, name=name)
test(model, name=name)


# #### 10 steps

# In[ ]:


TIMESTEPS = 10
DIM = 29
tgen = flat_generator(X, TIMESTEPS)
vgen = flat_generator(val_X, TIMESTEPS)
name = "nn2_10"


# In[ ]:


input_layer = Input(shape=(TIMESTEPS*DIM,))
hidden = Dense(500, activation='relu')(input_layer)
hidden = Dense(100, activation='relu')(hidden)
output = Dense(DIM, activation='sigmoid')(hidden)


# In[ ]:


model = Model(input_layer, output)
model.compile(loss='mean_absolute_error', optimizer='adam', metrics=['mae'])


# In[ ]:


train(model, tgen, vgen, name=name)
test(model, name=name)


# #### 20 steps

# In[ ]:


TIMESTEPS = 20
DIM = 29
tgen = flat_generator(X, TIMESTEPS)
vgen = flat_generator(val_X, TIMESTEPS)
name = "nn2_20"


# In[ ]:


input_layer = Input(shape=(TIMESTEPS*DIM,))
hidden = Dense(500, activation='relu')(input_layer)
hidden = Dense(100, activation='relu')(hidden)
output = Dense(DIM, activation='sigmoid')(hidden)


# In[ ]:


model = Model(input_layer, output)
model.compile(loss='mean_absolute_error', optimizer='adam', metrics=['mae'])


# In[ ]:


train(model, tgen, vgen, name=name)
test(model, name=name)


# #### 50 steps

# In[ ]:


TIMESTEPS = 50
DIM = 29
tgen = flat_generator(X, TIMESTEPS)
vgen = flat_generator(val_X, TIMESTEPS)
name = "nn2_50"


# In[ ]:


input_layer = Input(shape=(TIMESTEPS*DIM,))
hidden = Dense(500, activation='relu')(input_layer)
hidden = Dense(100, activation='relu')(hidden)
output = Dense(DIM, activation='sigmoid')(hidden)


# In[ ]:


model = Model(input_layer, output)
model.compile(loss='mean_absolute_error', optimizer='adam', metrics=['mae'])


# In[ ]:


train(model, tgen, vgen, name=name)
test(model, name=name)


# ### NN with 3 hidden layers

# #### 2 steps

# In[ ]:


TIMESTEPS = 2
DIM = 29
tgen = flat_generator(X, TIMESTEPS)
vgen = flat_generator(val_X, TIMESTEPS)
name = "nn3_2"


# In[ ]:


input_layer = Input(shape=(TIMESTEPS*DIM,))
hidden = Dense(1000, activation='relu')(input_layer)
hidden = Dense(500, activation='relu')(hidden)
hidden = Dense(100, activation='relu')(hidden)
output = Dense(DIM, activation='sigmoid')(hidden)


# In[ ]:


model = Model(input_layer, output)
model.compile(loss='mean_absolute_error', optimizer='adam', metrics=['mae'])


# In[ ]:


train(model, tgen, vgen, name=name)
test(model, name=name)


# #### 5 steps

# In[ ]:


TIMESTEPS = 5
DIM = 29
tgen = flat_generator(X, TIMESTEPS)
vgen = flat_generator(val_X, TIMESTEPS)
name = "nn3_5"


# In[ ]:


input_layer = Input(shape=(TIMESTEPS*DIM,))
hidden = Dense(1000, activation='relu')(input_layer)
hidden = Dense(500, activation='relu')(hidden)
hidden = Dense(100, activation='relu')(hidden)
output = Dense(DIM, activation='sigmoid')(hidden)


# In[ ]:


model = Model(input_layer, output)
model.compile(loss='mean_absolute_error', optimizer='adam', metrics=['mae'])


# In[ ]:


train(model, tgen, vgen, name=name)
test(model, name=name)


# #### 10 steps

# In[ ]:


TIMESTEPS = 10
DIM = 29
tgen = flat_generator(X, TIMESTEPS)
vgen = flat_generator(val_X, TIMESTEPS)
name = "nn3_10"


# In[ ]:


input_layer = Input(shape=(TIMESTEPS*DIM,))
hidden = Dense(1000, activation='relu')(input_layer)
hidden = Dense(500, activation='relu')(hidden)
hidden = Dense(100, activation='relu')(hidden)
output = Dense(DIM, activation='sigmoid')(hidden)


# In[ ]:


model = Model(input_layer, output)
model.compile(loss='mean_absolute_error', optimizer='adam', metrics=['mae'])


# In[ ]:


train(model, tgen, vgen, name=name)
test(model, name=name)


# #### 20 steps

# In[ ]:


TIMESTEPS = 20
DIM = 29
tgen = flat_generator(X, TIMESTEPS)
vgen = flat_generator(val_X, TIMESTEPS)
name = "nn3_20"


# In[ ]:


input_layer = Input(shape=(TIMESTEPS*DIM,))
hidden = Dense(1000, activation='relu')(input_layer)
hidden = Dense(500, activation='relu')(hidden)
hidden = Dense(100, activation='relu')(hidden)
output = Dense(DIM, activation='sigmoid')(hidden)


# In[ ]:


model = Model(input_layer, output)
model.compile(loss='mean_absolute_error', optimizer='adam', metrics=['mae'])


# In[ ]:


train(model, tgen, vgen, name=name)
test(model, name=name)


# #### 50 steps

# In[ ]:


TIMESTEPS = 50
DIM = 29
tgen = flat_generator(X, TIMESTEPS)
vgen = flat_generator(val_X, TIMESTEPS)
name = "nn3_50"


# In[ ]:


input_layer = Input(shape=(TIMESTEPS*DIM,))
hidden = Dense(1000, activation='relu')(input_layer)
hidden = Dense(500, activation='relu')(hidden)
hidden = Dense(100, activation='relu')(hidden)
output = Dense(DIM, activation='sigmoid')(hidden)


# In[ ]:


model = Model(input_layer, output)
model.compile(loss='mean_absolute_error', optimizer='adam', metrics=['mae'])


# In[ ]:


train(model, tgen, vgen, name=name)
test(model, name=name)


# ### RNN with 1 GRU layers

# #### 2 steps

# In[ ]:


TIMESTEPS = 2
DIM = 29
tgen = flat_generator(X, TIMESTEPS,0)
vgen = flat_generator(val_X, TIMESTEPS,0)
name = "gru1_2"


# In[ ]:


input_layer = Input(shape=(TIMESTEPS,DIM))
hidden = GRU(10, activation='relu')(input_layer)
output = Dense(DIM, activation='sigmoid')(hidden)


# In[ ]:


model = Model(input_layer, output)
model.compile(loss='mean_absolute_error', optimizer='adam', metrics=['mae'])


# In[ ]:


train(model, tgen, vgen, name=name)
test(model, ravel=0, name=name)


# #### 5 steps

# In[ ]:


TIMESTEPS = 5
DIM = 29
tgen = flat_generator(X, TIMESTEPS,0)
vgen = flat_generator(val_X, TIMESTEPS, 0)
name = "gru1_5"


# In[ ]:


input_layer = Input(shape=(TIMESTEPS,DIM))
hidden = GRU(10, activation='relu')(input_layer)
output = Dense(DIM, activation='sigmoid')(hidden)


# In[ ]:


model = Model(input_layer, output)
model.compile(loss='mean_absolute_error', optimizer='adam', metrics=['mae'])


# In[ ]:


train(model, tgen, vgen, name=name)
test(model, ravel=0, name=name)


# #### 10 steps

# In[ ]:


TIMESTEPS = 10
DIM = 29
tgen = flat_generator(X, TIMESTEPS, 0)
vgen = flat_generator(val_X, TIMESTEPS, 0)
name = "gru1_10"


# In[ ]:


input_layer = Input(shape=(TIMESTEPS,DIM))
hidden = GRU(10, activation='relu')(input_layer)
output = Dense(DIM, activation='sigmoid')(hidden)


# In[ ]:


model = Model(input_layer, output)
model.compile(loss='mean_absolute_error', optimizer='adam', metrics=['mae'])


# In[ ]:


train(model, tgen, vgen, name=name)
test(model, ravel=0, name=name)


# #### 20 steps

# In[ ]:


TIMESTEPS = 20
DIM = 29
tgen = flat_generator(X, TIMESTEPS,0)
vgen = flat_generator(val_X, TIMESTEPS,0)
name = "gru1_20"


# In[ ]:


input_layer = Input(shape=(TIMESTEPS,DIM))
hidden = GRU(10, activation='relu')(input_layer)
output = Dense(DIM, activation='sigmoid')(hidden)


# In[ ]:


model = Model(input_layer, output)
model.compile(loss='mean_absolute_error', optimizer='adam', metrics=['mae'])


# In[ ]:


train(model, tgen, vgen, name=name)
test(model, ravel=0, name=name)


# #### 50 steps

# In[ ]:


TIMESTEPS = 50
DIM = 29
tgen = flat_generator(X, TIMESTEPS,0)
vgen = flat_generator(val_X, TIMESTEPS,0)
name = "gru1_50"


# In[ ]:


input_layer = Input(shape=(TIMESTEPS,DIM))
hidden = GRU(10, activation='relu')(input_layer)
output = Dense(DIM, activation='sigmoid')(hidden)


# In[ ]:


model = Model(input_layer, output)
model.compile(loss='mean_absolute_error', optimizer='adam', metrics=['mae'])


# In[ ]:


train(model, tgen, vgen, name=name)
test(model, ravel=0, name=name)


# ### RNN with 2 GRU layers

# #### 2 steps

# In[ ]:


TIMESTEPS = 2
DIM = 29
tgen = flat_generator(X, TIMESTEPS,0)
vgen = flat_generator(val_X, TIMESTEPS,0)
name = "gru2_2"


# In[ ]:


input_layer = Input(shape=(TIMESTEPS,DIM))
hidden = GRU(10, activation='relu', return_sequences=True)(input_layer)
hidden = GRU(10, activation='relu')(hidden)
output = Dense(DIM, activation='sigmoid')(hidden)


# In[ ]:


model = Model(input_layer, output)
model.compile(loss='mean_absolute_error', optimizer='adam', metrics=['mae'])


# In[ ]:


train(model, tgen, vgen, name=name)
test(model, ravel=0, name=name)


# #### 5 steps

# In[ ]:


TIMESTEPS = 5
DIM = 29
tgen = flat_generator(X, TIMESTEPS,0)
vgen = flat_generator(val_X, TIMESTEPS, 0)
name = "gru2_5"


# In[ ]:


input_layer = Input(shape=(TIMESTEPS,DIM))
hidden = GRU(10, activation='relu', return_sequences=True)(input_layer)
hidden = GRU(10, activation='relu')(hidden)
output = Dense(DIM, activation='sigmoid')(hidden)


# In[ ]:


model = Model(input_layer, output)
model.compile(loss='mean_absolute_error', optimizer='adam', metrics=['mae'])


# In[ ]:


train(model, tgen, vgen, name=name)
test(model, ravel=0, name=name)


# #### 10 steps

# In[ ]:


TIMESTEPS = 10
DIM = 29
tgen = flat_generator(X, TIMESTEPS, 0)
vgen = flat_generator(val_X, TIMESTEPS, 0)
name = "gru2_10"


# In[ ]:


input_layer = Input(shape=(TIMESTEPS,DIM))
hidden = GRU(10, activation='relu', return_sequences=True)(input_layer)
hidden = GRU(10, activation='relu')(hidden)
output = Dense(DIM, activation='sigmoid')(hidden)


# In[ ]:


model = Model(input_layer, output)
model.compile(loss='mean_absolute_error', optimizer='adam', metrics=['mae'])


# In[ ]:


train(model, tgen, vgen, name=name)
test(model, ravel=0, name=name)


# #### 20 steps

# In[ ]:


TIMESTEPS = 20
DIM = 29
tgen = flat_generator(X, TIMESTEPS,0)
vgen = flat_generator(val_X, TIMESTEPS,0)
name = "gru2_20"


# In[ ]:


input_layer = Input(shape=(TIMESTEPS,DIM))
hidden = GRU(10, activation='relu', return_sequences=True)(input_layer)
hidden = GRU(10, activation='relu')(hidden)
output = Dense(DIM, activation='sigmoid')(hidden)


# In[ ]:


model = Model(input_layer, output)
model.compile(loss='mean_absolute_error', optimizer='adam', metrics=['mae'])


# In[ ]:


train(model, tgen, vgen, name=name)
test(model, ravel=0, name=name)


# #### 50 steps

# In[ ]:


TIMESTEPS = 50
DIM = 29
tgen = flat_generator(X, TIMESTEPS,0)
vgen = flat_generator(val_X, TIMESTEPS,0)
name = "gru2_50"


# In[ ]:


input_layer = Input(shape=(TIMESTEPS,DIM))
hidden = GRU(10, activation='relu', return_sequences=True)(input_layer)
hidden = GRU(10, activation='relu')(hidden)
output = Dense(DIM, activation='sigmoid')(hidden)


# In[ ]:


model = Model(input_layer, output)
model.compile(loss='mean_absolute_error', optimizer='adam', metrics=['mae'])


# In[ ]:


train(model, tgen, vgen, name=name)
test(model, ravel=0, name=name)


# ### RNN with 3 GRU layers

# #### 2 steps

# In[ ]:


TIMESTEPS = 2
DIM = 29
tgen = flat_generator(X, TIMESTEPS,0)
vgen = flat_generator(val_X, TIMESTEPS,0)
name = "gru3_2"


# In[ ]:


input_layer = Input(shape=(TIMESTEPS,DIM))
hidden = GRU(10, activation='relu', return_sequences=True)(input_layer)
hidden = GRU(10, activation='relu', return_sequences=True)(hidden)
hidden = GRU(10, activation='relu')(hidden)
output = Dense(DIM, activation='sigmoid')(hidden)


# In[ ]:


model = Model(input_layer, output)
model.compile(loss='mean_absolute_error', optimizer='adam', metrics=['mae'])


# In[ ]:


train(model, tgen, vgen, name=name)
test(model, ravel=0, name=name)


# #### 5 steps

# In[ ]:


TIMESTEPS = 5
DIM = 29
tgen = flat_generator(X, TIMESTEPS, 0)
vgen = flat_generator(val_X, TIMESTEPS, 0)
name = "gru3_5"


# In[ ]:


input_layer = Input(shape=(TIMESTEPS,DIM))
hidden = GRU(10, activation='relu', return_sequences=True)(input_layer)
hidden = GRU(10, activation='relu', return_sequences=True)(hidden)
hidden = GRU(10, activation='relu')(hidden)
output = Dense(DIM, activation='sigmoid')(hidden)


# In[ ]:


model = Model(input_layer, output)
model.compile(loss='mean_absolute_error', optimizer='adam', metrics=['mae'])


# In[ ]:


train(model, tgen, vgen, name=name)
test(model, ravel=0, name=name)


# #### 10 steps

# In[ ]:


TIMESTEPS = 10
DIM = 29
tgen = flat_generator(X, TIMESTEPS, 0)
vgen = flat_generator(val_X, TIMESTEPS, 0)
name = "gru3_10"


# In[ ]:


input_layer = Input(shape=(TIMESTEPS,DIM))
hidden = GRU(10, activation='relu', return_sequences=True)(input_layer)
hidden = GRU(10, activation='relu', return_sequences=True)(hidden)
hidden = GRU(10, activation='relu')(hidden)
output = Dense(DIM, activation='sigmoid')(hidden)


# In[ ]:


model = Model(input_layer, output)
model.compile(loss='mean_absolute_error', optimizer='adam', metrics=['mae'])


# In[ ]:


train(model, tgen, vgen, name=name)
test(model, ravel=0, name=name)


# #### 20 steps

# In[ ]:


TIMESTEPS = 20
DIM = 29
tgen = flat_generator(X, TIMESTEPS,0)
vgen = flat_generator(val_X, TIMESTEPS,0)
name = "gru3_20"


# In[ ]:


input_layer = Input(shape=(TIMESTEPS,DIM))
hidden = GRU(10, activation='relu', return_sequences=True)(input_layer)
hidden = GRU(10, activation='relu', return_sequences=True)(hidden)
hidden = GRU(10, activation='relu')(hidden)
output = Dense(DIM, activation='sigmoid')(hidden)


# In[ ]:


model = Model(input_layer, output)
model.compile(loss='mean_absolute_error', optimizer='adam', metrics=['mae'])


# In[ ]:


train(model, tgen, vgen, name=name)
test(model, ravel=0, name=name)


# #### 50 steps

# In[ ]:


TIMESTEPS = 50
DIM = 29
tgen = flat_generator(X, TIMESTEPS,0)
vgen = flat_generator(val_X, TIMESTEPS,0)
name = "gru3_50"


# In[ ]:


input_layer = Input(shape=(TIMESTEPS,DIM))
hidden = GRU(10, activation='relu', return_sequences=True)(input_layer)
hidden = GRU(10, activation='relu', return_sequences=True)(hidden)
hidden = GRU(10, activation='relu')(hidden)
output = Dense(DIM, activation='sigmoid')(hidden)


# In[ ]:


model = Model(input_layer, output)
model.compile(loss='mean_absolute_error', optimizer='adam', metrics=['mae'])


# In[ ]:


train(model, tgen, vgen, name=name)
test(model, ravel=0, name=name)


# ### RNN with 4 GRU layers dim compression.

# #### 2 steps

# In[ ]:


TIMESTEPS = 2
DIM = 29
tgen = flat_generator(X, TIMESTEPS,0)
vgen = flat_generator(val_X, TIMESTEPS,0)
name = "gru4_2"


# In[ ]:


input_layer = Input(shape=(TIMESTEPS,DIM))
hidden = GRU(10, activation='relu', return_sequences=True)(input_layer)
hidden = GRU(7, activation='relu', return_sequences=True)(hidden)
hidden = GRU(5, activation='relu', return_sequences=True)(hidden)
hidden = GRU(DIM, activation='relu')(hidden)
output = Dense(DIM, activation='sigmoid')(hidden)


# In[ ]:


model = Model(input_layer, output)
model.compile(loss='mean_absolute_error', optimizer='adam', metrics=['mae'])


# In[ ]:


train(model, tgen, vgen, name=name)
test(model, ravel=0, name=name)


# #### 5 steps

# In[ ]:


TIMESTEPS = 5
DIM = 29
tgen = flat_generator(X, TIMESTEPS,0)
vgen = flat_generator(val_X, TIMESTEPS, 0)
name = "gru4_5"


# In[ ]:


input_layer = Input(shape=(TIMESTEPS,DIM))
hidden = GRU(10, activation='relu', return_sequences=True)(input_layer)
hidden = GRU(7, activation='relu', return_sequences=True)(hidden)
hidden = GRU(5, activation='relu', return_sequences=True)(hidden)
hidden = GRU(DIM, activation='relu')(hidden)
output = Dense(DIM, activation='sigmoid')(hidden)


# In[ ]:


model = Model(input_layer, output)
model.compile(loss='mean_absolute_error', optimizer='adam', metrics=['mae'])


# In[ ]:


train(model, tgen, vgen, name=name)
test(model, ravel=0, name=name)


# #### 10 steps

# In[ ]:


TIMESTEPS = 10
DIM = 29
tgen = flat_generator(X, TIMESTEPS, 0)
vgen = flat_generator(val_X, TIMESTEPS, 0)
name = "gru4_10"


# In[ ]:


input_layer = Input(shape=(TIMESTEPS,DIM))
hidden = GRU(10, activation='relu', return_sequences=True)(input_layer)
hidden = GRU(7, activation='relu', return_sequences=True)(hidden)
hidden = GRU(5, activation='relu', return_sequences=True)(hidden)
hidden = GRU(DIM, activation='relu')(hidden)
output = Dense(DIM, activation='sigmoid')(hidden)


# In[ ]:


model = Model(input_layer, output)
model.compile(loss='mean_absolute_error', optimizer='adam', metrics=['mae'])


# In[ ]:


train(model, tgen, vgen, name=name)
test(model, ravel=0, name=name)


# #### 20 steps

# In[ ]:


TIMESTEPS = 20
DIM = 29
tgen = flat_generator(X, TIMESTEPS,0)
vgen = flat_generator(val_X, TIMESTEPS,0)
name = "gru4_20"


# In[ ]:


input_layer = Input(shape=(TIMESTEPS,DIM))
hidden = GRU(10, activation='relu', return_sequences=True)(input_layer)
hidden = GRU(7, activation='relu', return_sequences=True)(hidden)
hidden = GRU(5, activation='relu', return_sequences=True)(hidden)
hidden = GRU(DIM, activation='relu')(hidden)
output = Dense(DIM, activation='sigmoid')(hidden)


# In[ ]:


model = Model(input_layer, output)
model.compile(loss='mean_absolute_error', optimizer='adam', metrics=['mae'])


# In[ ]:


train(model, tgen, vgen, name=name)
test(model, ravel=0, name=name)


# #### 50 steps

# In[ ]:


TIMESTEPS = 50
DIM = 29
tgen = flat_generator(X, TIMESTEPS,0)
vgen = flat_generator(val_X, TIMESTEPS,0)
name = "gru4_50"


# In[ ]:


input_layer = Input(shape=(TIMESTEPS,DIM))
hidden = GRU(10, activation='relu', return_sequences=True)(input_layer)
hidden = GRU(7, activation='relu', return_sequences=True)(hidden)
hidden = GRU(5, activation='relu', return_sequences=True)(hidden)
hidden = GRU(DIM, activation='relu')(hidden)
output = Dense(DIM, activation='sigmoid')(hidden)


# In[ ]:


model = Model(input_layer, output)
model.compile(loss='mean_absolute_error', optimizer='adam', metrics=['mae'])


# In[ ]:


train(model, tgen, vgen, name=name)
test(model, ravel=0, name=name)

