import Vue from 'vue'
import Vuex from 'vuex'
import user from './modules/user'
import location from './modules/location'
import items from './modules/items'
import stores from './modules/stores'

Vue.use(Vuex)

const debug = process.env.NODE_ENV !== 'production'

export default new Vuex.Store({
  modules: {
    user,
    location,
    items,
    stores
  },
  strict: debug
})
