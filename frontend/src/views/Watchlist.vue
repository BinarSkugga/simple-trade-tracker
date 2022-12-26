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

    let sortField = ref('symbol')
    const reverseSort = ref(false)

    const filterChoices = [
      {text: 'Symbol', value: 'symbol'},
      {text: 'Name', value: 'name'},
      {text: 'Yield', value: 'dividend_yield'},
      {text: 'Price', value: 'price'},
      {text: 'Income', value: 'getMonthlyIncome'},
    ]

    return {
      stocksFetched, updatingStocks,
      sortField, reverseSort, filterChoices,
      twPrimary: twPrimary
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
    <div class="text-center mt-4 con-switch">
      <div class="inline-block mb-[-5px]">
        <vs-select v-model="sortField" class="mr-2" :color="twPrimary">
          <vs-select-item :key="item.value" :text="item.text" :modelValue="item.value"
                          v-for="item in filterChoices"/>
        </vs-select>
      </div>
      <div class="inline-block mb-[-5px]">
        <vs-switch v-model="reverseSort" :color="twPrimary">
          <template #off>Ordered</template>
          <template #on>Reversed</template>
        </vs-switch>
      </div>
    </div>
    <div class="body">
      <div class="flex flex-wrap justify-center" v-if="!updatingStocks">
        <WatchedStock :stock="stock" v-for="stock in this.sortedStock(this.sortField, this.reverseSort)"/>
      </div>
      <div class="flex justify-center p-10 pt-[100px]" v-else>
        <vs-progress class="min-w-[300px] max-w-[700px]" indeterminate :color="twPrimary">primary</vs-progress>
      </div>
    </div>
  </div>
</template>

<style scoped>

</style>