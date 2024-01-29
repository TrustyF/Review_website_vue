export async function check_server_awake(curr_api) {
    let retry = 3
    let found = false

    while (retry > 0) {

        console.info('pinging server')

        const url = new URL(`${curr_api}/awake`)
        await fetch(url)
            .then(response => {
                console.log('server response',response)
                if (response.ok) {
                    console.info('server awake')

                    found = true
                    retry = 0
                } else {
                    console.info('server sleeping')

                    retry -= 1
                }
            })
            .catch(error => {
                console.info('server error')

                retry -= 1
            })
    }

    if (retry < 1 && !found) {
        console.error('server could not be reached')
        return false
    } else {
        return true
    }

}