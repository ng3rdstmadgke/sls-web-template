import { ActionTree, MutationTree } from 'vuex'

/**
 * Nuxt x TypeScript: Store
 * https://typescript.nuxtjs.org/ja/cookbook/store
 */

export const state = () => ({
  authenticated: false
})

export type RootState = ReturnType<typeof state>

export const mutations: MutationTree<RootState> = {
  setAuthenticated(state, authenticated: boolean) {
    state.authenticated = authenticated
  },
}

export const actions: ActionTree<RootState, RootState> = {
  sample(context) {
  }
}