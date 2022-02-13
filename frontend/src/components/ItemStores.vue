<template>
  <div>
    <Item :slug="slug"></Item>
    <div id="Stores" class="container-fluid pt-3">
      <div class="row">
        <div class="col-md-1 d-none d-md-block"/>
        <div class="col-md-3 col-12 text-left text-left filter-div">
          <SearchRadiusFilters/>
        </div>

        <div class="col-12 col-md-7">
          <div class="container-fluid">
            <div class="row">

              <div class="col-6 px-0">
                <p class="text-left">
                  Showing {{ (this.currentPage - 1) * this.actualCount + 1 }} -
                  {{ this.currentPage * this.actualCount }} of {{ this.totalCount }}
                </p>
              </div>

              <div class="col-6 px-0">
                <div class="float-right">
                  <label for="sortby">Sort by: </label>
                  <select id="sortby" v-model="order" class="float-right no-outline pointer-cursor bg-white" @change="orderUpdated">
                    <option value="dist-asc">Distance low</option>
                    <option value="dist-desc">Distance high</option>
                    <option value="price-desc">Price high</option>
                    <option value="price-asc" selected="selected">Price low</option>
                  </select>
                </div>
              </div>

            </div>
          </div>

          <table class="text-left table">
            <tr v-for="store in storeData" v-bind:key="store.storeId">
              <td class="text-center">
                <img class="item-image" :src="brandImageUrl(store.brandId)">
              </td>
              <td>
                <p class="mb-0">{{ store.storeName }}</p>
                <p class="mb-0 d-inline text-muted">
                  <span :class="[wasUpdatedOverAWeekAgo(store.dateChecked) ? 'text-danger' : 'text-muted']">
                  Updated {{ getDaysAgoStr(store.dateChecked) }}</span><span v-if="store.distance !== 0">, {{ store.distance.toFixed(1) }}km</span>
                </p>
              </td>
              <td v-if="store.salePrice !== null">
                <s>${{ roundPrice(store.price) }}</s><br/>
                ${{ roundPrice(store.salePrice) }}
              </td>
              <td v-else>${{ store.price }}</td>
            </tr>
          </table>

          <Pagination :pages="pages" :currentPage.sync="currentPage" />

        </div>
        <div class="col-1"/>
      </div>
    </div>
  </div>
</template>

