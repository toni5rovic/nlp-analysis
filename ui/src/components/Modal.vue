<template>
  <v-dialog v-model="show" max-width="500px">
    <v-card raised>
      <v-card-title class="headline teal lighten-5" primary-title>
        Add Text or File
      </v-card-title>

      <v-divider></v-divider>

      <v-card-text class="mt-2">
        <v-textarea
            v-model="textareaValue"
            :disabled="useFileInput"
            :auto-grow=false
            :no-resize=true
            :clearable=true
            :placeholder="`Enter text here...`"
            :filled=true
            :row-height=24
            :rows=8
        ></v-textarea>
          <v-divider></v-divider>
        <v-file-input 
          accept=".txt"
          label="Choose a .txt file"
          outlined
          v-model="chosenFile"
          :disabled="!useFileInput"
          ></v-file-input>
      </v-card-text>

      <v-divider></v-divider>

      <v-card-actions>
        <v-switch
          v-model="useFileInput"
          :label="`Use file input:`"
        ></v-switch>
        <v-spacer></v-spacer>
        <v-btn color="primary" @click.stop="importText">OK</v-btn>
        <v-btn color="primary" @click.stop="show=false">Close</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
export default {
  props: {
    value: Boolean,
    loadText: null
  },
  data: () => ({
    chosenFile: null,
    textareaValue: null,
    useFileInput: false,
    fileContent: null
  }),
  computed: {
    show: {
      get() {
        return this.value;
      },
      set(value) {
        this.$emit("input", value);
      }
    }
  },
  methods: {
    importText() {
      if (this.useFileInput === true) {
        var reader = new FileReader();   
        // Use the javascript reader object to load the contents
        // of the file in the v-model prop
        reader.readAsText(this.chosenFile);
        reader.onload = () => {
          this.fileContent = reader.result;
          this.loadText(this.fileContent)
        }
      }
      else {
        // Text from textarea is passed to parent component
        this.loadText(this.textareaValue)
      }
      // close modal
      this.show = false
    }
  }
};
</script>