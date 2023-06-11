<script>
import {ref} from 'vue';
import {mapActions} from "pinia";
import {usePositionStore} from "@/stores/PositionsStore";
import {useStocksStore} from "@/stores/StocksStore";
import PositionCard from "@/components/PositionCard.vue";
import {useActivityStore} from "@/stores/ActivitiesStore";

export default {
  name: "portfolio",
  components: {PositionCard},
  data() {
    const positionsFetched = ref(false)
    const updatingPositions = ref(false)

    const searchString = ref('')
    const reverseSort = ref(false)
    const sortField = ref('symbol')

    const filterChoices = [
      {text: 'Symbol', value: 'symbol'},
      {text: 'Name', value: 'name'},
      {text: 'Shares', value: 'quantity'},
      {text: 'Value', value: 'getPositionTotalValue'},
      {text: 'Income', value: 'getIncome'},
      {text: 'Gain', value: 'getAbsoluteGain'}
    ]

    return {
      positionsFetched, updatingPositions, primaryColor: twPrimary,
      searchString, reverseSort, sortField, filterChoices
    }
  },
  methods: {
    ...mapActions(usePositionStore, ['getPositions', "fetchPositions", "updatePositions"]),
    ...mapActions(useStocksStore, ['getStocks', "fetchStocks"]),
    ...mapActions(useActivityStore, ['getActivities', "fetchActivities", "updateActivities"]),

    updatePositionsWithLoading() {
      this.updatingPositions = true
      Promise.all([this.updatePositions(), this.updateActivities()]).finally(_ => {
        this.updatingPositions = false
      })
    },
    getStockFromWSID(ws_id) {
      return this.getStocks().find(e => e.ws_id === ws_id)
    },
    getPositionTotalValue(position, stock) {
      return (position.quantity * stock.price).toFixed(2)
    },
    getCapitalGain(position) {
      return (position.market_value - position.book_value)
    },
    getLifetimeDividends(stock) {
      return this.getActivities().reduce((a, activity) => {
        console.log(stock, activity)
        if(activity.type !== 'dividend' || activity.symbol != stock.symbol) return a
        return a + activity.amount
      }, 0)
    },
    getAbsoluteGain(position, stock) {
      return (this.getCapitalGain(position) + this.getLifetimeDividends(stock)).toFixed(2)
    },
    getIncome(position, stock) {
      const distributionDivision = stock.div_distribution === 'Monthly' ? 12 : 4
      return (position.quantity * stock.div_yield * stock.price / distributionDivision).toFixed(2)
    },
    getTotalMonthlyIncome() {
      return this.getPositions().reduce((a, position) => {
        const stock = this.getStockFromWSID(position.ws_id)
        if (stock.div_distribution !== 'Monthly') return a

        const monthly_inc = (position.quantity * stock.div_yield * stock.price / 12)
        return a + monthly_inc
      }, 0).toFixed(2)
    },
    getTotalQuarterlyIncome() {
      return this.getPositions().reduce((a, position) => {
        const stock = this.getStockFromWSID(position.ws_id)
        if (stock.div_distribution !== 'Quarterly') return a

        const monthly_inc = (position.quantity * stock.div_yield * stock.price / 4)
        return a + monthly_inc
      }, 0).toFixed(2)
    },
    getTotalLifetimeDividends() {
      return this.getActivities().reduce((a, activity) => {
        if(activity.type !== 'dividend') return a
        return a + activity.amount
      }, 0).toFixed(2)
    },
    manglePositions(field, reverse, search) {
      const positions = this.getPositions()
      const upperSearch = search.toUpperCase()

      let sortedPositions = positions.slice().sort((a, b) => {
        const stockA = this.getStockFromWSID(a.ws_id)
        const stockB = this.getStockFromWSID(b.ws_id)

        if (['getPositionTotalValue', 'getAbsoluteGain', 'getIncome'].includes(field))
          return this[field](a, stockA) - this[field](b, stockB)
        if (['name', 'symbol'].includes(field))
          return stockA[field].localeCompare(stockB[field])

        return a[field] - b[field]
      })

      if (reverse) sortedPositions = sortedPositions.slice().reverse()

      return sortedPositions.filter(position => {
        if (upperSearch.length === 0) return true
        const stock = this.getStockFromWSID(position.ws_id)
        return stock.name.toUpperCase().indexOf(upperSearch) > -1
            || stock.symbol.toUpperCase().indexOf(upperSearch) > -1
            || stock.div_distribution.toUpperCase().indexOf(upperSearch) > -1
      })
    },
  },
  mounted() {
    Promise.all([this.fetchStocks(), this.fetchPositions(), this.fetchActivities()]).then(_ => {
      this.positionsFetched = true
    })
  }
}
</script>

<template>
  <div>
    <div class="text-center mt-4 font-bold text-lg">
      Overview
    </div>
    <div class="flex justify-around mt-2">
      <span class="text-center" v-if="positionsFetched">
        ${{ getTotalMonthlyIncome() }} <br/>Total Monthly Income
      </span>
      <span class="text-center" v-if="positionsFetched">
        ${{ getTotalQuarterlyIncome() }} <br/>Total Quarterly Income
      </span>
      <span class="text-center" v-if="positionsFetched">
        ${{ getTotalLifetimeDividends() }} <br/>Lifetime Dividends Paid
      </span>
    </div>

    <div class="separator my-5"></div>

    <div class="text-center mt-4 font-bold text-lg">
      Positions
      <button v-ripple class="button round ml-2" @click="updatePositionsWithLoading()"
              :disabled="updatingPositions">↻
      </button>
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
      <div class="flex flex-wrap justify-center" v-if="!updatingPositions && positionsFetched">
        <PositionCard :position="position" :stock="getStockFromWSID(position.ws_id)"
                      v-for="position in manglePositions(sortField, reverseSort, searchString)"/>
      </div>
      <div class="flex justify-center p-10 pt-[100px]" v-else>
        <vs-progress class="min-w-[300px] max-w-[700px]" indeterminate :color="primaryColor"/>
      </div>
    </div>
  </div>
</template>

<style scoped>

</style>