<script>
import Item from '@/components/Item'
import Pagination from '@/components/Pagination'
import SearchRadiusFilters from '@/components/SearchRadiusFilters'
import {eventBus} from '@/main.js'
import { mapGetters } from 'vuex'
import { mapFields } from 'vuex-map-fields'
export default {
  data () {
    return {
      actualCount: 0,
      totalCount: 0,
      currentPage: 1,
      isLoading: 1,
      itemsPerPage: 24,
      slug: null,
      storeData: null,
      itemData: null,
      order: 'price-asc'
    }
  },
  watch: {
    // Update items when search params update
    parameters () {
      this.getStores()
    }
  },
  components: {
    Item,
    Pagination,
    SearchRadiusFilters
  },
  created () {
    this.slug = this.$route.params.slug
    eventBus.$on('setCurrentPage', (page) => {
      this.currentPage = page
      this.scrollToTop()
    })
    eventBus.$on('remoteUpdateItems', () => {
      this.getStores()
    })
    eventBus.$on('updateItemStoresPage', () => {
      this.slug = this.$route.params.slug
      this.loadPage()
    })
  },
  mounted () {
    this.loadPage()
  },
  computed: {
    ...mapGetters(['lat', 'lng']),
    ...mapFields(['mode']),
    radius: {
      set (radius) {
        this.$route.query.r = radius
        this.$store.commit('radius', radius)
      },
      get () {
        return this.$store.state.location.radius
      }
    },
    pages () {
      if (this.isLoading || this.totalCount <= this.itemsPerPage) {
        return [1]
      }
      return [
        ...Array(Math.ceil(this.totalCount / this.itemsPerPage)).keys()
      ].map(e => e + 1)
    },
    parameters () {
      let paramObj = {
        mode: 'slug',
        count: this.itemsPerPage,
        index: ((this.currentPage - 1) * this.itemsPerPage)
      }

      if ((this.radius !== null || this.lat !== null || this.lng !== null) && this.mode === 'near') {
        paramObj.r = this.radius
      }

      paramObj.order = this.order
      paramObj.lat = this.lat
      paramObj.lng = this.lng
      return paramObj
    }
  },
  methods: {
    loadPage () {
      let that = this
      this.$store.dispatch('getLocation', true).then((_) => { that.getStores() })
      this.setRadiusParams()
      this.getStores()
    },
    getStores () {
      this.$http.get(`${process.env.API_URL}/items/${this.slug}/stores`,
        {
          params: this.parameters
        })
        .then((res) => {
          this.storeData = res.data.items
          this.actualCount = res.data.count
          this.totalCount = res.data.totalCount
          this.isLoading = 0
        })
    },
    setRadiusParams () {
      if (typeof this.$route.query.r !== 'undefined') {
        this.mode = 'near'
        this.radius = parseInt(this.$route.query.r)
        this.$store.dispatch('getLocation')
      } else {
        this.mode = 'all'
      }
    },
    orderUpdated () {
      if (this.lat === null || this.lng === null) {
        this.$store.dispatch('getLocation')
          .catch(() => {
            this.order = 'price-asc'
          })
      }
    },
    wasUpdatedOverAWeekAgo (dateStr) {
      // Get dates
      let today = new Date()
      let past = new Date(dateStr)

      // Calculate times
      let days = (today - past) / (1000 * 3600 * 24)

      return days > 7
    },
    getDaysAgoStr (dateStr) {
      // Get dates
      let today = new Date()
      let past = new Date(dateStr)

      // Calculate times
      let days = (today - past) / (1000 * 3600 * 24)
      let hours = (today - past) / (1000 * 3600)
      let minutes = (today - past) / ((1000 * 3600) / 60)
      const datesAreOnSameDay = (
        past.getFullYear() === today.getFullYear() &&
        past.getMonth() === today.getMonth() &&
        past.getDate() === today.getDate())
      const dateIsYesterday = (
        (past.getDay() + 1) === today.getDay() &&
        days < 2)

      if (hours < 1) {
        return `${Math.floor(minutes)} minutes ago`
      } else if (hours < 4) {
        return `${Math.floor(hours)} hours ago`
      } else if (datesAreOnSameDay) {
        // updated today
        if (past.getHours() < 12) {
          // Updated this morning
          return 'this morning'
        } else if (past.getHours() < 14) {
          return 'midday today'
        } else {
          return 'this afternoon'
        }
      } else if (dateIsYesterday) {
        return 'yesterday'
      } else if (days < 7) {
        return parseInt(days) + ' days ago'
      } else if (days < 30) {
        return 'over a week ago'
      } else {
        return 'over a month ago'
      }
    },
    itemImageUrl (sku) {
      return process.env.VUE_APP_STATIC_URL + 'items/' + sku + '.jpeg'
    },
    brandImageUrl (brandId) {
      return `${process.env.VUE_APP_STATIC_URL}brands/${brandId}.jpeg`
    },
    scrollToTop () {
      window.scrollTo(0, 100)
    },
    roundPrice (num) {
      return (Math.round(num * 100) / 100).toFixed(2)
    }
  },
  name: 'ItemStores'
}
</script>

<style scoped>

  .item-image {
    max-width: 50px;
    height: 50px;
  }
  .no-outline {
    outline: none;
    border: 0;
  }

  .bottom-border {
    border-bottom: 1px solid #dee2e6!important;
  }

  .pointer-cursor {
    cursor: pointer;
  }

  .filter-div {
    border-right: 1px solid #dee2e6!important;
  }
</style>
