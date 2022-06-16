import Vue from 'vue'
import App from './App.vue'
import ElementUI from 'element-ui';
import 'element-ui/lib/theme-chalk/index.css';
import router from "@/router";
import VueRouter from "vue-router";
import store from "@/store";
import axios from "axios";
import VueAxios from "vue-axios";
import JsonViewer from 'vue-json-viewer'
import '@/assets/css/reset.css'

Vue.config.devtools = true
Vue.config.productionTip = false
Vue.use(ElementUI)
Vue.use(VueRouter)
Vue.use(JsonViewer)
Vue.use(VueAxios, axios)

console.log(process.env.VUE_APP_BASEURL)
axios.defaults.baseURL = process.env.VUE_APP_BASEURL
axios.interceptors.request.use(
    config =>{
        let token = localStorage.getItem('accessToken')
        if(token){
            config.headers.Authorization = `Bearer ${token}`
        }
        return config
    },
    error => {
        return Promise.reject(error)
    }
)
// axios.interceptors.response.use(
//     response =>{
//         return response
//     },
//     error => {
//         return Promise.reject(error)
//     }
// )
router.beforeEach(
    (to, from, next) =>{
        let isAuthenticated = !!localStorage.getItem('accessToken')
        if(to.name !== 'login' && to.name !== 'signup' && !isAuthenticated){
            next({name: 'login', query: {redirect: to.path}})
        }else{
            next()
        }
    }
)
new Vue({
  render: h => h(App),
  router: router,
  store
}).$mount('#app')
