<template>
  <v-snackbar
    v-model="error"
    timeout="-1"
  >
    {{ error }}

    <template v-slot:action="{ attrs }">
    <v-btn
      color="indigo"
      text
      v-bind="attrs"
      @click="emitClose"
    >
      Close
    </v-btn>
    </template>
  </v-snackbar>
</template>

<script>

export default {
  name: 'error-snackbar',
  props: ['error'],
  methods: {
    emitClose () {
      this.$emit('closed')
    }
  }
}
</script>
