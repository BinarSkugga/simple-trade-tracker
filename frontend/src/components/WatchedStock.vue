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
  <div class="card m-2 min-w-[300px] max-w-[300px]" type="button" v-ripple="'#1abc9c35'">
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
        <div>
          <span :class="[stock.buyable ? 'stock-tag-primary':'stock-tag-red']">Buyable</span>
          <span :class="[stock.can_use_fractional ? 'stock-tag-primary':'stock-tag-red']">Fractional</span>
        </div>
        <div>
          <span class="stock-tag-gray">{{stock.exchange}}</span>
          <span class="stock-tag-gray">{{stock.currency}}</span>
        </div>
      </div>
      <div class="text-center mt-3">
        <span class="text-[10px] inline-block text-gray-500 pt-1.5 w-[250px] truncate">{{stock.name}}</span>
      </div>
    </div>
</template>

<style scoped>

</style>