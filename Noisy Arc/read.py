import pandas as pd
filename = "captcha_model.hdf5"

import h5py

# Open the HDF5 file
with h5py.File('captcha_model.hdf5', 'r') as f:
    # List all the keys in the root group
    print(list(f.keys()))

    # Get the dataset with the name 'dataset_name'
    dataset = f[b'optimizer_weights']
    # Get the data from the dataset
    data = dataset[()]
