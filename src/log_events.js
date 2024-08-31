import axios from "axios";
import {check_admin} from "@/firebase_auth.js";

// let local_url = 'http://192.168.1.11:5000'
let server_url = ' https://analytics-trustyfox.pythonanywhere.com'
export async function log_event(name, type, info) {

    //dont log event if admin logged in
    if (await check_admin("https://review-trustyfox.pythonanywhere.com")) return

    if (import.meta.env.DEV) console.log(name, {'info': String(info)})

    const url = `${server_url}/event/add`
    const params = {
        name: String(name),
        source: 'trusty_corner',
        type: String(type),
        info: String(info),
    }

    axios.get(url, {params: params})
        .then()
}