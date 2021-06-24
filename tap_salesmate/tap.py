"""salesmate tap class."""

from typing import List

from singer_sdk import Tap, Stream
from singer_sdk import typing as th  # JSON schema typing helpers

from tap_salesmate.streams import (
    salesmateStream,
    DealsStream,
    ActivityStream,
)

STREAM_TYPES = [
    DealsStream,
    ActivityStream
]


class Tapsalesmate(Tap):
    """salesmate tap class."""
    name = "tap-salesmate"
    
    config_jsonschema = th.PropertiesList(
        th.Property("start_date", th.DateTimeType, required=True),
        th.Property("instance_name", th.StringType, required=True),
        th.Property("sessionToken", th.StringType, required=True)
    ).to_dict()

    def discover_streams(self) -> List[Stream]:
        """Return a list of discovered streams."""
        return [stream_class(tap=self) for stream_class in STREAM_TYPES]

# CLI execution

cli = Tapsalesmate.cli