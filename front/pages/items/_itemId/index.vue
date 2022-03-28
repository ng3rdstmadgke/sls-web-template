<template>
<div>
  <Alert ref="alert" alertType="error" :message="$data.alertMessage"></Alert>
  <div class="mt-3 mb-3">
    <v-row>
      <v-col cols="4" sm="2">
        <v-btn block color="primary" @click="download()">Download</v-btn>
      </v-col>
      <v-col cols="4" sm="2" v-if="item.owner && isItemAdmin">
        <v-btn block color="warning" v-bind:to="`/items/${$route.params.itemId}/edit`">Edit</v-btn>
      </v-col>
      <v-col cols="4" sm="2" v-if="item.owner && isItemAdmin">
        <v-btn block color="error" v-on:click="openDeleteConfirmDialog()">Delete</v-btn>
      </v-col>
    </v-row>
  </div>
  <v-simple-table class="mb-3">
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
          <td>{{ $data.item.id }}</td>
        </tr>
        <tr>
          <td>username</td>
          <td>{{ $data.item.name }}</td>
        </tr>
        <tr>
          <td>is_common <v-icon small @click="openTooltip()"> mdi-help </v-icon></td>
          <td>{{ $data.item.is_common }}</td>
        </tr>
        <tr>
          <td>data_format <v-icon small @click="openTooltip()"> mdi-help </v-icon></td>
          <td>{{ $data.item.data_format }}</td>
        </tr>
        <tr>
          <td>owner<v-icon small @click="openTooltip()"> mdi-help </v-icon></td>
          <td>{{ $data.item.owner }}</td>
        </tr>
      </tbody>
    </template>
  </v-simple-table>
  <div>
    <v-card class="pa-2" outlined tile >
      <v-textarea
        v-model="$data.item.content"
        label="Content"
        rows=20
        readonly
      ></v-textarea>
    </v-card>
  </div>

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
    title="Delete Item"
    message="本当に削除しますか"
    buttonMessage="Delete"
    v-on:confirm="confirmDeletion"
  ></ConfirmDialog>
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
import ConfirmDialog from '~/components/ConfirmDialog.vue'
import Alert from '~/components/Alert.vue'
import {Util} from '@/plugins/common'
import Auth from "@/plugins/auth"

interface Item {
  id: number,
  name: string,
  is_common: boolean,
  data_format: string,
  owner: boolean,
  content: string,
}

interface ItemData {
  item: Item | null
  alertMessage: string
  tooltip: {
    title: string,
    message: string,
  }
}

export default Vue.extend({
  middleware: ['auth'],
  components: {
    TooltipDialog: TooltipDialog,
    ConfirmDialog: ConfirmDialog,
    Alert: Alert,
  },

  data(): ItemData {
    return {
      item: null,
      alertMessage: "",
      tooltip: {title: "", message: ""},
    }
  },

  computed: {
    isItemAdmin() {
      return Auth.hasRole(this.$cookies, this.$itemAdminRole);
    },
  },

  methods: {
    openTooltip() {
      let msg = ItemsUtil.testMsg();
      this.tooltip.title = msg.title;
      this.tooltip.message = msg.message;
      (this.$refs.tooltip as any).open()
    },
    // アイテム削除時のダイアログ表示
    openDeleteConfirmDialog() {
      (this.$refs.confirm as any).open()
    },
    download() {
      if (this.item) {
        Util.download(
          this.item.content,
          this.item.name + "." + this.item.data_format.toLowerCase(),
          "text/plain"
        )
      } else {
        this.$data.alertMessage = "Download content not found.";
        (this.$refs.alert as any).open();
      }
    },
    async confirmDeletion() {
      this.$axios.delete(`/api/v1/items/${this.$route.params.itemId}`)
        .then(_res => {
          this.$router.push({path: "/items/"})
        })
        .catch(e => {
          this.$data.alertMessage = Util.getAlertMessage(e);
          (this.$refs.alert as any).open();
        })
    }
  },

  async asyncData(context) {
    return context.$axios.get(`/api/v1/items/${context.params.itemId}`)
      .then(res => {
        return {item: res.data}
      })
      .catch(e => {
        Util.redirectErrorPage(context, e)
      })
  },
})
</script>