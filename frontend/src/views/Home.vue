<script>
import Login from "@/views/Login.vue";
import MyPortfolios from "@/views/MyPortfolios.vue";
import {mapActions, storeToRefs} from "pinia";
import {useUsersStore} from "@/stores/UsersStore";

export default {
  name: "Home",
  components: {MyPortfolios, Login},
  data() {
    const {loggedIn} = storeToRefs(useUsersStore())

    return {
      loggedIn
    }
  },
  methods: {
    ...mapActions(useUsersStore, ['logout'])
  },
}
</script>

<template>
  <div>
    <Login v-if="!loggedIn"/>
    <MyPortfolios v-else/>
  </div>
</template>

<style scoped>

</style>