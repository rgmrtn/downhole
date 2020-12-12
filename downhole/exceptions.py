class Error(Exception):
    """Generic Error Class
    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message="An error occurred."):
        self.message = message
        super().__init__(self.message)


class SurveyLengthError(Error):
    """Raised when the survey input data does not match up."""
    """Exception raised for errors in the input data.

    Attributes:
        azm_data -- list of azimuth orientations
        dip_data -- list of dip angles
        depth_data -- list of survey depths
        message -- explanation of the error
    """

    def __init__(self,azm_data, dip_data, depth_data):
        dataset_records = (len(azm_data), len(dip_data), len(depth_data))
        self.message = (
            f"""The survey datasets have varying lengths.
            AZM records: {dataset_records[0]}
            DIP records: {dataset_records[1]}
            DEPTH records: {dataset_records[2]}"""
            )
        super().__init__(self.message)
