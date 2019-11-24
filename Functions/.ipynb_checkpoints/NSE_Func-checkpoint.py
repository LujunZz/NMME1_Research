def NSE_Func(measurement,simulation):
    """
    -------------------------------------------------------
    two inputes must be ndarray.obejcts with the same shape
    ------------------------------------------------------
    Last updated on 11/24/2019 by Lujun Zhang
    ------------------------------------------------------
    """
    
    numerator = np.square(measurement - simulation)
    numerator = numerator.sum()
    denominator = np.power(measurement - measurement.mean(),2)
    denominator = denominator.sum()
    NSE = 1 - numerator/denominator
    return[NSE]