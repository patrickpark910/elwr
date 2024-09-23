import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt

# Sample data (replace with your own data)
x_data = np.array([0, 1, 2, 3, 4, 5])
y_data = np.array([2.0, 2.5, 3.5, 5.0, 7.0, 10.0])

# Define the exponential model function
def exponential_model(x, a, b):
    return a * np.exp(b * x)

# Initial guess for parameters a and b
initial_guess = [1.0, 0.1]

# Perform the curve fit
params, covariance = curve_fit(exponential_model, x_data, y_data, p0=initial_guess)

# Extract parameters
a, b = params
print(f"Estimated parameters: a = {a:.4f}, b = {b:.4f}")
print(f"Exponential model: y = {a:.4f} * e^({b:.4f} * x)")

# Calculate predicted y values and R-squared
def calculate_r_squared(y_true, y_pred):
    residuals = y_true - y_pred
    ss_res = np.sum(residuals**2)
    ss_tot = np.sum((y_true - np.mean(y_true))**2)
    r_squared = 1 - (ss_res / ss_tot)
    return r_squared

y_pred = exponential_model(x_data, a, b)
r_squared = calculate_r_squared(y_data, y_pred)
print(f"Coefficient of determination (R^2): {r_squared:.4f}")

# Plot data and fit
plt.scatter(x_data, y_data, label='Data Points', color='blue')
x_fit = np.linspace(min(x_data), max(x_data), 100)
y_fit = exponential_model(x_fit, a, b)
plt.plot(x_fit, y_fit, label='Exponential Fit', color='red')
plt.xlabel('x')
plt.ylabel('y')
plt.title('Direct Exponential Regression')
plt.legend()
plt.show()
