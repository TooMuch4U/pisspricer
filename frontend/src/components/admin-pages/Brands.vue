<template>
  <div class="container-fluid">
    <div class="row">
      <div class="col-3"/>

      <div class="col-6">
        <div class="row" v-if="success">
          <div class="col-12 my-2">
            <div class="alert alert-success" role="alert">
              {{ success }}
            </div>
          </div>
        </div>

        <table class="table">
          <tr>
            <th>Img</th>
            <th>Brand Id</th>
            <th>Name</th>
            <th>Url</th>
          </tr>

          <tr v-bind:key="brand.brandId" v-for="brand in brands">
            <td><img class="brand-img" :src="brandImgUrl(brand.brandId)"></td>
            <td>{{ brand.brandId }}</td>
            <td>{{ brand.name }}</td>
            <td>{{ brand.url }}</td>
          </tr>

          <tr>
            <td/><td/><td/><td/>
          </tr>
        </table>
      </div>

      <div class="col-3"/>
    </div>

    <div class="row">
      <div class="col-12">
        <button data-toggle="modal" data-target="#createModal" type="button" class="btn btn-primary">Create New</button>
      </div>
    </div>

    <!-- Modal -->
    <div class="modal fade" id="createModal" tabindex="-1" role="dialog" aria-labelledby="exampleModalLabel">
      <div class="modal-dialog" role="document">
        <div class="modal-content">

          <div class="modal-header">
            <h5 class="modal-title" id="exampleModalLabel">Create Brand</h5>
            <button type="button" class="close" data-dismiss="modal" aria-label="Close">
              <span aria-hidden="true">&times;</span>
            </button>
          </div>

          <div class="modal-body">
            <div class="row my-2" v-if="error">
              <div class="col-12">
                <div class="alert alert-danger" role="alert">
                  {{ error }}
                </div>
              </div>
            </div>

            <div v-if="creating">
              <img class="brand-img" src="@/assets/loading.gif">
            </div>

            <form>
              <div class="form-group text-left">
                <input v-model="name" id="name" type="text" class="form-control" placeholder="name">
              </div>
              <div class="form-group text-left">
                <input v-model="url" type="text" class="form-control" id="url" placeholder="url">
              </div>
              <div class="form-group text-left custom-file">
                <input type="file" accept="image/*" @change="saveImage($event)" id="file-input">
                <p class="text-muted">(jpg 204x204)</p>
              </div>
            </form>
          </div>

          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>
            <button type="button" class="btn btn-primary" @click="createBrand">Create</button>
          </div>

        </div>
      </div>
    </div>

  </div>
</template>

<script>
export default {
  name: 'Brands',
  data () {
    return {
      name: null,
      url: null,
      image: null,
      success: null,
      error: null,
      brands: [],
      creating: false
    }
  },
  mounted () {
    this.getBrands()
  },
  methods: {
    getBrands () {
      this.$store.dispatch('getBrands')
        .then((res) => {
          this.brands = res.data
        })
    },
    createBrand () {
      this.creating = true
      const payload = {
        name: this.name,
        url: this.url
      }

      // Check if any params are null
      if (this.name === null) {
        this.error = "Name can't be null"
        return
      }
      if (this.url === null) {
        this.error = "Url can't be null"
        return
      }

      this.$store.dispatch('createBrand', payload)
        .then((res) => {
          const brandId = res.data.brandId

          // Create image
          if (this.image !== null) {
            this.$store.dispatch('putBrandImage', {brandId, imageData: this.image})
              .then((res) => {
                // Success
                this.createSuccess('Successfully created new brand with brandId: ' + brandId)
              })
              .catch((err) => {
                this.createError(`Error uploading image: ${err.response.statusText}`)
              })
          } else {
            this.createSuccess('Successfully created new brand with brandId: ' + brandId)
          }
        })
        .catch((err) => {
          this.createError(err.response.statusText)
        })
    },
    brandImgUrl (brandId) {
      return process.env.VUE_APP_STATIC_URL + 'brands/' + brandId + '.jpeg'
    },
    saveImage (event) {
      this.image = event.target.files[0]
    },
    createSuccess (message) {
      this.success = message
      this.image = null
      this.creating = false
      // eslint-disable-next-line
      $('#createModal').modal('hide')
      this.getBrands()
    },
    createError (message) {
      this.creating = false
      this.error = message
      this.getBrands()
    }
  }
}
</script>

<style scoped>
.brand-img {
  width: 30px;
}
</style>
