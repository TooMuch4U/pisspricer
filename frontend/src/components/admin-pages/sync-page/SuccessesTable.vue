<template>
  <div>
    <table class="mx-auto">
      <!-- header -->
      <tr>
        <th></th>
        <th>Item</th>
        <th>Combine</th>
      </tr>

      <!-- content -->
      <success-table-row
        v-for="item in loadedItems"
        v-bind:key="`${item.item.sku}-${item.store.id}`"
        :item="item"
      />

    </table>

    <pagination2
      :currentPage.sync="page"
      :loading="false"
      :total-count="totalCount"
      :items-per-page="itemsPerPage"
    />
  </div>
</template>

<script>
import items from '@/api/main-api/items'
import Pagination2 from '@/components/utils/Pagination2'
import Spinner from '@/components/utils/Spinner'
import SuccessTableRow from '@/components/admin-pages/sync-page/SuccessTableRow'

export default {
  name: 'SuccessesTable',

  components: { Pagination2, Spinner, SuccessTableRow },

  data () {
    return {
      page: 1,
      itemsPerPage: 10,
      loadedItems: [],
      skuToCombine: null
    }
  },

  props: {
    successes: Array,
    totalCount: Number
  },

  mounted () {
    this.loadedItems = this.pagedItems
  },

  watch: {
    pagedItems (newPagedItems) {
      this.loadedItems = newPagedItems
    },

    loadedItems () {
      this.loadedItems.forEach((item, index) => {
        this.addFullItemData(item, index, this.loadedItems)
      })
    }
  },

  computed: {
    /** Fails array paginated **/
    pagedItems () {
      return this.successes.slice((this.page - 1) * this.itemsPerPage, this.itemsPerPage * this.page)
    }
  },

  methods: {
    /**
     * Request the item's data (i.e. name) from api and adds it to provided array at index
     * @param item Full item from sync endpoint
     * @param index Index of the item in the array
     * @param arr The array to update
     */
    addFullItemData (item, index, arr) {
      items.getOne(item.item.sku)
        .then((res) => {
          const newItem = res.data
          item['item'] = {...item.item, ...newItem, loaded: true}
          arr[index] = item
        })
    }
  }
}
</script>

<style scoped>
.small {
  height: 50px;
}
</style>
