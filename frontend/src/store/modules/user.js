import axios from 'axios'
import Cookies from 'js-cookie'
const COOKIE_EXPIRE = 365

let state = {
  loggedIn: (typeof Cookies.get('authToken') !== 'undefined'),
  authToken: null,
  userId: null,
  permissionLevel: 0,
  firstname: null,
  lastname: null,
  email: null
}

let mutations = {
  setLoggedIn (state, bool) {
    state.loggedIn = bool
  },
  permissionLevel (state, perm) {
    state.permissionLevel = perm
  },
  authToken (state, token) {
    Cookies.set('authToken', token, {expires: COOKIE_EXPIRE})
    state.authToken = token
  },
  userId (state, id) {
    Cookies.set('userId', id, {expires: COOKIE_EXPIRE})
    state.userId = id
  },
  userDetails (state, data) {
    state.permissionLevel = data.permission
    state.firstname = data.firstname
    state.latname = data.lastname
    state.email = data.email
  }
}

let actions = {
  login ({commit, dispatch}, reqBody) {
    return new Promise((resolve, reject) => {
      axios.post(`${process.env.API_URL}/users/login`, reqBody)
        .then((res) => {
          // Set userId and authtoken
          commit('userId', res.data.userId)
          commit('authToken', res.data.authToken)

          // Get user details
          dispatch('getCurUserInfo').then(() => { resolve() })
        })
        .catch((err) => {
          reject(err)
        })
    })
  },
  getUserInfo ({commit, state, dispatch}, userId) {
    return new Promise((resolve, reject) => {
      let header = {
        'X-Authorization': state.authToken
      }

      axios.get(`${process.env.API_URL}/users/${userId}`, {headers: header})
        .then((res) => {
          resolve(res.data)
        })
        .catch((err) => {
          if (err.response.status === 401) {
            dispatch('logout')
          }
          reject(err)
        })
    })
  },
  getCurUserInfo ({commit, dispatch, state}) {
    return new Promise((resolve, reject) => {
      dispatch('getUserInfo', state.userId)
        .then((res) => {
          commit('userDetails', res)
          commit('setLoggedIn', true)
          resolve(res)
        })
        .catch((err) => {
          dispatch('logout')
          reject(err)
        })
    })
  },
  logout ({commit}) {
    Cookies.remove('userId')
    Cookies.remove('authToken')
    commit('setLoggedIn', false)
    commit('userDetails', {})
    // Todo send logout to api
  },
  register ({commit}, {referer, reqBody}) {
    return new Promise((resolve, reject) => {
      axios.post(`${process.env.API_URL}/users/register`, reqBody, {params: {referer}})
        .then((res) => {
          resolve()
        })
        .catch((err) => {
          reject(err)
        })
    })
  },
  verifyUser ({commit}, {userId, code}) {
    return new Promise((resolve, reject) => {
      axios.post(`${process.env.API_URL}/users/${userId}/verify/${code}`)
        .then((res) => {
          resolve(res)
        })
        .catch((err) => {
          reject(err)
        })
    })
  },
  resendVerify ({commit}, {email, referer}) {
    return new Promise((resolve, reject) => {
      axios.post(`${process.env.API_URL}/users/${email}/resend`, {}, {params: {referer}})
        .then((res) => {
          resolve(res)
        })
        .catch((err) => {
          reject(err)
        })
    })
  },
  loadUserDetails ({dispatch, commit, getters}) {
    return new Promise((resolve, reject) => {
      // Check if the auth token cookie was set
      const tokenCookie = Cookies.get('authToken')
      if (tokenCookie && getters.userDetailsLoaded) {
        // Load in userId and cookie
        commit('authToken', tokenCookie)
        commit('userId', Cookies.get('userId'))

        // Get user details
        dispatch('getCurUserInfo')
          .then((res) => { resolve(res) })
          .catch((err) => { dispatch('logout').then(reject(err)) })
      } else {
        resolve()
      }
    })
  }
}

let getters = {
  loggedIn: state => {
    return state.loggedIn
  },
  permissionLevel: state => {
    return state.permissionLevel
  },
  firstname: state => {
    return state.firstname
  },
  isAdmin: state => {
    return state.permissionLevel > 4
  },
  userDetailsLoaded: state => {
    return !state.firstname
  },
  getAuthHeader: state => {
    return { 'X-Authorization': state.authToken }
  }
}

export default {
  state,
  mutations,
  actions,
  getters
}
