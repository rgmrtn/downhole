from math import acos, cos, sin, radians, degrees, tan, copysign, sqrt
from .exceptions import *


class Survey():
    """A set of downhole surveys"""
    def __init__(self, downhole_surveys=[]):
        self.downhole_surveys = downhole_surveys
    
    def __repr__(self):
        return f"Survey containing {len(self.downhole_surveys)} records."

    def add_downhole_survey(self, downhole_survey):
        self.downhole_surveys.append(downhole_survey)
    
    def export_shapefile(self, location='.', filename="Survey_Export"):
        from pyshp import shapefile
        w = shapefile.Writer(location + '\\' + filename)
        w.field('HOLE_ID', 'C')
        for downhole_survey in self.downhole_surveys:
            w.linez([downhole_survey.min_curv.xyz_points()])
            w.record(downhole_survey.id)
        w.close()
    

class DownholeSurvey():
    """Only a single hole survey at the moment"""
    def __init__(self, azm_data, dip_data, depth_data, x, y, z, id='NO-ID',**kwargs):
        self.id = id
        self.azm_data = azm_data
        self.dip_data = dip_data
        self.depth_data = depth_data
        self.x = x
        self.y = y
        self.z = z
        self.attributes = list(kwargs.items())
        self.min_curv = Min_Curv(self)
    
    def __repr__(self):
        return f"Downhole Survey - {self.id}"
    
class Min_Curv():
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
    def __init__(self, DownholeSurvey):
        self.dip_data = DownholeSurvey.dip_data
        self.depth_data = DownholeSurvey.depth_data
        self.azm_data = DownholeSurvey.azm_data
        self.x = DownholeSurvey.x
        self.y = DownholeSurvey.y
        self.z = DownholeSurvey.z
        self.records = len(self.dip_data)
        self.survey_intervals = self.survey_intervals()
    
    def sample_point(self, dist):
        if dist > self.depth_data[-1]:
            print('Depth out of range.')
        else:
            for i in range(self.records):
                if dist == self.survey_intervals[i]:
                    return self.survey_intervals[i][1][:3]
                elif not i == self.records - 1:
                    if self.survey_intervals[i] < dist < self.survey_intervals[i+1]:
                        x1 = self.survey_intervals[i][1][0]
                        x2 = self.survey_intervals[i+1][1][0]
                        y1 = self.survey_intervals[i][1][1]
                        y2 = self.survey_intervals[i+1][1][1]
                        z1 = self.survey_intervals[i][1][2]
                        z2 = self.survey_intervals[i+1][1][2]

                        intervaldist = sqrt(((x2 - x1)**2)+((y2 - y1)**2)+((z2 - x1)**2))
                        u = dist / intervaldist
                        x = (1-u)* x1 + (u*x2)
                        y = (1-u)* y1 + (u*y2)
                        z = (1-u)* z1 + (u*b2)
                        return [x,y,z]






    
    def survey_intervals(self):
        if not (len(self.dip_data) == len(self.depth_data) == len(self.azm_data)):
            raise SurveyLengthError(self.azm_data, self.dip_data, self.depth_data)
            return None
        
        x_coords = [self.x,]
        y_coords = [self.y,]
        z_coords = [self.z,]

        for i in range(self.records):
            if not i == self.records-1:
                try:
                    MD = self.depth_data[i+1] - self.depth_data[i] 
                    i_1 = radians(self.dip_data[i]+90)
                    i_2 = radians(self.dip_data[i+1]+90)
                    a_1 = radians(self.azm_data[i])
                    a_2 = radians(self.azm_data[i+1])
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
                    x_coords.append(round(x,3))
                    y_coords.append(round(y,3))
                    z_coords.append(round(z,3))
                except:
                    raise Error("rest failed")
                    return None
        
        survey_intervals = [
            [idx,list(coords)] for idx, coords in enumerate(zip(
                x_coords,
                y_coords,
                z_coords,
                self.depth_data,
                self.azm_data,
                self.dip_data,
                ))
            ]
        return survey_intervals

    def xyz_points(self):
        return [i[1][:3] for i in self.survey_intervals()]



