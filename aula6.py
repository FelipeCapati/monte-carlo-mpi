from abc import ABC, abstractmethod
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from enum import Enum
import math
from __future__ import division
from sympy import *
init_printing()
from random import randrange, uniform
from datetime import datetime
# %matplotlib notebook
# import matplotlib.pyplot as plt
# from mpl_toolkits.mplot3d import axes3d 

class TypeOfIntegral(Enum):
    RECTANGULAR = 1,
    TRAPEZOIDAL = 2,
    SIMPSON = 3
    ADAPTATIVE_QUADRATURE = 4
    MONTE_CARLO = 5

class AbstractMathFunction(ABC):
    def __init__(self, BETA:float = 0.1):
        # Define a default function
        self.BETA = BETA
        self.RESOLUTION = 0.00001
        self.n_iterations = 0
#         self.dx = 0.000001
        self.dx = 0.25
       
    @abstractmethod
    def get_result(self, x:float) -> float:
        pass
    
    def get_integral(self, _type:TypeOfIntegral, lim_min:int, lim_max:int, error:float = 0.001, N:int = 1000):
        if(lim_min >= lim_max):
            raise('[AbsMathFunction][ERROR]: Min limit integral bigger than max limit integral')
        
        array_a = np.arange(lim_min, lim_max, self.dx)
        integral = 0
        
        if(_type == TypeOfIntegral.RECTANGULAR):
            print('[AbsMathFunction][LOG]: Solve type is RECTANGULAR')
            for a in array_a:
                b = a + self.dx
                integral += (b-a)*self.get_result((a+b)/2)
                
        elif(_type == TypeOfIntegral.TRAPEZOIDAL):
            print('[AbsMathFunction][LOG]: Solve type is TRAPEZOIDAL')
            for a in array_a:
                b = a + self.dx
                integral += (b-a)*((self.get_result(a)+self.get_result(b))/2)
        
        elif(_type == TypeOfIntegral.SIMPSON):
            print('[AbsMathFunction][LOG]: Solve type is SIMPSON')
            for a in array_a:
                b = a + self.dx
                integral += (b-a)*((self.get_result(a)+4*self.get_result((a+b)/2)+self.get_result(b))/6)
        
        elif(_type == TypeOfIntegral.ADAPTATIVE_QUADRATURE):
            print('[AbsMathFunction][LOG]: Solve type is ADAPTATIVE_QUADRATURE')
            I1 = TypeOfIntegral.TRAPEZOIDAL
            I2 = TypeOfIntegral.RECTANGULAR
            
            result_i1 = self.get_integral(_type=I1, lim_min=lim_min, lim_max=lim_max)
            result_i2 = self.get_integral(_type=I2, lim_min=lim_min, lim_max=lim_max)
            
            error_estimate = abs(result_i1 - result_i2)
            
            if(error_estimate <= error):
                integral = result_i1
            else:
                m = (lim_min+lim_max)/2
                
                print('[AbsMathFunction][LOG]: Solve using "m: %s and error: %s" to divide interval in two integrals' %(m, error_estimate))
                if(lim_min != m) and (lim_max != m):
                    integral_part_one = self.get_integral(_type=_type, lim_min=lim_min, lim_max=m, error=error) 
                    integral_part_two = self.get_integral(_type=_type, lim_min=m, lim_max=lim_max, error=error)
                    integral = integral_part_one + integral_part_two
                else:
                    integral = result_i1
                    print('[AbsMathFunction][ERROR]: The value of error: %s is not converging' %(error))
        elif(_type == TypeOfIntegral.MONTE_CARLO):
            print('[AbsMathFunction][LOG]: Solve type is MONTE CARLO')
            now = datetime.now()
            lim_x_min = lim_min
            lim_x_max = lim_max
            f_average = 0
            f2_average = 0

            for i in range(0, N):
                x_random = uniform(lim_x_min, lim_x_max)
                f_average += f.get_result(x_random)
                f2_average += f.get_result_f2(x_random)

            f_average *= (1/N)
            f2_average *= (1/N)
            integral = (lim_x_max-lim_x_min)*f_average
            self.integral_error = abs(((f2_average-f_average**2)/N)**0.5)
            self.time_process = round((datetime.now() - now).total_seconds(), 2)
            print("Integral: %s" %integral)
            print("Error:    %s" %self.integral_error)
            print("Time Pr.: %s seconds" %self.time_process)
            
        print('[AbsMathFunction][LOG]: Integral result is: %s' %(integral))
        
        return integral
            
    
    def get_diff(self, x:float) -> float:
        return round((self.get_result(x+self.dx) - self.get_result(x))/self.dx, 2)
    
    def get_min_x(self, x0:float) -> float:
        xi = x0
        while(abs(self.get_result(xi)) >= self.RESOLUTION):
            old_value = abs(self.get_result(xi))
            si = self.get_diff(xi)
            xi = xi - self.BETA*si
            new_value = abs(self.get_result(xi))
            
            if(old_value == new_value):
                break
            self.n_iterations += 1

        return round(xi, 2)
    def plot(self, x_min:float, x_max:float):
        data_x = np.arange(x_min, x_max, 0.01)
        data_y = []
        for x in data_x:
            print(self.get_result(0))
            data_y.append(self.get_result(x))
        
        plt.plot(data_x, data_y, label= 'function')
        plt.xlabel('x')
        plt.ylabel('y')
        plt.legend()
        plt.show()

