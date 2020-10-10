export const state = () => ({
  userToken: localStorage.getItem('userToken') || null,
  snackbarError: null
})

export const mutations = {
  setUserToken (state, userToken) {
    localStorage.setItem('userToken', userToken)
    state.userToken = userToken
  },
  setError (state, error) {
    state.snackbarError = error
  }
}
