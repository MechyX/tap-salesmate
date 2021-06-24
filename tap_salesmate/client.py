"""REST client handling, including salesmateStream base class."""

import requests
from pathlib import Path
from typing import Any, Dict, Optional, Union, List, Iterable, cast
from singer_sdk.streams import RESTStream
import datetime as dt
import json

API_DATE_FORMAT = '%b %d, %Y %H:%M %p'
RFC_DATE_FORMAT = '%Y-%m-%dT%H:%M:%SZ'

class salesmateStream(RESTStream):
    """salesmate stream class."""

    @property
    def url_base(self) -> str:
        """Return the API URL root, configurable via tap settings."""
        instance_name = self.config["instance_name"]
        url_base = f'https://{instance_name}/apis/v3'
        return url_base

    @property
    def http_headers(self) -> dict:
        """Return the http headers needed."""
        headers = {}
        if "user_agent" in self.config:
            headers["User-Agent"] = self.config.get("user_agent")
        
        headers["sessionToken"] = self.config.get("sessionToken")
        headers["Content-Type"] = "application/json"
        return headers

    def get_next_page_token(
        self, response: requests.Response, previous_token: Optional[Any]
    ) -> Optional[Any]:
        """Return a token for identifying next page or None if no more pages."""
        next_page_token = response.headers.get("X-Next-Page", None)
        if next_page_token:
            self.logger.debug(f"Next page token retrieved: {next_page_token}")
        return next_page_token

    def get_url_params(
        self, context: Optional[dict], next_page_token: Optional[Any]
    ) -> Dict[str, Any]:
        """Return a dictionary of values to be used in URL parameterization."""
        params: dict = {}
        return params

    def prepare_request_payload(
        self, context: Optional[dict], next_page_token: Optional[Any]
    ) -> Optional[dict]:
        """Prepare the data payload for the REST API request."""
        payload: dict = {}
        payload = self.payload
        state_ts = self.get_starting_timestamp(context).strftime(RFC_DATE_FORMAT)
        state_ts = self.convert_date_format(state_ts, RFC_DATE_FORMAT, API_DATE_FORMAT)
        payload['query']['group']['rules'][0]["data"] = state_ts
        return json.dumps(payload)

    def convert_date_format(self, date_api: str, format_from: str, format_to: str) -> str:
        """ Convert Date from API format to RFC 3339 """
        date_rfc_str: str = ''
        date_rfc = dt.datetime.strptime(date_api, format_from)
        date_rfc_str = date_rfc.strftime(format_to)
        return date_rfc_str

    def parse_response(self, response: requests.Response) -> Iterable[dict]:
        """Parse the response and return an iterator of result rows."""
        data = response.json().get("Data").get("data")
        
        date_key = ''
        if self.name == 'Activity':
            date_key = 'dueDate'
        else:
            date_key = 'closedDate'
        
        for row in data:
            if date_key in row and row[date_key] != '':
                row[date_key] = self.convert_date_format(row[date_key], API_DATE_FORMAT, RFC_DATE_FORMAT)
            elif date_key in row and row[date_key] == '':
                row[date_key] = None
                
            row['lastModifiedAt'] = self.convert_date_format(row['lastModifiedAt'], API_DATE_FORMAT, RFC_DATE_FORMAT)
            row.pop('Followers', None)
            
            pcont_id, pcomp_id, owner_id = None, None, None
            
            if self.name == 'Activity':
                if 'relatedToId' in row:
                    if row['relatedToId'] != '':
                        row['relatedToId'] = str(row['relatedToId']) 
                        

            if 'PrimaryCompany' in row and bool(row['PrimaryCompany']):
                pcomp_id = row['PrimaryCompany']['id']
                row.pop('PrimaryCompany', None)
            
            row['PrimaryCompanyId'] = pcomp_id
            
            if 'PrimaryContact' in row and bool(row['PrimaryContact']):
                pcont_id = row['PrimaryContact']['id']
                row.pop('PrimaryContact', None)
            
            row["PrimaryContactId"] = pcont_id
            
            if 'Owner' in row and bool(row['Owner']):
                owner_id = row['Owner']['id']
                row.pop('Owner', None) 
            
            row["OwnerId"] = owner_id  

            yield row

    def prepare_request(
        self, context: Optional[dict], next_page_token: Optional[Any]
    ) -> requests.PreparedRequest:
        """Prepare a request object.

        If partitioning is supported, the `context` object will contain the partition
        definitions. Pagination information can be parsed from `next_page_token` if
        `next_page_token` is not None.
        """
        http_method = self.rest_method
        url: str = self.get_url(context)
        # params: dict = self.get_url_params(context, next_page_token)
        headers = self.http_headers
        request_data = self.prepare_request_payload(context, next_page_token)
        

        authenticator = self.authenticator
        if authenticator:
            headers.update(authenticator.auth_headers or {})

        request = cast(
            requests.PreparedRequest,
            self.requests_session.prepare_request(
                requests.Request(
                    method='POST',
                    url=url,
                    headers=headers,
                    data=request_data
                )
            ),
        )
        return request


    

