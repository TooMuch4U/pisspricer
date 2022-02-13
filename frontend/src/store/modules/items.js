import axios from 'axios'

let state = {}

let mutations = {}

let actions = {
  getItem ({dispatch, commit, getters}, {sku}) {
    return new Promise((resolve, reject) => {
      axios.get(`${process.env.API_URL}/items/${sku}`, { headers: getters.getAuthHeader })
        .then((res) => {
          resolve(res)
        })
        .catch((err) => {
          reject(err)
        })
    })
  },
  combineItems ({dispatch, getters}, {skuA, skuB, newItem}) {
    return new Promise((resolve, reject) => {
      axios.patch(
        `${process.env.API_URL}/items/${skuA}/combine/${skuB}`,
        newItem,
        { headers: getters.getAuthHeader })
        .then((res) => { resolve(res) })
        .catch((err) => { reject(err) })
    })
  },
  editItem ({dispatch, getters}, {sku, newParams}) {
    return new Promise((resolve, reject) => {
      axios.patch(
        `${process.env.API_URL}/items/${sku}`,
        newParams,
        { headers: getters.getAuthHeader })
        .then((res) => { resolve(res) })
        .catch((err) => { reject(err) })
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
