<template>
  <div id="logout" class="container-fluid pt-3">

    <div class="row mb-3 mx-1">
      <div class="col-lg-4 col-md-3 col-sm-2 d-none d-sm-block"/>

      <div class="col-lg-4 col-md-6 col-sm-8 col-12 border-bottom">
        <h4> Logout </h4>
      </div>

      <div class="col-lg-4 col-md-3 col-sm-2 d-none d-sm-block"/>
    </div>

    <div class="row px-1">
      <div class="col-lg-4 col-md-3 col-sm-2 d-none d-sm-block"/>

      <div class="col-lg-4 col-md-6 col-sm-8 col-12">

        <div v-if="error !== null" class="alert alert-danger" role="alert">
          {{ error }}
        </div>

        <div v-if="loggedIn">
          currently logged in as {{firstname}}
          <button class="btn btn-primary" @click="logout">Logout</button>
        </div>

        <div v-else>
          You're already logged out. <router-link :to="{name: 'login'}">Login</router-link> instead
        </div>

      </div>

      <div class="col-lg-4 col-md-3 col-sm-2 d-none d-sm-block"/>
    </div>
  </div>
</template>

<script>
import {mapGetters} from 'vuex'
export default {
  name: 'Logout',
  data () {
    return {
      error: null,
      name: null
    }
  },
  computed: {
    ...mapGetters(['loggedIn', 'firstname'])
  },
  methods: {
    logout () {
      this.name = null
      this.$store.dispatch('logout')
      this.$router
        .push({name: 'login'})
    }
  }
}
</script>

<style scoped>
#logout {
  min-height: 400px;
}
</style>
