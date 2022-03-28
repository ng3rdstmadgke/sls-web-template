<template>
  <!--
    v-modelのdialogがtrueなら表示、falseなら非表示
    https://vuetifyjs.com/ja/components/dialogs/
  -->
  <v-dialog v-model="dialog" persistent max-width="400px">
    <v-card>
      <v-card-title>
        <span class="headline">{{title}}</span>
      </v-card-title>
      <v-card-text v-html="message">
      </v-card-text>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn color="primary" class="dialog-Button" @click="confirm">Close</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script lang="ts">
import Vue from 'vue'


export default Vue.extend({
  // propsは親コンポーネントから子コンポーネントへ引き渡す情報
  // https://ktamido.esa.io/posts/398#%E2%96%A0%20%E8%A6%AA%E3%82%B3%E3%83%B3%E3%83%9D%E3%83%BC%E3%83%8D%E3%83%B3%E3%83%88%E3%81%8B%E3%82%89%E5%AD%90%E3%82%B3%E3%83%B3%E3%83%9D%E3%83%BC%E3%83%8D%E3%83%B3%E3%83%88%E3%81%B8%E3%81%AE%E4%BC%9D%E9%81%94%20(%E3%83%97%E3%83%AD%E3%83%91%E3%83%86%E3%82%A3)
  props: {
    title: {
      type: String,
      required: true
    },
    message: {
      type: String,
      required: true
    },
  },
  data() {
    return {
      dialog: false,
    }
  },
  methods: {
    open(): void {
      this.dialog = true
    },
    confirm(): void {
      this.dialog = false
    },
  },
})
</script>

<style scoped>
.dialog-Button {
  font-weight: bold;
}
</style>