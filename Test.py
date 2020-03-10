import numpy as np

def u_func(l,w,m=1,v=10,eps=0.3,t0=.4,t1=.1,k=.4):
    return np.log(m+w*l-t0*w*l-t1*max(w*l-k,0))-v*l**(1+1/eps)/(1+1/eps)

#print(u_func(0))
##print(u_func(0.5))
#print(u_func(0.75))
#print(u_func(1))

#for i in range(100):
 #   print(f'i = {i/100:.2f}')
 #   print(f'u = {u_func(i/100):.4f}')
 #   print('')
        

# Fra Lecture 3
def find_best_choice_monotone(N,w=1,do_print=True):
    
    # a. allocate numpy arrays
    shape_tuple = (N)
    l_values = np.empty(shape_tuple)
    u_values = np.empty(shape_tuple)
    
    # b. start from guess of x1=x2=0
    l_best = 0
    u_best = u_func(0,w)
    
    # c. loop through all possibilities
    for i in range(N):
        
        # i. x1
        l_values[i] = l = i/100
            
        # ii. utility    
        u_values[i] = u_func(l,w)
        
        if u_values[i] >= u_best:    
            l_best = l_values[i]
            u_best = u_values[i]
            
    # d. print
    if do_print:
        print_solution(l_best,u_best)   

    return l_best,u_best,l_values,u_values

def print_solution(l,u):
    print(f'l = {l:.8f}')
    print(f'u  = {u:.8f}')

sol = find_best_choice_monotone(N=100,w=0.5)
sol = find_best_choice_monotone(N=100,w=1)
sol = find_best_choice_monotone(N=100,w=1.5)

# Optimal choice of w

for i in range(50,150,1)
    sol = find_best_choice_monostone(N=100,i/100)
