<template>
<div>
  <div class="mt-3 mb-3">
    <v-row v-if="isItemAdmin">
      <v-col cols="12" sm="2">
        <v-btn block color="success" to="/items/create">new</v-btn>
      </v-col>
    </v-row>
  </div>
  <v-simple-table>
    <template v-slot:default>
      <thead>
        <tr>
          <th class="text-left">Id</th>
          <th class="text-left">Name</th>
          <th class="text-left">
            DataFormat <v-icon small @click="openTooltip()"> mdi-help </v-icon>
          </th>
          <th class="text-left"></th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="item in $data.items" v-bind:key="item.id">
          <td>{{ item.id }}</td>
          <td><nuxt-link v-bind:to="`/items/${item.id}`">{{ item.name }}</nuxt-link></td>
          <td>{{ item.data_format }}</td>
          <td>
            <v-btn
            color="primary"
            @click="download(item.id, $event)">Download</v-btn>
            <v-btn
            v-if="item.owner && isItemAdmin"
            color="warning"
            v-bind:to="`/items/${item.id}/edit`">Edit</v-btn>
          </td>
        </tr>
      </tbody>
    </template>
  </v-simple-table>
  <TooltipDialog
    ref="tooltip"
    :title="$data.tooltip.title"
    :message="$data.tooltip.message"
  ></TooltipDialog>
</div>
</template>

<script lang="ts">
import Vue from 'vue'
import TooltipDialog from '~/components/TooltipDialog.vue'
import {ItemsUtil} from '@/plugins/items'
import {Util} from '@/plugins/common'
import {Context} from '@nuxt/types'
import { AxiosError, AxiosResponse } from 'axios'
import Auth from "@/plugins/auth"

interface Item {
  id: number,
  name: string,
  is_common: boolean,
  data_format: string,
  owner: boolean,
}

interface ItemsData {
  items: Item[]
  tooltip: {
    title: string,
    message: string,
  }
}

/**
 * プロパティ一覧
 * https://nuxtjs.org/docs/directory-structure/pages/#properties
 */
export default Vue.extend({
  middleware: ['auth'],  // middleware/auth.tsで未認証時にログインページにリダイレクトします
  components: {
    TooltipDialog: TooltipDialog,
  },

  data(): ItemsData {
    return {
      items: [],
      tooltip: {title: "", message: ""},
    }
  },
  computed: {
    isItemAdmin() {
      return Auth.hasRole(this.$cookies, this.$itemAdminRole);
    },
  },
  async asyncData(context: Context) {
    // plugins/axios.tsによって、tokenが存在する場合は Authorization ヘッダを付与してリクエストします。
    return context.$axios.get("/api/v1/items/")
      .then((res: AxiosResponse)=> {
        return {items: res.data}
      })
      .catch((e: AxiosError) => {
        Util.redirectErrorPage(context, e)
      })
  },
  methods: {
    openTooltip() {
      let msg = ItemsUtil.testMsg();
      this.tooltip.title = msg.title;
      this.tooltip.message = msg.message;
      (this.$refs.tooltip as any).open()
    },
    download(itemId: number, event: Event) {
      this.$axios.get(`/api/v1/items/${itemId}`)
        .then(res => {
          Util.download(
            res.data.content,
            res.data.name + "." + res.data.data_format.toLowerCase(),
            "text/plain"
          )
        })
        .catch(e => {
          this.$data.alertMessage = Util.getAlertMessage(e);
          (this.$refs.alert as any).open();
        })
    },
  },
})
</script>
