<script>
import {mapActions} from "pinia";
import {usePositionStore} from "@/stores/PositionsStore";
import {useActivityStore} from "@/stores/ActivitiesStore";
import {useAccountsStore} from "@/stores/AccountsStore";
import {ref} from "vue";
import VueApexCharts from "vue3-apexcharts";
import {formnum} from "@/utils";
import {gainBreakdownChart, stockBreakdownChart} from "@/charts";
import {useStocksStore} from "@/stores/StocksStore";

export default {
  name: "Breakdown",
  components: {
    apexchart: VueApexCharts
  },
  data() {
    const positionsFetched = ref(false)
    const gainSeries = []
    const gainOptions = gainBreakdownChart

    const stocksSeries = []
    const stocksOptions = stockBreakdownChart

    return {positionsFetched, gainOptions, gainSeries, stocksSeries, stocksOptions}
  },
  methods: {
    formnum,
    ...mapActions(usePositionStore, ['getPositions', 'fetchPositions']),
    ...mapActions(useActivityStore, ['getActivities', 'fetchActivities']),
    ...mapActions(useStocksStore, ['getStocks', "fetchStocks"]),
    ...mapActions(useAccountsStore, ['getCurrentAccount', 'fetchCurrentAccount']),

    getStockFromWSID(ws_id) {
      return this.getStocks().find(e => e.ws_id === ws_id)
    },
    currentTotalValue() {
      return this.getPositions().reduce((a, position) => {
        return a + position.book_value
      }, 0)
    },
    getTotalDeposits() {
      return this.getActivities().reduce((a, activity) => {
        if (activity.type !== 'deposit') return a
        return a + activity.amount
      }, 0)
    },
    getTotalLifetimeDividends() {
      return this.getActivities().reduce((a, activity) => {
        if (activity.type !== 'dividend') return a
        return a + activity.amount
      }, 0)
    },
    getUsedDeposits() {
      return this.getTotalDeposits() - this.getCurrentAccount().available_balance
    },
    getCapitalGain() {
      return this.currentTotalValue() - this.getUsedDeposits() - this.getTotalLifetimeDividends()
    },
    getCapitalGainPercent() {
      return this.getCapitalGain() / this.currentTotalValue() * 100
    },
    getDividendGainPercent() {
      return this.getTotalLifetimeDividends() / this.currentTotalValue() * 100
    },
    getTotalGain() {
      return this.getTotalLifetimeDividends() + this.getCapitalGain()
    },
    getTotalGainPercent() {
      return this.getTotalGain() / this.currentTotalValue() * 100
    }
  },
  mounted() {
    Promise.all([this.fetchStocks(), this.fetchPositions(), this.fetchActivities(), this.fetchCurrentAccount()]).then(_ => {
      this.positionsFetched = true
      this.gainSeries = [this.getTotalLifetimeDividends(), this.getCapitalGain()]

      this.getPositions().reduce((a, position) => {
        this.stocksSeries.push(position.book_value)
        const stock = this.getStockFromWSID(position.ws_id)
        this.stocksOptions.labels.push(stock.symbol)
      }, 0)
    })
  }
}
</script>

<template>
  <div v-if="positionsFetched">
    <div class="p-10 text-center">
      <div class="uppercase mb-2">Portfolio Value</div>
      <div class="text-4xl">
        ${{ formnum(currentTotalValue()) }}
        <span :class="[getTotalGainPercent() >= 0 ? 'text-green-600': 'text-red-600']">
          ({{ formnum(getTotalGainPercent()) }}%)
        </span>
      </div>
    </div>

    <div class="separator my-5"></div>

    <div class="flex flex-wrap justify-around">
      <div class="min-w-[380px] w-[380px] m-2">
        <div class="text-center font-bold">Gains</div>
        <apexchart type="pie" :options="gainOptions" :series="gainSeries"></apexchart>
      </div>

      <div class="min-w-[380px] w-[380px] m-2">
        <div class="text-center font-bold">Stocks</div>
        <apexchart type="pie" :options="stocksOptions" :series="stocksSeries"></apexchart>
      </div>
    </div>
  </div>
</template>

<style scoped>

</style>