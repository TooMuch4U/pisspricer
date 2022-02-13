<template>
  <nav>
    <ul class="pagination">
      <li
        v-for="page in pages"
        :data-test="`page-link-${page}`"
        :key="page"
        :class="paginationClass(page)"
        @click.prevent="changePage(page)"
      >
        <a class="page-link" href v-text="page" />
      </li>
    </ul>
  </nav>
</template>

<script>
import {eventBus} from '@/main.js'

export default {
  name: 'Pagination',
  props: {
    pages: {
      type: Array,
      required: true
    },
    currentPage: {
      type: Number,
      required: true
    }
  },
  methods: {
    changePage (goToPage) {
      if (goToPage === this.currentPage) return
      eventBus.$emit('setCurrentPage', goToPage)
      eventBus.$emit('remoteUpdateItems')
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
