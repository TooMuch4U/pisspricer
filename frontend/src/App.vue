<template>
  <div id="app">
    <HeaderNav></HeaderNav>
    <router-view/>
    <Footer/>
  </div>
</template>

<script>
import HeaderNav from '@/components/HeaderNav'
import Footer from '@/components/Footer'
export default {
  components: {
    HeaderNav,
    Footer
  },
  mounted () {
    this.$store.dispatch('loadUserDetails')
  },
  name: 'App'
}
</script>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}
</style>
