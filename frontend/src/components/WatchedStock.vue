<script>
export default {
  name: "WatchedStock",
  props: ['stock'],
  data() {
    return {
      primaryColor: twPrimary
    }
  },
  methods: {
    getYield(stock) {
      console.log(stock)
      return (stock.div_yield * 100).toFixed(2)
    },
    getIncome(stock) {
      const distributionDivision = stock.div_distribution === 'Monthly' ? 12 : 4
      return (stock.div_yield * stock.price / distributionDivision).toFixed(3)
    },
    getExDividendDate(stock) {
      if(stock.div_ex_date == null)
        return null

      return new Date(stock.div_ex_date * 1000).toLocaleDateString()
    },
    isExDataPassed(stock) {
      return Date.now() / 1000 >= stock.div_ex_date
    }
  }
}
</script>

<template>
  <div class="card m-2 min-w-[300px] max-w-[300px] select-none flex-row" type="button" v-ripple="primaryColor + '35'">
      <div class="flex justify-between">
        <span class="font-bold">{{stock.symbol}}</span>
        <span class="font-bold text-sm">${{stock.price}}</span>
      </div>
      <div class="my-3 flex justify-around">
        <span class="text-center">
          {{getYield(stock)}}% <br/>Yield
        </span>
        <span class="text-center">
          ${{getIncome(stock)}} <br/>{{stock.limited ? 'Monthly' : stock.div_distribution}}
        </span>
      </div>
      <div class="flex justify-between">
        <div v-if="!stock.limited">
          <span :class="[isExDataPassed(stock) ? 'stock-tag-red':'stock-tag-green']">Ex: {{getExDividendDate(stock)}}</span>
        </div>
        <div v-else>
          <span class="stock-tag-gray">Limited</span>
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