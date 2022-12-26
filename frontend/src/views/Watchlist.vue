<script>
import Login from "@/views/Login.vue";
import { ref } from 'vue'
import {mapActions} from "pinia";
import {useUsersStore} from "@/stores/UsersStore";
import {useStocksStore} from "@/stores/StocksStore";
import WatchedStock from "@/components/WatchedStock.vue";

export default {
  name: "watchlist",
  components: {Login, WatchedStock},
  data() {
    const stocksFetched = ref(false)
    const updatingStocks = ref(false)

    const sortField = ref('symbol')
    const reverseSort = ref(false)

    return {
      stocksFetched, updatingStocks,
      sortField, reverseSort
    }
  },
  methods: {
    ...mapActions(useUsersStore, ['logout', 'getUser']),
    ...mapActions(useStocksStore, ['getStocks', "fetchStocks", "updateStocks"]),
    getMonthlyIncome(stock) {
      return (stock.dividend_yield * stock.price / 12)
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
    updateStocksWithLoading() {
      this.updatingStocks = true
      this.updateStocks().finally(_ => {
        this.updatingStocks = false
      })
    }
  },
  // computed: {
  //   averageYield() {
  //     return (this.getStocks().reduce((a, b) => {
  //       return a + b.dividend_yield
  //     }, 0) / this.getStocks().length * 100).toFixed(2)
  //   },
  //   averageMonthlyIncome() {
  //     return (this.getStocks().reduce((a, b) => {
  //       return a + this.getMonthlyIncome(b)
  //     }, 0) / this.getStocks().length).toFixed(2)
  //   }
  // },
  mounted() {
    this.fetchStocks().then(_ => {
      this.stocksFetched = true
    })
  }
}
</script>

<template>
  <div>
    <div class="text-center mt-4 font-bold text-lg">
      Watchlist
      <button v-ripple class="button round ml-2" @click="updateStocksWithLoading()"
        :disabled="updatingStocks">↻</button>
    </div>
    <div class="text-center mt-3">
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
    <div class="body">
      <div class="flex flex-wrap justify-center" v-if="!updatingStocks">
        <WatchedStock :stock="stock" v-for="stock in this.sortedStock(this.sortField, this.reverseSort)"/>
      </div>
    </div>
  </div>
</template>

<style scoped>

</style>