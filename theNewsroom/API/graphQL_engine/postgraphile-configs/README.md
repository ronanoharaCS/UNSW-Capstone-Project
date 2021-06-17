# postgraphile-connection-filter-plugin_index.js

This plugin extends the capability of the Postgraphile GraphQL API engine. It adds the means to have more complex filtering on GraphQL queries.

Github - https://github.com/graphile-contrib/postgraphile-plugin-connection-filter

The problem is that its default configurations aren't set to what we need, hence, we need this file.

## NOTE: Security Concern

The reason why the defaults aren't switched on is because it raises security concerns described on the github page.

// TODO - protect our graphQL before it goes live

## Loading the config script in

We could have the entire codebase in our repository, though that would be 'heavy'.

I think the way to avoid holding the code base on our repo is to install the plugin via npm and then replace the `index.js` file in the plugin root directory which seems (by the devs choice/by chance) to contain all of the configuration options.

So, first the config options, I just copied and pasted the base file from the github and then made the changes I needed to make according to the README.md in the github.

So, second putting the config file into the docker container correct, in the `Dockerfile`, we run the following line to grab the library contents of this plugin.

```
RUN npm install -g postgraphile-plugin-connection-filter@latest
```

This installs a folder in the `node_modules` folder called `postgraphile-plugin-connection-filter` as per typical npm install.

So, in the `Dockerfile`, I just need to copy the approriate configuration file into the correct place. 

I found the correct place by executing this in the `Dockerfile`.

```
RUN find . -name node_modules
```

So when I built it, I found out where the node_modules folder is and then removed the above line.