// https://github.com/microcipcip/cookie-universal/blob/master/packages/cookie-universal-nuxt/types/index.d.ts#L19
import {NuxtCookies} from "cookie-universal-nuxt" 
import Vue from 'vue'
/**
 * 認証用のトークン(JWT)を扱うクラス
 * 
 * [usage]
 * ```nuxt.config.js
 * export default {
 *   plugins: [
 *     '@/plugins/auth.ts'
 *   ],
 * }
 * ``` 
 * 
 * ```pages/login.vue
 * <script>
 * import Auth from '@/plugins/auth'
 * 
 * export default Vue.extend({
 *   methods: {
 *     submit(): void {
 *       Auth.getAccessToken(this.$cookies);
 *     }
 *   }
 * })
 * </script>
 * ```
 */
export default class Auth {
  private static ACCESS_TOKEN_KEY: string = "__access_token"

  // 認証済みかどうかの判定
  public static authenticated(cookie: NuxtCookies): boolean {
    let payload = this.getPayload(cookie)
    if (payload) {
      // トークンの有効期限を検証
      let exp  = parseInt(payload["exp"]);
      let now  = Math.floor((new Date()).getTime() / 1000)
      if (exp && exp > now) {
        return true
      }
    }
    return false
  }

  // CookieからJWTを削除
  public static logout(cookie: NuxtCookies): void {
    cookie.remove(this.ACCESS_TOKEN_KEY)
  }

  // CookieからJWTを取得
  public static getAccessToken(cookie: NuxtCookies): string {
    return cookie.get(this.ACCESS_TOKEN_KEY)
  }

  // JWTをCookieに保存
  public static login(cookie: NuxtCookies, token: string): void {
    return cookie.set(this.ACCESS_TOKEN_KEY, token)
  }

  // Cookieに保存されているTokenのJWTのheaderをオブジェクト形式で取得する
  public static getHeader(cookie: NuxtCookies): {[index: string]: any} | null {
    let token = this.getAccessToken(cookie)
    if (!token) return null
    let header = token.split(".")[0]
    let decoded = Buffer.from(header, "base64").toString()
    return JSON.parse(decoded)
  }

  // Cookieに保存されているTokenのJWTのpayloadをオブジェクト形式で取得する
  public static getPayload(cookie: NuxtCookies): {[index: string]: any} | null {
    let token = this.getAccessToken(cookie)
    if (!token) return null
    let payload = token.split(".")[1]
    let decoded = Buffer.from(payload, "base64").toString()
    return JSON.parse(decoded)
  }

  public static isSuperuser(cookie: NuxtCookies): boolean {
    let payload = Auth.getPayload(cookie);
    let is_superuser = (payload) ? !!payload.is_superuser : false
    return is_superuser
  }

  public static hasRole(cookie: NuxtCookies, role: string): boolean {
    if (Auth.isSuperuser(cookie)) {
      // 管理者は無条件ですべての権限を持つ
      return true
    }
    let payload = Auth.getPayload(cookie);
    let roles: string[] = (payload && !!payload.scopes) ? payload.scopes : []
    return roles.indexOf(role) >= 0
  }

  public static getUsername(cookie: NuxtCookies): string | null {
    let payload = Auth.getPayload(cookie);
    return (payload && !!payload.sub) ? payload.sub : null
  }
}
