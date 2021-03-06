import numpy as np
from scipy.optimize import fmin_l_bfgs_b

'''
Collection of useful statistics routines
'''

def simpSample(f, numTest, xMin, xMax, M = None, verb = False):
    '''
    Use the rejection sampling method to generate a 
    probability distribution according to the given function f, 
    between some range xMin and xMax.
    If xMin==xMax, return an array where all values are equal to 
    this value.
    '''

    if xMin==xMax:
        return np.zeros(numTest)+xMin

    #find max value if not provided
    if M is None:
        M = calcM(f,xMin,xMax)
        
    #initialize
    n = 0
    X = np.zeros(numTest);
    numIter = 0;
    maxIter = 1000;

    nSamp = int(np.max([2*numTest,1e6]))
    while n < numTest and numIter < maxIter:
        xd = np.random.random(nSamp) * (xMax - xMin) + xMin
        yd = np.random.random(nSamp) * M
        pd = f(xd)

        xd = xd[yd < pd]
        X[n:min(n+len(xd), numTest)] = xd[:min(len(xd),numTest-n)]
        n += len(xd)
        numIter += 1

    if numIter == maxIter:
        raise Exception("Failed to converge.")

    if verb:
        print 'Finished in '+repr(numIter)+' iterations.'

    return X

def calcM(f,xMin,xMax):
    #first do a coarse grid to get ic
    dx = np.linspace(xMin,xMax,1000000)
    ic = np.argmax(f(dx))
    
    #now optimize
    g = lambda x: -f(x)
    M = fmin_l_bfgs_b(g,[dx[ic]],approx_grad=True,bounds=[(xMin,xMax)])
    M = f(M[0])

    return M