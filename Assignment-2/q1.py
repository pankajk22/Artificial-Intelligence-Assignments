import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm

def x1givenx2(a,x2):
    imu=1+a*(x2-1)
    isigma=(1-(a*a))
    s = np.random.normal(imu, isigma)
    return s

def x2givenx1(a,x1):
    imu=1+a*(x1-1)
    isigma=(1-(a*a))
    s = np.random.normal(imu, isigma)
    return s

def gibbssampler(x1,x2,a):
    x1=x1givenx2(a,x2)
    x2=x2givenx1(a,x1)
    return (x1,x2)

def plot(x1,x2,title):
    plt.xlim(-10,10)
    plt.ylim(-10,10)
    plt.plot(x1,x2)
    plt.title(title)
    plt.show()

def traceplots(x1,x2):
    iterations = []
    for i in range(1,len(x1)+1):
        iterations.append(i)
    
    plt.plot(iterations,x1)
    
    plt.title("X1 values traceplot")
    plt.grid(axis='x')
    plt.show()
    plt.plot(iterations,x2)
    plt.grid(axis='x')
    plt.title("X2 values traceplot")
    plt.show()

def main():

    a_vector=[0,0.99]

    for a in a_vector:
        print("For a = ",a)
        mu=[1,2]
        sigma=[[1,a],[a,1]]

        x1=5
        x2=5

        actual_plotx1=[]
        actual_plotx2=[]
        plotx1=[]
        plotx2=[]

        for i in tqdm(range(0,10000)):
            (x1,x2)=gibbssampler(x1,x2,a)
            (x,y)= np.random.multivariate_normal(mu, sigma).T
            actual_plotx1.append(x)
            actual_plotx2.append(y)
            plotx1.append(x1)
            plotx2.append(x2)

        plot(plotx1,plotx2,'Plot of Simulations')
        plot(actual_plotx1,actual_plotx2,'Bivariate Gaussian distribution')
        traceplots(plotx1,plotx2)

main()

