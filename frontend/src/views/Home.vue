<script>
import Login from "@/views/Login.vue";
import StockCard from "@/components/StockCard.vue";
import {useStocksStore} from "@/stores/StocksStore";
import {storeToRefs} from "pinia";
import {useUsersStore} from "@/stores/UsersStore";

export default {
  name: "Home",
  components: {Login, StockCard},
  data() {
    const {stocks} = storeToRefs(useStocksStore())
    const {loggedIn} = storeToRefs(useUsersStore())

    return {
      stocks: stocks,
      loggedIn
    }
  }
}
</script>

<template>
  <div>
    <Login v-if="!loggedIn"/>
    <div v-else>
        <StockCard v-for="stock in stocks"
                   :symbol="stock.symbol"
                   :price="stock.price"
                   :dividend_yield="stock.dividend_yield * 100"
                   :monthly_return="stock.monthly_return"
                   :payout_ratio="stock.payout_ratio * 100"
                   :sector="stock.sector"
                   :currency="stock.currency"
        ></StockCard>
    </div>
  </div>
</template>

<style scoped>

</style>