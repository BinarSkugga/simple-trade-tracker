import {defineStore, storeToRefs} from 'pinia'
// @ts-ignore
import {StockModel} from "@/models/StockModel";
import {useUsersStore} from "@/stores/UsersStore";
import {api_stocks} from "@/api/stock";


export const useStocksStore = defineStore({
    id: 'stocks',
    state: () => ({
        stocks: []
    }),
    actions: {
        getStocks() {
            console.log(this.stocks)
            return this.stocks
        },
        fetchStocks() {
            const {token} = storeToRefs(useUsersStore())
            return api_stocks(token.value!).then(response => {
                this.stocks = response.data
            }).catch(error => {

            })
        },
    }
})
