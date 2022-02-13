<template>
  <div id="verify" class="container-fluid pt-3">

    <div class="row mb-3 mx-1">
      <div class="col-lg-4 col-md-3 col-sm-2 d-none d-sm-block"/>

      <div class="col-lg-4 col-md-6 col-sm-8 col-12 border-bottom">
        <h4> Resend Verification </h4>
      </div>

      <div class="col-lg-4 col-md-3 col-sm-2 d-none d-sm-block"/>
    </div>

    <div class="row px-1">
      <div class="col-lg-4 col-md-3 col-sm-2 d-none d-sm-block"/>

      <div class="col-lg-4 col-md-6 col-sm-8 col-12">

        <div v-if="error !== null" class="alert alert-danger" role="alert">
          {{ error }}
        </div>
        <div v-else-if="success" class="alert alert-success" role="alert">
          {{ success }}
        </div>

        <form v-on:submit.prevent>
          <div class="form-group text-left">
            <label for="email">Email address</label>
            <input v-model="email" type="email" class="form-control" id="email" aria-describedby="emailHelp" placeholder="email">
          </div>

          <div class="form-row">
            <div class="form-group col-6">
              <button type="button" class="btn btn-block btn-light" @click="gotoLogin">Login</button>
            </div>
            <div class="form-group col-6">
              <button class="btn btn-block btn-primary" @click="sendVerification">Resend</button>
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
  name: 'ResendCode',
  data () {
    return {
      error: null,
      success: null,
      email: null
    }
  },
  methods: {
    sendVerification () {
      this.success = null
      this.error = null
      if (!this.email) {
        this.error = 'An email must be entered!'
        return
      }
      this.$store.dispatch('resendVerify', {email: this.email, referer: location.origin})
        .then((res) => {
          this.success = `Success! A confirmation email was sent to ${this.email}.`
          this.error = null
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
