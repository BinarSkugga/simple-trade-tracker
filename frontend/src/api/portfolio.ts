import axios from "axios";

const host = import.meta.env.VITE_API_URL


export function api_portfolios(token: string) {
    return axios.get(host + '/api/v1/portfolios', {headers: {'Authorization': 'Bearer ' + token}})
}