import numpy as np 
import matplotlib.pyplot as plt 
from scipy import stats

from sklearn.linear_model import BayesianRidge, LinearRegression

np.random.seed(42)
n_samples ,n_features = 100, 100
X = np.random.randn(n_samples,n_features)

lambda_ = 4. 
w = np.zeros(n_features)
relevant_features = np.random.randint(0,n_features,10)
for i in relevant_features:
    w[i] = stats.norm.rvs(loc=0, scale=1. / np.sqrt(lambda_))
alpha_ = 50
noise = stats.norm.rvs(loc=0, scale=1. / np.sqrt(alpha_),size=n_samples)
y = np.dot(X,w) + noise

clf = BayesianRidge(compute_score=True)
clf.fit(X,y)

ols = LinearRegression()
ols.fit(X,y)


plt.subplot(221)
plt.title("Weights of the model")
plt.plot(clf.coef_ , color='lightgreen',          
        label="BayesianRidgeRegression")
plt.plot(w , color='gold',label="Ground truth")
plt.plot(ols.coef_,color='red',linestyle="--",label="OLS")
plt.xlabel("Features")
plt.ylabel("Value of the weights")
plt.legend(loc='best',prop = dict(size=12))

plt.subplot(222)
plt.title("Histogram of the weights")
plt.hist(clf.coef_,bins=n_features,color='gold',log=True,   
            edgecolor='black')
plt.scatter(clf.coef_[relevant_features],
        np.full(len(relevant_features),5.),
        color='navy',label="Relevant features")
plt.ylabel("Features")
plt.xlabel("Values of the weights")
plt.legend(loc="upper left")

plt.subplot(223)
plt.title("Marginal log-likehood")
plt.plot(clf.scores_, color='navy')
plt.ylabel("Score")
plt.xlabel("Interations")


def f(x,noise_amount):
    y = np.sqrt(x) * np.sin(x)
    noise = np.random.normal(0,1,len(x))
    return y + noise_amount * noise

degree = 10
X = np.linspace(0, 10, 100)
y = f(X, noise_amount=0.1)
clf_poly = BayesianRidge()
clf_poly.fit(np.vander(X,degree), y)

X_plot = np.linspace(0,11,25)
y_plot = f(X_plot, noise_amount=0)
y_mean ,y_std = clf_poly.predict(np.vander(X_plot,degree),  
                        return_std=True)
plt.subplot(224)
plt.errorbar(X_plot, y_mean, y_std, color='navy',
             label="Polynomial Bayesian Ridge Regression",)
plt.plot(X_plot, y_plot, color='gold', label="Ground Truth")
plt.ylabel("Output y")
plt.xlabel("Feature X")
plt.legend(loc="lower left")


plt.show()