import {defineStore, storeToRefs} from "pinia";
import {api_portfolios} from "@/api/portfolio";
import {useUsersStore} from "@/stores/UsersStore";
// @ts-ignore
import {PortfolioModel} from "@/models/PortfolioModel";


export const usePortfolioStore = defineStore({
    id: 'portfolios',
    state: () => ({
        portfolios: Array<PortfolioModel>
    }),
    actions: {
        getPortfolios() {
            return this.portfolios
        },
        fetchPortfolios() {
            const {token} = storeToRefs(useUsersStore())
            return api_portfolios(token.value!).then(response => {
                this.portfolios = response.data
            }).catch(error => {})
        },
    }
})