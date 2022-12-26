<script>
import Login from "@/views/Login.vue";
import { ref } from 'vue'
import {mapActions, storeToRefs} from "pinia";
import {useUsersStore} from "@/stores/UsersStore";
import {useStocksStore} from "@/stores/StocksStore";
import WatchedStock from "@/components/WatchedStock.vue";

export default {
  name: "Home",
  components: {Login, WatchedStock},
  data() {
    const {loggedIn} = storeToRefs(useUsersStore())
    const stocksFetched = ref(false)

    return {
      loggedIn, stocksFetched
    }
  },
  methods: {
    ...mapActions(useUsersStore, ['logout', 'getUser']),
    ...mapActions(useStocksStore, ['getStocks', "fetchStocks"])
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
        <div class="p-1 text-center font-bold">{{this.getUser().username}}</div>
        <div v-ripple class="button m-2 flex-end text-center" type="button" @click="this.logout()">
          logout
        </div>
      </div>

      <div class="text-center ml-[150px] mt-4 font-bold text-lg">Watchlist</div>
      <div class="body flex flex-wrap justify-center">
        <WatchedStock :stock="stock" v-for="stock in this.getStocks()"/>
      </div>
    </div>
  </div>
</template>

<style scoped>

</style>