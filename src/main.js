import Vue from 'vue'
import App from './App.vue'
import vuetify from './plugins/vuetify';

import axios from 'axios'
import VueAxios from 'vue-axios'

Vue.config.productionTip = true
Vue.use(VueAxios, axios)

import uploader from 'vue-simple-uploader'
Vue.use(uploader)

new Vue({
  vuetify,
  render: h => h(App)
}).$mount('#app')
