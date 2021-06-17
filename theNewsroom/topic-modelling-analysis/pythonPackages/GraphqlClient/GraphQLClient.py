from gql import Client, gql
from gql.transport.aiohttp import AIOHTTPTransport
import json
import logging

class GraphQLClient:
    _client = None

    def __init__(self, configFilePath="./config.json"):
      try:
        with open(configFilePath, "r") as configFile:
          config = json.load(configFile)
      except Exception as e:
        exit(f"Unable to json.load from: {configFilePath} - Exception: {e}.")

      # gql - select transport method
      transport = AIOHTTPTransport(url=config["graphQL_server"]["URLendpoint"])
      self._client = Client(transport=transport, fetch_schema_from_transport=True)

    def executeQuery(self, query, parameters=None):
      try:
        return self._client.execute(gql(query), variable_values=parameters)
      except Exception as e:
        exit(f"Unable to execute query: |||{query}||| - Exception: {e}")
  