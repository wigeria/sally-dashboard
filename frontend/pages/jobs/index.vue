<template>
  <v-card>
    <v-card-title>Jobs</v-card-title>
    <v-card-text>
      <v-list>
        <v-list-item
          v-for="job in jobs"
          :key="job.id"
          :to="`/jobs/${job.id}/`"
          router
          exact
        >
          <v-list-item-content>
            <v-list-item-title
              :class="{ 'green--text': job.finish_time !== null, 'yellow--text': job.finish_time === null }"
            >
              {{ job.bot.name }} `{{ job.id }}`
            </v-list-item-title>
          </v-list-item-content>
        </v-list-item>
      </v-list>
    </v-card-text>
  </v-card>
</template>

<script>

export default {
  name: 'jobs-list',
  data () {
    return {
      jobs: []
    }
  },
  methods: {
    getJobs () {
      const url = '/api/jobs/'
      this.$api.get(url).then((r) => {
        this.jobs = r.data
      }).catch((error) => {
        this.$store.commit('setError', error.response.statusText)
      })
    }
  },
  created () {
    if (this.$store.state.userToken === null) {
      this.$router.push('/')
      return
    }
    this.getJobs()
  }
}
</script>
