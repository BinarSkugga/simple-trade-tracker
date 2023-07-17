import {defineStore, storeToRefs} from "pinia";
import {useUsersStore} from "@/stores/UsersStore";
import {api_activities, api_update_activities} from "@/api/activity";


export const useActivityStore = defineStore({
    id: 'activities',
    state: () => ({
        activities: []
    }),
    actions: {
        getActivities() {
            return this.activities
        },
        fetchActivities() {
            const {token} = storeToRefs(useUsersStore())
            return api_activities(token.value!).then(response => {
                this.activities = response.data
            }).catch(error => {})
        },
        updateActivities() {
            const {token} = storeToRefs(useUsersStore())
            return api_update_activities(token.value!).then(response => {
                this.activities = response.data
            }).catch(error => {})
        }
    }
})