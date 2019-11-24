# Bayesian Moedl Averagin weights computation
def Bayesian_weights(simulations, observations):
    """
    -------------------------------------------------------
    m ensemble members
    n number of observations
    simulations - m by n simulations from ensemble members
    observations - n by 1 observation data
    BIC - Bayesian Information Critirion
    -------------------------------------------------------
    This function return the weights for m ensemble members
    -------------------------------------------------------
    Last updated by Lujun Zhang on 11/24/2019
    -------------------------------------------------------
    """
    [n,m] = np.shape(simulations)
    BIC = np.zeros(m)
    wgt = np.zeros(m)
    for i in range(m):
        error_variance = np.sum(np.power(simulations[:,i]-observations,2))/n
        BIC[i] = 2*n*np.log(error_variance)
    for i in range(m):
        BIC_sub = BIC - BIC[i]
        wgt[i] = 1/np.sum(np.exp(-0.5*BIC_sub))
    return wgt