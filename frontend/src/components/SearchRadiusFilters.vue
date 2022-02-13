<template>
  <div class="bottom-border pb-2 mb-3">
    <h5 class="mb-1 d-inline-block">Stores</h5>
    <img class="loading-img" v-if="this.loading" src="@/assets/loading.gif">
    <br/>

    <span class="mr-1 mb-1 px-2 d-inline-block cat"
          v-bind:class="{ active: this.mode !== 'all' }"
          @click="nearMeClicked">
              near me
    </span>
    <span class="mr-1 mb-1 px-2 d-inline-block cat"
          v-bind:class="{ active: this.mode === 'all' }"
          @click="allClicked">
              all
    </span>
    <div v-if="this.mode !== 'all'">
      <input id="radius-slider"
             type="range"
             min='1' :max="max"
             v-model="radius"
             class="d-inline-block"
             @change="rangeUpdated">
      <p class="d-inline-block">{{ radius }} km</p>
    </div>

  </div>
</template>

<script>
import {eventBus} from '@/main.js'
export default {
  name: 'SearchRadiusFilters',
  data () {
    return {
      max: 50,
      min: 1,
      loading: 0
    }
  },
  created: function () {
    eventBus.$on('searchRadiusUpdateMode', (mode) => {
      if (mode === 'all') {
        this.mode = 'all'
        return
      }
      this.mode = 'near'
    })
  },
  mounted () {
    this.setRadiusParams()
    if (typeof this.$route.query.r !== 'undefined') {
      this.radius = this.$route.query.r
      this.nearMeClicked()
    }
  },
  computed: {
    lat () {
      return this.$store.state.location.lat
    },
    lng () {
      return this.$store.state.location.lng
    },
    radius: {
      set (radius) {
        this.$store.commit('radius', radius)
      },
      get () {
        return this.$store.state.location.radius
      }
    },
    mode: {
      set (mode) {
        if (mode === 'all') {
          this.$store.commit('modeAll')
        } else {
          this.$store.commit('modeNear')
        }
      },
      get () {
        return this.$store.state.location.mode
      }
    }
  },
  methods: {
    allClicked () {
      this.mode = 'all'
      this.$emit('updateMode', this.mode)
      eventBus.$emit('remoteUpdateItems')
      this.updateUrl()
    },
    setRadiusParams () {
      if (this.$route.query.r != null) {
        this.mode = 'near'
        this.radius = parseInt(this.$route.query.r)
      }
    },
    nearMeClicked () {
      this.mode = 'near'
      this.loading = 1
      if (this.lat === null) {
        this.$store.dispatch('getLocation')
          .then((loc) => {
            if (loc.lat !== null) {
              this.$emit('updateMode', this.mode)
              this.rangeUpdated()
            } else {
              this.allClicked()
            }
            this.updateUrl()
            this.loading = 0
          }).catch((err) => { console.log(err) })
      } else {
        this.$emit('updateMode', this.mode)
        this.rangeUpdated()
        this.updateUrl()
        this.loading = 0
      }
    },
    updateUrl () {
      let oldQuery = {...this.$route.query}
      if (this.mode === 'near') {
        oldQuery.r = this.radius
      } else {
        delete oldQuery.r
      }
      this.$router.replace({ query: oldQuery }).catch(() => {})
    },
    rangeUpdated () {
      this.$emit('updateRadius', parseInt(this.radius), this.lat, this.lng)
      eventBus.$emit('remoteUpdateItems')
    }
  }
}
</script>

<style scoped>
#radius-slider {
  color: black;
}

.loading-img {
  width: 15px;
}
</style>
