FROM node:alpine
LABEL description="Instant high-performance GraphQL API for your PostgreSQL database https://github.com/graphile/postgraphile"

# Install the postgraphile GraphQL engine generator library
RUN npm install -g postgraphile@latest

# Install postgraphile plugin that adds filter options to GraphQL queries
# + copy 'config' file into the appropriate place
RUN npm install -g postgraphile-plugin-connection-filter@latest
COPY ./postgraphile-configs/postgraphile-connection-filter-plugin_index.js ./usr/local/lib/node_modules/postgraphile-plugin-connection-filter/index.js

RUN npm install -g @graphile-contrib/pg-order-by-related@latest

EXPOSE 5000

# exec format, which means command in docker-compose.yml fill
# will be appended
ENTRYPOINT ["postgraphile", "-n", "0.0.0.0"]


#### LEGACY CODE - fyis

# Code used temporarily to explore the container what will be created
# RUN find . -name postgraphile-plugin-connection-filter
# ./usr/local/lib/node_modules/postgraphile-plugin-connection-filter