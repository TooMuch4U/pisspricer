import instance from './instance'

export default {
  brandImgUrl (brandId) {
    return process.env.VUE_APP_STATIC_URL + 'brands/' + brandId + '.jpeg'
  },

  getAll: () => instance.get(`brands`)
}
