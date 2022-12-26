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

    const sortField = ref('dividend_yield')
    const reverseSort = ref(true)

    return {
      loggedIn, stocksFetched,
      sortField, reverseSort
    }
  },
  methods: {
    ...mapActions(useUsersStore, ['logout', 'getUser']),
    ...mapActions(useStocksStore, ['getStocks', "fetchStocks"]),
    getMonthlyIncome(stock) {
      return (stock.dividend_yield * stock.price / 12)
    },
    getIncomePriceRatio(stock) {

    },
    sortedStock(field, reversed = true) {
      return this.getStocks().sort((a, b) => {
        if(['getMonthlyIncome'].includes(field)) {
          if(reversed)
            return this[field](b) - this[field](a)
          return this[field](a) - this[field](b)
        }

        if(['name', 'symbol'].includes(field)) {
          if(reversed)
            return a[field].localeCompare(b[field]) * -1
          return a[field].localeCompare(b[field])
        }

        if(reversed)
          return b[field] - a[field]
        return a[field] - b[field]
      })
    },
  },
  computed: {
    averageYield() {
      return (this.getStocks().reduce((a, b) => {
        return a + b.dividend_yield
      }, 0) / this.getStocks().length * 100).toFixed(2)
    },
    averageMonthlyIncome() {
      return (this.getStocks().reduce((a, b) => {
        return a + this.getMonthlyIncome(b)
      }, 0) / this.getStocks().length).toFixed(2)
    }
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
      <div class="sidebar flex flex-col justify-between bg-white">
        <div class="p-1 text-center font-bold">{{this.getUser().username}}</div>
        <div v-ripple class="button m-2 flex-end text-center" type="button" @click="this.logout()">
          logout
        </div>
      </div>

      <div class="text-center ml-[150px] mt-4 font-bold text-lg">Key Stats</div>
      <div class="body flex flex-wrap justify-around">
        <span class="text-center">
          {{averageYield}}% <br/>Avg. Yield
        </span>
        <span class="text-center">
          ${{averageMonthlyIncome}} <br/>Avg. Monthly Income
        </span>
      </div>

      <div class="separator"></div>

      <div class="text-center ml-[150px] mt-4 font-bold text-lg">Watchlist</div>
      <div class="ml-[150px] text-center mt-3">
        Sort:
        <select v-model="sortField" class="mr-2">
          <option value="name">Name</option>
          <option value="symbol">Symbol</option>
          <option value="dividend_yield">Yield</option>
          <option value="price">Price</option>
          <option value="getMonthlyIncome">Income</option>
        </select>
        Reversed: <input type="checkbox" v-model="reverseSort"/>
      </div>
      <div class="body flex flex-wrap justify-center">
        <WatchedStock :stock="stock" v-for="stock in this.sortedStock(this.sortField, this.reverseSort)"/>
      </div>
    </div>
  </div>
</template>

<style scoped>

</style>