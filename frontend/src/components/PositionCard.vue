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
    getTotalMonthlyIncome(position, stock) {
      return (position.quantity * stock.dividend_yield * stock.price / 12)
          .toFixed(2)
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
      ${{ getTotalMonthlyIncome(position, stock) }} <br/>Monthly
    </span>
      <span class="text-center">
      ${{ getCapitalGain(position) }} <br/>Gain
    </span>
    </div>
  </div>
</template>

<style scoped>

</style>