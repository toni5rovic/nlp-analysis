<template>
  <!-- <div v-if="showResults && results!=null && results.sentList!=null && results.sentList.length > 0"> -->
  
</template>

<script>
export default {
  name: "TextView",
  props: ['getResults', 'typeOfAnalysis', 'text', 'typeOfSemanticAnalysis'],
  watch: { 
    getResults: function(newVal) {
      if (newVal == true) {
        console.log(newVal)
        this.sendRequest(this.typeOfAnalysis, this.text, this.typeOfSemanticAnalysis)
        this.showResults = true
      }
    }
  },
  data: function() {
    return {
      drawer: null, 
      results: null, 
      showResults: false, 
      mockResults: {
        sentList: [{
            id:0, 
            sentence: [{
              id: 0,
              part: "Opsa",
              tag: "Opsasa"
            },
            {
              id: 1,
              part: "A sto ti ja znam",
              tag: "koje be"
            }
            ] 
          }
        ]
      }
  }},
  
};
</script>