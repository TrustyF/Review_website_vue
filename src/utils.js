export async function check_server_awake(curr_api) {
    let retry = 3

    while (retry > 0) {
        console.log(retry)
        const url = new URL(`${curr_api}/awake`)
        await fetch(url)
            .then(response => {
                if (response.ok) {
                    retry = 0
                    return true
                }
                else {
                    retry -= 1
                }
            })
            .catch(error => {
                retry -= 1
            })
    }
    return false
}