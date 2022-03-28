<template>
  <v-app dark>
    <v-navigation-drawer
      v-model="drawer"
      temporary
      app
    >
      <v-list>
        <v-list-item
          v-for="(item, i) in getNavigationItems($store.state.authenticated)"
          :key="i"
          :to="item.to"
          router
          exact
        >
          <v-list-item-action>
            <v-icon>{{ item.icon }}</v-icon>
          </v-list-item-action>
          <v-list-item-content>
            <v-list-item-title v-text="item.title" />
          </v-list-item-content>
        </v-list-item>
      </v-list>
    </v-navigation-drawer>
    <v-app-bar
      fixed
      app
    >
      <v-app-bar-nav-icon @click.stop="drawer = !drawer" />
      <v-toolbar-title  @click="$router.push('/')" style="cursor:pointer" v-text="title" />
      <v-spacer />
      <v-btn text to="/logout" v-if="$store.state.authenticated">
        <v-icon>mdi-logout</v-icon>
        logout
      </v-btn>
      <v-btn text color="primary" to="/login" v-else>
        <v-icon>mdi-login</v-icon>
        login
      </v-btn>
      <div class="ml-2" v-if="$store.state.authenticated">
        <v-icon>mdi-account</v-icon>
        {{getUsername()}}
      </div>
    </v-app-bar>
    <v-main>
      <v-container>
        <div>
          <v-breadcrumbs :items="getBreadcrumbsItems()" v-if="$store.state.authenticated">
            <template v-slot:item="{ item }">
              <v-breadcrumbs-item
                link
                nuxt
                exact-active-class="v-breadcrumbs__item--disabled"
                active-class=""
                :to="item.href"
                :disabled="item.disabled"
              >{{ item.text }}</v-breadcrumbs-item>
            </template>
          </v-breadcrumbs>
        </div>
        <Nuxt />
      </v-container>
    </v-main>
    <v-footer
      :absolute="!fixed"
      app
    >
      <span>&copy; {{ new Date().getFullYear() }}</span>
    </v-footer>
  </v-app>
</template>

<script lang="ts">
import Vue from 'vue'
import Auth from "@/plugins/auth"

export default Vue.extend({
  async middleware ({store, $cookies }) {
    // methodやcomputedはページ遷移時に評価されないのでmiddlewareでstoreの認証ステータスを更新する
    // https://nuxtjs.org/docs/concepts/views
    let authenticated = Auth.authenticated($cookies)
    store.commit("setAuthenticated", authenticated)
  },
  data () {
    return {
      drawer: false,
      fixed: false,
      title: 'TransApp',
    }
  },

  methods: {
    getUsername(): string {
      return Auth.getUsername(this.$cookies) ?? "Unknown";
    },
    getBreadcrumbsItems(): any[] {
      let items = [
        {
          text: 'top',
          disabled: false,
          href: '/',
        },
      ];

      let path: string[] = [];
      this.$route.fullPath
        .split("/")
        .filter((e: string) => e.length > 0)
        .forEach((e: string) => {
          path.push(`/${e}`);
          items.push(
            {
              text: e,
              disabled: false,
              href: path.join(""),
            }
          )
        });
      
      return items

    },
    getNavigationItems(authenticated: boolean): any[] {
      let items = [
        {
          icon: 'mdi-login',
          title: 'Login',
          to: '/login',
          display: "notLoggedIn",
          requireRole: null,
        },
        {
          icon: 'mdi-home',
          title: 'Home',
          to: '/',
          display: "always",
          requireRole: null,
        },
        {
          icon: 'mdi-file-multiple',
          title: 'Items',
          to: '/items/',
          display: "loggedIn",
          requireRole: null,
        },
        {
          icon: 'mdi-account',
          title: 'Users',
          to: '/users/',
          display: "loggedIn",
          requireRole: "SystemAdminRole",
        },
      ];

      let ret = [];

      for (let item of items) {
        if (authenticated && item.display == "notLoggedIn") {
          continue;
        }
        if (!authenticated && item.display == "loggedIn") {
          continue;
        }
        if (!item.requireRole) {
          ret.push(item);
          continue;
        }
        if (item.requireRole && Auth.hasRole(this.$cookies, item.requireRole)) {
          ret.push(item);
          continue;
        }
      }
      return ret;
    },
  }
})
</script>
