<template>
    <div class="container-fluid">
      <div class="row">
        <div class="col-12">
          <button @click="combine" type="button" class="btn btn-primary">Combine</button>
          <button @click="swapPlaces" type="button" class="btn btn-secondary">Swap</button>
        </div>
      </div>

      <div class="row my-2" v-if="error">
        <div class="col-12">
          <div class="alert alert-danger" role="alert">
            {{ error }}
          </div>
        </div>
      </div>

      <div class="row" v-if="success">
        <div class="col-12 my-2">
          <div class="alert alert-success" role="alert">
            {{ success }}
          </div>
        </div>
      </div>

      <div class="row">
        <div class="col-6 text-centre">
          <input class="form-control m-1 w-50 mx-auto mb-2 text-center" type="text" v-model="itemInfoA.sku">

          <div v-if="itemInfoA.error !== null" class="alert alert-danger" role="alert">
            {{ itemInfoA.error }}
          </div>

          <img class="d-inline-block img-height" v-if="itemInfoA.item.hasImage" :src="imageUrl(itemInfoA.sku)">

          <p v-if="itemInfoA.imgSize.height">{{ itemInfoA.imgSize.height }} x {{ itemInfoA.imgSize.height }}</p>

          <table class="m-auto w-100 p-2">
            <tbody>

              <tr>
                <router-link target="_blank" :to="{name: 'item', params: {slug: itemInfoA.item.slug}}">
                  {{ itemInfoA.item.name }}
                </router-link>
              </tr>

              <tr v-bind:key="name" v-for="(value, name) in itemInfoA.item">
                <td class="text-left" v-if="canChange(name)">
                  <input v-if="isNumber(name)" class="form-control" :placeholder="name" v-model.number="itemInfoA.item[name]">
                  <input v-else class="form-control" :placeholder="name" v-model="itemInfoA.item[name]">
                </td>
                <td class="text-left" v-else>
                  <input class="form-control" :placeholder="name" :value="value" readonly>
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <div class="col-6 text-centre">
          <input class="form-control m-1 w-50 mx-auto mb-2 text-center" type="text" v-model="itemInfoB.sku">

          <div v-if="itemInfoB.error !== null" class="alert alert-danger" role="alert">
            {{ itemInfoB.error }}
          </div>

          <img class="d-inline-block img-height" v-if="itemInfoB.item.hasImage" :src="imageUrl(itemInfoB.sku)">

          <p v-if="itemInfoB.imgSize.height">{{ itemInfoB.imgSize.height }} x {{ itemInfoB.imgSize.height }}</p>

          <table class="m-auto w-100 p-2">
            <tbody>

            <tr>
              <router-link target="_blank" :to="{name: 'item', params: {slug: itemInfoB.item.slug}}">
                {{ itemInfoB.item.name }}
              </router-link>
            </tr>

            <tr v-bind:key="name" v-for="(value, name) in itemInfoB.item">

              <td class="text-left">
                <input class="form-control" @click="useValue(name, value)" :placeholder="name" :value="value" readonly>
              </td>
            </tr>
            </tbody>
          </table>
        </div>

      </div>
    </div>
</template>

<script>
export default {
  name: 'CombineSkus',
  data () {
    return {
      error: null,
      success: null,
      changeable: ['name', 'slug', 'brand', 'stdDrinks', 'alcoholContent', 'volumeEach', 'categoryId', 'subcategoryId', 'packSize'],
      numberFields: ['stdDrinks', 'alcoholContent', 'volumeEach', 'categoryId', 'subcategoryId', 'packSize'],
      itemInfoA: {
        sku: null,
        error: null,
        item: {},
        imgSize: {}
      },
      itemInfoB: {
        sku: null,
        error: null,
        item: {},
        imgSize: {}
      }
    }
  },
  computed: {
    skuA () {
      return this.itemInfoA.sku
    },
    skuB () {
      return this.itemInfoB.sku
    }
  },
  watch: {
    skuA (newSku, oldSku) {
      if (newSku !== oldSku) {
        this.getItem(this.itemInfoA)
      }
    },
    skuB (newSku, oldSku) {
      if (newSku !== oldSku) {
        this.getItem(this.itemInfoB)
      }
    }
  },
  mounted () {
    this.itemInfoA.sku = this.$route.query.a
    this.itemInfoB.sku = this.$route.query.b
  },
  methods: {
    getItem (itemInfo) {
      if (itemInfo.sku) {
        this.$store.dispatch('getItem', {sku: itemInfo.sku})
          .then((res) => {
            itemInfo.item = res.data
            itemInfo.error = null
            this.getImageSize(this.imageUrl(res.data.sku))
              .then((size) => {
                itemInfo.imgSize = size
              })
          })
          .catch((err) => {
            itemInfo.item = {}
            itemInfo.error = err.response.statusText
          })
      }
    },
    canChange (name) {
      for (let i = 0; i < this.changeable.length; i++) {
        if (this.changeable[i] === name) {
          return true
        }
      }
      return false
    },
    isNumber (name) {
      for (let i = 0; i < this.numberFields.length; i++) {
        if (this.numberFields[i] === name) {
          return true
        }
      }
      return false
    },
    imageUrl: function (sku) {
      return process.env.VUE_APP_STATIC_URL + 'items/' + sku + '.jpeg'
    },
    getImageSize (url) {
      return new Promise((resolve) => {
        let img = new Image()
        img.addEventListener('load', function () {
          resolve({
            width: this.naturalWidth,
            height: this.naturalHeight
          })
        })
        img.src = url
      })
    },
    swapPlaces () {
      const sku = this.itemInfoA.sku
      this.itemInfoA.sku = this.itemInfoB.sku
      this.itemInfoB.sku = sku
    },
    combine () {
      if (window.confirm('Do you really want to combine these skus?')) {
        // Remove null and un-changable items
        let newItem = {...this.itemInfoA.item}
        for (let key in newItem) {
          if (newItem[key] === null || newItem[key] === undefined || !this.canChange(key)) {
            delete newItem[key]
          }
        }

        // Send api request
        this.$store.dispatch(
          'combineItems',
          {
            skuA: this.itemInfoA.sku,
            skuB: this.itemInfoB.sku,
            newItem
          })
          .then((res) => {
            this.success = 'Success!'
            this.error = null
          })
          .catch((err) => {
            this.error = err.response.statusText
            this.success = null
          })
      }
    },
    useValue (key, value) {
      this.itemInfoA.item[key] = value
    }
  }
}
</script>

<style scoped>
.img-height {
  max-height: 100px;
}
</style>
