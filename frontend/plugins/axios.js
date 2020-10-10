
export default function ({ redirect, store, app: { $axios } }, inject) {
  // Create a custom axios instance with the authorization interceptor
  const api = $axios.create({})

  api.onRequest((config) => {
    if (store.state.userToken !== null) {
      config.headers.common.Authorization = 'Token ' + store.state.userToken
    }
  })

  api.onError((error) => {
    const code = parseInt(error.response && error.response.status)
    if (code === 401) {
      store.commit('setUserToken', null)
      redirect('/')
    }
  })

  // Inject to context as $api
  inject('api', api)
}
