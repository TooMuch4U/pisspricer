<template>
  <nav class="navbar navbar-expand navbar-light bg-light rounded mb-2">
    <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarsExample09" aria-controls="navbarsExample09" aria-expanded="false" aria-label="Toggle navigation">
      <span class="navbar-toggler-icon"></span>
    </button>

    <div class="collapse navbar-collapse" id="navbarsExample09">
      <ul class="navbar-nav mr-auto">
        <li class="nav-item">
          <router-link class="nav-link" exact-active-class="active" to="/admin">Home</router-link>
        </li>
        <li class="nav-item">
          <router-link class="nav-link" exact-active-class="active" to="/admin/combine">Combine</router-link>
        </li>
        <li class="nav-item">
          <router-link class="nav-link" exact-active-class="active" to="/admin/brands">Brands</router-link>
        </li>
        <li class="nav-item dropdown">
          <a class="nav-link dropdown-toggle" id="dropdown09" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">Dropdown</a>
          <div class="dropdown-menu" aria-labelledby="dropdown09">
            <a class="dropdown-item" href="#">Action</a>
            <a class="dropdown-item" href="#">Another action</a>
            <a class="dropdown-item" href="#">Something else here</a>
          </div>
        </li>
      </ul>
      <form class="form-inline my-2 my-md-0">
        <router-link class="nav-link" :to="{name: 'logout'}">Logout</router-link>
      </form>
    </div>
  </nav>
</template>

<script>
export default {
  name: 'AdminNav'
}
</script>

<style scoped>

</style>
