<script>
export default {
  name: "PositionCard",
  props: ['position', 'stock'],
  methods: {
    getTotalValue(position, stock) {
      return (position.quantity * stock.price).toFixed(2)
    },
    getShareCount(position) {
      return position.quantity.toFixed(2)
    },
    getIncome(position, stock) {
      const distributionDivision = stock.div_distribution === 'Monthly' ? 12 : 4
      return (position.quantity * stock.div_yield * stock.price / distributionDivision).toFixed(2)
    },
    getCapitalGain(position) {
      return (position.market_value - position.book_value).toFixed(2)
    }
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
      <span class="text-center" :class="[getCapitalGain(position) >= 0 ? 'text-green-600': 'text-red-600']">
        ${{ getCapitalGain(position) }} <br/>Gain
      </span>
    </div>
  </div>
</template>

<style scoped>

</style>