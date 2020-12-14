from downhole.survey import Survey, DownholeSurvey
import pandas as pd

s = Survey()

survey_df = pd.read_excel('Survey.xlsx', index_col=0)
collar_df = pd.read_excel('Collar.xlsx', index_col=0)

holes = list(pd.unique(collar_df.index))
for hole in holes:
    try:
        if len(survey_df.loc[[hole]]) == 1: # survey table only has top of hole
            print(f"No Downhole Survey {hole}")
            ds = DownholeSurvey(
                [collar_df.at[hole, 'Azimuth_GridN'],collar_df.at[hole, 'Azimuth_GridN']],
                [collar_df.at[hole, 'DIP'],collar_df.at[hole, 'DIP']],
                [0,collar_df.at[hole, 'TotalDepth_m']],
                collar_df.at[hole, 'UTM_N83_EASTING'],
                collar_df.at[hole, 'UTM_N83_NORTHING'],
                collar_df.at[hole, 'UTM_N83_ELEV_MSL'], hole
            )
        else:
            ds = DownholeSurvey(
                list(survey_df.loc[[hole]]['AzimGridN']),
                list(survey_df.loc[[hole]]['Final_Dip']),
                list(survey_df.loc[[hole]]['Depth_m']),
                collar_df.at[hole, 'UTM_N83_EASTING'],
                collar_df.at[hole, 'UTM_N83_NORTHING'],
                collar_df.at[hole, 'UTM_N83_ELEV_MSL'], hole
            ) 

    except KeyError: # no survey at all
        print(f"Missing {hole}")
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
