import axios from "axios";

const host = import.meta.env.VITE_API_URL

export function api_stocks(token: string) {
    return axios.get(host + '/api/v1/watchlist', {headers: {'Authorization': 'Bearer ' + token}})
}

export function api_update_stocks(token: string) {
    return axios.get(host + '/api/v1/watchlist/update', {headers: {'Authorization': 'Bearer ' + token}})
}
