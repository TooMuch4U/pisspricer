import Vue from 'vue'
import Router from 'vue-router'
import Home from '@/components/Home'
import Items from '@/components/Items'
import ItemStores from '@/components/ItemStores'
import Login from '@/components/Login'
import Logout from '@/components/Logout'
import Register from '@/components/Register'
import VerifyUser from '@/components/VerifyUser'
import ResendCode from '@/components/ResendCode'
import AdminPage from '../components/AdminPage'
import AdminCombineSkus from '../components/admin-pages/CombineSkus'
import AdminHome from '../components/admin-pages/Home'
import Brands from '../components/admin-pages/Brands'
import Syncs from '../components/admin-pages/sync-page/Syncs'

Vue.use(Router)

let router = new Router({
  routes: [
    {
      path: '/',
      name: 'home',
      component: Home
    },
    {
      path: '/login',
      name: 'login',
      component: Login
    },
    {
      path: '/logout',
      name: 'logout',
      component: Logout
    },
    {
      path: '/register',
      name: 'register',
      component: Register
    },
    {
      path: '/register/:userId/verify/:code',
      name: 'verify',
      component: VerifyUser
    },
    {
      path: '/register/resend',
      name: 'resend',
      component: ResendCode
    },
    {
      path: '/items',
      name: 'items',
      component: Items
    },
    {
      path: '/items/:slug',
      name: 'item',
      component: ItemStores
    },
    {
      path: '/admin',
      name: 'admin',
      component: AdminPage,
      children: [
        {
          path: '',
          component: AdminHome
        },
        {
          path: 'combine',
          component: AdminCombineSkus
        },
        {
          path: 'brands',
          component: Brands
        },
        {
          path: 'syncs',
          component: Syncs
        }
      ]
    }
  ],
  mode: 'history'
})

router.beforeEach((to, from, next) => {
  // hide any modals before leaving
  // eslint-disable-next-line
  $('.modal.show').modal('hide')
  next()
})

export default router
