<template>
  <div class="grid grid-cols-5 h-screen bg-blue-gray-50">
    <div class="shadow overflow-hidden bg-white z-10">
      <div class="bg-pink-600 text-white p-4 items-center flex">
        <div class="text-xl">
          {{ profile.name || '&nbsp;' }}
        </div>

        <div class="ml-auto"></div>
        <div class="bg-pink-500 p-2 rounded-full transform transition duration-200 hover:scale-120 cursor-pointer">
          <i-ri-chat-new-fill class="w-6 h-6" />
        </div>
      </div>
      <div class="relative">
        <input type="text" class="w-full pl-10 pr-4 py-2 border-b border-pink-600" placeholder="Szukaj pokoju" />
        <i-uil-comment-alt-search class="absolute left-2 top-1/2 transform -translate-y-1/2 text-gray-600"/>
      </div>

      <h2 class="text-lg px-4 pt-4 pb-2 text-gray-400 uppercase text-xs">Ostatnie pokoje</h2>

      <div class="max-w-full px-4 flex overflow-x-auto py-2">
        <div class="w-8 h-8 rounded-full bg-pink-500 flex-shrink-0 mr-2 flex-shrink-0"></div>
        <div class="w-8 h-8 rounded-full bg-pink-500 flex-shrink-0 mr-2 flex-shrink-0"></div>
        <div class="w-8 h-8 rounded-full bg-pink-500 flex-shrink-0 mr-2 flex-shrink-0"></div>
        <div class="w-8 h-8 rounded-full bg-pink-500 flex-shrink-0 mr-2 flex-shrink-0"></div>
        <div class="w-8 h-8 rounded-full bg-pink-500 flex-shrink-0 mr-2 flex-shrink-0"></div>
        <div class="w-8 h-8 rounded-full bg-pink-500 flex-shrink-0 mr-2 flex-shrink-0"></div>
        <div class="w-8 h-8 rounded-full bg-pink-500 flex-shrink-0 mr-2 flex-shrink-0"></div>
        <div class="w-8 h-8 rounded-full bg-pink-500 flex-shrink-0 mr-2 flex-shrink-0"></div>
        <div class="w-8 h-8 rounded-full bg-pink-500 flex-shrink-0 mr-2 flex-shrink-0"></div>
        <div class="w-8 h-8 rounded-full bg-pink-500 flex-shrink-0 mr-2 flex-shrink-0"></div>
      </div>

      <h2 class="text-lg px-4 pt-4 text-gray-400 uppercase text-xs">Zaproszenia</h2>

      <div class="border-b border-gray-200 p-4">
        <div class="flex items-center">
          <div class="w-8 h-8 rounded-full bg-pink-500 flex-shrink-0"></div>
          <div class="pl-4 text-gray-700">aoP86xTu7</div>
          <div class="ml-auto"></div>
          <div class="bg-green-400 p-2 rounded-full transform transition duration-200 hover:scale-120 cursor-pointer mr-2">
            <i-ri-chat-check-fill class="w-4 h-4 text-white" />
          </div>
          <div class="bg-red-400 p-2 rounded-full transform transition duration-200 hover:scale-120 cursor-pointer">
            <i-ri-chat-delete-fill class="w-4 h-4 text-white" />
          </div>
        </div>
      </div>

      <h2 class="text-lg px-4 pt-4 pb-2 text-gray-400 uppercase text-xs">Pokoje</h2>

      <div v-for="room of Object.values(profile.rooms)" @click="select(room)" :class="selectedRoom === room ? 'border-pink-600 border-r-4 bg-pink-50' : 'border-gray-200 border-b'" class="p-4 hover:bg-pink-50 cursor-pointer">
        <div class="flex items-center">
          <div class="w-8 h-8 rounded-full bg-pink-500 flex-shrink-0 flex items-center justify-center text-white text-xs uppercase relative">
            {{ room?.name?.slice(0, 2) }}
            <img class="absolute inset-0 rounded-full block object-cover w-full h-full" :src="room.image" />
          </div>
          <div class="pl-4">
            <div class="text-gray-700">{{ room.name }}</div>
            <div class="text-xs text-gray-600 truncate">
              <span v-if="room.message">{{ room.message }}</span>
              <span v-else>-- Brak wiadomości --</span>
            </div>
          </div>
        </div>
      </div>
    </div>


    <div class="col-span-4 grid" style="grid-template-rows: 1fr auto">
      <div class="relative">
        <div class="absolute inset-0">
          <undraw-group-chat class="opacity-30 block w-full h-full" preserveAspectRatio="xMidYMid meet" />
        </div>

        <div class="flex items-center justify-center text-4xl font-bold text-gray-600 h-full relative z-10" v-if="selectedRoom === null">
          Wybierz pokój
        </div>

        <div v-else class="pt-16 px-20">
          <div v-for="message of selectedRoom?.messages" class="flex mb-2">
            <div class="mr-auto relative">
              <div class="absolute top-1/2 transform -translate-y-2/3 -translate-x-14">
                <div :class="message.from.name === profile.name ? 'bg-pink-500' : 'bg-blue-300'" class="w-10 h-10 rounded-full flex-shrink-0 flex items-center justify-center text-white text-xs uppercase relative">
                  {{ message.from.name.slice(0, 2) }}
                  <img class="absolute inset-0 rounded-full block object-cover w-full h-full" :src="message.from.image" />
                </div>
              </div>

              <div :class="message.from.name === profile.name ? 'text-white bg-pink-600' : 'text-gray-800 bg-blue-100'" class="p-4 text-sm rounded-tr-3xl rounded-bl-3xl max-w-lg">
                {{ message.message }}
              </div>
            </div>
          </div>
        </div>
      </div>
      <div class="border-t border-pink-300 flex items-center relative">
        <i-bx-bxs-send @click="send" class="w-12 h-12 text-pink-600 mx-5 absolute cursor-pointer"/>
        <input :disabled="selectedRoom === null" v-model="message" @keyup.enter.prevent="send" type="text" class="pl-22 pr-4 py-4 text-lg block w-full outline-none" placeholder="Napisz wiadomość">
      </div>
    </div>
  </div>
