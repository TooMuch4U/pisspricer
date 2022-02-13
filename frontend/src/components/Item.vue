<template>
  <div>
    <div id="Item" class="container-fluid pt-3">
      <div class="row my-1">
        <div class="col-1 d-none d-md-block"></div>
        <div class="col-12 col-md-10 bottom-border pb-3">

          <div class="row" v-if="success">
            <div class="col-12 my-2 text-center">
              <div class="alert alert-success" role="alert">
                {{ success }}
              </div>
            </div>
          </div>

          <table class="m-auto" v-if="itemData !== null">
            <tr>
              <td>
                <img v-if="itemData.hasImage" class="mr-3 item-image-big" :src="`${staticUrl}items/${itemData.sku}.jpeg`">
                </td>
              <td class="text-left">

                <h5 class="m-0 d-inline">
                  <b>{{ itemData.name }}</b>
                </h5>
                <font-awesome-icon v-if="isAdmin"
                                   data-toggle="modal"
                                   data-target="#editModal"
                                   size="xs" icon="wrench"
                                   class="text-secondary mb-1 clickable"/>
                <br/>

                <p class="m-0 d-inline-block">Brand: </p>
                <p class="text-muted d-inline-block m-0">{{ itemData.brand ? itemData.brand : '?' }}</p>
                <br/>

                <p class="m-0 d-inline-block">Category: </p>
                <p class="text-muted d-inline-block m-0">{{ itemData.category ? itemData.category : '?' }}</p>
                <br/>

                <p class="m-0 d-inline-block">Volume Each: </p>
                <p class="text-muted d-inline-block m-0">
                  {{ itemData.volumeEach ? itemData.volumeEach + 'ml' : '?' }}
                </p>
                <br/>

                <p class="m-0 d-inline-block">Pack Size: </p>
                <p class="text-muted d-inline-block m-0">
                  {{ itemData.packSize ? itemData.packSize : '?' }}
                </p>
                <br/>

                <p class="m-0 d-inline-block">Abv: </p>
                <p class="text-muted d-inline-block m-0">
                  {{ itemData.alcoholContent ? itemData.alcoholContent + '%' : '?' }}
                </p>
                <br/>

                <p class="m-0 d-inline-block">Std Drinks: </p>
                <p class="text-muted d-inline-block m-0">
                  {{ itemData.stdDrinks ? itemData.stdDrinks : '?' }}
                </p>
                <br/>
              </td>
            </tr>
          </table>

        </div>
        <div class="col-1 d-none d-md-block"></div>
      </div>
    </div>

      <!-- Modal -->
      <div class="modal fade" id="editModal" tabindex="-1" role="dialog" aria-labelledby="exampleModalLabel">
        <div class="modal-dialog" role="document">
          <div class="modal-content">

            <div class="modal-header">
              <h5 class="modal-title" id="exampleModalLabel">Edit</h5>
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

              <table class="table">
                <tbody>
                  <tr v-for="(value, name) in newItemData" v-if="isEditable(name)" v-bind:key="name">
                    <td class="text-right">
                      {{ name }}
                    </td>
                    <td>
                      <input class="form-control" type="text" v-model="newItemData[name]">
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>

            <div class="modal-footer">
              <button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>
              <button type="button" class="btn btn-primary" @click="submitChanges">Save changes</button>
            </div>

          </div>
        </div>
      </div>

  </div>
</template>

<script>
import { mapGetters } from 'vuex'
export default {
  data () {
    return {
      itemData: null,
      staticUrl: process.env.VUE_APP_STATIC_URL,
      newItemData: {},
      editable: ['slug', 'name', 'brand', 'categoryId', 'subcategoryId', 'stdDrinks',
        'alcoholContent', 'volumeEach', 'packSize'],
      error: null,
      success: null
    }
  },
  props: ['slug'],
  mounted () {
    this.getItem()
  },
  watch: { // Watch to see if the item slug changes
    slug: function () {
      this.getItem()
    }
  },
  computed: {
    ...mapGetters(['isAdmin'])
  },
  methods: {
    getItem () {
      this.$http.get(`${process.env.API_URL}/items/${this.slug}`,
        {
          params: { mode: 'slug' }
        })
        .then((res) => {
          this.itemData = res.data
          this.newItemData = res.data
        })
    },
    isEditable (paramName) {
      let any = false
      this.editable.forEach(name => {
        if (name === paramName) {
          any = true
        }
      })
      return any
    },
    submitChanges () {
      this.error = null
      this.success = null

      let changes = {...this.newItemData}
      for (let key in changes) {
        if (changes[key] === '' || changes[key] === null || changes[key] === undefined || !this.isEditable(key)) {
          delete changes[key]
        }
      }

      this.$store.dispatch('editItem', {newParams: changes, sku: this.itemData.sku})
        .then((res) => {
          this.success = 'Success'
          // eslint-disable-next-line
          $('#editModal').modal('hide')
        })
        .catch((err) => {
          this.error = err.response.statusText
        })
    }
  },
  name: 'Item'
}
</script>

<style scoped>
.item-image-big {
  max-width: 80px;
}
.bottom-border {
  border-bottom: 1px solid #dee2e6!important;
}
.clickable {
  cursor: pointer;
}

</style>
