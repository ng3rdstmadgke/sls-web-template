<template>
  <v-app dark>
    <div class="text-h2">
      {{ $props.error.statusCode }} {{ $props.error.message }}
    </div>
  </v-app>
</template>

<script lang="ts">
/**
 * このページは error({statusCode: xxx message: "..."}) で呼び出される。
 * パラメータ中のstatusCode, messageプロパティは必須
 * errorメソッド: https://nuxtjs.org/ja/docs/internals-glossary/context#error
 */

import Vue, { PropOptions } from 'vue'

interface Error {
  statusCode: number,
  message: string,
}

export default Vue.extend({
  layout: 'empty',

  props: {
    error: {
      type: Object,
      required: true
    } as PropOptions<Error>
  },

  data () {
    return {
    }
  },

  /**
   * headプロパティはhtmlのheadタグに相当する要素を返却する
   * https://nuxtjs.org/ja/docs/components-glossary/head/
   */
  head () {
    return {
      title: `${this.error.statusCode} ${this.error.message}`
    }
  }
})
</script>