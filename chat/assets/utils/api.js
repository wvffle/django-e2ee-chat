import axios from 'axios'
import useCryptoStore, { b64tab } from './cryptoStore'
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

    const sessionKey = await store.decryptPKI(b64tab(res.sessionKey))
    // TODO [#19]: Decrypt iv with PKI
    const authKey = await store.decryptAES(sessionKey, b64tab(res.iv), b64tab(res.authKey))

    // TODO [#22]: Encrypt authKey with PKI
    const { data } = await axios.post('/api/v1/login/verify/', { authKey })
      .catch(err => err.response)

    if (!data.success) {
      toast.error(data.message)
      isLogged.reject(data.message)
      return false
    }

    state.sessionKey = sessionKey
    state.sessionIv = b64tab(res.iv)
    state.loggedIn = true
    isLogged.resolve()
    return true
  }

  return {
    register,
    login
  }
}
