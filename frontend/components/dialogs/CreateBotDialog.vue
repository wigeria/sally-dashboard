<template>
  <v-dialog
    v-model="dialogOpen"
    width="450"
  >
    <v-card>
      <v-card-title>
        Create Bot
      </v-card-title>
      <v-card-text>
        <v-text-field
          v-model="formdata.name"
          label="Name"
        ></v-text-field>
        <v-file-input
          label="YAML Bot"
          v-model="formdata.file"
        ></v-file-input>
      </v-card-text>
      <v-card-actions>
        <v-spacer />
        <v-btn
          color="primary"
          @click="createBot"
        >Create</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>

export default {
  name: 'create-bot-dialog',
  props: {
    value: Boolean // meant to be used via v-model="showDialog"
  },
  methods: {
    createBot () {
      const url = '/api/bots/'
      const formData = new FormData()
      formData.append('name', this.formdata.name)
      formData.append('file', this.formdata.file)
      this.$api.post(url, formData).then((r) => {
        this.$emit('botCreated', r.data)
        this.dialogOpen = false
        this.formdata = { name: '', file: null }
      }).catch((error) => {
        this.$store.commit('setError', error.response.statusText)
      })
    }
  },
  data () {
    return {
      formdata: {
        name: '',
        file: null
      }
    }
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
  }
}
</script>
