def Get_NMME_index_order(ncInput):
    """
    ------------------------------------------------------
    ncInput must be a NC.object created by netCDF4 package
    Example on NC.object:
     import netCDF4 as nc
     NC.object = nc.Dataset('xxx/xx.nc')
    ------------------------------------------------------
    Each NMME member's indeces could be in
    different order. This function returns an 
    list object that save all variables of given
    dataset in order
    ------------------------------------------------------
    Last updated on 11/24/2019 by Lujun Zhang
    ------------------------------------------------------
    """
    Var_name = str(ncInput)
    start_index = Var_name.find('prec')
    if Var_name.find('prec')!=-1:
        Var_name = Var_name[start_index+5:start_index+14]
        Order_list = ['a','a','a','a','a']
        for i in range(len(Var_name)):
            if i%2 == 0:
                Order_list[int(i/2)] = Var_name[i]               
    elif Var_name.find('prec')==-1:
        start_index = Var_name.find('prate')
        Var_name = Var_name[start_index+6:start_index+11]
        Order_list = ['a','a','a']
        for i in range(len(Var_name)):
            if i%2 == 0:
                Order_list[int(i/2)] = Var_name[i]        
    else:
        print ('Error there have no dim')
        os.system("pause")
        exit(0)
    return Order_list