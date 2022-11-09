<script>
import {mapActions} from "pinia";
import {useUsersStore} from "@/stores/UsersStore";

export default {
  name: "Login",
  data() {
    return {
      renderReady: false,
      username: '',
      password: ''
    }
  },
  methods: {
    ...mapActions(useUsersStore, ['login', 'tokenLogin'])
  },
  mounted() {
    // Auto login if a valid token is present
    this.tokenLogin().finally(_ => {
      this.renderReady = true
    })
  }
}
</script>

<template>
  <div v-if="renderReady" class="card fixed top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 flex flex-col">
    <span class="font-bold mb-3">Login</span>
    <input class="text-in w-[350px] mt-2" type="text" placeholder="Username" v-model="username"/>
    <input class="text-in w-[350px] mt-2" type="password" placeholder="Password" v-model="password"/>
    <div v-ripple tabindex="0" class="button mt-2 self-end" type="button"
         @click="this.login(username, password)" @keypress.enter="this.login(username, password)">
      Submit
    </div>
  </div>
</template>

<style scoped>
</style>