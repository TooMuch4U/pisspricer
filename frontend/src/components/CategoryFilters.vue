<template>
  <div class="bottom-border pb-2 mb-3">
    <h5 class="mb-1">Categories</h5>
    <span class="mr-1 mb-1 px-2 d-inline-block cat"
          v-bind:class="{ active: filterCats.includes(cat.categoryId) }"
          v-for="cat in categories"
          v-bind:key="cat.categoryId"
          @click="filterCategory(cat.categoryId)"
          :id="'cat' + cat.categoryId">
              {{ cat.category }}
    </span>
  </div>
</template>

<script>
import {eventBus} from '@/main.js'
export default {
  name: 'CategoryFilters',
  data () {
    return {
      categories: null,
      filterCats: []
    }
  },
  mounted () {
    this.getCategories()
  },
  methods: {
    getCategories: function () {
      this.$http.get(process.env.API_URL + '/categories')
        .then((res) => {
          this.categories = res.data
        })
    },
    filterCategory: function (catId) {
      if (this.filterCats.includes(catId)) {
        this.filterCats.splice(this.filterCats.indexOf(catId), 1)
      } else {
        this.filterCats.push(catId)
      }
      this.$emit('update', this.filterCats)
      eventBus.$emit('remoteUpdateItems')
    }
  }
}
</script>

<style scoped>

</style>
