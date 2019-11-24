def NSE_Func(measurement,simulation):
    """
    measurement and simulation must be two ndarray with same shape
    Last updated at 11/24/2019 by Lujun Zhang
    """
    
    numerator = np.square(measurement - simulation)
    numerator = numerator.sum()
    denominator = np.power(measurement - measurement.mean(),2)
    denominator = denominator.sum()
    NSE = 1 - numerator/denominator
    return[NSE]