import instance from './instance'

export default {
  imgUrl (sku) {
    return process.env.VUE_APP_STATIC_URL + 'items/' + sku + '.jpeg'
  },

  getAll: () => instance.get(`items`),
  getOne: (sku) => instance.get(`items/${sku}`),
  getSuggestions: (search, count) => instance.get('/suggestions', { params: { search, count } })
}