</template>

<script>
import { reactive, ref } from 'vue'
import useCryptoStore, { abtb64 } from '../utils/cryptoStore'
import ReconnectingWebSocket from 'reconnecting-websocket'
import axios from 'axios'

export default {
  name: 'Index',
  setup () {
    const store = useCryptoStore()

    const message = ref('')
    const selectedRoom = ref(null)

    const profile = reactive({
      name: null,
      rooms: {}
    })

    const rws = new ReconnectingWebSocket(`wss://${location.hostname}/ws/chat/test`);
    rws.addEventListener('open', async () => {
      profile.name = await store.get('name')

      rws.send(JSON.stringify({
        type: 'login',
        name: profile.name
      }))
    })

    rws.addEventListener('message', ({ data: str }) => {
      const data = JSON.parse(str)

      switch (data.type) {
        case 'rooms':
          for (const room of data.rooms) {
            profile.rooms[room.name] =  room
          }
          return
        case 'message':
          break
        case 'invites':
          break
      }

      console.log(data)
    })

    const select = room => {
      selectedRoom.value = room
    }

    const send = async () => {
      const room = selectedRoom.value

      const key = await crypto.subtle.generateKey({
        name: 'AES-CBC',
        length: 256
      }, true, ['encrypt', 'decrypt'])

      const iv = await crypto.getRandomValues(new Uint8Array(16))

      const encryptedMessage = await store.encryptAES(key, iv, message.value)

      const keys = {}
      await Promise.all(room.participants.map(async ({ name, public_key }) => {
        keys[name] = [
            abtb64(await store.encryptPKI(public_key, key)),
            abtb64(await store.encryptPKI(public_key, abtb64(iv)))
        ].join('|')
      }))

      const { data } = await axios.post('/api/v1/messages/', {
        room: room.name,
        date: +new Date,
        // TODO: Implement message retention
        retention_seconds: 20,
        message: {
          message: encryptedMessage,
          keys
        }
      })

      console.log(data)
      message.value = ''
    }

    return { profile, selectedRoom, message, select, send }
  }
}
</script>
