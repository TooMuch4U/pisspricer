<template>
  <div>
    <table>
      <!-- header -->
      <tr>
        <th>Image</th>
        <th>Response</th>
        <th>Store</th>
        <th>Location</th>
        <th>Item</th>
      </tr>

      <!-- content -->
      <tr
        v-if="!loading"
        v-for="fail in pagedFails"
        v-bind:key="`${fail.item.itemPrice.internalSku}-${fail.item.store.internalId}`"
      >
        <!-- image -->
        <td>
          <img :alt="fail.item.item.name" class="small" :src="`data:image/png;base64,${fail.item.item.image}`" />
        </td>

        <!-- response -->
        <td>{{ fail.status }} {{ fail.message }}</td>

        <!-- store -->
        <td>
          {{ fail.item.store.name }}
          <p class="text-muted">({{ fail.item.store.internalId }})</p>
        </td>

        <!-- location -->
        <td class="text-left">
          Latitude: {{ fail.item.store.location.lattitude }}<br/>
          Longitude: {{ fail.item.store.location.longitude }}<br/>
          Address: {{ fail.item.store.location.address }}<br/>
          Region: {{ fail.item.store.location.region }}<br/>
          Postcode: {{ fail.item.store.location.postcode }}<br/>
        </td>

        <!-- item -->
        <td class="text-left">
          <strong>Name:</strong> {{ fail.item.item.name }} <span class="text-muted">
          ({{ fail.item.itemPrice.internalSku }})</span><br/>
          <strong>InternalSku:</strong> <br/>
          <strong>Price:</strong> {{ fail.item.itemPrice.price }}<br/>
          <strong>Sale Price:</strong> {{ fail.item.itemPrice.salePrice }}<br/>
          <strong>Stock:</strong> {{ fail.item.itemPrice.stock }}<br/>
        </td>
      </tr>
    </table>

    <spinner v-if="loading" />

    <pagination2
      :currentPage.sync="page"
      :loading="loading"
      :total-count="totalCount"
      :items-per-page="itemsPerPage"
    />
  </div>
</template>

<script>
import syncs from '@/api/scrape-api/syncs'
import Pagination2 from '@/components/utils/Pagination2'
import Spinner from '@/components/utils/Spinner'

export default {
  name: 'FailsTable',

  components: { Pagination2, Spinner },

  data () {
    return {
      loading: false,
      page: 1,
      loadedFails: null,
      itemsPerPage: syncs.FAIL_ITEMS_PER_PAGE
    }
  },

  props: {
    fails: Array,
    syncDate: String,
    brandId: String,
    totalCount: Number
  },

  watch: {
    page (newPage) {
      this.loading = true
      if (newPage === 1) {
        this.loading = false // we still want to toggle this to bring user to top of modal
        return
      }
      syncs.getOne(this.syncDate, this.page)
        .then((res) => {
          this.loadedFails = res.data.brands.find(brand => brand.id === this.brandId).fails
          this.loading = false
        })
    }
  },

  computed: {
    /** Fails array paginated **/
    pagedFails () {
      if (this.page === 1) return this.fails
      return this.loadedFails
    }
  }
}
</script>

<style scoped>
.small {
  height: 50px;
}
</style>
