<script>
import {mapActions} from "pinia";
import {usePositionStore} from "@/stores/PositionsStore";
import {useActivityStore} from "@/stores/ActivitiesStore";
import {useAccountsStore} from "@/stores/AccountsStore";
import {ref} from "vue";
import VueApexCharts from "vue3-apexcharts";
import {formnum} from "@/utils";
import {gainBreakdownChart, sectorBreakdownChart, stockBreakdownChart} from "@/charts";
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

    const sectorSeries = []
    const sectorOptions = sectorBreakdownChart

    return {positionsFetched, gainOptions, gainSeries, stocksSeries, stocksOptions, sectorSeries, sectorOptions}
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
    currentTotalMarketValue() {
      return this.getPositions().reduce((a, position) => {
        return a + position.market_value
      }, 0)
    },
    currentTotalBookValue() {
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
      return this.currentTotalMarketValue() - this.currentTotalBookValue()
    },
    getCapitalGainPercent() {
      return this.getCapitalGain() / this.currentTotalMarketValue() * 100
    },
    getDividendGainPercent() {
      return this.getTotalLifetimeDividends() / this.currentTotalMarketValue() * 100
    },
    getTotalGain() {
      return this.getTotalLifetimeDividends() + this.getCapitalGain()
    },
    getTotalGainPercent() {
      return this.getTotalGain() / this.currentTotalMarketValue() * 100
    },
    getSectorValue(sector) {
      return this.getPositions().reduce((a, position) => {
        const stock = this.getStockFromWSID(position.ws_id)
        if (stock.sector !== sector) return a
        return a + position.market_value
      }, 0)
    }
  },
  mounted() {
    Promise.all([this.fetchStocks(), this.fetchPositions(), this.fetchActivities(), this.fetchCurrentAccount()]).then(_ => {
      this.positionsFetched = true

      if (this.getCapitalGain() > 0)
        this.gainSeries = [this.getTotalLifetimeDividends(), this.getCapitalGain()]
      else
        this.gainSeries = [this.getTotalLifetimeDividends()]

      // Reset labels
      this.sectorOptions.labels = []

      this.getPositions().reduce((a, position) => {
        this.stocksSeries.push(position.market_value)
        const stock = this.getStockFromWSID(position.ws_id)
        this.stocksOptions.labels.push(stock.symbol)

        if (stock.sector === 'Consumer Discretionary') stock.sector = 'Consumer'
        if (this.sectorOptions.labels.includes(stock.sector)
            || (stock.sector === null && this.sectorOptions.labels.includes('Diversified'))) return

        this.sectorSeries.push(this.getSectorValue(stock.sector))
        this.sectorOptions.labels.push(stock.sector === null ? 'Diversified' : stock.sector)
      }, 0)
    })
  }
}
</script>

<template>
  <div v-if="positionsFetched">
    <div class="p-5 text-center">
      <div class="uppercase mb-2">Portfolio Value</div>
      <div class="text-4xl">
        ${{ formnum(currentTotalMarketValue()) }}
        <span :class="[getTotalGainPercent() >= 0 ? 'text-green-600': 'text-red-600']">
          ({{ formnum(getTotalGainPercent()) }}%)
        </span>
      </div>
    </div>
    <div class="flex flex-wrap justify-around">
      <div class="p-5 text-center">
        <div class="uppercase mb-2">Capital</div>
        <div class="text-2xl">
          ${{ formnum(getCapitalGain()) }}
          <span :class="[getCapitalGain() >= 0 ? 'text-green-600': 'text-red-600']">
            ({{ formnum(getCapitalGainPercent()) }}%)
          </span>
        </div>
      </div>
      <div class="p-5 text-center">
        <div class="uppercase mb-2">Dividend</div>
        <div class="text-2xl">
          ${{ formnum(getTotalLifetimeDividends()) }}
          <span :class="[getTotalLifetimeDividends() >= 0 ? 'text-green-600': 'text-red-600']">
          ({{ formnum(getDividendGainPercent()) }}%)
          </span>
        </div>
      </div>
    </div>

    <div class="separator my-5"></div>

    <div class="flex flex-wrap justify-around">
      <div class="min-w-[380px] w-[30%] m-2">
        <div class="text-center font-bold">Gains</div>
        <apexchart type="pie" :options="gainOptions" :series="gainSeries"></apexchart>
      </div>

      <div class="min-w-[380px] w-[30%] m-2">
        <div class="text-center font-bold">Stocks</div>
        <apexchart type="pie" :options="stocksOptions" :series="stocksSeries"></apexchart>
      </div>

      <div class="min-w-[380px] w-[30%] m-2">
        <div class="text-center font-bold">Sectors</div>
        <apexchart type="pie" :options="sectorOptions" :series="sectorSeries"></apexchart>
      </div>
    </div>
  </div>
</template>

<style scoped>

</style>