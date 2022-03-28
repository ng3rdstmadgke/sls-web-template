
<template>
<div>
  <Alert ref="alert" alertType="error" :message="$data.alertMessage"></Alert>
  <!-- ref属性でthis.$refsから参照できるようにする -->
  <v-form ref="form" v-model="valid" lazy-validattion>
    <v-text-field
      v-model="$data.username"
      :rules="usernameRules"
      :counter="30"
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
    <v-btn class="mr-4" @click="submit" >submit</v-btn>
    <v-btn @click="clear">clear</v-btn>
  </v-form>
</div>
</template>

<script lang="ts">
import Vue from 'vue'
import Alert from '~/components/Alert.vue'
import {Util} from '@/plugins/common'

export default Vue.extend({
  middleware: ['auth'],

  data() {
    return {
      username: '',
      password: '',
      alertMessage: "",
      valid: true, // formのバリデーションステータス
      usernameRules: [ // username項目のバリデーションルール
        (v: string): (boolean | string) => {return !!v || "Username is required"},
        (v: string): (boolean | string) => {return ((v?.length ?? 0) <= 30) || "Username is too long"},
      ],
      passwordRules: [ // password項目のバリデーションルール
        (v: string): (boolean | string) => {return !!v || "Password is required"},
        (v: string): (boolean | string) => {return ((v?.length ?? 0) <= 30) || "Password is too long"},
        (v: string): (boolean | string) => {return ((v?.length ?? 0) >= 8) || "Password is too short"},
      ],
    }
  },

  components: {
    Alert: Alert
  },

  methods: {
    async submit () {
      // バリデーションの実行
      // https://vuetifyjs.com/ja/components/forms/#submit-26-clear3067306e30d030ea30c730fc30b730e730f3
      let success = (this.$refs.form as HTMLFormElement).validate();
      if (success) {
        let data = {
          username: this.username,
          password: this.password
        }
        this.$axios.post("/api/v1/users/", data)
          .then(res => {
            this.$router.push({path: "/users"})
          })
          .catch(e => {
            this.$data.alertMessage = Util.getAlertMessage(e);
            (this.$refs.alert as any).open();
          })
      }
    },
    clear() {
      // 入力値とバリデーションステータスのリセット
      (this.$refs.form as HTMLFormElement).reset();
    },
  },
})
</script>