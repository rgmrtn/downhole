from math import acos, cos, sin, radians, degrees, tan, copysign, sqrt
from .exceptions import *
import logging

logging.basicConfig(filename='survey.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s', level="WARNING")

class Hole_Set():
    """Hole Set
    Container object for a set of holes

    Attributes:
        holes -- list of hole objects
    
    Methods:
        add_hole -- add a hole to the list of holes
    """
    def __init__(self):
        logging.info('Hole set created.')
        self.holes = []
    
    def add_hole(self, hole):
        if type(hole) == Hole:
            self.holes.append(hole)
        else:
            logging.warning('Cannot add object to Hole_Set, incorrect type.')
    


class Hole():
    """Hole

    Attributes:
        id -- Hole ID
        samples -- list of samples
    
    Methods:
        add_sample -- Add sample to list of samples in hole
    """

    def __init__(self, id):
        self.id = id
        self.samples = []
    
    def add_sample(self, sample):
        self.samples.append(sample)
    
    def __hash__(self):
        return hash(self.id)

    def __repr__(self):
        return self.id
    
    def __eq__(self,other):
        return self.id == other

    def __ne__(self,other):
        return self.id != other


class Sample_Set():
    """Sample Set

    Attributes:
        samples -- list of samples in sample set
    
    Methods:
        export_shapefile -- pyshp of sample set to line traces

    """
    def __init__(self):
        self.samples = []
    
    def add_sample(self, sample):
        self.samples.append(sample)
    
    def export_shapefile(self, location='.', filename='Sample_Set'):
        from pyshp import shapefile
        w = shapefile.Writer(location + '\\' + filename)
        w.field('SAMPLE_ID', 'C')
        w.field('HOLE_ID', 'C')
        for sample in self.samples:
            w.linez([sample.xyz_points()])
            w.record(sample.id, sample.hole_id)
        w.close()
        logging.info('Shapefile exported.')

class Sample():
    """Sample

    Attributes:
        id -- Sample ID
        hole_id -- Hole ID
        sample_type -- 'INT' or 'PT' (Interval or Point)
        sample_location -- list of XYZ points representing the sample

    Methods:
        xyz_points -- returns the list of XYZ points representing the sample
    """

    def __init__(self, id, hole_id, sample_type, sample_location):
        self.id = id
        self.hole_id = hole_id
        self.sample_type = sample_type
        self.sample_location = sample_location

    def __repr__(self):
        return self.id
    
    def xyz_points(self):
        return [i[1][:3] for i in self.sample_location]


class Survey():
    """Survey
    A set of downhole surveys
    Attributes:
        downhole_surveys -- list of downhole surveys associated with the survey
        set
    
    Methods:
        add_downhole_survey -- Add downhole survey to list of downhole surveys
        export_shapefile -- pyshp of survey traces to shapefile
    """
    def __init__(self):
        logging.info('Survey object created.')
        self.downhole_surveys = []
    
    def __repr__(self):
        return f"Survey containing {len(self.downhole_surveys)} records."

    def add_downhole_survey(self, downhole_survey):
        logging.info(f'{downhole_survey.id} downhole survey added to Survey dataset.')
        self.downhole_surveys.append(downhole_survey)
    
    def export_shapefile(self, location='.', filename="Survey_Export"):
        from pyshp import shapefile
        w = shapefile.Writer(location + '\\' + filename)
        w.field('HOLE_ID', 'C')
        for downhole_survey in self.downhole_surveys:
            w.linez([downhole_survey.min_curv.xyz_points()])
            w.record(downhole_survey.id)
        w.close()
        logging.info('Shapefile exported.')
    

class DownholeSurvey():
    """Downhole Survey
    Container object for the downhole survey data.

    Attributes:
        dip_data -- A list of the dip angles from the survey dataset
        azm_data -- A list of the azimuth orientations from the survey dataset
        depth_data -- A list of the dip angles from the survey dataset
        x -- x coordinate of the collar location
        y -- y coordinate of the collar location
        z -- z coordinate of the collar location
        attributes -- currently unused
        min_curv -- XYZ points representing the minimum curvature path of the
        downhole survey trace

    """
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
        return f"{self.id}"

    def __eq__(self,other):
        return self.id == other

    def __ne__(self,other):
        return self.id != other
    
class Min_Curv():
    """Minimum Curvature Results
    Attributes:
        DownholeSurvey -- the DownholeSurvey object containing the survey info.
    
    Methods:
        sample_point -- produces the X,Y,Z coordinates of a point at a distance
        along the line

        survey_intervals -- produces the X,Y,Z coordinates of points
        representing the downhole survey trace along with the original survey
        data and interval number

        xyz_points -- only the X,Y,Z coordinates of the survey_intervals
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
                if dist == self.survey_intervals[i][1][3]:
                    return [i,self.survey_intervals[i][1][:4]]
                elif not i == self.records - 1:
                    if self.survey_intervals[i][1][3] < dist < self.survey_intervals[i+1][1][3]:
                        x1 = self.survey_intervals[i][1][0]
                        x2 = self.survey_intervals[i+1][1][0]
                        y1 = self.survey_intervals[i][1][1]
                        y2 = self.survey_intervals[i+1][1][1]
                        z1 = self.survey_intervals[i][1][2]
                        z2 = self.survey_intervals[i+1][1][2]
                        intervaldist = sqrt(((x2 - x1)**2)+((y2 - y1)**2)+((z2 - z1)**2))
                        dist_along = dist - self.survey_intervals[i][1][3] # distance from last interval
                        u = dist_along / intervaldist
                        x = round((1-u)* x1 + (u*x2),3)
                        y = round((1-u)* y1 + (u*y2),3)
                        z = round((1-u)* z1 + (u*z2),3)
                        return [i,[x,y,z,dist]]
        
    def sample_interval(self, from_dist, to_dist):
        start = self.sample_point(from_dist)
        end = self.sample_point(to_dist)
        between = [
            [
                self.survey_intervals[i][0],
                self.survey_intervals[i][1][:4]
            ] for i in range(start[0]+1,end[0]+1)
        ]
        between.insert(0,start)
        if end != between[-1]: # prevents duplicate last point in interval
            between.append(end)
        return between


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
        return [i[1][:3] for i in self.survey_intervals]



