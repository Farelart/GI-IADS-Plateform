import random
import streamlit as st
import numpy as np
from PIL import Image
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from sklearn.decomposition import PCA




def n_imgs(X_transform,n=2):
    col1, col2, col3 = st.columns(3)
    with col1:
        for _ in range(2):
            i=random.randint(0,X_transform.shape[0])
            st.image(X_transform[i], caption="image "+str(_+1), use_column_width=True)
    with col2:
        for _ in range(2):
            i=random.randint(0,X_transform.shape[0])
            st.image(X_transform[i], caption="image "+str(_+3), use_column_width=True)
    with col3:
        for _ in range(2):
            i=random.randint(0,X_transform.shape[0])
            st.image(X_transform[i], caption="image "+str(_+5), use_column_width=True)

def reshape_image(X,height,width,dim):
    X_reshape=[]
    for x in X:
        pil_image = Image.fromarray(x) 
        pil_image = pil_image.resize((height, width), Image.ANTIALIAS)
        if dim==1: 
            pil_image = pil_image.convert('L')
        resized_image = np.array(pil_image)  
        X_reshape.append(resized_image)
    X_transform=np.array(X_reshape)
    return X_transform

def data_aug(X_transform):
    datagen = ImageDataGenerator(rotation_range=20,
                                    shear_range=0.1, 
                                    zoom_range=0.1, 
                                    horizontal_flip=True, 
                                    fill_mode='nearest' 
                                    )
    datagen.fit(X_transform)
    X_transform = datagen.flow(X_transform, batch_size=X_transform.shape[0]).next()
    return X_transform

def pca_transform(X):
    X_transform=X[:,:,:,0]
    X_transform=X_transform/255.0
    X_transform=X_transform.reshape(200,-1)
    pca = PCA(0.99)
    pca.fit(X_transform)
    shape=int(np.sqrt(pca.components_.shape[0]))+1
    pca=PCA(shape**2)
    X_transform=pca.fit_transform(X_transform)
    X_reverse=pca.inverse_transform(X_transform)
    X_transform = X_transform.reshape(X_transform.shape[0], shape, shape,1)
    X_reverse=X_reverse.reshape(X.shape[0],X.shape[1],X.shape[2],1)
    X_reverse = (X_reverse- np.min(X_reverse)) / (np.max(X_reverse) - np.min(X_reverse))
    return X_transform,X_reverse

