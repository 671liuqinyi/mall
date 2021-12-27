import Vue from 'vue'
import App from './App.vue'
import router from './router'
import Element from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css';
import '../src/assets/css/global.css'
import axios from 'axios'
import TreeTable from 'vue-table-with-tree-grid'

Vue.prototype.$axios = axios
Vue.component('tree-table',TreeTable)

Vue.use(Element)
Vue.config.productionTip = false

new Vue({
  router,
  render: h => h(App)
}).$mount('#app')
