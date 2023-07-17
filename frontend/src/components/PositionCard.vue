<script>
import {mapActions} from "pinia";
import {useActivityStore} from "@/stores/ActivitiesStore";
import {formnum} from "@/utils";

export default {
  name: "PositionCard",
  props: ['position', 'stock', 'includeDivGains'],
  methods: {
    formnum,
    ...mapActions(useActivityStore, ['getActivities']),

    getTotalValue(position, stock) {
      return (position.quantity * stock.price)
    },
    getShareCount(position) {
      return position.quantity
    },
    getIncome(position, stock) {
      const distributionDivision = stock.div_distribution === 'Monthly' ? 12 : 4
      return (position.quantity * (stock.div_yield * stock.price) / distributionDivision)
    },
    getCapitalGain(position) {
      return (position.market_value - position.book_value)
    },
    getLifetimeDividends(stock) {
      return this.getActivities().reduce((a, activity) => {
        if(activity.type !== 'dividend' || activity.symbol !== stock.symbol) return a
        return a + activity.amount
      }, 0)
    },
    getAbsoluteGain(position, stock) {
      if(this.includeDivGains)
        return (this.getCapitalGain(position) + this.getLifetimeDividends(stock))
      return this.getCapitalGain(position)
    },
  }
}
</script>

<template>
  <div class="card m-2 min-w-[365px] max-w-[365px] select-none">
    <div class="flex justify-between">
      <span class="font-bold">{{ stock.symbol }}</span>
      <span class="font-bold text-sm">${{ formnum(getTotalValue(position, stock)) }}</span>
    </div>
    <div class="my-3 flex justify-around">
      <span class="text-center">
        {{ formnum(getShareCount(position)) }} <br/>Shares
      </span>
      <span class="text-center">
        ${{ formnum(getIncome(position, stock)) }} <br/>{{ stock.div_distribution }}
      </span>
      <span class="text-center" :class="[getAbsoluteGain(position, stock) >= 0 ? 'text-green-600': 'text-red-600']">
        ${{ formnum(getAbsoluteGain(position, stock)) }} <br/>Gain
      </span>
    </div>
  </div>
</template>

<style scoped>

</style>