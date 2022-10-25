import axios from "axios";

const host = import.meta.env.VITE_API_URL


export function api_login(username: string, password: string) {
    return axios.post(host + '/api/v1/login', {'username': username, 'password': password})
}


export function api_me(token: string) {
    return axios.get(host + '/api/v1/me', {headers: {'Authorization': 'Bearer ' + token}})
}
