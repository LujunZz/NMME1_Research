def Get_NMME_Precip(ncInput,Leadtime_idx):
    """
    ------------------------------------------------------
    ncInput must be a NC.object created by netCDF4 package
    Example on NC.object:
     import netCDF4 as nc
     NC.object = nc.Dataset('xxx/xx.nc')
    Leadtime_idx specifies the index of the Leadtime 
    for most the NMME members,leadtime index:
    [0,    1,    2,    3,   ...]
    [0.5M, 1.5M, 2.5M, 3.5M,...]
    ------------------------------------------------------
    The returned varData matrixa could be either monthly
    precipitation or precipitation rate
    ------------------------------------------------------
    Last updated on 11/24/2019 by Lujun Zhang
    ------------------------------------------------------
    """
    Order_list = Get_NMME_index_order(ncInput)
    if np.size(Order_list)==5 and Order_list[1] == 'L':
        Var_name = 'prec'
        varData = ncInput.variables[Var_name][:,Leadtime_idx,:,:,:]
        return varData
    if np.size(Order_list)==5 and Order_list[2] == 'L':
        Var_name = 'prec'
        varData = ncInput.variables[Var_name][:,:,Leadtime_idx,:,:]
        return varData 
    if np.size(Order_list)==3:
        Var_name = 'prate'
        varData = ncInput.variables[Var_name][:,:,:]   
        return varData