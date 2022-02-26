<template>
  <nav>
    <ul class="pagination">
      <li
        v-for="page in shownPages"
        :data-test="`page-link-${page}`"
        :key="`${page}-${currentPage}`"
        :class="paginationClass(page)"
        @click.prevent="changePage(page)"
      >
        <a class="page-link" role="button" href v-text="page" />
      </li>
    </ul>
  </nav>
</template>

<script>

export default {
  name: 'Pagination2',

  data () {
    return {
      currentPage: 1,
      numbersShown: 7
    }
  },

  props: {
    loading: Boolean,
    totalCount: Number,
    itemsPerPage: Number
  },

  computed: {
    /** List of page numbers available **/
    pages () {
      if (this.loading || this.totalCount <= this.itemsPerPage) {
        return [1]
      }
      return [
        ...Array(Math.ceil(this.totalCount / this.itemsPerPage)).keys()
      ].map(e => e + 1)
    },

    shownPages () {
      let start = this.currentPage - ((this.numbersShown - 1) / 2)
      let end = this.currentPage + ((this.numbersShown - 1) / 2)

      if (start < 1) {
        end += 1 - start
        start = 1
      }
      if (end > this.totalCount) {
        end = this.pages[-1]
      }

      return this.pages.slice(start - 1, end)
    }
  },

  methods: {
    changePage (goToPage) {
      if (goToPage === this.currentPage) return
      this.currentPage = goToPage
      this.$emit('update:currentPage', this.currentPage)
    },
    paginationClass (page) {
      return {
        'page-item': true,
        active: this.currentPage === page
      }
    }
  }
}
</script>

<style>

.pagination {
  display: inline;
  width: 50px;
}

.page-item {
  display: inline-block;
}

.page-link {
  color: #c5c5c5;
  border-color: #c5c5c5;
}

.page-item.active .page-link {
  background-color: #c5c5c5;
  border-color: #c5c5c5;
}

.page-item.active .page-link:hover {
  color: black;
  border-color: #c5c5c5;
}

.page-link:hover {
  color: black;
}

.page-link:focus {
  box-shadow: none;
}
</style>
