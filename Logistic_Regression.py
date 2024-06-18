import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LogisticRegression

# Define the data
X = np.array([[0.50, 0.75, 1.00, 1.25, 1.50, 1.75, 1.75, 2.00, 2.25, 2.50, 
               2.75, 3.00, 3.25, 3.50, 4.00, 4.25, 4.50, 4.75, 5.00, 5.50]]).T
y = np.array([0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1])

# Create and fit the model
clf = LogisticRegression().fit(X, y)

# Print the coefficients and intercept
print("Coefficients:", clf.coef_)
print("Intercept:", clf.intercept_)

# Plot the data points
plt.scatter(X, y, color='blue', label='Data points')

# Plot the logistic regression curve
X_test = np.linspace(0, 6, 300).reshape(-1, 1)
y_prob = clf.predict_proba(X_test)[:, 1]
plt.plot(X_test, y_prob, color='red', linewidth=2, label='Logistic Regression Curve')

# Labels and title
plt.xlabel('X')
plt.ylabel('Probability')
plt.title('Logistic Regression Fit')
plt.legend()

# Show plot
plt.show()
