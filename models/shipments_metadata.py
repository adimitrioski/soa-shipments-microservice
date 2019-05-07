class ShipmentsMetadata:
    def __init__(
            self,
            total_shipments=None,
            total_in_progress=None,
            total_arrived=None,
            total_not_successful=None,
            total_returned=None,
            total_rating_very_good=None,
            total_rating_good=None,
            total_rating_ok=None,
            total_rating_bad=None,
            total_rating_very_bad=None):

        self.total_shipments = total_shipments
        self.total_in_progress = total_in_progress
        self.total_arrived = total_arrived
        self.total_not_successful = total_not_successful
        self.total_returned = total_returned
        self.total_rating_very_good = total_rating_very_good
        self.total_rating_good = total_rating_good
        self.total_rating_ok = total_rating_ok
        self.total_rating_bad = total_rating_bad
        self.total_rating_very_bad = total_rating_very_bad
