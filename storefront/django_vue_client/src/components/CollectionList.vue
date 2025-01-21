<template>
  <div class="content">
    <h1>Collection List</h1>
    <div class="list">
      <ul class="list_content">
        <li v-for="collection in collections" :key="collection.id">
          <h4>Название: {{ collection.title }}</h4>
        </li>
      </ul>
    </div>
  </div>
</template>
<script>
export default {
  data() {
    return {
      collections: [],
      title: ''
    }
  },
  methods: {
    async getCollections() {
      try {
        await this.$http.get(`http://127.0.0.1:8000/collections/`).then((response) => {
          this.collections = response.data
        })
      } catch (error) {
        console.log(error)
      }
    }
  },
  created() {
    this.getCollections()
  }
}
</script>

// apply styling to the component

<style scoped>
</style>