import {axios} from '@bundled-es-modules/axios';
import {check_admin} from "@/firebase_auth.js";
import {geo_location, session_seed} from "/src/scripts/session.js";

let local_url = 'http://127.0.0.1:8080'
let server_url = 'https://analytics-trustyfox.pythonanywhere.com'
let curr_api = server_url
let project = 'trusty_corner'


export async function log_event(name, type, info) {

    if (await check_admin("https://review-trustyfox.pythonanywhere.com")) return

    let url = `${curr_api}/event/add`

    let params = {
        name: String(name),
        source: project,
        type: String(type),
        info: String(info),
        uid: session_seed,
        geo: await geo_location,
        timestamp: Date.now()
    }

    if (import.meta.env.DEV && curr_api !== local_url) {
        console.log('dev log', params)
        return
    }

    axios.post(url, params)
        .then(resp => {
            console.log('successfully logged event')
        })
        .catch(error => null)
}

export async function ping_user_leave() {

    if (await check_admin("https://review-trustyfox.pythonanywhere.com")) return

    let url = `${curr_api}/event/ping_user_alive`

    let params = {
        source: project,
        uid: session_seed,
        geo: await geo_location,
        timestamp: Date.now()
    }

    if (import.meta.env.DEV && curr_api !== local_url) {
        return
    }

    axios.put(url, params)
        .then(resp => null)
        .catch(error => null)
}