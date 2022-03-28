<template>
<div>
  <Alert ref="alert" alertType="error" :message="alertMessage"></Alert>
  <!--
    https://vuetifyjs.com/ja/components/forms/#submit-26-clear3067306e30d030ea30c730fc30b730e730f3

    v-form コンポーネントはref属性を設定することで、3つの関数にアクセスできる
    this.$refs.form.validate(): すべての入力を検証し、すべて有効であるかを確認する
    this.$refs.form.reset(): すべての入力を消去し、バリデーションエラーをリセットする
    this.$refs.form.resetValidation(): 入力バリデーションのみをリセットする
  -->
  <v-form ref="form" v-model="valid" lazy-validation>
   <!-- $touch: $dirtyフラグを trueにする -->
    <v-text-field
      v-model="username"
      :rules="usernameRules"
      label="Username"
      required
    ></v-text-field>
    <v-text-field
      v-model="password"
      :rules="passwordRules"
      label="Password"
      required
      type="password"
    ></v-text-field>
    <v-btn color="primary" class="mr-4" @click="submit">login</v-btn>
    <v-btn @click="clear">clear</v-btn>
  </v-form>
</div>
</template>

<script lang="ts">
import Vue from 'vue';
import Alert from '@/components/Alert.vue'
import {Util} from '@/plugins/common'
import Auth from '@/plugins/auth'
import { Middleware, Context } from "@nuxt/types"

interface LoginData {
  valid: boolean
  username: string,
  password: string,
  alertMessage: string,
  usernameRules: ((v: string) => (boolean | string))[]
  passwordRules: ((v: string) => (boolean | string))[]
}

export default Vue.extend({
  middleware(context: Context) {
    if (Auth.authenticated(context.$cookies)) {
      return context.redirect('/');
    }
  },

  components: {
    Alert: Alert
  },

  data(): LoginData {
    return {
      valid: true,
      username: '',
      password: '',
      alertMessage: '',
      usernameRules: [
        (v: string): (boolean | string) => {return !!v || "Username is required"},
      ],
      passwordRules: [
        (v: string): (boolean | string) => {return !!v || "Password is required"},
      ],
    }
  },

  methods: {
    submit(): void {
      let success = (this.$refs.form as HTMLFormElement).validate();
      if (success) {
        let form = new FormData()
        form.append("username", this.$data.username)
        form.append("password", this.$data.password)
        this.$axios.post("/api/v1/token", form)
          .then(res => {
            let token = res.data.access_token
            Auth.login(this.$cookies, token)
            // ひとつ前のページに戻る: https://router.vuejs.org/guide/essentials/navigation.html
            this.$router.push("/")
          })
          .catch(e => {
            this.$data.alertMessage = Util.getAlertMessage(e);
            (this.$refs.alert as any).open();
          })
      }
    },
    clear(): void {
      (this.$refs.form as HTMLFormElement).reset();
    }
  }

})
</script>
