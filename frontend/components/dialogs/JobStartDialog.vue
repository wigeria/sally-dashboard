<template>
  <v-dialog
    v-model="dialogOpen"
    width="450"
  >
    <v-card>
      <v-card-title>Run Job against {{ bot.name }}</v-card-title>
      <v-card-text>
        <h4>Add Runtime Data</h4>
        <span>Note; this form is very flimsy at the moment, so be gentle</span>
        <key-value-form
          v-model="formdata.runtime_data"
        ></key-value-form>
      </v-card-text>
      <v-card-actions>
        <v-spacer />
        <v-btn
          primary
          @click="startJob"
        >Start Job</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
import KeyValueForm from '@/components/KeyValueForm'

export default {
  name: 'job-start-dialog',
  components: { KeyValueForm },
  props: {
    value: Boolean, // meant to be used via v-model="showDialog"
    bot: Object
  },
  computed: {
    dialogOpen: {
      get () {
        return this.value
      },
      set (newValue) {
        this.$emit('input', newValue)
      }
    }
  },
  data () {
    return {
      formdata: {
        runtime_data: {}, // TODO: Figure out a way to parse this from json/form input
        bot_id: this.bot.id
      }
    }
  },
  methods: {
    startJob () {
      const url = '/api/jobs/'
      this.$api.post(url, this.formdata).then((r) => {
        this.dialogOpen = false
        this.runtime_data = {}
      }).catch((error) => {
        this.$store.commit('setError', error.response.status)
        this.dialogOpen = false
      })
    }
  }
}
</script>
