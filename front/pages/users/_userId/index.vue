<template>
<div>
  <Alert ref="alert" alertType="error" :message="$data.alertMessage"></Alert>
  <div class="mt-3 mb-3">
    <v-row>
      <v-col cols="4" sm="2" >
        <v-btn block color="warning" v-bind:to="`/users/${$route.params.userId}/edit`">Edit</v-btn>
      </v-col>
      <v-col cols="4" sm="2" >
        <v-btn block color="error" v-on:click="openDeleteConfirmDialog()">Delete</v-btn>
      </v-col>
    </v-row>
  </div>
  <v-simple-table>
    <template v-slot:default>
      <thead>
        <tr>
          <th class="text-left">Column</th>
          <th class="text-left">Value</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td>id</td>
          <td>{{ $data.user.id }}</td>
        </tr>
        <tr>
          <td>username</td>
          <td>{{ $data.user.username }}</td>
        </tr>
        <tr>
          <td>is_active</td>
          <td>{{ $data.user.is_active }}</td>
        </tr>
        <tr>
          <td>is_superuser</td>
          <td>{{ $data.user.is_superuser }}</td>
        </tr>
        <tr>
          <td>roles</td>
          <td>{{ $data.user.roles.map((e) => e.name).join(", ") }}</td>
        </tr>
      </tbody>
    </template>
  </v-simple-table>
  <!--
    ConfirmDialogコンポーネントの呼び出し
    - ref="..."
      this.$refs.{...} で要素を参照できる
    - v-on:confirm="..."
      confirmはConfirmDialogコンポーネントのconfirm()メソッド内のemitで発生させるイベント
    - 属性
      propに割り当てる値を属性として定義
  -->
  <ConfirmDialog
    ref="confirm"
    title="Delete User"
    message="本当に削除しますか"
    buttonMessage="Delete"
    v-on:confirm="confirmDeletion"
  ></ConfirmDialog>
</div>

</template>

<script lang="ts">
import Vue from 'vue'
import ConfirmDialog from '~/components/ConfirmDialog.vue'
import Alert from '~/components/Alert.vue'
import {Util} from '@/plugins/common'

export default Vue.extend({
  middleware: ['auth'],

  data() {
    return {
      alertMessage: "",
    }
  },

  components: {
    ConfirmDialog: ConfirmDialog,
    Alert: Alert,
  },

  methods: {
    // アイテム削除時のダイアログ表示
    openDeleteConfirmDialog() {
      // ConfirmDialogタグのref属性のconfirmを指定している
      // https://zenn.dev/kokota/articles/247d4f61590dab
      // ConfirmDialogコンポーネントのopen()を呼びu出すことでdialogを表示する
      (this.$refs.confirm as any).open()
    },
    async confirmDeletion() {
      this.$axios.delete(`/api/v1/users/${this.$route.params.userId}`)
        .then(_res => {
          this.$router.push({path: "/users"})
        })
        .catch(e => {
          this.$data.alertMessage = Util.getAlertMessage(e);
          (this.$refs.alert as any).open();
        })
    }
  },

  async asyncData(context) {
    // contestのメンバ: https://nuxtjs.org/docs/internals-glossary/context/
    //                  https://develop365.gitlab.io/nuxtjs-2.8.X-doc/ja/api/context/
    //   contextからaxiosを利用する場合は context.$axios.get(...)
    return context.$axios.get(`/api/v1/users/${context.params.userId}`)
      .then(res => {
        return {user: res.data}
      })
      .catch(e => {
        Util.redirectErrorPage(context, e)
      })
  },
})
</script>