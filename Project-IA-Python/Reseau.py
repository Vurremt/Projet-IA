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

    def load(self, weight, bias):
        self.weight = weight  # Weight
        self.bias = bias  # Bias

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

    def save(self, file):
        file.write("%d %d\n" % (self.input_dimension, self.output_dimension))
        for i in range(self.input_dimension):
            for j in range(self.output_dimension):
                if j != self.output_dimension - 1 : file.write(str(self.weight[i][j]) + " ")
                else : file.write(str(self.weight[i][j]) + "\n")
        for j in range(self.output_dimension):
            if j != self.output_dimension - 1:
                file.write(str(self.bias[j]) + " ")
            else:
                file.write(str(self.bias[j]) + "\n")

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

    def save(self, file):
        pass

# Marche peut etre, pas sur, à n'utiliser qu'avec plus de 1 sortie
class Softmax:
    def __init__(self):
        pass

    def feedforward(self, X):
        e_x = numpy.exp(X - numpy.max(X))
        return e_x / e_x.sum(axis=0)

    def backpropagation(self, X, gradient_Y):
        s = self.feedforward(X)
        S = numpy.diagflat(s) - numpy.outer(s, s)
        gradient_X = numpy.dot(S, gradient_Y)
        return gradient_X

    def update(self, learning_rate):
        pass  # Nothing to do

    def save(self, file):
        pass  # Nothing to do


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

    def save(self, filename):
        with open(filename, 'w') as file:
            line = ""
            for l in self.layers:
                if type(l) == Linear:
                    line += "L "
                elif type(l) == Sigmoid:
                    line += "S "
                elif type(l) == Softmax:
                    line += "M "
                else : exit(1)
            file.write(line.rstrip() + "\n")
            for l in self.layers:
                l.save(file)

    def load(self, filename):
        with open(filename, 'r') as file:
            line = file.readline()
            layers = line.strip("\n").split(' ');
            model = Network()
            neuro_current = 0
            for l in layers :
                if l == "S" :
                    self.addLayer(Sigmoid())

                elif l == "M":
                    self.addLayer(Softmax())

                elif l == "L" :
                    line = file.readline()
                    dimension = line.strip("\n").split(' ');
                    input_dimension = int(dimension[0])
                    output_dimension = int(dimension[1])

                    weight = []
                    bias = []

                    for i in range(input_dimension) :
                        line = file.readline()
                        line_weight = line.strip("\n").split(' ');
                        weight.append([])
                        for l in line_weight :
                            weight[i].append(float(l))

                    line = file.readline()
                    line_bias = line.strip("\n").split(' ');
                    for l in line_bias:
                        bias.append(float(l))

                    self.addLayer(Linear(input_dimension,output_dimension))
                    self.layers[neuro_current].load(numpy.array(weight), numpy.array(bias))

                else :
                    exit(1)
                neuro_current += 1

class Network_RL (Network):
    def __init__(self):
        super().__init__()
        self.states_rewards = list()
        self.states_inputs = list()

    def add_state(self, reward, input):
        self.states_rewards.append(reward)
        self.states_inputs.append(input)
