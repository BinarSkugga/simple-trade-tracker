<script>
export default {
  name: "StockCard",
  props: ['symbol', 'price', 'dividend_yield', 'payout_ratio', 'monthly_return', 'sector', 'currency'],
  computed: {
    dividendClass() {
      if(this.dividend_yield <= 2) return 'bad';
      if(this.dividend_yield > 2 && this.dividend_yield <= 5) return 'ok';
      if(this.dividend_yield > 5) return 'good';
    },
    payoutRatioClass() {
      if(this.payout_ratio <= 3) return 'bad';
      if(this.payout_ratio > 3 && this.payout_ratio < 5) return 'ok';
      if(this.payout_ratio > 15 && this.payout_ratio < 20) return 'ok';
      if(this.payout_ratio >= 5 && this.payout_ratio <= 15) return 'good';
      if(this.payout_ratio >= 20) return 'bad';
    }
  }
}
</script>

<template>
  <n-card :title="symbol" size="medium">
    <template #header-extra>
      <span class="bold">{{price}}$</span>
      <n-tag size="small" round style="margin-left: 10px">
        {{currency}}
      </n-tag>
    </template>
    <n-space horizontal>
      <n-statistic label="Yield" tabular-nums :class="dividendClass">
        <span :class="dividendClass">
          <n-number-animation
            ref="numberAnimationInstRef"
            :to="dividend_yield"
            :precision="2"
          />
        </span>
        <template #suffix>
          <span :class="dividendClass">%</span>
        </template>
      </n-statistic>
      <n-statistic label="Payout Ratio" tabular-nums>
        <span :class="payoutRatioClass">
          <n-number-animation
            ref="numberAnimationInstRef"
            :to="payout_ratio"
            :precision="2"
          />
        </span>
        <template #suffix>
          <span :class="payoutRatioClass">%</span>
        </template>
      </n-statistic>
      <n-statistic label="Monthly Return" tabular-nums>
        <n-number-animation
          ref="numberAnimationInstRef"
          :to="monthly_return"
          :precision="2"
        />
        <template #suffix>
          $
        </template>
      </n-statistic>
    </n-space>
    <template #action>
      {{ sector }}
    </template>
  </n-card>
</template>

<style scoped>
.n-card {
  max-width: 450px;
  margin: 10px;
}

.n-statistic {
  margin: 0 10px;
}

.bold {
  font-weight: bold;
}

.good {
  color: #27ae60;
}

.ok {
  color: #f39c12;
}

.bad {
  color: #e74c3c;
}
</style>