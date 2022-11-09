<script>
import {mapActions} from "pinia";
import {useStocksStore} from "@/stores/StocksStore";

export default {
  name: "PortfolioCard",
  props: ['name', 'entries'],
  methods: {
    ...mapActions(useStocksStore, ['getStocks']),
    stockCount(stock_id) {
      return this.entries.filter(e => e.stock_id === stock_id).reduce((sum, entry) => sum + entry.count, 0)
    }
  },
  computed: {
    totalStocksCount() {
      const stocks = this.getStocks()
      return stocks.reduce((sum, stock) => sum + this.stockCount(stock.id), 0)
    },
    stocksOrderedByCount() {
      return this.getStocks().sort(stock => this.stockCount(stock.id)).reverse()
    },
    totalMonthlyIncome() {
      const stocks = this.getStocks()
      return stocks.reduce((sum, stock) => sum + (stock.monthly_return * this.stockCount(stock.id)), 0)
    },
    currentValue() {
      const stocks = this.getStocks()
      return stocks.reduce((sum, stock) => sum + (stock.price * this.stockCount(stock.id)), 0).toFixed(2)
    },
    strikeValue() {
      return this.entries.reduce((sum, entry) => sum + (entry.strike * entry.count), 0).toFixed(2)
    },
    profit() {
      return (this.currentValue - this.strikeValue).toFixed(2)
    },
    profitClass() {
      if(this.profit >= 0) return 'good'
      else return 'bad'
    },
    monthlyYield() {
      if(this.totalMonthlyIncome === 0 || this.currentValue === 0) return 0
      return (this.totalMonthlyIncome / this.currentValue * 100).toFixed(2)
    }
  }
}
</script>

<template>
  <n-card :title="name" hoverable size="medium">
    <template #header-extra>
        Monthly Income:&nbsp;
        <span class="bold">
          <n-number-animation
            :from="0.00"
            :to="totalMonthlyIncome"
            :precision="2"
            :duration="1500"
          />$
        </span>
    </template>
    <div v-if="this.totalStocksCount === 0" class="empty-portfolio">
      No stocks in this portfolio
    </div>
    <div v-else>
      <span v-for="stock in this.stocksOrderedByCount.slice(0, 10)" class="stock_tag">
        <n-tag v-if="stockCount(stock.id) > 0">
          {{ stockCount(stock.id) }}x{{ stock.symbol }}
        </n-tag>
      </span>
    </div>
    <template #action>
      <n-space horizontal>
        <n-statistic label="Current Value" :value="currentValue">
          <template #suffix>$</template>
        </n-statistic>
        <n-statistic label="Profit">
          <span :class="profitClass">{{profit}}$</span>
        </n-statistic>
        <n-statistic label="Monthly Yield">
          {{monthlyYield}}%
        </n-statistic>
      </n-space>
    </template>
  </n-card>
</template>

<style scoped>
.bold {
  font-weight: bold;
}

.good {
  color: #27ae60;
}

.bad {
  color: #e74c3c;
}

.empty-portfolio {
  text-align: center;
  font-size: 17px;
  color: rgb(118, 124, 130);
}

.n-card {
  max-width: 500px;
  margin: 0 auto;
}

.n-card + .n-card {
  margin-top: 15px;
}

.stock_tag + .stock_tag {
  margin-left: 5px;
}
</style>