<template>
  <div class="grid grid-cols-2 h-screen">
    <div class="bg-pink-600 flex items-center justify-center">
      <div class="bg-white rounded py-4 shadow-lg max-w-md w-full">
        <h1 class="text-2xl pb-2 px-8 border-b border-gray-200">Wpisz kod z zaproszenia</h1>
        <p class="text-lg pt-4 px-8">Aby rozpocząć korzystanie z aplikacji, podaj kod z zaproszenia.</p>
        <div class="px-8 pt-4">
          <invite-input v-model:value="invite" />
          <div class="flex justify-center pt-8">
            <h-captcha
                sitekey="69ec32bd-a362-4ef1-907e-edb7c071f3fd"
                @verify="captchaVerify"
            />
          </div>
          <div class="flex pt-8 justify-center">
            <waff-button @click="register">Zarejestruj się</waff-button>
          </div>
        </div>
      </div>
    </div>
    <div class="flex items-center justify-center relative">
      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 140 1440" class="absolute left-0 top-0 h-full transform -translate-x-1/2">
        <rect fill="#ffffff" height="1440" id="svg_2" stroke="#000000" stroke-width="0" width="140" x="0" y="0"/>
        <path d="m-649.85052,713.85052l120,21.3c120,21.7 360,63.7 600,53.4c240,-10.7 480,-74.7 600,-106.7l120,-32l0,0l-120,0c-120,0 -360,0 -600,0c-240,0 -480,0 -600,0l-120,0l0,64z" fill="#db2777" id="svg_1" transform="rotate(-90, 70.1495, 720)"/>
        <line stroke-width="2" stroke="#db2777" x1="0" x2="0" y1="0" y2="1440" />
      </svg>
      <undraw-unlock class="w-7/9" />
    </div>
  </div>
</template>

<script>
import HCaptcha from '@jdinabox/vue-3-hcaptcha'
import { ref } from 'vue'
import { useToast } from 'vue-toastification'
import { state, useAPI } from '../utils/api'
import { useRouter } from 'vue-router'

export default {
  name: 'Register',

  components: {
    HCaptcha
  },

  setup () {
    const toast = useToast()
    const api = useAPI()
    const router = useRouter()

    const invite = ref('')
    const captcha = ref(null)

    if (state.loggedIn) {
      return router.replace('/')
    }

    const captchaVerify = token => {
      captcha.value = token
    }

    const register = async () => {
      if (!await api.register(invite.value, captcha.value)) {
        return
      }

      toast.success('Zarejestrowano nowy profil.')

      if (!await api.login()) {
        return
      }

      toast.success('Zalogowano.')

      return router.replace('/')
    }

    return { invite, register, captchaVerify }
  }
}
</script>
