<template>
  <div />
</template>
<script>
import Vue from 'vue'
import Auth from "@/plugins/auth"

export default Vue.extend({
  async middleware ({redirect, $cookies }) {
    Auth.logout($cookies);
    redirect("/login");
  },
})
</script>