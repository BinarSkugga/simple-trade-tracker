import axios from "axios";

const host = import.meta.env.VITE_API_URL

export function api_current_account(token: string) {
    return axios.get(host + '/api/v1/account', {headers: {'Authorization': 'Bearer ' + token}})
}