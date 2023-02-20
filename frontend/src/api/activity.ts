import axios from "axios";

const host = import.meta.env.VITE_API_URL


export function api_activities(token: string) {
    return axios.get(host + '/api/v1/activities', {headers: {'Authorization': 'Bearer ' + token}})
}
