import axios from "axios";

const host = import.meta.env.VITE_API_URL

export function api_stocks(token: string) {
    return axios.get(host + '/api/v1/stocks', {headers: {'Authorization': 'Bearer ' + token}})
}