<template>
  <v-card v-if="job !== null">
    <v-card-title
      :class="{ 'green--text': job.finish_time !== null, 'yellow--text': job.finish_time === null }"
    >
      {{ job.bot.name }} `{{ job.id }}`
      <v-spacer />
      <v-btn
        color="secondary"
        @click="getJobDetails"
      >
        Reload
      </v-btn>
    </v-card-title>

    <v-card-text>
      <div id="vnc-container" ref="vncContainer"></div>
      <v-expansion-panels
        multiple
        value="true"
      >
        <v-expansion-panel>
          <v-expansion-panel-header>
            Timestamps
          </v-expansion-panel-header>
          <v-expansion-panel-content>
            Started At: {{ job.start_time }}<br />
            Finished At: {{ job.finish_time }}
          </v-expansion-panel-content>
        </v-expansion-panel>
        <v-expansion-panel>
          <v-expansion-panel-header>
            Logs
          </v-expansion-panel-header>
          <v-expansion-panel-content>
            <pre>{{ job.logs }}</pre>
          </v-expansion-panel-content>
        </v-expansion-panel>
      </v-expansion-panels>
    </v-card-text>
  </v-card>
</template>

<script>
import RFB from '@/node_modules/@novnc/novnc/lib/rfb.js'

export default {
  name: 'job-details',
  data () {
    return {
      job: null,
      rfb: null
    }
  },
  methods: {
    getJobDetails () {
      const url = '/api/jobs/' + this.$route.params.id + '/'
      this.$api.get(url).then((r) => {
        this.job = r.data
      }).catch((error) => {
        this.$store.commit('setError', error.response.statusText)
      })
    },
    setSocketHandler () {
      const handler = (data) => {
        if (this.job !== null && data.id === this.job.id) {
          console.log(data, this.job)
          if (data.log) {
            this.job.logs += '\n' + data.log
          }
          if (data.finish_time) {
            setTimeout(() => { this.getJobDetails() }, 4000)
          }
        }
      }
      this.$nuxt.$on('job_update_notification', handler)
    },
    initVNC () {
      try {
        const container = document.getElementById('vnc-container')
        console.log({ ref: this.$refs, container })
        // TODO: Get Host from environment, and port from Job Details
        this.rfb = new RFB(this.$refs.vncContainer, 'ws://localhost:5801', {
          // TODO: get Password from environment
          credentials: { password: '12345678' }
        })

        this.rfb.addEventListener('connect', () => {
          console.log('Connected to VNC')
        })

        this.rfb.addEventListener('disconnect', () => {
          console.log('Disconnected from VNC')
        })

        this.rfb.addEventListener('error', (error) => {
          console.error('VNC Error:', error)
        })
      } catch (error) {
        console.error('Failed to initialize VNC:', error)
      }
    }
  },
  created () {
    if (this.$store.state.userToken === null) {
      this.$router.push('/')
      return
    }
    this.getJobDetails()
    this.setSocketHandler()
  },
  mounted () {
    const checkJob = setInterval(() => {
      if (this.job !== null) {
        console.log(document.getElementById('vnc-container'))
        this.initVNC()
        clearInterval(checkJob)
      }
    }, 100)
  },
  beforeDestroy () {
    this.$nuxt.$off('job_update_notification')
    if (this.rfb) {
      this.rfb.disconnect()
      this.rfb = null
    }
  }
}
</script>

<style scoped>
#vnc-container {
  width: 100%;
  height: 600px;
  margin-bottom: 20px;
}
</style>
