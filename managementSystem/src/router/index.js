import Vue from 'vue'
import VueRouter from 'vue-router'
import Home from '../components/Home.vue'
import login from '../components/login.vue'
import Welcome from '../components/welcome.vue'
import Users from '../components/user/user.vue'
import GoodsList from '../components/goods/List.vue'
import Order from '../components/order/Order.vue'
import Report from '../components/report/Report.vue'

Vue.use(VueRouter)

const routes = [

  { path: '/', redirect: '/login' },
  { path: '/login', component: login },
  {
    path: '/home', name: 'Home', component: Home, redirect: '/users',
    children: [
      { path: '/welcome', component: Welcome },
      { path: '/users', component: Users },
      { path: '/goods', component: GoodsList },
      { path: '/orders', component: Order },
      { path: '/reports', component: Report }
    ]
  }
]

const router = new VueRouter({
  routes
})

//路由导航守卫
router.beforeEach((to, from, next) => {
  if (to.path === '/login') return next()
  const tokenStr = window.sessionStorage.getItem('admin')
  if (!tokenStr) return next('/login')
  next()
})
export default router

//防止重复点击而报错
const originalPush = VueRouter.prototype.push
VueRouter.prototype.push = function push(location) {
  return originalPush.call(this, location).catch(err => err)
}
