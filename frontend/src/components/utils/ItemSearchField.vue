<template>
  <div>
    <form action="." @submit.prevent>
      <input class="form-control mt-2 input-outline shadow-none"
             type="search"
             v-model="searchTerm"
             id="search-input"
             placeholder="Search"
             @keyup="getPreview($event)">
    </form>

    <div  id="suggestions" v-if="items !== null" v-click-outside="hideWindow">
      <ul class="list-group">
        <li class="list-group-item suggestion-item text-left"
            v-for="item in items"
            :key="item.sku"
            @click="itemClicked(item)">
          <div class="img-div mr-3 text-center">
            <img v-if="item.hasImage" class="item-image" :src="imageSrc(item.sku)">
            <img v-else class="item-image" src="@/../static/favicon.png">
          </div>
          {{ item.name }}
        </li>
        <li class="list-group-item">
          <a id="search-link"
             v-on:click="searchClicked">
            Show all {{itemsTotalCount}} results →
          </a>
        </li>
      </ul>
    </div>
  </div>
</template>

<script>
import {eventBus} from '@/main'
import items from '@/api/main-api/items'

export default {
  name: 'ItemSearchField',
  data () {
    return {
      searchTerm: null,
      items: null,
      itemsCount: 0,
      itemsTotalCount: 0,
      itemLimit: 5,
      hide: false
    }
  },

  props: {
    filterSku: Number,
  },

  methods: {
    imageSrc: items.imgUrl,
    searchItems: function () {
      this.$router
        .push({name: 'items', query: {s: this.searchTerm}}) // Change page to items page
        .catch(() => {}) // Catch error if already on items page
      if (this.$route.name === 'items') {
        eventBus.$emit('updateCurrentPage', 1)
        eventBus.$emit('remoteUpdateItems')
      }
    },
    hideWindow () {
      this.hide = true
      document.getElementById('search-input').blur()
      document.getElementById('search-input2').blur()
      this.items = null
    },
    searchClicked () {
      this.searchItems()
      this.hideWindow()
    },
    itemClicked (item) {
      this.$emit('itemClicked', item)
      this.hideWindow()
    },
    getPreview (event) {
      if (this.searchTerm.length > 1 && event.key !== 'Enter') {
        // if current search term is longer than 1 char
        this.hide = false
        items.getSuggestions(this.searchTerm, this.itemLimit)
          .then((res) => {
            this.items = res.data.items.filter(item => +item.sku !== +this.filterSku)
            this.itemsCount = res.data.count
            this.itemsTotalCount = res.data.totalCount
            if (this.hide) {
              this.hideWindow()
            }
          })
      } else {
        // Don't get any items, search term not long enough
        this.items = null
      }
    }
  }
}
</script>

<style scoped>

.navbar-brand {
  font-size: 2rem;
}

.form-control:focus {
  border: 1px solid #ced4da;
}

.bg-custom {
  background-color: #00c5ba;
}

.border-bottom {
  border-bottom: black 1px;
}

#ul {
  background-color: white;
}

#suggestions {
  position: absolute;
  border-bottom: none;
  border-top: none;
  z-index: 99;
  /*position the autocomplete items to be the same width as the container:*/
  left: 10%;
  right: 10%;
}

.suggestion-item:first-child {
  border-top: 0;
  border-top-left-radius: 0;
  border-top-right-radius: 0;
}

.suggestion-item:hover {
  background-color: #eeeeee;
  cursor: pointer;
}

.suggestion-item {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

#search-link {
  color: #007bff;
  cursor: pointer;
}

#search-input {
  width: 200px;
}

.item-image {
  max-width: 40px;
  height: 20px;
}

.img-div {
  width: 40px;
  height: 20px;
  display: inline-block;
}

.gold-colour {
  color: #D4AF37;
}

/*#suggestions {*/
/*  left: 60%;*/
/*  right: 20%;*/
/*}*/

/*@media (min-width: 576px) {*/
/*  #suggestions {*/
/*    left: 60%;*/
/*    right: 20%;*/
/*  }*/
/*}*/

/*@media (min-width: 768px) {*/
/*  #suggestions {*/
/*    left: 25%;*/
/*    right: 25%;*/
/*  }*/
/*}*/

/*@media (min-width: 992px) {*/
/*  #suggestions {*/
/*    left: 35%;*/
/*    right: 35%;*/
/*  }*/
/*}*/

/*@media (min-width: 1200px) {*/
/*  #suggestions {*/
/*    left: 35%;*/
/*    right: 35%;*/
/*  }*/
/*}*/

</style>
