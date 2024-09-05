import axios from "axios";

export const session_seed = Math.round(Math.random() * 10000000)

let server_url = ' https://analytics-trustyfox.pythonanywhere.com'

const get_geo = async () => {
    let url = 'https://api.ipify.org?format=json';
    return await axios.get(url)
        .then(resp => {
            // console.log(resp.data)
            let geo_url = `${server_url}/event/geo_locate`
            return axios.get(geo_url, {params: {ip: resp.data['ip']}})
                .then(geo => geo.data)
                .catch(err => err)

        })
        .catch(err => err)
}

export const geo_location = await get_geo()
