<template>
  <div>
    <table class="table">
      <tr>
        <th>Brand</th>
        <th>Status</th>
        <th>Successes</th>
        <th>Fails</th>
      </tr>

      <tr v-bind:key="brand.id" v-for="brand in syncDataWithBrands.brands">

        <!-- brand info -->
        <td class="brand-col-width">
          <brand-image :brandId="brand.id" />
          <a
            v-if="brand.name"
            target="_blank"
            :href="brand.url">{{ brand.name }} ({{ brand.brandId }})
          </a>

          <!-- display loading on info not yet populated -->
          <spinner v-else class="small-spinner" />
        </td>

        <!-- status -->
        <td>
          <div class="text-success" v-if="hasFinished(brand)">
            finished ({{ getTimeDiffFormatted(brand.startTime, brand.endTime) }})
          </div>
          <div class="text-warning" v-else>
            in progress ({{ getTimeSinceNowFormatted(brand.startTime) }})
          </div>
        </td>

        <!-- success count -->
        <td>
          {{ brand.successCount }}
        </td>

        <!-- fail count -->
        <td>
          <a href="#" data-toggle="modal" :data-target="`#fails-${brand.id}`">
            {{ brand.failsCount }}
          </a>
        </td>

        <!-- fails modal -->
        <basic-modal
          :modalId="`fails-${brand.id}`"
          :modalHeader="`${brand.name} Fails`"
          modalDismissText="Close"
        >
          <fails-table
            :fails="brand.fails"
            :brandId="brand.id"
            :syncDate="syncData.id"
            :totalCount="brand.failsCount"
          />
        </basic-modal>

      </tr>

      <tr>
        <td/><td/><td/><td/>
      </tr>

    </table>
  </div>
</template>

<script>
import brands from '@/api/main-api/brands'
import { cloneDeep } from 'lodash'
import { getTimeDiffFormatted, getTimeSinceNowFormatted } from '@/utils/date'

import BrandImage from '@/components/images/BrandImage'
import BasicModal from '@/components/modal/BasicModal'
import FailsTable from '@/components/admin-pages/sync-page/FailsTable'
import Spinner from '@/components/utils/Spinner'

export default {
  name: 'Sync.vue',

  data () {
    return {
      syncDataWithBrands: this.syncData
    }
  },

  props: {
    syncData: {
      required: true
    }
  },

  components: { BrandImage, BasicModal, FailsTable, Spinner },

  mounted () {
    brands.getAll()
      .then((res) => {
        const allBrands = res.data
        let newSyncData = cloneDeep(this.syncData)

        // add brand details to each brand
        newSyncData.brands.forEach(function (brandEl, index) {
          const brandInfo = allBrands.find(item => item.brandId === +brandEl.id)
          newSyncData.brands[index] = {...brandInfo, ...brandEl}
        })

        // set data
        this.syncDataWithBrands = newSyncData
      })
  },
  methods: {
    brandImgUrl: brands.brandImgUrl,
    getTimeDiffFormatted,
    getTimeSinceNowFormatted,

    hasFinished (brand) {
      return brand.endTime != null
    }
  }
}
</script>

<style scoped>
.small-spinner {
  width: 20px;
  height: 20px;
}

.brand-col-width {
  width: 200px;
}
</style>
