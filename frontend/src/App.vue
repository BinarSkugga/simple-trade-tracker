<script>
import Login from '@/views/Login.vue'
import { ref } from 'vue'
import { RouterView } from 'vue-router'
import {mapActions, storeToRefs} from "pinia";
import {useUsersStore} from "@/stores/UsersStore";

export default {
  name: "App",
  components: {Login, RouterView},
  data() {
    const {loggedIn} = storeToRefs(useUsersStore())
    const sidebarClosed = ref(true)

    return {loggedIn, sidebarClosed}
  },
  computed: {
    currentRoute() {
      return this.$route.name
    }
  },
  methods: {
    ...mapActions(useUsersStore, ['logout', 'getUser']),
    toggleSidebar() {
      this.sidebarClosed = !this.sidebarClosed
    }
  }
}
</script>

<template>
  <div>
    <Login v-if="!loggedIn"/>
    <div v-else class="flex flex-row">
      <div class="open-cover" v-if="!sidebarClosed"></div>
      <div class="sidebar relative flex flex-col justify-between bg-white" :class="{'closed': sidebarClosed}">
        <div class="closed-cover"></div>
        <div class="relative">
          <div @click="toggleSidebar()"
               class="sidebar-toggler text-[15px] align-middle leading-[27px] select-none">➤</div>
          <div class="p-3 text-center font-bold">{{getUser().username}}</div>
          <router-link to="/" class="side-menu-item" :class="{'selected': currentRoute === 'watchlist'}" @click="toggleSidebar">
            Watchlist
          </router-link>
          <router-link to="/portfolio"  class="side-menu-item" :class="{'selected': currentRoute === 'portfolio'}" @click="toggleSidebar">
            Portfolio
          </router-link>
        </div>

        <div v-ripple class="button m-2 flex-end text-center" type="button" @click="logout()">
          logout
        </div>
      </div>

      <RouterView class="h-screen overflow-y-scroll grow"/>
    </div>
  </div>
</template>

<style scoped>

</style>
