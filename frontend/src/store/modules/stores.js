import axios from 'axios'

let state = {}

let mutations = {}

let actions = {
  getBrands ({dispatch, commit, getters}) {
    return new Promise((resolve, reject) => {
      axios.get(`${process.env.API_URL}/brands`, { headers: getters.getAuthHeader })
        .then((res) => {
          resolve(res)
        })
        .catch((err) => {
          reject(err)
        })
    })
  },
  createBrand ({dispatch, commit, getters}, newBrand) {
    return new Promise((resolve, reject) => {
      axios.post(`${process.env.API_URL}/brands`,
        newBrand,
        { headers: getters.getAuthHeader })
        .then((res) => {
          resolve(res)
        })
        .catch((err) => {
          reject(err)
        })
    })
  },
  putBrandImage ({dispatch, getters}, {imageData, brandId}) {
    return new Promise((resolve, reject) => {
      axios.put(`${process.env.API_URL}/brands/${brandId}/image`,
        imageData,
        { headers: getters.getAuthHeader })
        .then((res) => {
          resolve(res)
        })
        .catch((err) => {
          reject(err)
        })
    })
  }
}

let getters = {}

export default {
  state,
  mutations,
  actions,
  getters
}
