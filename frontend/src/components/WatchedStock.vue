<script>
export default {
  name: "WatchedStock",
  props: ['stock'],
  methods: {
    getYield(stock) {
      return (stock.dividend_yield * 100).toFixed(2)
    },
    getMonthlyIncome(stock) {
      return (stock.dividend_yield * stock.price / 12).toFixed(2)
    },
    getQuarterlyIncome(stock) {
      return (stock.dividend_yield * stock.price / 4).toFixed(2)
    }
  }
}
</script>

<template>
  <div class="card m-2 w-[350px]">
      <div class="flex justify-between">
        <span class="font-bold">{{stock.symbol}}</span>
        <span class="font-bold text-sm">${{stock.price}}</span>
      </div>
      <div class="my-3 flex justify-around">
        <span class="text-center">
          {{getYield(stock)}}% <br/>Yield
        </span>
        <span class="text-center">
          ${{getMonthlyIncome(stock)}} <br/>Monthly
        </span>
        <span class="text-center">
          ${{getQuarterlyIncome(stock)}} <br/>Quarterly
        </span>
      </div>
      <div class="flex justify-between">
        <span class="text-[10px] truncate align-middle pt-1.5 w-[200px]">{{stock.name}}</span>
        <div>
          <span class="stock-tag">{{stock.exchange}}</span>
          <span class="stock-tag">{{stock.currency}}</span>
        </div>
      </div>
    </div>
</template>

<style scoped>

</style>