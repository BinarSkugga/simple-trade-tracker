import {defineStore, storeToRefs} from "pinia";
import {useUsersStore} from "@/stores/UsersStore";
import {api_positions, api_update_positions} from "@/api/position";


export const usePositionStore = defineStore({
    id: 'positions',
    state: () => ({
        positions: []
    }),
    actions: {
        getPositions() {
            return this.positions
        },
        fetchPositions() {
            const {token} = storeToRefs(useUsersStore())
            return api_positions(token.value!).then(response => {
                this.positions = response.data
            }).catch(error => {})
        },
        updatePositions() {
            const {token} = storeToRefs(useUsersStore())
            return api_update_positions(token.value!).then(response => {
                this.positions = response.data
            }).catch(error => {})
        }
    }
})