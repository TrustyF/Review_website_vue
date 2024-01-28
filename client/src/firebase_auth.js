import {getAuth, GoogleAuthProvider,signOut , signInWithPopup, onAuthStateChanged} from "firebase/auth";

export async function login() {
    const provider = new GoogleAuthProvider()
    provider.setCustomParameters({
        prompt: 'select_account'
    })
    await signInWithPopup(getAuth(), provider)
}

export async function logout() {
    const auth = await getAuth()
    await signOut(auth)
}

export async function check_admin(curr_api) {
    const token = await get_current_user()

    if (!token) return false

    const url = new URL(`${curr_api}/login/verify`)
    const result = await fetch(url, {
        method: 'GET',
        headers: {
            'Authorization': token.uid,
            'Content-Type': 'application/json',
        }
    }).then(response => response.json())
    return result.ok;
}

export function get_current_user() {
    return new Promise((resolve, reject) => {
        const remove_listener = onAuthStateChanged(
            getAuth(),
            (user) => {
                remove_listener()
                resolve(user)
            },
            reject
        )
    })
}