<template>
  <v-container>
    <v-row
      v-for="(row, i) in formdata"
      :key="i"
    >
      <v-col
        :cols="5"
      >
        <v-text-field
          label="Key"
          v-model="formdata[i].key"
          @input="updateFormData($event, i, 'key')"
        ></v-text-field>
      </v-col>
      <v-col
        :cols="5"
      >
        <v-text-field
          label="Value"
          v-model="formdata[i].value"
          @input="updateFormData($event, i, 'value')"
        ></v-text-field>
      </v-col>
      <v-col
        :cols="2"
      >
        <v-btn
          color="accent"
          @click="removeRow(i)"
        ><v-icon>mdi-delete</v-icon></v-btn>
      </v-col>
    </v-row>
    <v-btn
      small
      color="accent"
      @click="addNewRow()"
    ><v-icon>mdi-plus</v-icon></v-btn>
  </v-container>
</template>

<script>

export default {
  name: 'key-value-form',
  props: {
    value: Object
  },
  computed: {
    formdata: {
      get () {
        const pivotedValue = []
        Object.keys(this.value).sort().forEach((key) => {
          pivotedValue.push({
            key,
            value: this.value[key]
          })
        })
        if (pivotedValue.length === 0) {
          return [{
            key: '',
            value: ''
          }]
        }
        return pivotedValue
      },
      set (newValue) {
        const convertedValue = {}
        newValue.forEach((row) => {
          convertedValue[row.key] = row.value
        })
        this.$emit('input', convertedValue)
      }
    }
  },
  methods: {
    updateFormData (value, index, attribute) {
      const formdata = this.formdata.sort()
      const updatedData = formdata[index]
      updatedData[attribute] = value
      this.$set(this, 'formdata', formdata)
    },
    addNewRow () {
      const formdata = this.formdata.sort()
      formdata.push({ key: '', value: '' })
      this.$set(this, 'formdata', formdata)
    },
    removeRow (index) {
      const formdata = this.formdata.sort()
      formdata.splice(index, 1)
      this.$set(this, 'formdata', formdata)
    }
  }
}
</script>
