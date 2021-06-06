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

      <h2 class="text-lg px-4 py-2 text-gray-400">Recent</h2>

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

      <h2 class="text-lg px-4 py-2 text-gray-400">Invites</h2>

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

      <h2 class="text-lg px-4 py-2 text-gray-400">Rooms</h2>

      <div class="border-b border-gray-200 p-4">
        <div class="flex items-center">
          <div class="w-8 h-8 rounded-full bg-pink-500 flex-shrink-0"></div>
          <div class="pl-4">
            <div class="text-gray-700">aoP86xTu7</div>
            <div class="text-xs text-gray-600 truncate">siema</div>
          </div>
        </div>
      </div>

      <div class="shadow p-4 border-r-4 border-pink-600 bg-pink-50">
        <div class="flex items-center">
          <div class="w-8 h-8 rounded-full bg-blue-300 flex-shrink-0"></div>
          <div class="pl-4">
            <div class="text-gray-700">ox4a66at</div>
            <div class="text-xs text-gray-600 truncate">dlugie wiadomosci tez sie ladnie wyswietlaja </div>
          </div>
        </div>
      </div>

      <div class="border-b border-gray-200 p-4">
        <div class="flex items-center">
          <div class="w-8 h-8 rounded-full bg-pink-500 flex-shrink-0"></div>
          <div class="pl-4">
            <div class="text-gray-700">aoP86xTu7</div>
            <div class="text-xs text-gray-600 truncate">siema</div>
          </div>
        </div>
      </div>
    </div>

    <div class="col-span-4 grid" style="grid-template-rows: 1fr auto">
      <div class="relative">
        <div class="absolute inset-0">
          <undraw-group-chat class="opacity-30 block w-full h-full" preserveAspectRatio="xMidYMid meet" />
        </div>

        <div class="pt-16 px-20">

          <div class="flex mb-2">
            <div class="mr-auto relative">
              <div class="absolute top-1/2 transform -translate-y-2/3 -translate-x-14">
                <div class="w-10 h-10 rounded-full bg-pink-500"></div>
              </div>

              <div class="bg-pink-600 text-white p-4 text-sm rounded-tr-3xl rounded-bl-3xl">
                Dziala?
              </div>
            </div>
          </div>

          <div class="flex mb-2">
            <div class="mr-auto relative">
              <div class="absolute top-1/2 transform -translate-y-2/3 -translate-x-14">
                <div class="w-10 h-10 rounded-full bg-blue-300"></div>
              </div>

              <div class="bg-blue-100 text-gray-800 p-4 text-sm rounded-tr-3xl rounded-bl-3xl">
                test
              </div>
            </div>
          </div>

          <div class="flex mb-2">
            <div class="mr-auto relative">
              <div class="absolute top-1/2 transform -translate-y-2/3 -translate-x-14">
                <div class="w-10 h-10 rounded-full bg-blue-300"></div>
              </div>

              <div class="bg-blue-100 text-gray-800 p-4 text-sm rounded-tr-3xl rounded-bl-3xl">
                o, dziala
              </div>
            </div>
          </div>

          <div class="flex mb-2">
            <div class="mr-auto relative">
              <div class="absolute top-1/2 transform -translate-y-2/3 -translate-x-14">
                <div class="w-10 h-10 rounded-full bg-pink-500"></div>
              </div>

              <div class="bg-pink-600 text-white p-4 text-sm rounded-tr-3xl rounded-bl-3xl">
                super
              </div>
            </div>
          </div>

          <div class="flex mb-2">
            <div class="mr-auto relative">
              <div class="absolute top-1/2 transform -translate-y-2/3 -translate-x-14">
                <div class="w-10 h-10 rounded-full bg-pink-500"></div>
              </div>

              <div class="bg-pink-600 text-white p-4 text-sm rounded-tr-3xl rounded-bl-3xl max-w-lg">
                Tenetur tempore nisi ipsam veniam ipsum. Eligendi doloribus atque iure incidunt. Odio qui expedita tenetur pariatur optio. Mollitia iste voluptas ullam labore accusantium. Consectetur ea dolor sit perferendis nisi consequatur. Ad autem mollitia veritatis nihil sint iusto.
              </div>
            </div>
          </div>

          <div class="flex mb-2">
            <div class="mr-auto relative">
              <div class="absolute top-1/2 transform -translate-y-2/3 -translate-x-14">
                <div class="w-10 h-10 rounded-full bg-blue-300"></div>
              </div>

              <div class="bg-blue-100 text-gray-800 p-4 text-sm rounded-tr-3xl rounded-bl-3xl">
                dlugie wiadomosci tez sie ladnie wyswietlaja
              </div>
            </div>
          </div>

        </div>

      </div>
      <div class="border-t border-pink-300 flex items-center relative">
        <i-bx-bxs-send class="w-12 h-12 text-pink-600 mx-5 absolute cursor-pointer"/>
        <input type="text" class="pl-22 pr-4 py-4 text-lg block w-full outline-none" placeholder="Napisz wiadomość">
      </div>
    </div>
  </div>
</template>

<script>
import { reactive } from 'vue'
import useCryptoStore from '../utils/cryptoStore'

export default {
  name: 'Index',
  setup () {
    const store = useCryptoStore()

    const profile = reactive({
      name: null
    })

    ;(async () => {
      profile.name = await store.get('name')
    })()

    return { profile }
  }
}
</script>
