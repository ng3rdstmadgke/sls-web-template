/**
 *  VueComponentとContext両方にグローバル変数・関数を定義する
 * インジェクトに関して: https://typescript.nuxtjs.org/ja/cookbook/plugins/
 * 
 * 使用方法
 * 
 * <script lang="ts">
 * import Vue from 'vue'
 * 
 * export default Vue.extend({
 *   mounted () {
 *     this.$myFunc('works in mounted')
 *   },
 *   asyncData (context) {
 *     context.app.$myFunc('works in asyncData')
 *   }
 * })
 * </script>
 */


import { Context } from '@nuxt/types'
import { Plugin } from '@nuxt/types'


declare module 'vue/types/vue' {
  interface Vue {
    $itemAdminRole: string
    $myFunc(message: string): void
  }
}

declare module '@nuxt/types' {
  interface NuxtAppOptions {
    $itemAdminRole: string
    $myFunc(message: string): void
  }
}

declare module 'vuex/types/index' {
  interface Store<S> {
    $itemAdminRole: string
    $myFunc(message: string): void
  }
}

const Settings: Plugin = (context, inject) => {
  // inject は context ではなく context.app にインジェクトされることに注意してください。
  inject('itemAdminRole', "ItemAdminRole")
  inject('myFunc', (message: string) => console.log(message))
}

export default Settings