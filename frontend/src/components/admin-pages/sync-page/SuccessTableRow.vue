<template>
  <tr>
    <!-- item image -->
    <td>
      <item-image class="align-middle mx-1" :sku="item.item.sku" />
    </td>

    <!-- item -->
    <td class="text-left">
      <span v-if="item.item.loaded">
        {{ item.item.name }}
      </span>
      <spinner v-else-if="!item.item.error" />
      <span class="text-danger" v-else>
        {{ item.item.error.message }}
      </span>
      <span class="text-muted"> {{ item.item.sku }} </span>
    </td>

    <!-- combine input -->
    <td>
      <item-search-field @itemClicked="goToCombine" :filter-sku="item.item.sku" />
    </td>

  </tr>
</template>

<script>
import ItemImage from '@/components/images/ItemImage'
import ItemSearchField from '@/components/utils/ItemSearchField'
import Spinner from '@/components/utils/Spinner'

export default {
  name: 'SuccessTableRow',

  components: {ItemImage, ItemSearchField, Spinner},

  props: {
    item: Object
  },

  methods: {
    goToCombine (newItem) {
      const routeData = this.$router.resolve(
        {path: '/admin/combine', query: {a: newItem.sku, b: this.item.item.sku}})
      window.open(routeData.href, '_blank')
    }
  }
}
</script>

<style scoped>

</style>
