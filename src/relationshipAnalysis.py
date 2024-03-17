import csv
import matplotlib.pyplot as plt
from scipy.stats import pearsonr
import numpy as np

def getPrediction(weight, coefficients):
    polyLine = np.poly1d(coefficients)
    return max(polyLine(weight), 0)

weights = []
values = []

with open("data/packs.csv", "r") as file:
    packs = csv.DictReader(file)
    for pack in packs:
        weights.append(float(pack["weight"]))  
        values.append(float(pack["value"]))    

plt.scatter(weights, values)
plt.title('Weight and Value of Pokemon Packs')
plt.xlabel('Weight')
plt.ylabel('Value')

plt.savefig("data/visualizations/raw.png")
plt.close()

q1 = np.percentile(values, 25)
q3 = np.percentile(values, 75)
iqr = q3 - q1

k = 1.5

lower = q1 - k * iqr
upper = q3 + k * iqr

cleanValue = []
cleanWeight = []

for weight, value in zip(weights, values):
    if value >= lower and value <= upper:
        cleanValue.append(value)
        cleanWeight.append(weight)

plt.scatter(cleanWeight, cleanValue)
plt.title('Weight and Value of Pokemon Packs After Removing Outliers')
plt.xlabel('Weight')
plt.ylabel('Value')


coefficients = np.polyfit(cleanWeight, cleanValue, 1)
polyLine = np.poly1d(coefficients)
plt.plot(cleanWeight, polyLine(cleanWeight), color='red')

corr, p = pearsonr(cleanWeight, cleanValue)
plt.annotate('Correlation Coefficient: {:.2f}'.format(corr),
             xy=(0.05, 0.95), xycoords='axes fraction',
             fontsize=10, ha='left', va='top',
             bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="black", lw=1))


plt.savefig("data/visualizations/withoutOutliers.png")
plt.close()



# example usage
w = 20 
predictedValue = getPrediction(w, coefficients)
print("Predicted value for weight {}: {}".format(w, predictedValue))
