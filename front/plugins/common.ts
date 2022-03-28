import { Context } from "@nuxt/types"
import { AxiosError } from 'axios'
/**
 * 共通関数を定義する。
 * 
 * [usage]
 * ```nuxt.config.js
 * export default {
 *   plugins: [
 *     '@/plugins/common.ts'
 *   ],
 * }
 * ``` 
 * 
 * ```pages/login.vue
 * <script>
 * import {Util} from '@/plugins/common'
 * 
 * export default Vue.extend({
 *   methods: {
 *     submit(): void {
 *       let message = Util.getAlertMessage(...)
 *     }
 *   }
 * })
 * </script>
 * ```
 */
export class Util {
  // layout/error.vueへ遷移する
  // https://nuxtjs.org/ja/docs/internals-glossary/context#error
  public static redirectErrorPage({error}: Context, e: AxiosError) {
    error({
      statusCode: e.response?.status ?? 500,
      message: e.response?.statusText ?? "Internal Server Error",
    })
  }

  // v-alertに表示するメッセージを取得する
  public static getAlertMessage(e: any): string {
    // エラー内容をJSONで見たいとき
    // console.error(e.toJSON())
    if (e.response) {
      return `${e.response.status} ${e.response.statusText}: ${e.response.data.detail}`
    } else {
      return `An error occurred: ${e.message}`
    }
  }
  /**
   * ArrayBufferとしてファイルを読み込む
   * 
   * FileReader: https://ja.javascript.info/file#ref-406
   * mdn FileReader: https://developer.mozilla.org/ja/docs/Web/API/FileReader
   */
  public static readFileAsync(file: File): Promise<ArrayBuffer> {
    return new Promise((resolve, reject) => {
      let reader = new FileReader();
      reader.onload = () => {resolve(reader.result as ArrayBuffer)}
      reader.onerror = reject
      reader.readAsArrayBuffer(file)
    })
  }

  /**
   * 指定された文字列をファイルとしてダウンロードする
   * @param content ファイルの中身となる文字列
   * @param filename ファイル名
   * @param contentType コンテンツタイプ。text/plainなど
   */
  public static download(content: string, filename: string, contentType: string): void {
    const blob = new Blob([content], { type: contentType });
    const url = (window.URL || window.webkitURL).createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = filename
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);

  }
}
