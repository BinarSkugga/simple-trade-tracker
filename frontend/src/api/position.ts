import axios from "axios";

const host = import.meta.env.VITE_API_URL


export function api_positions(token: string) {
    return axios.get(host + '/api/v1/positions', {headers: {'Authorization': 'Bearer ' + token}})
}

export function api_update_positions(token: string) {
    return axios.get(host + '/api/v1/positions/update', {headers: {'Authorization': 'Bearer ' + token}})
}
