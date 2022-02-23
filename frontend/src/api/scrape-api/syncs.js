import instance from './instance'

export default {
  getAll: () => instance.get('syncs'),
  getOne: (time, failPage = 1) => instance.get(`syncs/${time}`, { params: { failPage } }),
  FAIL_ITEMS_PER_PAGE: 10
}
