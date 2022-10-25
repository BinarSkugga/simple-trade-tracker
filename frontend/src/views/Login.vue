<script>
import {mapActions} from "pinia";
import {useUsersStore} from "@/stores/UsersStore";

export default {
  name: "Login",
  data() {
    return {
      username: '',
      password: ''
    }
  },
  methods: {
    ...mapActions(useUsersStore, {login: 'login'})
  }
}
</script>

<template>
  <div>
    <n-card title="Login" size="large">
      <n-input placeholder="Mail" v-model:value="username"/>
      <n-input type="password"
      show-password-on="mousedown"
      placeholder="Password" style="margin-top: 10px;" v-model:value="password"/>

      <n-space justify="end">
        <n-button type="success" style="margin-top: 10px;" @click="login(username, password)">Sign in</n-button>
      </n-space>
    </n-card>
  </div>
</template>

<style scoped>
.n-card {
  position: absolute;
  width: 400px;
  left: 50%;
  top: 50%;
  transform: translateY(-50%) translateX(-50%);
}
</style>