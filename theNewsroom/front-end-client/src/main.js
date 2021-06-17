
import Vue from 'vue'
import App from './App.vue'
import router from './router/'
import store from './store/'

import VueResizeText from 'vue-resize-text';
Vue.use(VueResizeText)

import vuetify from './plugins/vuetify'
import './scss/main.scss'

import VueApexCharts from 'vue-apexcharts'
Vue.use(VueApexCharts)

Vue.component('apexchart', VueApexCharts)

import MultiFiltersPlugin from './plugins/MultiFilters'
Vue.use(MultiFiltersPlugin)


Vue.config.productionTip = false

// Import the Auth0 configuration
import { domain, clientId, audience } from "../auth_config.json"
import { createProvider } from './plugins/vue-apollo'

// Import getInstance from the auth wrapper
import { Auth0Plugin } from './auth';


// Install the authentication plugin here
Vue.use(Auth0Plugin, {
  domain,
  clientId,
  audience,
  onRedirectCallback: appState => {

    router.push(
      appState && appState.targetUrl
        ? appState.targetUrl
        : window.location.pathname
    )
  }
})

new Vue({
  el: '#app',
  store,
  router,
  vuetify,
  apolloProvider: createProvider(),
  render: h => h(App)
})

// const instance = getInstance();
// import CREATE_USER from './graphql/createUser.gql'

// instance.$watch("isAuthenticated", async isAuthenticated => {
//   if (isAuthenticated) {
//     const token = await instance.getTokenSilently();
//     console.log(token);
//     var id = instance.user.sub
//             console.log(id)
//             Vue.apolloProvider.mutate({
//                 mutation: CREATE_USER,
//                 variables: {
//                     id
//                 }
//             })
//   }
// });




