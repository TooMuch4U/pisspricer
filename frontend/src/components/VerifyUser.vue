<template>
  <div id="verify" class="container-fluid pt-3">

    <div class="row mb-3 mx-1">
      <div class="col-lg-4 col-md-3 col-sm-2 d-none d-sm-block"/>

      <div class="col-lg-4 col-md-6 col-sm-8 col-12 border-bottom">
        <h4> Account Verification </h4>
      </div>

      <div class="col-lg-4 col-md-3 col-sm-2 d-none d-sm-block"/>
    </div>

    <div class="row px-1">
      <div class="col-lg-4 col-md-3 col-sm-2 d-none d-sm-block"/>

      <div class="col-lg-4 col-md-6 col-sm-8 col-12">

        <div v-if="success" class="alert alert-success" role="alert">
          Account successfully verified! <router-link :to="{name: 'login'}">Login</router-link>
        </div>

        <div v-else-if="error !== null">
          <div class="alert alert-danger" role="alert">
            {{ error }}
          </div>

          <div v-if="error.includes('already')">
            Try <router-link :to="{name: 'login'}">login</router-link> instead.
          </div>

          <div v-else>
            Resend a new code <router-link :to="{name: 'resend'}">here</router-link> instead
          </div>

        </div>

        <div v-else>
          Verifying your account... <img class="loading-img" src="@/assets/loading.gif">
        </div>

      </div>

      <div class="col-lg-4 col-md-3 col-sm-2 d-none d-sm-block"/>
    </div>
  </div>
</template>

<script>
export default {
  name: 'VerifyUser',
  data () {
    return {
      error: null,
      success: null
    }
  },
  created () {
    this.verifyAccount()
  },
  methods: {
    verifyAccount () {
      const userId = this.$route.params.userId
      const code = this.$route.params.code
      this.$store.dispatch('verifyUser', {userId, code})
        .then((res) => {
          this.success = true
        })
        .catch((err) => {
          this.error = err.response.statusText
        })
    }
  }
}
</script>

<style scoped>
#verify {
  min-height: 400px;
}
.loading-img {
  width: 15px;
}
</style>
