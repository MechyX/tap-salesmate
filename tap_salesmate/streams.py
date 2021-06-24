"""Stream type classes for tap-salesmate."""

from pathlib import Path
from typing import Any, Dict, Optional, Union, List, Iterable

from singer_sdk import typing as th  # JSON Schema typing helpers

from tap_salesmate.client import salesmateStream
import json

class ActivityStream(salesmateStream):
    name = "Activity"
    path = "/activities/search"
    
    payload = {
    "fields": [
        "title",
        "dueDate",
        "PrimaryContact.name",
        "PrimaryCompany.name",
        "description",
        "isCompleted",
        "duration",
        "type",
        "isCalendarInvite",
        "owner",
        "lastModifiedAt",
        "tags",
        "relatedTo",
        "relatedToModule",
        "outcome",
        "createdLongitude",
        "createdLatitude",
        "createdAddress"
    ],
    "query": {
    "group": {
      "rules": [
        {
          "condition": "IS_AFTER",
          "moduleName": "Task", 
          "field": {
            "fieldName": "lastModifiedAt"
          },
          "data": ""    
        }
      ]
    }
    }
    }

    primary_keys = ["id"]
    replication_key = "lastModifiedAt"
    schema = th.PropertiesList(
        th.Property("id", th.IntegerType),
        th.Property("title", th.StringType),
        th.Property("lastModifiedAt", th.DateTimeType),
        th.Property("dueDate", th.DateTimeType),
        th.Property("type", th.IntegerType),
        th.Property("tags", th.StringType),
        th.Property("PrimaryContactId", th.NumberType),
        th.Property("OwnerId", th.NumberType),
        th.Property("PrimaryCompanyId", th.NumberType),
        th.Property("isCompleted", th.NumberType),
        th.Property("description", th.StringType),
        th.Property("duration", th.NumberType),
        th.Property("isCalendarInvite", th.NumberType),
        th.Property("relatedToModule", th.StringType),
        th.Property("relatedToId", th.StringType),
        th.Property("outcome", th.StringType),
        th.Property("createdLatitude", th.NumberType),
        th.Property("createdLongitude", th.NumberType),
        th.Property("createdAddress", th.StringType)
    ).to_dict()

    def post_process(self, row: dict, context: Optional[dict]) -> dict:
        """As needed, append or transform raw data to match expected structure."""
        row.pop('Followers', None)
        return row

class DealsStream(salesmateStream):
    name = "Deals"
    path = "/deals/search"
    primary_keys = ["id"]

    payload = {
    "fields": [
        "title",
        "PrimaryContact.name",
        "PrimaryCompany.name",
        "description",
        "lostReason",
        "winProbability",
        "owner",
        "tags",
        "closedDate",
        "dealValue",
        "currency",
        "lastModifiedAt",
        "stage",
        "pipeline",
        "source",
        "status",
        "priority",
        "createdLatitude",
        "createdLongitude",
        "createdAddress"
    ],
    "query": {
    "group": {
      "rules": [
        {
          "condition": "IS_AFTER",
          "moduleName": "Deal", 
          "field": {
            "fieldName": "lastModifiedAt"
          },
          "data": ""    
        }
      ]
    }
    }
    }

    replication_key = "lastModifiedAt"
    schema = th.PropertiesList(
        th.Property("id", th.IntegerType),
        th.Property("title", th.StringType),
        th.Property("PrimaryContactId", th.NumberType),
        th.Property("PrimaryCompanyId", th.NumberType),
        th.Property("description", th.StringType),
        th.Property("tags", th.StringType),
        th.Property("lostReason", th.StringType),
        th.Property("winProbability", th.NumberType),
        th.Property("OwnerId", th.NumberType),
        th.Property("closedDate", th.DateTimeType),
        th.Property("dealValue", th.NumberType),
        th.Property("currency", th.StringType),
        th.Property("lastModifiedAt", th.DateTimeType),
        th.Property("stage", th.StringType),
        th.Property("pipeline", th.StringType),
        th.Property("source", th.StringType),
        th.Property("status", th.StringType),
        th.Property("priority", th.StringType),
        th.Property("createdLatitude", th.NumberType),
        th.Property("createdLongitude", th.NumberType),
        th.Property("createdAddress", th.StringType)
    ).to_dict()
