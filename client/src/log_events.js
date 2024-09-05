import axios from "axios";
import {check_admin} from "@/firebase_auth.js";
import {geo_location, session_seed} from "@/session.js";

// let local_url = 'http://192.168.1.11:5000'
let server_url = ' https://analytics-trustyfox.pythonanywhere.com'


export async function log_event(name, type, info = null) {

    if (await check_admin("https://review-trustyfox.pythonanywhere.com")) return

    let url = `${server_url}/event/add`

    let params = {
        name: String(name),
        source: 'trusty_corner',
        type: String(type),
        info: String(info),
        uid: session_seed,
        geo: await geo_location,
    }

    // console.log(params)

    axios.post(url, params)
        .then(resp => {
            console.log('successfully logged event')
        })
        .catch(error => null)
}