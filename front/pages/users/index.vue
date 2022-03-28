<template>
<div>
  <div class="mt-3 mb-3">
    <v-row>
      <v-col cols="12" sm="2">
        <v-btn block color="success" to="/users/create">new</v-btn>
      </v-col>
    </v-row>
  </div>
  <v-simple-table>
    <template v-slot:default>
      <thead>
        <tr>
          <th class="text-left">Id</th>
          <th class="text-left">Name</th>
          <th class="text-left">IsActive</th>
          <th class="text-left">IsSuperuser</th>
          <th class="text-left"></th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="user in $data.users" v-bind:key="user.id">
          <td>{{ user.id }}</td>
          <!-- 
            属性に変数を展開したい場合はv-bindを利用する
            https://jp.vuejs.org/v2/guide/syntax.html#%E5%B1%9E%E6%80%A7
          -->
          <td><nuxt-link v-bind:to="`/users/${user.id}`">{{ user.username }}</nuxt-link></td>
          <td>{{ user.is_active }}</td>
          <td>{{ user.is_superuser }}</td>
          <td><v-btn color="warning" v-bind:to="`/users/${user.id}/edit`">edit</v-btn></td>
        </tr>
      </tbody>
    </template>
  </v-simple-table>
</div>
</template>

<script lang="ts">
import Vue from 'vue'
import {Util} from '@/plugins/common'
import {Context} from '@nuxt/types'
import { AxiosError, AxiosResponse } from 'axios'

interface User {
  id: number,
  username: string,
  is_superuser: boolean,
  is_active: boolean,
  items: {[index: string]: (any)}
  roles: {[index: string]: (any)}
}

interface UsersData {
  users: User[]
}

/**
 * プロパティ一覧
 * https://nuxtjs.org/docs/directory-structure/pages/#properties
 */
export default Vue.extend({
  middleware: ['auth'],  // middleware/auth.tsで未認証時にログインページにリダイレクトします

  data(): UsersData {
    return {
      users: []
    }
  },
  /**
   * dataに非同期なデータを保存するためのプロパティ
   * サーバーサイドの処理
   * 
   * asyncDataは返却された値(オブジェクト)をコンポーネントのdataにマージされ、
   * asyncDataフックから返却されるpromiseはルートの繊維の間に解決される。
   * asyncDataは this(コンポーネントインスタンス) にアクセスできないため、引数の context を利用する
   * https://nuxtjs.org/ja/docs/features/data-fetching/#async-data
   */
  async asyncData(context: Context) {
    // plugins/axios.tsによって、tokenが存在する場合は Authorization ヘッダを付与してリクエストします。
    return context.$axios.get("/api/v1/users/")
      .then((res: AxiosResponse)=> {
        return {users: res.data}
      })
      .catch((e: AxiosError) => {
        Util.redirectErrorPage(context, e)
      })
  },
})
</script>
