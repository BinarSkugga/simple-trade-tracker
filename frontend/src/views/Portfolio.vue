<script>
import {ref} from 'vue';
import {mapActions} from "pinia";
import {usePositionStore} from "@/stores/PositionsStore";
import {useStocksStore} from "@/stores/StocksStore";
import PositionCard from "@/components/PositionCard.vue";

export default {
  name: "portfolio",
  components: {PositionCard},
  data() {
    const positionsFetched = ref(false)
    const updatingPositions = ref(false)

    return {positionsFetched, updatingPositions, primaryColor: twPrimary}
  },
  methods: {
    ...mapActions(usePositionStore, ['getPositions', "fetchPositions", "updatePositions"]),
    ...mapActions(useStocksStore, ['getStocks', "fetchStocks"]),

    updatePositionsWithLoading() {
      this.updatingPositions = true
      this.updatePositions().finally(_ => {
        this.updatingPositions = false
      })
    },
    getStockFromWSID(ws_id) {
      return this.getStocks().find(e => e.ws_id === ws_id)
    },
    getTotalMonthlyIncome() {
      return this.getPositions().reduce((a, position) => {
        const stock = this.getStockFromWSID(position.ws_id)
        const monthly_inc = (position.quantity * stock.dividend_yield * stock.price / 12)
        return a + monthly_inc
      }, 0).toFixed(2)
    }
  },
  mounted() {
    Promise.all([this.fetchStocks(), this.fetchPositions()]).then(_ => {
      this.positionsFetched = true
    })
  }
}
</script>

<template>
  <div>
    <div class="text-center mt-4 font-bold text-lg">
      Overview
    </div>
    <div class="flex justify-around mt-2">
      <span class="text-center" v-if="positionsFetched">
        ${{ getTotalMonthlyIncome() }} <br/>Total Monthly Income
      </span>
    </div>

    <div class="separator my-5"></div>

    <div class="text-center mt-4 font-bold text-lg">
      Positions
      <button v-ripple class="button round ml-2" @click="updatePositionsWithLoading()"
              :disabled="updatingPositions">↻
      </button>
    </div>
    <div class="body">
      <div class="flex flex-wrap justify-center" v-if="!updatingPositions && positionsFetched">
        <PositionCard :position="position" :stock="getStockFromWSID(position.ws_id)" v-for="position in getPositions()"/>
      </div>
      <div class="flex justify-center p-10 pt-[100px]" v-else>
        <vs-progress class="min-w-[300px] max-w-[700px]" indeterminate :color="primaryColor"/>
      </div>
    </div>
  </div>
</template>

<style scoped>

</style>