<template>
  <img class="item-image" :src="imgSrc" alt="item" >
</template>

<script>
import items from '@/api/main-api/items'

export default {
  name: 'ItemImage',

  props: {
    sku: {
      type: Number,
      required: true
    }
  },

  computed: {
    imgSrc () {
      return items.imgUrl(+this.sku)
    }
  }
}
</script>

<style scoped>

.item-image {
  max-width: 50px;
  height: auto;
  max-height: 50px
}
</style>
