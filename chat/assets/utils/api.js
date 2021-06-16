import axios from 'axios'
import useCryptoStore, { abtb64, b64tab } from './cryptoStore'
import { useToast } from 'vue-toastification'
import resolvable from '@josephg/resolvable'

export const state = {
  sessionKey: null,
  sessionIv: null,
  loggedIn: false,
}

export let isLogged = resolvable()

export const useAPI = () => {
  const store = useCryptoStore()
  const toast = useToast()

  const register = async (invite, hcaptcha) => {
    const { data } = await axios.post('/api/v1/register/', {
      public_key: await store.get('publicKey'),
      hcaptcha,
      invite
    })
      .then(res => res)
      .catch(err => err.response)

    if (!data.success) {
      toast.error(data.message)
      return false
    }

    await store.set('name', data.name)
    return true
  }

  const login = async () => {
    if (state.loggedIn) {
      isLogged = resolvable()
    }

    state.loggedIn = false

    const { data: res } = await axios.post('/api/v1/login/', {
      name: await store.get('name')
    })
      .catch(err => err.response)

    if (!res.success) {
      toast.error(res.message)
      isLogged.reject(res.message)
      return false
    }

    const [sessionKey, iv, verifyKey, verifyIv] = await Promise.all([
      store.decryptPKI(b64tab(res.sessionKey)),
      store.decryptPKI(b64tab(res.iv)),
      store.decryptPKI(b64tab(res.verifyKey)),
      store.decryptPKI(b64tab(res.verifyIv))
    ])

    const authKey = await store.decryptAES(sessionKey, iv, b64tab(res.authKey))
    const encAuthKey = await store.encryptAES(verifyKey, verifyIv, authKey)

    const { data } = await axios.post('/api/v1/login/verify/', { authKey: encAuthKey })
      .catch(err => err.response)

    if (!data.success) {
      toast.error(data.message)
      isLogged.reject(data.message)
      return false
    }

    state.sessionKey = sessionKey
    state.sessionIv = iv
    state.loggedIn = true
    isLogged.resolve()
    return true
  }

  return {
    register,
    login
  }
}
