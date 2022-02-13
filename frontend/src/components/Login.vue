<template>
  <div id="login" class="container-fluid pt-3">

    <div class="row mb-3 mx-1">
      <div class="col-lg-4 col-md-3 col-sm-2 d-none d-sm-block"/>

      <div class="col-lg-4 col-md-6 col-sm-8 col-12 border-bottom">
        <h4> Login </h4>
      </div>

      <div class="col-lg-4 col-md-3 col-sm-2 d-none d-sm-block"/>
    </div>

    <div class="row px-1">
      <div class="col-lg-4 col-md-3 col-sm-2 d-none d-sm-block"/>

      <div class="col-lg-4 col-md-6 col-sm-8 col-12">

        <div v-if="error !== null" class="alert alert-danger" role="alert">
          {{ error }}
        </div>
        <div v-if="error && error.includes('not verified')">
          Can't find you verification email? Resend it <router-link :to="{name: 'resend'}">here</router-link>
          <br><br>
        </div>

        <form v-on:submit.prevent>
          <div class="form-group text-left">
            <label for="email">Email address</label>
            <input v-model="email" type="email" class="form-control" id="email" aria-describedby="emailHelp" placeholder="email">
          </div>
          <div class="form-group text-left">
            <label for="password">Password</label>
            <input v-model="password" type="password" class="form-control" id="password" placeholder="Password">
          </div>

          <div class="form-row">
            <div class="form-group col-6">
              <button type="button" class="btn btn-block btn-light" @click="gotoRegister">Register</button>
            </div>
            <div class="form-group col-6">
              <button class="btn btn-block btn-primary" @click="loginPressed">Login</button>
            </div>
          </div>
        </form>

      </div>

      <div class="col-lg-4 col-md-3 col-sm-2 d-none d-sm-block"/>
    </div>
  </div>
</template>

<script>
export default {
  name: 'login',
  data () {
    return {
      email: null,
      password: null,
      error: null
    }
  },
  methods: {
    loginPressed () {
      if (this.email === null || this.email === '') {
        this.error = 'an email must be supplied'
      } else if (this.password === null) {
        this.error = 'a password must be supplied'
      } else {
        this.$store.dispatch('login', {email: this.email, password: this.password})
          .then(() => {
            this.$router
              .push({name: 'home'})
          })
          .catch((err) => {
            this.error = err.response.statusText
          })
      }
    },
    gotoRegister () {
      this.$router
        .push({name: 'register'})
    }
  }
}
</script>

<style scoped>
#login {
  min-height: 400px;
}
</style>
