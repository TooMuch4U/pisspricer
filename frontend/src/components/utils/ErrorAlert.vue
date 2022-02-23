<template>
  <div class="col-7 m-auto">
    <div class="alert alert-danger">
      <slot />
    </div>
  </div>
</template>

<script>
export default {
  name: 'AlertError'
}
</script>

<style scoped>

</style>
