<script>
import {mapActions} from "pinia";
import {usePortfolioStore} from "@/stores/PortfoliosStore";
import PortfolioCard from "@/components/PortfolioCard.vue";
import {useStocksStore} from "@/stores/StocksStore";

export default {
  name: "MyPortfolios",
  components: {PortfolioCard},
  methods: {
    ...mapActions(usePortfolioStore, ['fetchPortfolios', 'getPortfolios']),
    ...mapActions(useStocksStore, ['fetchStocks']),
  },
  mounted() {
      this.fetchStocks()
      this.fetchPortfolios()
  }
}
</script>

<template>
  <div class="centered">
    <PortfolioCard v-for="portfolio in this.getPortfolios()" :name="portfolio.name" :entries="portfolio.entries"/>
  </div>
</template>

<style scoped>
.centered {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translateX(-50%) translateY(-50%);
  max-width: 1000px;
  min-width: 450px;
}
</style>