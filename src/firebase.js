import { initializeApp } from 'firebase/app'
import { getFirestore, collection } from 'firebase/firestore'
import { getStorage } from 'firebase/storage'

export const firebaseApp = initializeApp({
    apiKey: process.env.VUE_APP_APIKEY,
    authDomain: process.env.VUE_APP_AUTHDOMAIN,
    projectId: process.env.VUE_APP_PROJECTID,
    storageBucket: process.env.VUE_APP_STORAGEBUCKET,
    messagingSenderId: process.env.VUE_APP_MESSAGINGSENDERID,
    appId: process.env.VUE_APP_APPID,
    measurementId: process.env.VUE_APP_MEASUREMENTID
})

// used for the firestore refs
export const database = getFirestore(firebaseApp)
export const img_database = getStorage(firebaseApp)

// here we can export reusable database references
// export const moviesDb = collection(database, 'movies')
// export const tvDb = collection(database, 'tv_series')
