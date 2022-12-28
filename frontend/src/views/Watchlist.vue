<script>
import { ref } from 'vue'
import {mapActions} from "pinia";
import {useUsersStore} from "@/stores/UsersStore";
import {useStocksStore} from "@/stores/StocksStore";
import WatchedStock from "@/components/WatchedStock.vue";

export default {
  name: "watchlist",
  components: {WatchedStock},
  data() {
    const stocksFetched = ref(false)
    const updatingStocks = ref(false)

    const sortField = ref('symbol')
    const reverseSort = ref(false)
    const searchString = ref('')

    const filterChoices = [
      {text: 'Symbol', value: 'symbol'},
      {text: 'Name', value: 'name'},
      {text: 'Yield', value: 'dividend_yield'},
      {text: 'Price', value: 'price'},
      {text: 'Income', value: 'getMonthlyIncome'},
      {text: 'ExDate', value: 'isExDataPassed'}
    ]

    return {
      stocksFetched, updatingStocks,
      sortField, reverseSort, filterChoices,
      primaryColor: twPrimary, searchString
    }
  },
  methods: {
    ...mapActions(useUsersStore, ['logout', 'getUser']),
    ...mapActions(useStocksStore, ['getStocks', "fetchStocks", "updateStocks"]),
    getMonthlyIncome(stock) {
      return (stock.dividend_yield * stock.price / 12)
    },
    mangleStocks(field, reverse, search) {
      const stocks = this.getStocks()
      const upperSearch = search.toUpperCase()

      let sortedStocks = stocks.slice().sort((a, b) => {
        if(['getMonthlyIncome', 'isExDataPassed'].includes(field))
          return this[field](a) - this[field](b)
        if(['name', 'symbol'].includes(field))
          return a[field].localeCompare(b[field])

        return a[field] - b[field]
      })

      if(reverse) sortedStocks = sortedStocks.slice().reverse()

      return sortedStocks.filter(stock => {
        if(upperSearch.length === 0) return true
        return stock.name.toUpperCase().indexOf(upperSearch) > -1
            || stock.symbol.toUpperCase().indexOf(upperSearch) > -1
            || stock.div_distribution.toUpperCase().indexOf(upperSearch) > -1
      })
    },
    updateStocksWithLoading() {
      this.updatingStocks = true
      this.updateStocks().finally(_ => {
        this.updatingStocks = false
      })
    },
    isExDataPassed(stock) {
      return Date.now() / 1000 >= stock.div_ex_date
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
    <div class="text-center mt-4 font-bold text-lg">
      Watchlist
      <button v-ripple class="button round ml-2" @click="updateStocksWithLoading()"
        :disabled="updatingStocks">↻</button>
    </div>
    <div class="text-center mt-4">
      <input class="text-in w-[285px] m-2" type="text" placeholder="Search" v-model="searchString"/>
      <div class="inline-block w-[285px] m-2">
        <div class="inline-block mb-[-5px]">
          <vs-select v-model="sortField" class="mr-2" :color="primaryColor">
            <vs-select-item :key="item.value" :text="item.text" :modelValue="item.value"
                            v-for="item in filterChoices"/>
          </vs-select>
        </div>
        <div class="inline-block mb-[-5px]">
          <vs-switch v-model="reverseSort" :color="primaryColor">
            <template #off>Ordered</template>
            <template #on>Reversed</template>
          </vs-switch>
        </div>
      </div>
    </div>
    <div class="body">
      <div class="flex flex-wrap justify-center" v-if="!updatingStocks && stocksFetched">
        <WatchedStock :stock="stock" v-for="stock in this.mangleStocks(this.sortField, this.reverseSort, this.searchString)"/>
      </div>
      <div class="flex justify-center p-10 pt-[100px]" v-else>
        <vs-progress class="min-w-[300px] max-w-[700px]" indeterminate :color="primaryColor"/>
      </div>
    </div>
  </div>
</template>

<style scoped>

</style>