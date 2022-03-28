import Auth from '@/plugins/auth'
import { Context } from '@nuxt/types'
// import { NuxtAxiosInstance  } from '@nuxtjs/axios'
import { AxiosError, AxiosRequestConfig } from 'axios'
/**
 * @nuxtjs/axios のプラグインを定義する
 * https://nuxtjs.org/ja/docs/directory-structure/plugins
 * 
 * Contextを引数に受け取る
 * https://nuxtjs.org/docs/internals-glossary/context/
 * 
 * - プラグインの登録
 * ```nuxt.config.js
 # export default {
 #   modules: [
 #     '@nuxtjs/axios',
 #   ],
 #   plugins: [
 #     '@/plugins/axios.js',
 #   ],
 * ```
 */
export default function ({$axios, $cookies, redirect, error }: Context) {
  // リクエストが失敗したときの共通処理を定義
  $axios.onError((e: AxiosError) => {
    if (e.response) {
      let log = {
        status: e.response?.status,
        statusText: e.response?.statusText,
        url: e.response?.config?.url,
        request_header: e.response?.config?.headers,
        request_data: e.response?.config?.data,
        response_header: e.response?.headers,
        response_data: e.response?.data,
      }
      console.error(log)
    } else {
      console.error(e)
    }
    // status code が取得できなかったりサーバー側のエラーの場合はエラーページに飛ばす
    /*
    if (!e.response || (e.response?.status ?? 0) >= 500) {
      console.error(e.toJSON())
      // https://nuxtjs.org/docs/internals-glossary/context/#redirect
      // pages配下に飛ばしたい場合はredirect(path)
      error({
        statusCode: e.response?.status ?? 500,
        message: "Internal Server Error",
      })
    }
    */
  })

  // リクエスト時の共通処理を定義
  // cookieにアクセストークンがあればAuthorizationヘッダを付与する
  $axios.onRequest((config: AxiosRequestConfig) => {
    if (Auth.authenticated($cookies)) {
      let token = Auth.getAccessToken($cookies)
      config.headers.common['Authorization'] = `Bearer ${token}`;
    }
  })
}