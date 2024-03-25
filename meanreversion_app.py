import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def index():
    # Read data
    file_path = 'GOOGL.csv'
    data = pd.read_csv(file_path)

    # Calculate moving average
    prices = data['Close']
    mu = [prices[:i].mean() for i in range(len(prices))]

    # Calculate z-scores
    z_scores = [(prices[i] - mu[i]) / np.std(prices[:i])
                for i in range(len(prices))]

    # Perform mean reversion strategy
    money = 0
    count = 0
    for i in range(len(prices)):
        # Sell short if the z-score is > 1
        if z_scores[i] > 1:
            money += prices[i]
            count -= 1
        # Buy long if the z-score is < -1
        elif z_scores[i] < -1:
            money -= prices[i]
            count += 1
        # Clear positions if the z-score between -0.5 and 0.5
        elif abs(z_scores[i]) < 0.5:
            money += count*prices[i]
            count = 0

    return render_template('index.html', money=money)


if __name__ == '__main__':
    app.run(port=5001)
