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
      >Reload</v-btn>
    </v-card-title>
    <v-card-text>
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

export default {
  name: 'job-details',
  data () {
    return {
      job: null
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
  beforeDestroy () {
    this.$nuxt.$off('job_update_notification')
  }
}
</script>
