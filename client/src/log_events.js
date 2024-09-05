import axios from "axios";
import {check_admin} from "@/firebase_auth.js";
import {geo_location, session_seed} from "@/session.js";

// let local_url = 'http://192.168.1.11:5000'
let server_url = ' https://analytics-trustyfox.pythonanywhere.com'

export async function log_event(name, type, info) {

    //dont log event if admin logged in
    if (await check_admin("https://review-trustyfox.pythonanywhere.com")) return

    if (import.meta.env.DEV) console.log(name, {'info': String(info)}, session_seed)

    const url = `${server_url}/event/add`

    let params = {
        name: String(name),
        source: 'trusty_corner',
        type: String(type),
        info: String(info),
        uid: session_seed,
        geo: geo_location,
    }


    axios.post(url, params)
        .then()
        .catch(error => null)
}