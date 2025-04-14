<template>
  <v-row justify="center" align="center">
    <v-col cols="12" sm="12" md="12">
      <v-card>
        <v-card-title>Bots</v-card-title>
        <v-card-text>
          <v-btn
            @click="showCreateBotDialog = true"
          >Create Bot</v-btn>
          <v-list>
            <template v-for="bot in bots">
              <v-list-item :key="bot.id + '-list-item'">
                <v-list-item-content>
                  <v-list-item-title v-text="bot.name" />
                </v-list-item-content>
                <v-list-item-action>
                  <v-btn
                    @click="openJobStartDialog(bot)"
                  >
                    <v-icon>mdi-play</v-icon>
                  </v-btn>
                </v-list-item-action>
                <v-list-item-action>
                  <v-btn
                    @click="deleteBot(bot)"
                  >
                    <v-icon>mdi-delete</v-icon>
                  </v-btn>
                </v-list-item-action>
              </v-list-item>
              <v-divider
                :key="bot.id"
              ></v-divider>
            </template>
          </v-list>
          <job-start-dialog
            v-model="showJobStartDialog"
            :bot="jobStartDialogBot"
            v-if="showJobStartDialog"
          ></job-start-dialog>
          <create-bot-dialog
            v-model="showCreateBotDialog"
            @botCreated="botCreated"
          ></create-bot-dialog>
        </v-card-text>
      </v-card>
    </v-col>
  </v-row>
</template>

<script>
import JobStartDialog from '@/components/dialogs/JobStartDialog'
import CreateBotDialog from '@/components/dialogs/CreateBotDialog'

export default {
  name: 'bots',
  components: { JobStartDialog, CreateBotDialog },
  data () {
    return {
      bots: [],
      showCreateBotDialog: false,
      showJobStartDialog: false,
      jobStartDialogBot: null
    }
  },
  created () {
    if (this.$store.state.userToken === null) {
      this.$router.push('/')
      return
    }
    this.getBots()
  },
  methods: {
    getBots () {
      const url = '/api/bots/'
      this.$api.get(url).then((r) => {
        this.bots = r.data
      }).catch((error) => {
        this.$store.commit('setError', error.response.statusText)
      })
    },
    deleteBot (bot) {
      const url = '/api/bots/' + bot.id + '/'
      this.$api.delete(url).then((r) => {
        this.$store.commit('addNotification', { notif: `Bot ${bot.name} Deleted` })
        this.bots.splice(this.bots.indexOf(bot), 1)
      }).catch((error) => {
        this.$store.commit('setError', error.response.statusText)
      })
    },
    openJobStartDialog (bot) {
      this.jobStartDialogBot = bot
      this.showJobStartDialog = true
    },
    closeJobStartDialog (bot) {
      this.jobStartDialogBot = null
      this.showJobStartDialog = false
    },
    botCreated (bot) {
      this.$store.commit('addNotification', { notif: `Bot ${bot.name} Created` })
      this.bots.push(bot)
    }
  }
}
</script>
