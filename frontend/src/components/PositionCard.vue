<script>
import {mapActions} from "pinia";
import {useActivityStore} from "@/stores/ActivitiesStore";

export default {
  name: "PositionCard",
  props: ['position', 'stock'],
  methods: {
    ...mapActions(useActivityStore, ['getActivities']),

    getTotalValue(position, stock) {
      return (position.quantity * stock.price).toFixed(2)
    },
    getShareCount(position) {
      return position.quantity.toFixed(2)
    },
    getIncome(position, stock) {
      const distributionDivision = stock.div_distribution === 'Monthly' ? 12 : 4
      return (position.quantity * (stock.div_yield * stock.price) / distributionDivision).toFixed(2)
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
  }
}
</script>

<template>
  <div class="card m-2 min-w-[300px] max-w-[300px] select-none">
    <div class="flex justify-between">
      <span class="font-bold">{{ stock.symbol }}</span>
      <span class="font-bold text-sm">${{ getTotalValue(position, stock) }}</span>
    </div>
    <div class="my-3 flex justify-around">
      <span class="text-center">
        {{ getShareCount(position) }} <br/>Shares
      </span>
      <span class="text-center">
        ${{ getIncome(position, stock) }} <br/>{{ stock.div_distribution }}
      </span>
      <span class="text-center" :class="[getAbsoluteGain(position, stock) >= 0 ? 'text-green-600': 'text-red-600']">
        ${{ getAbsoluteGain(position, stock) }} <br/>Gain
      </span>
    </div>
  </div>
</template>

<style scoped>

</style>