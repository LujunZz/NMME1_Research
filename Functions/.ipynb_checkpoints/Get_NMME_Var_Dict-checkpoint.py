def Get_NMME_Var_Dict(ncInput):
    """
    ------------------------------------------------------
    ncInput must be a NC.object created by netCDF4 package
    Example on NC.object:
     import netCDF4 as nc
     NC.object = nc.Dataset('xxx/xx.nc')
    ------------------------------------------------------
    The returned Var_Dict is a Dict object that contains 
    all the "variables" along with their "size" for a given 
    input NMME member dataset except for Prec or Prate
    ------------------------------------------------------
    Last updated on 11/24/2019 by Lujun Zhang
    ------------------------------------------------------
    """
    Var_name = list(ncInput.variables.keys())
    if np.size(Var_name) == 6:
        Var_name.remove('prec')
    else:
        Var_name.remove('prate')
    Var_Dict = {}
    for i in Var_name:
        Var_Dict[i]= np.size(ncInput[i][:])
    return Var_Dict