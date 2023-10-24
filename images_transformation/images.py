from tensorflow.keras.datasets import cifar10

def data():
    (x_train, y_train), (_, _) = cifar10.load_data()
    return x_train[:200],y_train[:200]