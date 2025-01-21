<template>
  <div class="app">
    <ProductList />
    <CollectionList />
  </div>
</template>

<script>
import ProductList from './components/ProductList.vue'
import CollectionList from './components/CollectionList.vue'
export default {
  name: 'App',
  components: {
    ProductList,
    CollectionList
  }
}
</script>

<style scoped>
</style>