<script>
import Login from "@/views/Login.vue";
import MyPortfolios from "@/views/MyPortfolios.vue";
import { ref } from 'vue'
import {mapActions, storeToRefs} from "pinia";
import {useUsersStore} from "@/stores/UsersStore";
import {useStocksStore} from "@/stores/StocksStore";

export default {
  name: "Home",
  components: {MyPortfolios, Login},
  data() {
    const {loggedIn} = storeToRefs(useUsersStore())
    const stocksFetched = ref(false)

    return {
      loggedIn, stocksFetched
    }
  },
  methods: {
    ...mapActions(useUsersStore, ['logout', 'getUser']),
    ...mapActions(useStocksStore, ['getStocks', "fetchStocks"]),
  },
  mounted() {
    this.fetchStocks().then(_ => {
      this.stocksFetched = true
    })
  }
}
</script>

<template>
  <div>
    <Login v-if="!loggedIn"/>
    <div v-else>
      <div class="sidebar flex flex-col justify-between">
        <div>{{this.getUser().username}}</div>
        <div v-ripple class="button m-2 flex-end text-center" type="button" @click="this.logout()">
          logout
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>

</style>