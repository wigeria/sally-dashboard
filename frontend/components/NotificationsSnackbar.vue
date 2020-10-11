<template>
  <v-snackbar
    v-model="snackbar"
    :timeout="timeout"
    color="red accent-1"
  >
    <nuxt-link
      v-if="message.to !== null && message.to !== undefined"
      :to="message.to"
    >{{ message.text }}</nuxt-link>
    <span v-if="message.to === null || message.to === undefined">{{ message.text }}</span>

    <template v-slot:action="{ attrs }">
    <v-btn
      text
      v-bind="attrs"
      @click="snackbar = false"
    >
      Close
    </v-btn>
    </template>
  </v-snackbar>
</template>

<script>

// Global Snackbar for displaying timed-out messages temporarily
export default {
  name: 'notifications-snackbar',
  computed: {
    notification () {
      return this.$store.state.notification
    }
  },
  watch: {
    notification (newValue) {
      if (newValue) {
        this.message = newValue
        this.snackbar = false
        this.snackbar = true
        this.timeout = 5000
      }
    }
  },
  data () {
    return {
      snackbar: false,
      timeout: 5000,
      message: {}
    }
  }
}
</script>
