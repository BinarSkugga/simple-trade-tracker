import {defineStore} from "pinia";

// Of course frontend will never have access to the raw password
const testUser = {'id': 45, 'mail': 'test@gmail.com', 'password': 'blopblopblop'}

export const useUsersStore = defineStore({
    id: 'users',
    state: () => ({
        users: [testUser],
        loggedIn: true  // Default to true for testing
    }),
    actions: {
        login(username: string, password: string) {
            // Mocked Login
            this.loggedIn = username === 'test@gmail.com' && password === 'blopblopblop';
        }
    }
})