from downhole.survey import Survey, DownholeSurvey

from downhole.examples.ex_survey import *

s = Survey()

import pandas as pd

survey_df = pd.read_excel('.\\Test Spreadsheets\\Survey.xlsx', index_col=0)
collar_df = pd.read_excel('.\\Test Spreadsheets\\Collar.xlsx', index_col=0)

holes = list(pd.unique(collar_df.index))
for hole in holes:
    try:
        if len(survey_df.loc[[hole]]) == 1:
            print(f"No Downhole Survey {hole}, collar info used.")
            ds = DownholeSurvey(
                [collar_df.at[hole, 'Azimuth_GridN'],collar_df.at[hole, 'Azimuth_GridN']],
                [collar_df.at[hole, 'DIP'],collar_df.at[hole, 'DIP']],
                [0,collar_df.at[hole, 'TotalDepth_m']],
                collar_df.at[hole, 'UTM_N83_EASTING'],
                collar_df.at[hole, 'UTM_N83_NORTHING'],
                collar_df.at[hole, 'UTM_N83_ELEV_MSL'], hole
            )
        else:
            azm_data = list(survey_df.loc[[hole]]['AzimGridN'])
            dip_data = list(survey_df.loc[[hole]]['Final_Dip'])
            depth_data = list(survey_df.loc[[hole]]['Depth_m'])
            
            if min(survey_df.loc[[hole]]['Depth_m']) > 0:
                print(f"No Depth=0.00 reading for {hole}, interval added.")
                azm_data.insert(0,azm_data[0])
                dip_data.insert(0,dip_data[0])
                depth_data.insert(0,0.00)
            
            ds = DownholeSurvey(
                azm_data,
                dip_data,
                depth_data,
                collar_df.at[hole, 'UTM_N83_EASTING'],
                collar_df.at[hole, 'UTM_N83_NORTHING'],
                collar_df.at[hole, 'UTM_N83_ELEV_MSL'], hole
            )
        

    except KeyError:
        print(f"No Downhole Survey or record of {hole}, collar info used.")
        ds = DownholeSurvey(
            [collar_df.at[hole, 'Azimuth_GridN'],collar_df.at[hole, 'Azimuth_GridN']],
            [collar_df.at[hole, 'DIP'],collar_df.at[hole, 'DIP']],
            [0,collar_df.at[hole, 'TotalDepth_m']],
            collar_df.at[hole, 'UTM_N83_EASTING'],
            collar_df.at[hole, 'UTM_N83_NORTHING'],
            collar_df.at[hole, 'UTM_N83_ELEV_MSL'], hole
        )
    
    s.add_downhole_survey(ds)


s.export_shapefile()