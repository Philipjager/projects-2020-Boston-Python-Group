# Inaugural project

In this project we seek to solve the Labor Supply Problem. 

- We first import the needed packages and write up the given equations from the problem and use the optimize.maximize with a wage value of 1, to find the optimal value of l that maximizes the utility function of the consumer.

- We plot the optimal labor supply and consumption for different wages using the optimizer in the range [0.5, 1.5]. 

- To calculate the total tax revenue we pull a random seed (2000), make the wage randomly uniform distributed with a low=0.5 and high=1.5 and defines the total tax revenue as the tax function which is defined earlier in the project and defaulting it, so that the former value of the tax function is excluded.

- Then we redefinde the value of espilon from 0.3 to 0.1 to find out what impact a lower Frisch-elasticity has on the tax revenue.

- To calculate the total tax revenue we 


The **results** of the project can be seen from running [inauguralproject.ipynb](inauguralproject.ipynb).

**Dependencies:** Apart from a standard Anaconda Python 3 installation, the project requires no further packages.