class SymbolicMathFunction(AbstractMathFunction):
    def __init__(self):
        super().__init__()
        self.z = symbols('z')
        self.symbolic_function = exp(self.z)
        
    def get_result(self, x:float) -> float:   
        return float(self.symbolic_function.subs(self.z,x))
    
    def get_result_f2(self, x:float) -> float:
        return float(self.symbolic_function.subs(self.z,self.symbolic_function).subs(self.z,x))
    
    def get_n_diff(self, x:float, n:int) -> float:
        symbolic_diff = diff(self.symbolic_function, self.z)
        
        if(n>1):
            for i in range(1,n):
                symbolic_diff = diff(symbolic_diff, self.z)
        return symbolic_diff.subs(self.z, x)
    
    def get_integral_error(self, _type:TypeOfIntegral, x:float, lim_min: float, lim_max: float):
        if(lim_min >= lim_max):
            raise('[AbsMathFunction][ERROR]: Min limit integral bigger than max limit integral')
        
        integral_error = 0
        
        if(_type == TypeOfIntegral.RECTANGULAR):
            print('[AbsMathFunction][LOG]: Solve type is RECTANGULAR')
            integral_error = (((lim_max - lim_min)^3)/24)*self.get_n_diff(x=x, n=2)
                
        elif(_type == TypeOfIntegral.TRAPEZOIDAL):
            print('[AbsMathFunction][LOG]: Solve type is TRAPEZOIDAL')
            integral_error = -(((lim_max - lim_min)^3)/12)*self.get_n_diff(x=x, n=2)
        
        elif(_type == TypeOfIntegral.SIMPSON):
            print('[AbsMathFunction][LOG]: Solve type is SIMPSON')
            integral_error = -(((lim_max - lim_min)^5)/2880)*self.get_n_diff(x=x, n=4)
        
        print('[AbsMathFunction][LOG]: Integral error result is: %s' %(integral_error))
        
        self.integral_error = integral_error
        
        return integral_error
    
    def plot(self, x_min:float, x_max:float):
        p1 = plot(self.symbolic_function, (self.z, x_min, x_max), show=True, line_color='b')

class FunctionTestLetterA(SymbolicMathFunction):
    def __init__(self):
        super().__init__()
        self.symbolic_function = (4)/(1+self.z**2)

class FunctionTestLetterB(SymbolicMathFunction):
    def __init__(self):
        super().__init__()
        self.symbolic_function = (self.z + self.z**(1/2))**(1/2)

class FunctionTestLetterC(SymbolicMathFunction):
    def __init__(self):
        super().__init__()
        self.symbolic_function = (self.z)**(1/2)


# Plot function
f = FunctionTestLetterA()
f.plot(0,2)

# Get array of N to calculate integral
a = (np.arange(9)+1)*10
b = (np.arange(9)+1)*100
c = (np.arange(9)+1)*1000
d = (np.arange(9)+1)*10000
array_n = np.concatenate((a,b,c,d),axis=0)

# Calculate integral array to plot graph
real_result = 3.141592654
for n in array_n:
    print("N: %s" %n)
    integer = f.get_integral(_type=TypeOfIntegral.MONTE_CARLO, lim_min=0, lim_max=1, N = int(n))
    if(n == 10):
        array_integral = np.array([integer])
        array_error = np.array([f.integral_error])
        array_time = np.array([f.time_process])
        array_real_result = np.array([real_result])
    else:
        array_integral = np.concatenate((array_integral, np.array([integer])),axis=0)
        array_error = np.concatenate((array_error, np.array([f.integral_error])),axis=0)
        array_time = np.concatenate((array_time, np.array([f.time_process])),axis=0)
        array_real_result = np.concatenate((array_real_result, np.array([real_result])),axis=0)

# Plot graph integral and error vs N
plt.plot(array_n, array_integral, label= 'integral [calc]')
plt.plot(array_n, array_real_result, label= 'integral [real]')
plt.plot(array_n, array_error + 3, label= 'error [shift + 3]')
plt.xlabel('N')
plt.legend()
plt.show()

# Plot graph time vs N
plt.plot(array_n, array_time, label= 'time [second]')
plt.xlabel('N')
plt.legend()
plt.show()