import {defineStore} from "pinia";
import {api_login, api_me} from "@/api/auth";

export const useUsersStore = defineStore({
    id: 'users',
    state: () => ({
        users: [],
        loggedIn: false,
        token: null,
        user: null
    }),
    actions: {
        login(username: string, password: string) {
            api_login(username, password).then(response => {
                this.token = response.data.access_token
                api_me(this.token!).then(response => {
                    this.user = response.data
                    localStorage.token = this.token
                    this.loggedIn = true
                }).catch(error => {
                    this.loggedIn = false
                    this.token = null
                    localStorage.token = null
                })
            }).catch(error => {
                this.loggedIn = false
                this.token = null
                localStorage.token = null
            })
        },
        tokenLogin() {
            if(localStorage.token !== 'null') {
                this.token = localStorage.token
                api_me(this.token!).then(response => {
                    this.user = response.data
                    this.loggedIn = true
                }).catch(error => {
                    this.loggedIn = false
                    this.token = null
                    localStorage.token = null
                })
            } else {
                this.loggedIn = false
                this.token = null
                localStorage.token = null
            }
        },
        logout() {
            this.loggedIn = false
            this.token = null
            localStorage.token = null
        }
    }
})