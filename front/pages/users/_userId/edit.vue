<template>
<div>
  <Alert ref="alert" alertType="error" :message="$data.alertMessage"></Alert>
  <v-form ref="form" v-model="valid" lazy-validattion>
    <v-text-field
      v-model="$data.user.username"
      :rules="usernameRules"
      :counter="30"
      label="Username"
      disabled
      required
    ></v-text-field>
    <v-select
      v-model="$data.user.is_active"
      :items="[true, false]"
      label="IsActive"
      item-text="text"
      item-value="value"
    ></v-select>
    <v-select
      v-model="$data.user.is_superuser"
      :items="[true, false]"
      label="IsSuperuser"
      item-text="text"
      item-value="value"
    ></v-select>
    <v-btn color="primary" class="mr-4" @click="submit" >submit</v-btn>
    <!--
      <v-btn @click="clear">clear</v-btn>
    -->
  </v-form>
</div>
</template>

<script lang="ts">
import Vue from 'vue'
import Alert from '~/components/Alert.vue'
import {Util} from '@/plugins/common'

interface User {
  username: string,
  is_active: boolean,
  is_superuser: boolean,
}

interface UserData {
  user: User | null,
  alertMessage: string,
  valid: boolean,
  usernameRules: any[]
}


export default Vue.extend({
  middleware: ['auth'], // middleware/auth.js

  data(): UserData {
    return {
      user: null,
      alertMessage: "",
      valid: true,
      usernameRules: [
        (v: string): (boolean | string) => {return !!v || "Username is required"},
        (v: string): (boolean | string) => {return ((v?.length ?? 0) <= 30) || "Username is too long"},
      ],
    }
  },

  components: {
    Alert: Alert
  },

  // サーバーサイドの処理
  async asyncData(context) {
    // contextのメンバ: https://nuxtjs.org/docs/internals-glossary/context/
    // awaitを利用してresponseを同期的に受け取ることもできる
    // let response = await context.$axios.get(`http://127.0.0.1:8000/api/v1/open/users/${context.params.userId}`)
    return context.$axios.get(`/api/v1/users/${context.params.userId}`)
      .then(res => {
        return {user: res.data}
      })
      .catch(e => {
        Util.redirectErrorPage(context, e);
      })
  },

  methods: {
    async submit () {
      let success = (this.$refs.form as HTMLFormElement).validate();
      if (success && this.user != null) {
        let data = {
          username: this.user.username,
          is_active: this.user.is_active,
          is_superuser: this.user.is_superuser,
        }
        // 現在のURLを取得する: https://qiita.com/TK-C/items/caab322156872d546331
        this.$axios.put(`/api/v1/users/${this.$route.params.userId}`, data)
          .then(res => {
            this.$router.push({path: "/users"})
          })
          .catch(e => {
            this.$data.alertMessage = Util.getAlertMessage(e);
            (this.$refs.alert as any).open();
          })
      }
    },
    clear () {
      (this.$refs.form as HTMLFormElement).reset();
    },
  },
})
</script>
