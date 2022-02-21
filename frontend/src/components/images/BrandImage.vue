<template>
  <img class="small" :src="imgSrc" alt="brand logo" >
</template>

<script>
import brands from '@/api/main-api/brands'

export default {
  name: 'ImageSmall',

  props: {
    brandId: {
      type: String,
      required: true
    }
  },

  computed: {
    imgSrc () {
      return brands.brandImgUrl(+this.brandId)
    }
  }
}
</script>

<style scoped>
.small {
  width: 30px
}
</style>
