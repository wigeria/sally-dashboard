<template>
  <v-app dark>
    <v-navigation-drawer
      v-model="drawer"
      :mini-variant="miniVariant"
      fixed
      app
    >
      <v-list>
        <v-list-item
          :to="firstNavItem.to"
          router
          exact
        >
          <v-list-item-action>
            <v-icon>{{ firstNavItem.icon }}</v-icon>
          </v-list-item-action>
          <v-list-item-content>
            <v-list-item-title v-text="firstNavItem.title" />
          </v-list-item-content>
        </v-list-item>
        <v-list-item
          v-for="(item, i) in items"
          :key="i"
          :to="item.to"
          router
          exact
        >
          <v-list-item-action>
            <v-icon>{{ item.icon }}</v-icon>
          </v-list-item-action>
          <v-list-item-content>
            <v-list-item-title v-text="item.title" />
          </v-list-item-content>
        </v-list-item>
        <v-list-item
          v-if="$store.state.userToken !== null"
          @click="$store.commit('setUserToken', null); $router.push('/')"
        >
          <v-list-item-action>
            <v-icon>mdi-logout</v-icon>
          </v-list-item-action>
          <v-list-item-content>
            <v-list-item-title>Logout</v-list-item-title>
          </v-list-item-content>
        </v-list-item>
      </v-list>
    </v-navigation-drawer>
    <v-app-bar
      fixed
      app
    >
      <v-app-bar-nav-icon @click.stop="drawer = !drawer" />
      <v-btn
        icon
        @click.stop="miniVariant = !miniVariant"
      >
        <v-icon>mdi-{{ `chevron-${miniVariant ? 'right' : 'left'}` }}</v-icon>
      </v-btn>
      <v-toolbar-title v-text="title" />
    </v-app-bar>
    <v-main>
      <v-container>
        <nuxt />
      </v-container>
    </v-main>
    <v-footer
      :absolute="true"
      app
    >
      <span>{{ this.signedIn }} &copy; {{ new Date().getFullYear() }}</span>
    </v-footer>

    <error-snackbar
      v-for="error in errors"
      :error="error.text"
      :key="error.id"
      @closed="closeError(error)"
    ></error-snackbar>
    <notifications-snackbar></notifications-snackbar>
  </v-app>
</template>

<script>

import ErrorSnackbar from '@/components/ErrorSnackbar'
import NotificationsSnackbar from '@/components/NotificationsSnackbar'

console.log(NotificationsSnackbar)
export default {
  components: { ErrorSnackbar, NotificationsSnackbar },
  data () {
    return {
      drawer: true,
      items: [
        {
          icon: 'mdi-chart-bubble',
          title: 'Jobs',
          to: '/jobs'
        }
      ],
      errors: [],
      miniVariant: false,
      title: 'Sally',
      socket: null
    }
  },
  computed: {
    stateError () {
      return this.$store.state.snackbarError
    },
    signedIn () {
      return this.$store.state.userToken !== null
    },
    firstNavItem () {
      return {
        icon: 'mdi-apps',
        title: !this.signedIn ? 'Login' : 'Bots',
        to: !this.signedIn ? '/' : '/bots'
      }
    }
  },
  methods: {
    closeError (error) {
      this.errors.splice(this.errors.indexOf(error), 1)
    },
    connectSocket () {
      this.socket = this.$nuxtSocket({
        channel: '/',
        transports: ['websocket'],
        query: {
          token: this.$store.state.userToken
        }
      })
      // Global event handling; use .on('*', (event, data) => {})
      const onevent = this.socket.onevent
      this.socket.onevent = function (packet) {
        const args = packet.data || []
        onevent.call(this, packet)
        packet.data = ['*'].concat(args)
        onevent.call(this, packet)
      }
      this.socket.on('connect', () => {
        console.log('Socket Connected')
      })
      this.socket.on('job_update_notification', (data) => {
        this.$nuxt.$emit('job_update_notification', data)
        if (data.finish_time) {
          setTimeout(() => {
            this.$store.commit('addNotification', {
              notif: `Job ${data.id} has finished`,
              to: `/jobs/${data.id}`
            })
          }, 4000)
        }
      })
    }
  },
  watch: {
    stateError (newValue) {
      if (newValue !== '' && newValue != null && this.errors.filter(e => e.text === newValue).length === 0) {
        this.errors.push({
          text: newValue,
          id: this.errors.length
        })
      }
      this.$store.commit('setError', null)
    },
    signedIn (newValue) {
      if (newValue) {
        this.connectSocket()
      } else if (this.socket !== null) {
        this.socket.disconnect(true)
      }
    }
  },
  created () {
    if (this.signedIn && this.socket === null) {
      this.connectSocket()
    }
  }
}
</script>
