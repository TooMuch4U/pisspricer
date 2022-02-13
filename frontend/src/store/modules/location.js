import VueGeolocation from 'vue-browser-geolocation/src'
import { getField, updateField } from 'vuex-map-fields'

let state = {
  lat: null,
  lng: null,
  radius: 50,
  mode: 'all'
}

let mutations = {
  updateField,
  lat (state, newLat) {
    state.lat = newLat
  },
  lng (state, newLng) {
    state.lng = newLng
  },
  radius (state, newRadius) {
    state.radius = newRadius
  },
  mode (state, newMode) {
    if (newMode === 'all') {
      state.mode = 'all'
    } else {
      state.mode = 'near'
    }
  },
  modeAll (state) {
    state.mode = 'all'
  },
  modeNear (state) {
    state.mode = 'near'
  }
}

let actions = {
  updateLocation ({commit}) {
    return new Promise((resolve, reject) => {
      VueGeolocation.getLocation()
        .then(coordinates => {
          commit('lat', coordinates.lat)
          commit('lng', coordinates.lng)
          resolve({lat: coordinates.lat, lng: coordinates.lng})
        }).catch((err) => {
          reject(err)
        })
    })
  },
  getLocation ({commit, dispatch, state}, noPrompt = false) {
    return new Promise((resolve, reject) => {
      if (state.lat === null) {
        if (noPrompt) {
          navigator.permissions.query({name: 'geolocation'})
            .then(function (status) {
              if (status.state === 'granted') {
                dispatch('updateLocation')
                  .then((loc) => {
                    resolve(loc)
                  }).catch((err) => {
                    reject(err)
                  })
              } else {
                commit('modeAll')
                reject(new Error('Location not available'))
              }
            })
        } else {
          dispatch('updateLocation')
            .then((loc) => {
              resolve(loc)
            }).catch((err) => {
              reject(err)
            })
        }
      } else {
        resolve({lat: this.lat, lng: this.lng})
      }
    })
  }
}

let getters = {
  getField,
  lat: state => {
    return state.lat
  },
  lng: state => {
    return state.lng
  },
  mode: state => {
    return state.mode
  }
}

export default {
  state,
  mutations,
  actions,
  getters
}
