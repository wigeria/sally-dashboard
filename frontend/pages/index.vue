<template>
  <v-row justify="center" align="center">
    <v-col cols="12" sm="8" md="6">
      <v-card>
        <v-card-title class="headline justify-center">
          Login
        </v-card-title>
        <v-card-text>
          <v-text-field
            v-model="formdata.email"
            label="Email"
            type="email"
          />
          <v-text-field
            v-model="formdata.password"
            label="Password"
            type="password"
          />
        </v-card-text>
        <v-card-actions class="justify-center">
          <v-btn
            color="primary"
            large
            @click="login"
          >
            Login
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-col>
  </v-row>
</template>

<script>

export default {
  components: {},
  data () {
    return {
      formdata: {
        email: '',
        password: ''
      }
    }
  },
  methods: {
    login () {
      const url = '/api/login/'
      this.$axios.$post(url, this.formdata).then((r) => {
        this.$store.commit('setUserToken', r.token)
        this.$router.push('/bots')
      }).catch((error) => {
        this.$store.commit('setError', error.response.statusText)
      })
    }
  },
  created () {
    if (this.$store.state.userToken !== null) {
      this.$router.push('/bots')
    }
  }
}
</script>
