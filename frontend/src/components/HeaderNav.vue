<template>
  <div>
    <div class="container-fluid">
      <div class="row border-bottom">
        <div class="col-1 d-none d-md-block"/>

        <nav class="navbar flex-nowrap d-flex d-md-flex navbar-light col-12 col-md-10">
          <div class="d-flex w-50 order-0">
          </div>
          <div class="d-flex justify-content-center order-2" id="collapsingNavbar">
            <ul class="navbar-nav flex-sm-row">
              <li class="nav-item">
                <router-link class="navbar-brand"
                             :to="{ name: 'home' }">
                  Pisspricer
                </router-link>
              </li>
              <li class="nav-item d-none d-sm-block">
                <form action="." @submit.prevent>
                  <input class="form-control mt-2 input-outline shadow-none"
                         type="search"
                         v-model="searchTerm"
                         id="search-input"
                         placeholder="Search"
                         @keyup="getPreview($event)"
                         @keyup.enter="searchClicked">
                </form>
              </li>
            </ul>
          </div>
          <span class="text-right order-last w-50 pr-1">
            <router-link :to="{name: 'logout'}" v-if="loggedIn && !isAdmin">
              <font-awesome-icon class="text-dark" size="sm" :icon="['fas', 'user']" />
            </router-link>

            <router-link :to="{name: 'admin'}" v-else-if="loggedIn">
              <font-awesome-icon class="gold-colour" size="sm" :icon="['fas', 'user']" />
            </router-link>

            <div v-else>

              <router-link :to="{name: 'login'}">
                <font-awesome-icon class="text-dark" size="sm" :icon="['far', 'user']" />
              </router-link>
            </div>
          </span>

        </nav>

        <nav class="navbar pt-0 w-100 mb-1 d-sm-none">

          <div class="d-flex justify-content-center order-2 w-100" >
            <ul class="navbar-nav flex-sm-row w-100">
              <li class="nav-item w-100">
                <form action="." @submit.prevent>
                  <input class="form-control input-outline mb-2 shadow-none w-100"
                         type="search"
                         v-model="searchTerm"
                         id="search-input2"
                         placeholder="Search"
                         @keyup="getPreview($event)"
                         @keyup.enter="searchClicked">
                </form>
              </li>
            </ul>
          </div>

        </nav>

        <div class="col-1 d-none d-md-block"/>
      </div>
    </div>

    <div class="mx-auto" id="suggestions" v-if="items !== null" v-click-outside="hideWindow">
      <ul class="list-group">
        <li class="list-group-item suggestion-item text-left"
            v-for="item in items"
            :key="item.sku"
            v-on:click="itemClicked(item)">
          <div class="img-div mr-3 text-center">
            <img v-if="item.hasImage" class="item-image" :src="imageSrc(item.sku)">
            <img v-else class="item-image" src="../../static/favicon.png">
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
import {eventBus} from '@/main.js'
import {mapGetters} from 'vuex'
export default {
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
  computed: {
    ...mapGetters(['isAdmin']),
    loggedIn () {
      return this.$store.state.user.loggedIn
    }

  },
  methods: {
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
      this.$router
        .push({ name: 'item', params: { slug: item.slug } }) // Change page to items page
        .catch(() => {}) // Catch error if already on items page
      if (this.$route.name === 'item') {
        eventBus.$emit('updateItemStoresPage')
      }
      this.hideWindow()
    },
    imageSrc (sku) {
      return process.env.VUE_APP_STATIC_URL + 'items/' + sku + '.jpeg'
    },
    getPreview (event) {
      if (this.searchTerm.length > 1 && event.key !== 'Enter') {
        // if current search term is longer than 1 char
        this.hide = false
        this.$http.get(process.env.API_URL + '/suggestions',
          { params: {
            search: this.searchTerm,
            count: this.itemLimit
          } })
          .then((res) => {
            this.items = res.data.items
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
  },
  name: 'HeaderNav'
}
</script>

<style>

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

@media (min-width: 576px) {
  #suggestions {
    left: 20%;
    right: 20%;
  }
}

@media (min-width: 768px) {
  #suggestions {
    left: 25%;
    right: 25%;
  }
}

@media (min-width: 992px) {
  #suggestions {
    left: 35%;
    right: 35%;
  }
}

@media (min-width: 1200px) {
  #suggestions {
    left: 35%;
    right: 35%;
  }
}

</style>
