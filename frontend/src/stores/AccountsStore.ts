import {defineStore, storeToRefs} from "pinia";
import {useUsersStore} from "@/stores/UsersStore";
import {api_current_account} from "@/api/account";

export const useAccountsStore = defineStore({
    id: 'accounts',
    state: () => ({
        current_account: null
    }),
    actions: {
        getCurrentAccount() {
            return this.current_account
        },
        fetchCurrentAccount() {
            const {token} = storeToRefs(useUsersStore())
            return api_current_account(token.value!).then(response => {
                this.current_account = response.data
            }).catch(error => {})
        }
    }
})