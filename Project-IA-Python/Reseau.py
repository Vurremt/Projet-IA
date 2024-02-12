import numpy
from sklearn.metrics import mean_squared_error
class Linear:
    def __init__(self, input_dimension, output_dimension):
        self.input_dimension = input_dimension  # input dimension
        self.output_dimension = output_dimension  # output dimension
        self.weight = numpy.random.normal(loc=0.0, scale=1.0, size=(input_dimension, output_dimension))  # Weight
        self.bias = numpy.zeros(shape=(output_dimension,))  # Bias
        self.gradient_weight = numpy.zeros(shape=(self.input_dimension, self.output_dimension))  # Weight gradient
        self.gradient_bias = numpy.zeros(shape=(self.output_dimension,))  # Bias gradient

    def feedforward(self, X):
        Y = numpy.matmul(X, self.weight) + self.bias  # Linear transformation
        return Y

    def backpropagation(self, X, gradient_Y):
        self.gradient_bias += gradient_Y  # gradient bias
        self.gradient_weight += numpy.tensordot(X, gradient_Y, axes=0)  # gradient weight

        gradient_X = numpy.matmul(self.weight, gradient_Y)  # gradient X
        return gradient_X

    def update(self, learning_rate):
        self.weight -= learning_rate * self.gradient_weight  # Update weight
        self.bias -= learning_rate * self.gradient_bias  # Update bias

        self.gradient_weight = numpy.zeros(shape=(self.input_dimension, self.output_dimension))  # reset gradient
        self.gradient_bias = numpy.zeros(shape=(self.output_dimension,))  # reset gradient


class Sigmoid:
    def __init__(self):
        pass

    def feedforward(self, X):
        Y = 1 / (1 + numpy.exp(-X))  # sigmoid activation
        return Y

    def backpropagation(self, X, gradient_Y):
        expo = numpy.exp(-X)
        gradient_X = gradient_Y * expo/numpy.square(1+expo) # gradient X
        return gradient_X

    def update(self, learning_rate):
        pass # Nothing to do

class Network:
    def __init__(self):
        self.layers = list()  # List of layers
        self.inputs = list()  # Memorize input

    def addLayer(self, layer):
        self.layers.append(layer)

    def feedforward(self, X):
        self.inputs.clear()  # clear list of inputs
        Input = X  # get first input
        for layer in self.layers:
            self.inputs.append(Input)  # Memorize input
            Input = layer.feedforward(Input)  # get next input

        return Input

    def backpropagation(self, gradient_Y):
        gradient = gradient_Y  # get first gradient
        for i in reversed(range(len(self.layers))):
            X = self.inputs[i]  # Input of layer i
            gradient = self.layers[i].backpropagation(X, gradient)  # get next gradient

    def update(self, learning_rate):
        for layer in self.layers:
            layer.update(learning_rate)  # Update all layers

    def fit(self, xData, yData, epochs, learning_rate):
        for epoch in range(epochs):

            # Compute MSE score
            pred = self.feedforward(xData)
            mse = mean_squared_error(yData, pred)
            print("epoch =", epoch, "score =", mse)

            for i in range(len(xData)):
                X = xData[i]  # Input value
                Y = self.feedforward(X)  # Output value

                target = yData[i]  # target value
                score_gradient = Y - target  # gradient of the score

                self.backpropagation(score_gradient)  # Compute gradients
                self.update(learning_rate)  # udpate