import numpy as np

def sigmoid(yin):
    return 1 / (1 + np.exp(-yin))

def tanh(yin):
    return np.tanh(yin)

def activation(activation_type, yin, theta, off_state):
    if activation_type == 1:
        return 1 if yin >= theta else off_state
    elif activation_type == 2:
        return 1 if sigmoid(yin) >= theta else off_state
    elif activation_type == 3:
        return 1 if tanh(yin) >= theta else off_state

def train(data, n, w, b, alpha, activation_type, theta, max_epochs=10):
    dataset = np.array(data)
    X = dataset[:, :-1]
    T = dataset[:, -1]

    off_state = -1 if -1 in np.unique(T) else 0

    for epoch in range(max_epochs):
        error_count = 0

        for i in range(len(X)):
            x_i = X[i]
            t_i = T[i]

            yin = np.dot(x_i, w) + b
            y = activation(activation_type, yin, theta, off_state)

            if y != t_i:
                w = w + alpha * t_i * x_i
                b = b + alpha * t_i
                error_count += 1

        if error_count == 0:
            return w, b

    return w, b


try:
    data = np.loadtxt("data.txt", dtype=int)

    n = int(input("Enter number of inputs: "))

    w = np.array([float(input(f"w{i+1}: ")) for i in range(n)])

    b = float(input("Enter bias: "))
    alpha = float(input("Enter learning rate: "))

    activation_type = int(input("1.Threshold 2.Sigmoid 3.Tanh: "))
    theta = float(input("Enter threshold: "))

    final_w, final_b = train(data, n, w, b, alpha, activation_type, theta)

    print("Weights:", final_w)
    print("Bias:", final_b)

except Exception as e:
    print("Error:", e)
