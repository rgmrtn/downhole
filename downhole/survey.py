from math import acos, cos, sin, radians, degrees, tan, copysign
from .exceptions import *

def min_curv(dip_data, depth_data, azm_data, x, y, z):
    """Minimum Curvature Points
    Attributes:
        dip_data -- A list of the dip angles from the survey dataset
        azm_data -- A list of the azimuth orientations from the survey dataset
        depth_data -- A list of the dip angles from the survey dataset
        x -- x coordinate of the collar location
        y -- y coordinate of the collar location
        z -- z coordinate of the collar location
    
    Result:
        A list of three arrays containing the X,Y,Z values of the points
        representing a minimum curvature line.
    """
    if not (len(dip_data) == len(depth_data) == len(azm_data)):
        raise SurveyLengthError(azm_data, dip_data, depth_data)
        return None
    else:
        records = len(dip_data)
    
    x_coords = [x,]
    y_coords = [y,]
    z_coords = [z,]

    for i in range(records):
        if not i == records-1:
            try:
                MD = depth_data[i+1] - depth_data[i] 
                i_1 = radians(dip_data[i]+90)
                i_2 = radians(dip_data[i+1]+90)
                a_1 = radians(azm_data[i])
                a_2 = radians(azm_data[i+1])
            except:
                raise Error('could not set up variables.')
                return None
            try:
                beta = acos(cos(i_2 - i_1)-(sin(i_1)*sin(i_2)*(1-cos(a_2-a_1))))
            except:
                raise Error('could not calculate beta')
                return None
            try:
                if beta != 0.0:
                    rf = (2.0/beta)* tan(beta/2)
                else:
                    rf = 1
            except:
                raise Error('could not calculate ratio factor')
                return None
            
            try:
                N = ((MD/2)*(sin(i_1)*cos(a_1)+sin(i_2)*cos(a_2)))*rf
                E = ((MD/2)*(sin(i_1)*sin(a_1)+sin(i_2)*sin(a_2)))*rf
                tvd = (MD/2)*(cos(i_1)+cos(i_2))*rf
                x = x_coords[i]+E
                y = y_coords[i]+N
                z = z_coords[i]-tvd
                x_coords.append(x)
                y_coords.append(y)
                z_coords.append(z)
            except:
                raise Error("rest failed")
                return 'Failed'
    return x_coords, y_coords, z_coords
