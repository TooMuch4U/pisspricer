<template>
  <div id="register" class="container-fluid pt-3">

    <div class="row mb-3 mx-1">
      <div class="col-lg-4 col-md-3 col-sm-2 d-none d-sm-block"/>

      <div class="col-lg-4 col-md-6 col-sm-8 col-12 border-bottom">
        <h4> Register </h4>
      </div>

      <div class="col-lg-4 col-md-3 col-sm-2 d-none d-sm-block"/>
    </div>

    <div class="row px-1">
      <div class="col-lg-4 col-md-3 col-sm-2 d-none d-sm-block"/>

      <div class="col-lg-4 col-md-6 col-sm-8 col-12">
        <div v-if="success">
          <div class="alert alert-success" role="alert">
            {{ success }}
          </div>
          Can't find the email? <router-link :to="{name: 'resend'}">Resend</router-link> a new code
        </div>
        <div v-else-if="error !== null" class="alert alert-danger" role="alert">
          {{ error }}
        </div>

        <form v-on:submit.prevent v-if="!success">
          <div class="form-group text-left">
            <label for="email">Email address</label>
            <input v-model="email" type="email" class="form-control" id="email" aria-describedby="emailHelp" placeholder="email">
          </div>
          <div class="form-group text-left">
            <label for="email">Firstname</label>
            <input v-model="firstname" type="text" class="form-control" id="firstname" placeholder="firstname">
          </div>
          <div class="form-group text-left">
            <label for="email">Lastname</label>
            <input v-model="lastname" type="text" class="form-control" id="lastname" placeholder="lastname">
          </div>

          <div class="form-group text-left">
            <label for="password">Password</label>
            <input v-model="password" type="password" class="form-control" id="password" placeholder="Password">
          </div>
          <div class="form-group text-left">
            <label for="password">Confirm Password</label>
            <input v-model="passwordConfirm" type="password" class="form-control" id="passwordConfirm"
                   placeholder="Confirm Password">
          </div>

          <div class="form-row">
            <div class="form-group col-6">
              <button type="button" class="btn btn-block btn-light" @click="gotoLogin">Login</button>
            </div>
            <div class="form-group col-6">
              <button class="btn btn-block btn-primary" @click="registerPressed">Register</button>
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
  name: 'Register',
  data () {
    return {
      email: null,
      password: null,
      passwordConfirm: null,
      lastname: null,
      firstname: null,
      error: null,
      success: null
    }
  },
  methods: {
    registerPressed () {
      if (this.email === null ||
          this.password === null ||
          this.firstname === null ||
          this.lastname === null) {
        this.error = 'All fields must be filled'
        return
      }
      if (this.password !== this.passwordConfirm) {
        this.error = 'Passwords must match'
        return
      }

      const reqBody = {
        email: this.email,
        password: this.password,
        firstname: this.firstname,
        lastname: this.lastname
      }
      const payload = {
        reqBody: reqBody,
        referer: location.origin
      }
      this.$store.dispatch('register', payload)
        .then(() => {
          this.success = `Success! A confirmation email was sent to ${this.email}.`
        })
        .catch((err) => {
          this.error = err.response.statusText
        })
    },
    gotoLogin () {
      this.$router.push({name: 'login'})
    }

  }
}
</script>

<style scoped>

</style>
