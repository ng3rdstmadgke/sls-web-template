<template>
<div>
  <Alert ref="alert" alertType="error" :message="$data.alertMessage"></Alert>
  <!-- ref属性でthis.$refsから参照できるようにする -->
  <v-form ref="itemForm" v-model="valid" lazy-validattion>
    <v-row dense class="mb-2" align="center">
      <v-col cols="12" sm="3">
        <div align="center" >
          <v-subheader>
          Name
          </v-subheader>
        </div>
      </v-col>
      <v-col cols="12" sm="9">
        <v-text-field
          v-model="$data.item.name"
          :rules="nameRules"
          :counter="100"
          label="Name"
          dense
        ></v-text-field>
      </v-col>
    </v-row>

    <!-- vuetifyでファイルアップロード: https://www.paveway.info/entry/2021/07/12/vuetifyjs_vfileinput -->
    <!-- v-file-input: https://vuetifyjs.com/ja/components/file-inputs/ -->
    <v-row dense class="mb-2" align="center">
      <v-col cols="12" sm="3">
        <div align="center">
          <v-subheader>
          Item File
          <v-icon small @click="openTooltip()"> mdi-help </v-icon>
          </v-subheader>
        </div>
      </v-col>
      <v-col cols="12" sm="9">
        <v-file-input
          @change="inputFile"
          :rules="fileRules"
          accept="text/*"
          label="Item File"
          show-size
          prepend-inner-icon="mdi-book-open-blank-variant"
          prepend-icon=""
          dense
        ></v-file-input>
      </v-col>
    </v-row>

    <v-row dense class="mb-2" align="center">
      <v-col cols="12" sm="3">
        <div align="center">
          <v-subheader>
          IsCommon
          <v-icon small @click="openTooltip()"> mdi-help </v-icon>
          </v-subheader>
        </div>
      </v-col>
      <v-col cols="12" sm="9">
        <v-select
          v-model="$data.item.is_common"
          :items="[true, false]"
          label="IsCommon"
          item-text="text"
          item-value="value"
          dense
        ></v-select>
      </v-col>
    </v-row>

    <v-row dense class="mb-2" align="center">
      <v-col cols="12" sm="3">
        <div align="center">
          <v-subheader>
          DataFormat
          <v-icon small @click="openTooltip()"> mdi-help </v-icon>
          </v-subheader>
        </div>
      </v-col>
      <v-col cols="12" sm="9">
        <v-select
          v-model="$data.item.data_format"
          :items="['CSV', 'TSV']"
          label="DataFormat"
          item-text="text"
          item-value="value"
          dense
        ></v-select>
      </v-col>
    </v-row>
    <v-btn class="mr-4" color="primary" @click="submit" >submit</v-btn>
  </v-form>

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
import Alert from '~/components/Alert.vue'
import {Util} from '@/plugins/common'

interface Item {
  id: number,
  name: string,
  is_common: boolean,
  data_format: string,
  owner: boolean,
  content: string,
}

interface ItemData {
  item: Item | null,
  alertMessage: string,
  valid: boolean,
  nameRules: any[],
  fileRules: any[],
  fileObject: ({
    name: string,
    type: string,
    size: number,
    data: ArrayBuffer
  } | null),
  tooltip: {
    title: string,
    message: string,
  },
}

export default Vue.extend({
  middleware: ['auth'], // middleware/auth.js
  components: {
    TooltipDialog: TooltipDialog,
    Alert: Alert
  },

  data(): ItemData {
    return {
      item: null,
      fileObject: null,
      alertMessage: "",
      valid: true,
      nameRules: [
        (v: string): (boolean | string) => {return !!v || "Name is required"},
        (v: string): (boolean | string) => {return ((v?.length ?? 0) <= 100) || "Name is too long"},
      ],
      fileRules: [
        (v: File): (boolean | string) => {return ((v?.size ?? 0) <= 10485760) || "Item File is too Large.limit is 10MB."},
      ],
      tooltip: {title: "", message: ""},
    }
  },

  methods: {
    openTooltip() {
      let msg = ItemsUtil.testMsg();
      this.tooltip.title = msg.title;
      this.tooltip.message = msg.message;
      (this.$refs.tooltip as any).open()
    },
    async inputFile(event: File) {
      this.fileObject = {
        name: event.name,
        type: event.type,
        size: event.size,
        data: (await Util.readFileAsync(event)
          .then((result) => { return result })
          .catch((e) => {
            this.$data.alertMessage = Util.getAlertMessage(e);
            (this.$refs.alert as any).open();
          }) as ArrayBuffer)
      }
    },
    async submit () {
      if (!this.fileObject?.data) {
        this.$data.alertMessage = "Item File is not specified.";
        (this.$refs.alert as any).open();
        return
      }

      let success = (this.$refs.itemForm as HTMLFormElement).validate();
      if (success && this.item != null) {
        let formData = new FormData()
        formData.append("name", this.item.name)
        // https://www.paveway.info/entry/2021/07/12/vuetifyjs_vfileinput
        formData.append(
          "file",
          new Blob([this.fileObject.data], { type: this.fileObject.type }),
          this.fileObject.name
        )
        formData.append("is_common", this.item.is_common.toString())
        formData.append("data_format", this.item.data_format)
        this.$axios.put(`/api/v1/items/${this.$route.params.itemId}`, formData)
          .then(res => {
            this.$router.push({path: "/items/"})
          })
          .catch(e => {
            this.$data.alertMessage = Util.getAlertMessage(e);
            (this.$refs.alert as any).open();
          })
      }
    },
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
