<template>
  <div class="content">
    <h1>Products List</h1>
    <div class="list">
      <ul class="list_content">
        <li v-for="product in products" :key="product.id">
          <h4>Название: {{ product.title }}</h4>
          <h4>Описание:  {{ product.description }}</h4>
          <h4>Цена: {{ product.price }}$</h4>
          <h4>ID Категории: {{ product.collection }}</h4>
        </li>
      </ul>
    </div>
  </div>
</template>
<script>
export default {
  data() {
    return {
      products: [],
      title: ''
    }
  },
  methods: {
    async getProducts() {
      try {
        await this.$http.get(`http://127.0.0.1:8000/products/`).then((response) => {
          this.products = response.data.results
        })
      } catch (error) {
        console.log(error)
      }
    }
  },
  created() {
    this.getProducts()
  }
}
</script>

// apply styling to the component

<style scoped>
</style>