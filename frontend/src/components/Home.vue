<template>
  <div id="home" class="container">
    <div class="row py-3 bottom-border">
      <div class="col-sm-2 d-none d-sm-block"></div>
      <div class="col-sm-8 col-12">
        <h1 class="h4">Search & compare prices from New Zealand liquor stores and supermarkets, and get the most beer for your buck.</h1>
      </div>
      <div class="col-sm-2 d-none d-sm-block"></div>
    </div>

    <div class="row py-3 mx-1">
      <div class="col-sm-2 d-none d-sm-block"></div>
      <div class="col-sm-8 col-12">
        <h4 class="mb-0">Browse</h4>
      </div>
      <div class="col-sm-2 d-none d-sm-block"></div>
    </div>

    <div class="row mx-lg-0 mx-1 mb-3 no-gutters">

      <div class='col-md-2 col-1'></div>

      <div class='col-md-2 col-5 text-center mb-md-0 mb-3'>
        <a class='browse rob-font text-dark text-decoration-none' href='/items?s=beer'>

          <img class='cat-img' src='@/assets/beer.png'>
          <h5 class='rob-font'>Beer</h5>
        </a>
      </div>

      <div class='col-md-2 col-5 text-center'>
        <a class='browse rob-font text-dark text-decoration-none' href='/items?s=wine'>

          <img class='cat-img' src='@/assets/wine.jpeg'>
          <h5 class='rob-font'>Wine</h5>
        </a>
      </div>

      <div class='d-md-none col-1'></div>
      <div class='d-md-none col-1'></div>

      <div class='col-md-2 col-5 text-center'>
        <a class='browse rob-font text-dark text-decoration-none' href='/items?s=cider'>

          <img class='cat-img' src='@/assets/cider.jpg'>
          <h5 class='rob-font'>Cider</h5>
        </a>
      </div>

      <div class='col-md-2 col-5 text-center'>
        <a class='browse rob-font text-dark text-decoration-none' href='/items?s=rtd'>

          <img class='cat-img' src='@/assets/rtd.png'>
          <h5 class='rob-font'>RTD</h5>
        </a>
      </div>

      <div class='d-md-none col-1'></div>

    </div>

    <div class="row mx-lg-0 mx-1 mb-5 no-gutters">

      <div class='col-md-2 col-1'></div>

      <div class='col-md-2 col-5 text-center mb-md-0 mb-3'>
        <a class='browse rob-font text-dark text-decoration-none' href='/items?s=craft%20beer'>

          <img class='cat-img' src='@/assets/craft-beer.png'>
          <h5 class='rob-font'>Craft Beer</h5>
        </a>
      </div>

      <div class='col-md-2 col-5 text-center'>
        <a class='browse rob-font text-dark text-decoration-none' href='/items?s=liqueurs'>

          <img class='cat-img' src='@/assets/liqueurs.png'>
          <h5 class='rob-font'>Liqueurs</h5>
        </a>
      </div>

      <div class='d-md-none col-1'></div>
      <div class='d-md-none col-1'></div>

      <div class='col-md-2 col-5 text-center'>
        <a class='browse rob-font text-dark text-decoration-none' href='/items?s=spirits'>

          <img class='cat-img' src='@/assets/spirits.jpeg'>
          <h5 class='rob-font'>Spirits</h5>
        </a>
      </div>

      <div class='col-md-2 col-5 text-center'>
        <a class='browse rob-font text-dark text-decoration-none' href='/items?s=%20low%20'>

          <img class='cat-img' src='@/assets/low.png'>
          <h5 class='rob-font'>Low Alcohol</h5>
        </a>
      </div>

      <div class='d-md-none col-1'></div>
    </div>

  </div>
</template>

<script>
export default {
  name: 'Home'
}
</script>

<style scoped>
.main {
  height: 400px;
}
.bottom-border {
  border-bottom: 1px solid #dee2e6!important;
}
.cat-img {
  height: 75px;
}
</style>
