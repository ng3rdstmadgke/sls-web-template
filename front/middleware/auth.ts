/**
 * 
 * Document: https://nuxtjs.org/docs/directory-structure/middleware/
 * Middleware Typescript: https://typescript.nuxtjs.org/ja/cookbook/middlewares
 * Qiita 【nuxt】middlewareについて: https://qiita.com/yama-t/items/97871a4c2f1cd8325078
 * 
 * - 第一引数にはcontextをとる
 * 
 * - nuxt.config.jsへの設定
 *  認証が必要なpageにauthミドルウェアを設定する
 * ```pages/users/index.vue
 * export default Vue.extend({
 *  middleware: ['auth']
 * }
 * ```
 * すべてのルートで認証が必要なら
 * ```nuxt.config.js
 * export default {
 *   router: {
 *     middleware: [
 *       'auth'
 *     ]
 *   },
 * }
 * ```
 */
import { Middleware, Context } from "@nuxt/types"
import Auth from "@/plugins/auth"

const auth: Middleware = (context: Context) => {
  if (!Auth.authenticated(context.$cookies)) {
    // redirectはasyncData、fetch、plugins、middlewareで使える
    return context.redirect('/login');
  }
}

export default auth;