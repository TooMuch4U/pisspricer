<template>
  <div id="home" class="container">
    <div v-if="!isAdmin">
      <div class="row py-3">
        <div class="col-sm-2 d-none d-sm-block"></div>

        <div class="col-sm-8 col-12 min-height">
          <p v-if="loggedIn">
            Oops! You don't have sufficient privileges to view this page. Perhaps you're using the wrong account? <router-link :to="{name: 'logout'}">Logout</router-link>
          </p>
          <p v-else>
            You're not logged in. <router-link :to="{name: 'login'}">Login</router-link>
          </p>
        </div>

        <div class="col-sm-2 d-none d-sm-block"></div>
      </div>
    </div>

    <div v-else>
      <div class="row py-3 bottom-border">
        <div class="col-sm-2 d-none d-sm-block"></div>
        <div class="col-sm-8 col-12">
          <h4>Admin</h4>
        </div>
        <div class="col-sm-2 d-none d-sm-block"></div>
      </div>

      <AdminNav></AdminNav>

      <div class="row text-center min-height">
        <div class="col-12 text-center">

          <router-view/>
        </div>

      </div>
    </div>

  </div>
</template>

<script>
import {mapGetters} from 'vuex'
import AdminNav from '@/components/admin-pages/AdminNav'
export default {
  name: 'AdminPage',
  computed: {
    ...mapGetters(['isAdmin', 'loggedIn'])
  },
  components: {
    AdminNav
  }
}
</script>

<style scoped>
.min-height {
  min-height: 400px;
}
</style>
