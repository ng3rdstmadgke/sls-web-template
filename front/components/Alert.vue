<template>
  <v-alert v-model="alert" dismissible v-bind:type="alertType">{{ message }}</v-alert>
</template>

<script lang="ts">
import Vue from 'vue'

interface AlertData {
  alert: boolean
}
export default Vue.extend({
  props: {
    alertType: {
      type: String,
      required: true,
      validator (v) {
        return [
          'info',
          'warning',
          'error',
        ].includes(v)
      }
    },
    message: {
      type: String,
      required: true,
    },
  },

  data(): AlertData {
    return {
      alert: false,
    }
  },
  methods: {
    open() {
      this.$data.alert = true
    },
    close() {
      this.$data.alert = false
    },
  }
})
</script>