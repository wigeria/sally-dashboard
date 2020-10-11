export const state = () => ({
  userToken: localStorage.getItem('userToken') || null,
  snackbarError: null,
  notification: null
})

export const mutations = {
  setUserToken (state, userToken) {
    localStorage.setItem('userToken', userToken)
    state.userToken = userToken
    if (userToken === null) {
      localStorage.clear()
    }
  },
  setError (state, error) {
    state.snackbarError = error
  },
  addNotification (state, { notif, to }) {
    state.notification = {
      text: notif,
      to
    }
  }
}
