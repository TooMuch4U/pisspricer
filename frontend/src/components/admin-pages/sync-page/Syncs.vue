<template>
  <div>
    <error-alert v-if="error">
      {{ error }}
    </error-alert>

    <!-- Loading div -->
    <spinner v-if="loadingSyncs" />

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
    <spinner v-if="loadingSync"/>

    <!-- Selected sync -->
    <div v-else-if="selectedSync">
      <sync :sync-data="selectedSync"/>
    </div>
  </div>
</template>

<script>
import syncs from '@/api/scrape-api/syncs'
import { getDateString } from '@/utils/date'
import Sync from '@/components/admin-pages/sync-page/Sync'
import Spinner from '@/components/utils/Spinner'
import ErrorAlert from '@/components/utils/ErrorAlert'

export default {
  name: 'Syncs',

  data: () => {
    return {
      syncs: [],
      loadingSyncs: true,
      selectedSyncId: null,
      selectedSync: null,
      loadingSync: false,
      error: null
    }
  },

  components: { Sync, Spinner, ErrorAlert },

  mounted () {
    this.loadSyncs()
  },

  watch: {
    async selectedSyncId () {
      try {
        this.selectedSync = null
        this.loadingSync = true
        this.selectedSync = (await syncs.getOne(this.selectedSyncId)).data
      } catch (err) {
        this.error = err
      } finally {
        this.loadingSync = false
      }
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
          this.selectedSyncId = this.syncsAscending[0].id
          this.loadingSyncs = false
        })
        .catch((err) => {
          this.error = err
          this.loadingSyncs = false
        })
    },
    getDateString: getDateString
  }
}
</script>

<style scoped>

</style>
