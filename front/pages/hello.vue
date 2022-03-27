<template>
  <div>
    <div>
      <v-btn @click="hello">click</v-btn>
    </div>
    <h1>{{ message }}</h1>
  </div>
</template>

<script>
export default {
  data() {
    return {
      message: ""
    }
  },
  methods: {
    hello() {
      let data = this.$data;
      this.$axios.get("/api/healthcheck")
        .then(res => {
          data.message = res.data["message"];
        })
        .catch((e) => {
          console.error(e);
        })
    }
  }
}
</script>