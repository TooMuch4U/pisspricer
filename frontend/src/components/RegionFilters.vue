<template>
  <div class="bottom-border pb-2 mb-3">
    <h5 class="mb-1">Store Location</h5>
    <span class="mr-1 mb-1 px-2 d-inline-block cat"
          v-bind:class="{ active: region.regionId === regionFilter }"
          v-for="region in regions"
          v-bind:key="region.regionId"
          @click="filterRegion(region.regionId)"
          :id="'region' + region.regionId">
              {{ region.name }}
    </span>
  </div>
</template>

<script>
import {eventBus} from '@/main.js'
export default {
  name: 'RegionFilters',
  data () {
    return {
      regions: null,
      regionFilter: null
    }
  },
  mounted: function () {
    this.getRegions()
  },
  methods: {
    getRegions: function () {
      this.$http.get(process.env.API_URL + '/regions')
        .then((res) => {
          this.regions = res.data
        })
    },
    filterRegion: function (regId) {
      if (regId === this.regionFilter) {
        this.regionFilter = null
      } else {
        this.regionFilter = regId
      }
      this.$emit('update', this.regionFilter)
      eventBus.$emit('remoteUpdateItems')
    }
  }
}
</script>

<style scoped>

</style>
