<template>
  <div>
    <!-- Loading div -->
    <div v-if="loadingSyncs" class="spinner-border text-muted" />

    <!-- Sync list div -->
    <div v-else class="form-group">
      <select v-model="selectedSyncId" class="form-control w-50 m-auto">
        <option
          v-bind:key="sync.id"
          v-for="sync in syncs"
          :value="sync.id"
        >
          {{ getDateString(sync.id) }}
        </option>
      </select>
    </div>

    <!-- Selected sync loading -->
    <div v-if="loadingSync" class="spinner-border text-muted"></div>

    <!-- Selected sync -->
    <div v-else-if="selectedSync">
      <sync :sync-data="selectedSync"/>
    </div>
  </div>
</template>

<script>
import syncs from '@/api/scrape-api/syncs'
import { getDateString } from '../../../utils/date'
import Sync from '@/components/admin-pages/sync-page/Sync'

export default {
  name: 'Syncs',

  data: () => {
    return {
      syncs: [],
      loadingSyncs: true,
      selectedSyncId: null,
      selectedSync: null,
      loadingSync: false
    }
  },

  components: {Sync},

  mounted () {
    this.loadSyncs()
  },

  watch: {
    async selectedSyncId () {
      this.selectedSync = null
      this.loadingSync = true
      this.selectedSync = (await syncs.getOne(this.selectedSyncId)).data
      this.loadingSync = false
    }
  },

  computed: {
    syncsAscending () {
      return Array.reverse(this.syncs)
    }
  },

  methods: {
    loadSyncs () {
      syncs.getAll()
        .then((res) => {
          this.syncs = res.data
          if (this.syncs.length > 0) {
            this.selectedSyncId = this.syncsAscending[0].id
          }
          this.loadingSyncs = false
        })
    },
    getDateString: getDateString
  }
}
</script>

<style scoped>

</style>
