import instance from './instance'

export default {
  getAll: () => instance.get('syncs'),
  getOne: (time) => instance.get(`syncs/${time}`)
}
